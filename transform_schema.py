from lxml import etree
import sys

def usage():
	print "Usage: python " + sys.argv[0] + " <AUTOSAR_#-#-#.xsd>"

def transform(e):
	if e.tag == '{http://www.w3.org/2001/XMLSchema}pattern':
		return
	for attr in e.attrib:
		if not e.attrib[attr].startswith('xsd:'):
			e.attrib[attr] = e.attrib[attr].replace('-','_')

def main():
	if (len(sys.argv) < 2):
		usage()
		return
	f=open(sys.argv[1])
	schema = f.read()
	doc = etree.XML(schema)
	for e in doc.xpath('//*'):
		transform(e)
	print etree.tostring(doc)

if __name__ == '__main__':
	main()