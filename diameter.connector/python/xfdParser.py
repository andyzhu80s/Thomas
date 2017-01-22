import xml.etree.ElementTree as ET
from xml.dom import minidom
from collections import deque
import copy
import sys

def loadXFD(rootFolder,xfdFile):
    eTree=ET.parse(rootFolder+xfdFile)
    root=eTree.getroot()
    xfds={}
    xfd={"cmds":{},"avps":{}}
    cmds={}
    avps={}   

    #read namespace & import xfd
    importXFD=root.get('import')
    namespace=root.find('root').get('snmeNamespace')

    if not importXFD is None:
       importNamespace, xfds = loadXFD(rootFolder, importXFD)
       xfd=copy.deepcopy(xfds[importNamespace])

    xfds[namespace]=xfd
    cmds=xfd["cmds"]
    avps=xfd["avps"]       
        
    print "Load",xfdFile,"start"
    
    #read AVP
    for avpNode in root.findall(".//tlv[@type='AVP']/.."):

        #Load AVP Definition
        avp={'name':avpNode.get('name'),'type':avpNode.tag}
        avps[avp['name']]=avp
        
        for field in avpNode.findall('.//tlv/field'):
            avp[field.get('name')]=field.get('value')

        #Load Group AVP member
        if not avpNode.get("extends") is None:
            extends=avpNode.get("extends").split('.')
            avpName=extends[len(extends)-1]
            del extends[len(extends)-1]
            extendNamespace='.'.join(extends)
            extendAVP=xfds[extendNamespace]['avps'][avpName]
            avp['groupAVPs']=extendAVP.get('groupAVPs')

        groupAVPs=[]
        if avp.get('groupAVPs') is None:
            avp['groupAVPs']=groupAVPs
        else:
            groupAVPs=avp['groupAVPs']
            
        for field in avpNode.findall('field'):                
            #groupAVPs[field.get('name')]={'name':field.get('name'),'type':field.get('type'), 'usage':field.get('usage')}
            groupAVPs.append({'name':field.get('name'),'type':field.get('type'), 'usage':field.get('usage')})
        
    #read AVP array
    for avpNode in root.findall("array"):
        avp={'name':avpNode.get('name'),'field':avpNode.get('field'),'isArray':True}
        avps[avp['name']]=avp

    #read Commmand
    #read Commmand: read command type and code
    cmdTypes={}
    for cmdTypeNode in root.findall("choice[@name='Body']/field"):
        cmdTypes[cmdTypeNode.get('type')]=cmdTypeNode.find("raw[@reference='commandCode']").get("value")

    #read Commmand: read command (request & response)
    for cmdType in cmdTypes.keys():
        for cmdNode in root.findall("choice[@name='"+cmdType+ "']/field"):
            cmd={'name':cmdNode.get('name'),'type':cmdNode.get('type'), 'commandCode':cmdTypes.get(cmdType),'rFlag': cmdNode.find("raw[@reference='rFlag']").get("value")}
            cmds[cmd['type']]=cmd
  
    
    #read Command: read command AVP structure
    for cmdKey in cmds.keys():
        cmd=cmds[cmdKey]
        avpNode=root.find("set[@name='"+cmdKey+"']")
        if avpNode is None:
            continue
        if not avpNode.get("extends") is None:
            extends=avpNode.get("extends").split('.')
            avpName=extends[len(extends)-1]
            del extends[len(extends)-1]
            extendNamespace='.'.join(extends)
            extendAVP=xfds[extendNamespace]['cmds'][avpName]
            cmd['groupAVPs']=extendAVP.get('groupAVPs')

        groupAVPs=[]
        if cmd.get('groupAVPs') is None:
            cmd['groupAVPs']=groupAVPs
        else:
            groupAVPs=cmd['groupAVPs']
            
        for field in avpNode.findall('field'):
            #groupAVPs[field.get('name')]={'name':field.get('name'),'type':field.get('type'), 'usage':field.get('usage')}
            groupAVPs.append({'name':field.get('name'),'type':field.get('type'), 'usage':field.get('usage')})
    
    print "Load",xfdFile,"complete"
    
    return namespace, xfds


def exportXFD2Seagull(xfd, rootFolder):
    typeMap={'integer':'Unsigned32',
                 'long':'Unsigned64',
                 'string':'OctetString',
                 'set':'Grouped'} 
    cmds=xfd['cmds']
    avpsDef=xfd['avps'] # avp definition like avp type, avp code, flag & etc
    avpsDict={} #used to record unique AVP list
    
    dictTemplateXML='''<?xml version="1.0" encoding="ISO-8859-1"?>
<protocol name="diameter-v1" type="binary" padding="4">

    <types>
      <typedef name="Integer32" type="signed" size="4" unit="octet"> </typedef>
      <typedef name="Unsigned32" type="number" size="4" unit="octet"> </typedef>
      <typedef name="Integer64" type="signed64" size="8" unit="octet"> </typedef>
      <typedef name="Unsigned64" type="number64" size="8" unit="octet"> </typedef>
      <typedef name="OctetString" type="string" size="4" unit="octet"> </typedef>
      <typedef name="Grouped" type="grouped"></typedef>
    </types>

    <header name="command" length="msg-length" type="cmd-code">
      <fielddef name="protocol-version" size="1" unit="octet"></fielddef>
      <fielddef name="msg-length" size="3" unit="octet"> </fielddef>
      <fielddef name="flags" size="1" unit="octet"> </fielddef>
      <fielddef name="cmd-code" size="3" unit="octet"> </fielddef>
      <fielddef name="application-id" size="4" unit="octet"> </fielddef>
      <fielddef name="HbH-id" size="4" unit="octet"> </fielddef>
      <fielddef name="EtE-id" size="4" unit="octet"> </fielddef>
    </header>

    <body>
      <header name="avp" length="avp-length" type="avp-code">
         <fielddef name="avp-code" size="4" unit="octet"> </fielddef>
         <fielddef name="flags" size="1" unit="octet"> </fielddef>
         <fielddef name="avp-length" size="3" unit="octet"> </fielddef>
         <optional>
            <fielddef name="Vendor-ID" size="4" unit="octet"
                      condition="mask" field="flags" mask="128">
            </fielddef>
         </optional>
      </header>
    </body>

    <dictionary>
      <avp>
      </avp>
      <command session-id="Session-Id" out-of-session-id="HbH-id">
      </command>
    </dictionary>
</protocol>
'''
    cmdTreeRoot=ET.Element("Sample")  # cmd tree xml tree
    
    dictRoot=ET.fromstring(dictTemplateXML)    #dictionary xml tree
    
    dictAVPListNode=dictRoot.find('.//avp')
    dictCMDListNode=dictRoot.find('.//command')
    sessionAVPName=None
    for cmd in cmds.values():
        cmdTreeNode=ET.SubElement(cmdTreeRoot,"command", {'name':cmd['name']}) #command in sample 

        #build command dictionary
        cmdNode=ET.SubElement(dictCMDListNode, "define",{'name':cmd['name']}) 
        flags=0
        if cmd.get('rFlag')=='1':
            flags=128
        ET.SubElement(cmdNode,"setfield",{'name':'flags','value':str(flags)})
        ET.SubElement(cmdNode,"setfield",{'name':'cmd-code','value':cmd['commandCode']})
        ET.SubElement(cmdNode,"setfield",{'name':'protocol-version','value':"1"})

        #collect avps & consturct avp tree in command
        buildAVPTree(cmd.get('groupAVPs'), cmdTreeNode, avpsDef, typeMap, avpsDict)

    #build avp dictionary    
    sessionAVPName=buildDict(avpsDict, dictAVPListNode, avpsDef, typeMap)
    
    if not sessionAVPName is None:
        dictCMDListNode.attrib['session-id']=sessionAVPName            

    dictXMLString=ET.tostring(dictRoot, 'utf-8')
    parsedDictXMLString = minidom.parseString(dictXMLString)
    #print parsedDictXMLString.toprettyxml(indent="    ")

    sampleCmdXMLString=ET.tostring(cmdTreeRoot, 'utf-8')
    parsedSampleCmdXMLString = minidom.parseString(sampleCmdXMLString)
    #print parsedSampleCmdXMLString.toprettyxml(indent="    ")
    #etree.write(rootFolder+"/dictionary.xml")

def buildAVPTree(groupAVPs, cmdParentNode, avpsDef, typeMap, avpsDict):
    for avp in groupAVPs:
        avpDef=avpsDef.get(avp['type'])
        if avpDef.get('isArray') is True:
            avpDef=avpsDef.get(avpDef['field'])
        avpsDict[avp['name']]=avpDef
        
        if avpDef.get('type')=='set':
            cmdNode=ET.SubElement(cmdParentNode,"avp",{'name':avp['name']})
            buildAVPTree(avpDef.get('groupAVPs'), cmdNode, avpsDef, typeMap, avpsDict)
        else:
            ET.SubElement(cmdParentNode,"avp",{'name':avp['name'],'value':"["+typeMap[avpDef['type']]+"]"})

def buildDict(avpsDict, dictAVPListNode, avpsDef, typeMap):
    sessionAVPName=None
    for avpName in avpsDict.keys():
        avpDef=avpsDict[avpName]
        #create avp defintion node
        avpNode=ET.SubElement(dictAVPListNode, "define",{'name':avpName,'type':typeMap[avpDef['type']]})
        if avpDef.get('avpCode')=="263":
            sessionAVPName=avpName
        ET.SubElement(avpNode,"setfield",{'name':'avp-code','value':avpDef['avpCode']})        
        flag=0
        if avpDef.get('vFlag')=='1':
            flag=flag | 128
            ET.SubElement(avpNode,"setfield",{'name':'Vendor-ID','value':avpDef['vendorID']})
        if avpDef.get('mFlag')=='1':
            flag=flag | 64
        if avpDef.get('pFlag')=='1':
            flag=flag | 32
        ET.SubElement(avpNode,"setfield",{'name':'flags','value':str(flag)})
        
    return sessionAVPName

def usage():
    print '''xfdConvert usage:
    -h: print help message
    -d: xfd root folder
    -f: xfd file name to be parsed
    -o: output folder
'''
def main(argv):

    
    namespace, xfds=loadXFD('c:/','diameter-gy.xfd')
    exportXFD2Seagull(xfds[namespace],"c:/seagulldic/")
        
#--Main--
if __name__=='__main__':
    main(sys.argv)
    


