import struct

class DiameterAVP:
    code=0
    length=0
    isVendor=False
    isMandatory=False
    isEncryption=False    
    vendorId=0
    dataType=None
    rawValue=None
    value=None
    __avps=[]

    def __init__(self,code,length,isVendor,isMandatory,isEncryption,vendorId, dataType, rawValue):  
        self.code= code
        self.length=length
        self.isVendor=isVendor
        self.isMandatory=isMandatory
        self.isEncryption=isEncryption
        self.vendorId=vendorId
        self.dataType=dataType
        self.rawValue=rawValue

    def getValue(self):
        #if value is None, calculate the value

    def getSubAVPs(self):
        return self.__avps;

    def toString(self):
        return "xxx"

    def __repr__(self):
        return self.toString()

class DiameterMessage:
    name=None
    version=0
    length=0
    flag=0
    isRequest=False
    isProxiable=False
    isError=False
    isRetransmitted=False
    code=0
    appId=0
    hbhId=0
    e2eId=0
    avps=[]

    def __init__(self,version,length,flag,code,appId,hbhId,e2eId,avps):  
        self.version= version
        self.length=length
        self.flag=flag
        self.code=code
        self.appId=appId
        self.hbhId=hbhId
        self.e2eId=e2eId
        self.avps=avps
        #FIX
        self.name=code
        
        self.__parseFlag()

    def __parseFlag(self):
        if (self.flag & 0x80)>0: self.isRequest=True
        if (self.flag & 0x40)>0: self.isProxiable=True
        if (self.flag & 0x20)>0: self.isError=True
        if (self.flag & 0x10)>0: self.isRetransmitted=True

    def toString(self):
        str="%s ::=< Diameter Header: %s" % (self.name,self.code)
        if self.isRequest==True: str=str + ", REQ"
        if self.isProxiable==True: str=str + ", PXY"
        if self.isError==True: str=str + ", ERR"
        if self.isRetransmitted==True: str=str + ", RTMT"
        str=str + (", %s >\n" % (self.appId))
        return str
        
    def __repr__(self):
        return self.toString()

class DiameterAVPDefinition:
    

avpDic={
    443:{'name':'Subscription-Id','type':'Grouped'}
    }

def printAVPTree(avps,index):
    for avp in avps:
        subAVPs=avp.get("avps")
        if subAVPs is None:
            print 8*index*" ",avp
        else:
            del avp["avps"]
            print 8*index*" ",avp
            printAVPTree(subAVPs,index+1)
            avp["avps"]=subAVPs
        

#CCR
raw=b'\x01\x00\x02\x28\xc0\x00\x01\x10\x00\x00\x00\x04\x00\x00\x00\xca\
\x6c\x20\x79\xef\x00\x00\x01\x07\x40\x00\x00\x32\x61\x63\x63\x65\
\x73\x73\x70\x6f\x69\x6e\x74\x37\x2e\x61\x63\x6d\x65\x2e\x63\x6f\
\x6d\x3b\x31\x34\x32\x37\x39\x36\x35\x36\x33\x36\x3b\x36\x39\x35\
\x33\x34\x33\x30\x36\x33\x00\x00\x00\x00\x01\x02\x40\x00\x00\x0c\
\x00\x00\x00\x04\x00\x00\x01\x08\x40\x00\x00\x19\x67\x78\x43\x6c\
\x69\x65\x6e\x74\x48\x6f\x73\x74\x5f\x7a\x77\x64\x31\x00\x00\x00\
\x00\x00\x01\x28\x40\x00\x00\x1a\x67\x78\x43\x6c\x69\x65\x6e\x74\
\x52\x65\x61\x6c\x6d\x5f\x7a\x77\x64\x31\x00\x00\x00\x00\x01\x1b\
\x40\x00\x00\x12\x75\x70\x6d\x47\x78\x52\x65\x61\x6c\x6d\x00\x00\
\x00\x00\x01\xa0\x40\x00\x00\x0c\x00\x00\x00\x01\x00\x00\x01\x9f\
\x40\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x01\x25\x40\x00\x00\x1b\
\x41\x4d\x53\x50\x72\x69\x6d\x61\x72\x79\x55\x50\x4d\x47\x78\x48\
\x6f\x73\x74\x00\x00\x00\x01\xbb\x40\x00\x00\x2c\x00\x00\x01\xc2\
\x40\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x01\xbc\x40\x00\x00\x15\
\x38\x36\x31\x35\x39\x30\x30\x31\x33\x36\x30\x35\x31\x00\x00\x00\
\x00\x00\x01\xbb\x40\x00\x00\x2c\x00\x00\x01\xc2\x40\x00\x00\x0c\
\x00\x00\x00\x01\x00\x00\x01\xbc\x40\x00\x00\x17\x34\x36\x30\x30\
\x30\x30\x30\x30\x30\x31\x33\x36\x30\x36\x30\x00\x00\x00\x03\xfc\
\xc0\x00\x00\x11\x00\x00\x28\xaf\x30\x30\x30\x30\x35\x00\x00\x00\
\x00\x00\x03\xfd\xc0\x00\x00\x10\x00\x00\x28\xaf\x00\x00\x00\x01\
\x00\x00\x01\xca\x00\x00\x00\x2c\x00\x00\x01\xcb\x00\x00\x00\x0c\
\x00\x00\x00\x00\x00\x00\x01\xcc\x00\x00\x00\x18\x31\x30\x30\x33\
\x30\x30\x37\x39\x36\x35\x36\x33\x36\x30\x36\x30\x00\x00\x03\xf8\
\xc0\x00\x00\x8c\x00\x00\x28\xaf\x00\x00\x04\x04\xc0\x00\x00\x10\
\x00\x00\x28\xaf\x00\x00\x00\x05\x00\x00\x02\x04\xc0\x00\x00\x10\
\x00\x00\x28\xaf\x00\x7a\x12\x00\x00\x00\x02\x03\xc0\x00\x00\x10\
\x00\x00\x28\xaf\x03\xd0\x90\x00\x00\x00\x03\xfc\xc0\x00\x00\x11\
\x00\x00\x28\xaf\x30\x30\x30\x30\x35\x00\x00\x00\x00\x00\x04\x0a\
\xc0\x00\x00\x3c\x00\x00\x28\xaf\x00\x00\x04\x16\xc0\x00\x00\x10\
\x00\x00\x28\xaf\x00\x00\x00\x01\x00\x00\x04\x17\xc0\x00\x00\x10\
\x00\x00\x28\xaf\x00\x00\x00\x01\x00\x00\x04\x18\xc0\x00\x00\x10\
\x00\x00\x28\xaf\x00\x00\x00\x01\x00\x00\x03\xe8\xc0\x00\x00\x10\
\x00\x00\x28\xaf\x00\x00\x00\x00\x00\x00\x07\xe0\xc0\x00\x00\x10\
\x00\x00\x6f\x2a\x00\x00\x00\x01'


#print " ".join(hex(ord(n)) for n in raw[0:6])


#0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#| Version       |                    Message Length             |
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#| command flags |                     Command-Code              |
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|                          Application-ID                       |
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|                      Hop-by-Hop Identifier                    |
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|                      End-to-End Identifier                    |
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#| AVPs ...
#+-+-+-+-+-+-+-+-+-+-+-+-+-


MSG_HEADER_LENGTH=20

msgIndex=0 #assume msgIndex start from 0

version=struct.unpack('!B',raw[msgIndex])[0]
msgLength=struct.unpack('!I',raw[msgIndex:msgIndex+4])[0] & 0x00ffffff
cmdFlag=struct.unpack('!B',raw[msgIndex+4])[0]
cmdCode=struct.unpack('!I',raw[msgIndex+4:msgIndex+8])[0] & 0x00ffffff
appId=struct.unpack('!I',raw[msgIndex+8:msgIndex+12])[0] #type? unsigned integer?
hbhId=struct.unpack('!I',raw[msgIndex+12:msgIndex+16])[0]
e2eId=struct.unpack('!I',raw[msgIndex+16:msgIndex+20])[0]

msg=DiameterMessage(version,msgLength,cmdFlag,cmdCode,appId,hbhId,e2eId,[])

#0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|                           AVP Code                            |
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|V M P r r r r r|                   AVP Length                  |
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|                        Vendor-ID (opt)                        |
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#| Data ...
#+-+-+-+-+-+-+-+-+

avpRoot=[]
avpIndexStack=[]
avpIndexStack.append([msgIndex+MSG_HEADER_LENGTH,msgIndex+msgLength,avpRoot]) #avp index pos, maximum index, parent avp

while len(avpIndexStack)>0:
    avpIndex, maxIndex,parentAVP=avpIndexStack.pop()    
    avpCode=struct.unpack('!I',raw[avpIndex:avpIndex+4])[0]
    avpFlag=struct.unpack('!B',raw[avpIndex+4])[0]
    vendorFlag=avpFlag & 0x80 >0
    mandatoryFlag= avpFlag & 0x40 >0
    encryptionFlag= avpFlag & 0x20 >0
    avpLength=struct.unpack('!I',raw[avpIndex+4:avpIndex+8])[0] & 0x00ffffff
    vendorId= None
    
    dataIndex=avpIndex+8
    if vendorFlag==True:
        vendorId=struct.unpack('!I',raw[avpIndex+8:avpIndex+12])[0] & 0x00ffffff
        dataIndex=avpIndex+12

    avp={'avpCode':avpCode,
         'vendorFlag':vendorFlag,
         'mandatoryFlag':mandatoryFlag,
         'encryptionFlag':encryptionFlag,
         'avpLength':avpLength,
         'vendorId':vendorId
         }

    #(self,code,length,isVendor,isMandatory,isEncryption,vendorId, dataType, rawValue):
    avp2=DiameterAVP(avpCode, avpLength, vendorFlag,mandatoryFlag,encryptionFlag, vendorId, 'dataType',[])

    #calculate next AVP index position and put in stack
    realLength=avpLength
    if avpLength%4>0: realLength=int(avpLength/4)*4+4
    if (avpIndex+realLength)<maxIndex:
        avpIndexStack.append([avpIndex+realLength, maxIndex,parentAVP])

    #lookup AVP Data Type form AVP Dictionary
    avpType=None
    avpDef=avpDic.get(avpCode)
    if not avpDef is None: avpType=avpDef['type']

    #parse AVP    
    if avpType=="Grouped":
        avp["avps"]=[]
        avpIndexStack.append([dataIndex,avpIndex+avpLength,avp["avps"]])

    parentAVP.append(avp)
    

msg.avps=avpRoot

print msg
    
#printAVPTree(avpRoot,0)
