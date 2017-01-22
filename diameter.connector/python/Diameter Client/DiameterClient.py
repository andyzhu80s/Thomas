
class DiameterEvent
    version=1
    messageLength=0
    flags
    commandCode
    applicationId
    HbHId #Hop-by-Hop Identifier
    EtEId #End-to-End Identifier

    AVPs{}

    def isRequest():

    def isProxiable():

    def isError():

    def isRetransmitted():

    def getReservedFlag():

    def setRequest():

    def setProxiable():

    def setError():

    def setRetransmitted():

    def getReservedFlag():

class DiameterEventFactory
    cmdDefMap={}
    dictionaryTree
    def __init__(self, dictionary):
        dictionaryTree=ET.parse(dictionary)
        parseCommandDefinition()

    def parseCommandDefinition():
        root=dictionaryTree.getroot()
        for cmdNode in root.findall('dictionary/command/define'):
            cmdDef={'name':cmdNode.attrib['name']}
            for fieldNode in cmdNode.findall('setfield'):
                cmdDef[fieldNode.attrib['name']]=fieldNode.attrib['value']
            cmdDefMap[cmdDef['name']]=cmdDef
            cmdDefMap[cmdDef['cmd-code']]=cmdDef


#Basic Type:
#   OctetString
#   Integer32
#   Integer64
#   Unsigned32
#   Unsigned64
#   Float32
#   Float64
#   Grouped
    def parseTypeDefinition():
        

    def parseAVPDefinition():

    
        

    def createCommand(identifier):
        cmdDef=cmdDefMap.get(identifier)
        if cmdDef is None: return None

        cmd=DiameterEvent()
        cmd.commandCode=long(cmdDef['cmd-code'])
        cmd.applicationId=long(cmdDef['application-id'])
        cmd.flags=int(cmdDef['flags'])

        return cmd


class DiameterConnector:
    def __init__(self):
        print "initial diameter connector"


dc=DiameterConnector()
