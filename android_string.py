__author__ = 'fanjunwei003'


import xml.dom.minidom as minidom


def main():
    dom=minidom.parse('strings.xml')
    strings = dom.getElementsByTagName('string')
    for e in strings:
        print e.nodeName
        for c in e.childNodes:
            if c.nodeType in ( c.TEXT_NODE, c.CDATA_SECTION_NODE):
                print c.data
                c.data='xxx'

    f=open('new.xml','w')
    dom.writexml(f,encoding = 'utf-8')
    f.close()


main()