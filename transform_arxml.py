from lxml import etree
import sys
import re

DATE_OR_NUMBER_PATTERN = re.compile(r"[0-9-]+")
NAME_PATTERN = re.compile(r"([A-Z0-9]+-[A-Z0-9]+)+")

def usage():
	print "Usage: python " + sys.argv[0] + " <file.arxml>"

def transform(e):
	e.tag = e.tag.replace('-','_')
	for attr in e.attrib:
		e.attrib[attr] = e.attrib[attr].replace('-','_')
	if not e.text:
		return
	if re.match(DATE_OR_NUMBER_PATTERN, e.text):
		return
	if re.match(NAME_PATTERN, e.text):
		e.text = e.text.replace('-','_')

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