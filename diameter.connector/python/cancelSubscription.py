#!/usr/bin/python

from suds.client import Client
import sys, getopt, csv, logging, suds,time, datetime

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.FATAL)

def main(argv):
    inputfile=''
    endpoint='' #http://16.173.234.54:7442/atomws/RtServices?wsdl
    try:
        opts, args = getopt.getopt(argv,"he:i:",["help","endpoint=","ifile="])
    except getopt.GetoptError:
        print 'cancelSubscription.py -e <endpoint> -i <inputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            print 'cancelSubscription.py -e <endpoint> -i <inputfile>'
            sys.exit()
        elif opt in ("-e", "--endpoint"):
            endpoint = arg
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        
    print 'Endpoint:', endpoint
    print 'Input file:', inputfile

    client = Client(endpoint)

    #TODO open a write file "error.log", if the file already exist, override the old one
    errorFile=open("error.log",'wb')
    
    inputCSVFile=open(inputfile, 'rb')
    parameters=csv.reader(inputCSVFile, delimiter=',')
    processCounter=0
    failedProcessCounter=0
    for subscriberId,subscriptionId in parameters:
        processCounter=processCounter+1
        try:    
            result=client.service.cancelSubscription(subscriberId,subscriptionId) #subscirberid, subscriptionid
        except suds.WebFault as detail:
            failedProcessCounter=failedProcessCounter+1
            #TODO write subscriberId,subscriptionId and fault detail into error log file
            errorFile.write("%s,%s\n" % (subscriberId,subscriptionId))
            errorFile.write(str(detail))
            errorFile.write("\n")

        if processCounter%50==0:
            print str(datetime.datetime.now()) + (": Has processed %s records with %s failed" %(processCounter,failedProcessCounter))
        time.sleep(0.01)

    print str(datetime.datetime.now())+ (": Totally processed %s records with %s failed" %(processCounter,failedProcessCounter))
        
    inputCSVFile.close()
    #TODO close error log file
    errorFile.close()
    
if __name__ == "__main__":
    #python cancelSubscription.py -e http://16.173.234.54:7442/atomws/RtServices?wsdl -i toronto.txt
    main(sys.argv[1:])
