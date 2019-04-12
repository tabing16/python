import csv
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


def prettyfy(element):
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")


root = ET.Element("Root")
doc = ET.SubElement(root, "doc")
ET.SubElement(doc, "field1", name="blah").text = "some value1"

with open("filename.xml", "w") as f:
    f.write(prettyfy(root))
   