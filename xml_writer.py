from xml.dom import minidom
from HTMLParser import HTMLParser
import sys,ast, traceback

def outputToXmlFile(fileName,batchRef):
    try:
        outFile = open (fileName + ".xml" , "wb")
        xmlStr = batchRef.toxml()
        hp = HTMLParser()
        try:
            outFile.write(hp.unescape(xmlStr))
            #print (hp.unescape(xmlStr))#for debugging
        finally:
            #print '' #for debugging
            outFile.close
    except IOError:
        traceback.print_exc()           
    
def main(argv):
    # argument checks
    if len(sys.argv)!= 4:
        print "usage: xml_writer.py xmlSample.xml inputfile.txt outputfileName"
        sys.exit(1)
    
    elif not str(sys.argv[1]).lower().endswith('.xml'):
        print "usage: xml_writer.py xmlSample.xml inputfile.txt outputfileName"
        sys.exit(1)

    elif not str(sys.argv[2]).lower().endswith('.txt'):
        print "usage: xml_writer.py xmlSample.xml inputfile.txt outputfileName"
        sys.exit(1)           

    #read fuzzing input file
    inputFile=str(sys.argv[2])
    inputArr =[]
    i=0
    for line in open(inputFile, 'r'):
        inputArr.append(line.rstrip())

    #read xml file
    xmlFile=str(sys.argv[1])
    md = minidom.parse(xmlFile)
    
    #root element 
    batch=md.getElementsByTagName('ROOT') 
    batchRef = batch[0]
    outFileCounter = 0 
    
    #only goes 3 levels deep after root
    #1st level, root level
    for fuzzInput in inputArr: #iterate through sample input      
        if len(batchRef.attributes.items()) > 0:
            for batchAttrName, batchAttrValue in batchRef.attributes.items():
                batchRef.setAttribute(batchAttrName,fuzzInput)
                outputToXmlFile(sys.argv[3] + str(outFileCounter),batchRef)
                batchRef.setAttribute(batchAttrName, batchAttrValue)
                outFileCounter += 1
        if batchRef.hasChildNodes():
            #2nd level
            for bc in batchRef.childNodes:
                bcMd = md.getElementsByTagName(bc.nodeName)
                bcRef = bcMd[0]
                bcNodeValue = bcRef.firstChild
                if bcNodeValue:
                    if bcNodeValue.nodeValue:
                        origbcRefVal = bcNodeValue.nodeValue
                        bcNodeValue.replaceWholeText(fuzzInput)
                        outputToXmlFile(sys.argv[3] + str(outFileCounter),batchRef)
                        bcNodeValue.replaceWholeText(origbcRefVal)
                if len(bcRef.attributes.items()) > 0:
                    for bcAttrName, bcAttrValue in bcRef.attributes.items():
                        bcRef.setAttribute(bcAttrName, fuzzInput)
                        outputToXmlFile(sys.argv[3] + str(outFileCounter),batchRef)
                        bcRef.setAttribute(bcAttrName,  bcAttrValue)
                        outFileCounter += 1
                #3rd level
                if bcRef.hasChildNodes():
                    for y in bcRef.childNodes:
                        yMd = md.getElementsByTagName(y.nodeName)
                        yRef = yMd[0]
                        yNodeValue = yRef.firstChild
                        if yNodeValue:
                            if yNodeValue.nodeValue:
                                origyRefVal = yNodeValue.nodeValue
                                yNodeValue.replaceWholeText(fuzzInput)
                                outputToXmlFile(sys.argv[3] + str(outFileCounter),batchRef)
                                yNodeValue.replaceWholeText(origyRefVal)
                        if len(yRef.attributes.items())>0:
                            for yAttrName, yAttrValue in yRef.attributes.items():
                                yRef.setAttribute(yAttrName, fuzzInput)
                                outputToXmlFile(sys.argv[3] + str(outFileCounter),batchRef)
                                yRef.setAttribute(yAttrName, yAttrValue)
                        #4th level
                        if yRef.hasChildNodes:
                            for z in yRef.childNodes:
                                zMd = md.getElementsByTagName(z.nodeName)
                                zRef = zMd[0]
                                zNodeValue = zRef.firstChild
                                if zNodeValue:
                                    if zNodeValue.nodeValue:
                                        origzRefVal = zNodeValue.nodeValue
                                        zNodeValue.replaceWholeText(fuzzInput)
                                        outputToXmlFile(sys.argv[3] + str(outFileCounter),batchRef)
                                        zNodeValue.replaceWholeText(origzRefVal)
                                if len(zRef.attributes.items())>0:
                                    for zAttrName, zAttrValue in zRef.attributes.items():
                                        zRef.setAttribute(zAttrName, fuzzInput)
                                        outputToXmlFile(sys.argv[3] + str(outFileCounter),batchRef)
                                        zRef.setAttribute(zAttrName, zAttrValue)                                    
                                        outFileCounter += 1    
if __name__ == "__main__":
   main(sys.argv)
