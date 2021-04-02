import xml.etree.ElementTree as ET

def parse_yt_xml(xml_body: str) -> (str, str):
    root = ET.fromstring(xml_body)
    entry = root.find("{http://www.w3.org/2005/Atom}entry")
    title = entry.find("{http://www.w3.org/2005/Atom}title") 
    link = entry.find("{http://www.w3.org/2005/Atom}link")

    return title.text, link.attrib["href"]


if __name__ == "__main__":
    with open("test.xml", "r") as xml_file:
        text = xml_file.read()
        root = ET.fromstring(text)
        print(root)
