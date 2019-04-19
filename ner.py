from lxml.etree import iterparse

# sentence per line, tokenized, entities enclosed w/ start, end tag
"""<START:person> Pierre Vinken <END> , 61 years old , will join the board as a nonexecutive director Nov. 29 .
Mr . <START:person> Vinken <END> is chairman of Elsevier N.V. , the Dutch publishing group .
"""

filename = 'data\ssj500k-sl.body.xml'

ner_file = open("data\\ner.txt", 'wb')

for event, elem in iterparse(filename, tag=("{http://www.tei-c.org/ns/1.0}s"), events=(
        'end',), recover=True, encoding='utf8', huge_tree=True, collect_ids=False):

    words = list()

    for child in elem:
        if child.attrib.get('ana', None) and child.text and child.text.strip() != "":
            words.append(child.text)
        elif child.tag == "{http://www.tei-c.org/ns/1.0}seg" and child.attrib.get('type', None) == 'name':
            ner = child.attrib.get('subtype', None)
            words.append("<START:{}>".format(ner, ))

            for seg_child in child:
                if seg_child.attrib.get('ana', None) and seg_child.text:
                    words.append(seg_child.text)

            words.append("<END>")

    ner_file.write(" ".join(words).encode('utf-8'))
    ner_file.write("\n".encode('utf-8'))
    words.clear()

    elem.clear()

ner_file.close()
