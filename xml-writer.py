from xml.dom import minidom
from HTMLParser import HTMLParser
import sys,ast, traceback

def outputToXmlFile(fileName,rootRef):
    try:
        outFile = open (fileName + ".xml" , "wb")
        xmlStr = rootRef.toxml()
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
    root=md.getElementsByTagName('ROOT') 
    rootRef = root[0]
    outFileCounter = 0 
    
    #only goes 3 levels deep after root
    #1st level, root level
    for fuzzInput in inputArr: #iterate through sample input      
        if len(rootRef.attributes.items()) > 0:
            for rtAttrName, rtAttrValue in rootRef.attributes.items():
                rootRef.setAttribute(rtAttrName,fuzzInput)
                outputToXmlFile(sys.argv[3] + str(outFileCounter),rootRef)
                rootRef.setAttribute(rtAttrName, rtAttrValue)
                outFileCounter += 1
        if rootRef.hasChildNodes():
            #2nd level
            for node in rootRef.childNodes:
                rtMd = md.getElementsByTagName(rt.nodeName)
                rtRef = rtMd[0]
                rtNodeValue = rtRef.firstChild
                if rtNodeValue:
                    if rtNodeValue.nodeValue:
                        origrtRefVal = rtNodeValue.nodeValue
                        rtNodeValue.replaceWholeText(fuzzInput)
                        outputToXmlFile(sys.argv[3] + str(outFileCounter),rootRef)
                        rtNodeValue.replaceWholeText(origrtRefVal)
                if len(rtRef.attributes.items()) > 0:
                    for rtAttrName, rtAttrValue in rtRef.attributes.items():
                        rtRef.setAttribute(rtAttrName, fuzzInput)
                        outputToXmlFile(sys.argv[3] + str(outFileCounter),rootRef)
                        rtRef.setAttribute(rtAttrName,  rtAttrValue)
                        outFileCounter += 1
                #3rd level
                if rtRef.hasChildNodes():
                    for y in rtRef.childNodes:
                        yMd = md.getElementsByTagName(y.nodeName)
                        yRef = yMd[0]
                        yNodeValue = yRef.firstChild
                        if yNodeValue:
                            if yNodeValue.nodeValue:
                                origyRefVal = yNodeValue.nodeValue
                                yNodeValue.replaceWholeText(fuzzInput)
                                outputToXmlFile(sys.argv[3] + str(outFileCounter),rootRef)
                                yNodeValue.replaceWholeText(origyRefVal)
                        if len(yRef.attributes.items())>0:
                            for yAttrName, yAttrValue in yRef.attributes.items():
                                yRef.setAttribute(yAttrName, fuzzInput)
                                outputToXmlFile(sys.argv[3] + str(outFileCounter),rootRef)
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
                                        outputToXmlFile(sys.argv[3] + str(outFileCounter),rootRef)
                                        zNodeValue.replaceWholeText(origzRefVal)
                                if len(zRef.attributes.items())>0:
                                    for zAttrName, zAttrValue in zRef.attributes.items():
                                        zRef.setAttribute(zAttrName, fuzzInput)
                                        outputToXmlFile(sys.argv[3] + str(outFileCounter),rootRef)
                                        zRef.setAttribute(zAttrName, zAttrValue)                                    
                                        outFileCounter += 1    
if __name__ == "__main__":
   main(sys.argv)
