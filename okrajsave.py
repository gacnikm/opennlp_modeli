from lxml.etree import iterparse
from lxml import etree

abbrvs = set()

# SSJ
filename = 'data\ssj500k-sl.body.xml'

for event, elem in iterparse(filename, tag=("{http://www.tei-c.org/ns/1.0}p"), events=(
        'end',),recover=True, encoding='utf8', huge_tree=True,collect_ids=False):
    for child in elem.findall(".//{http://www.tei-c.org/ns/1.0}*[@ana='mte:O']"):
        abbrvs.add(child.text)

    elem.clear()

# create xml
dictionary = etree.Element('dictionary',case_sensitive="false")

for abbrv in abbrvs:
    entry = etree.SubElement(dictionary, 'entry')
    token = etree.SubElement(entry, 'token')
    token.text = abbrv

outFile = open('data\okr.xml', 'wb')
outFile.write(etree.tostring(dictionary, xml_declaration=True,pretty_print=True,encoding="utf-8"))