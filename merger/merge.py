#!/usr/bin/env python
import sys
import xml.etree.ElementTree as etree

KEY='SHORT-NAME'

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def shortTag(elt):
	return elt.tag[32:]

def merge(*trees):
	tree = etree.parse('root.xml')
	features = [feature for a in trees for feature in a.getroot().getchildren()]
	feature_merge(tree.getroot(), features)
	indent(tree.getroot())
	return tree

def feature_key(feature):
	return feature.tag

def merged_values(split_features):
	result = []
	for fragment in split_features:	
		result += fragment.getchildren()		
	return result

def merge_feature(parent, to_merge):
	merged = etree.SubElement(parent, to_merge[0].tag)
	vals = merged_values(to_merge)
	if len(vals) != 0:
		value_merge(merged, vals)
	else:
		merged.text = to_merge[0].text

def feature_merge(parent, features):
	if not features:
		return
	features.sort(key=feature_key)
	key = feature_key(features[0])
	to_merge = [features[0]]
	for feature in features[1:]:
		if key == feature_key(feature):
			to_merge.append(feature)
		else:
			merge_feature(parent, to_merge)
			to_merge = [feature]
			key = feature_key(feature)
	merge_feature(parent, to_merge)

def short_name(value):
	global KEY
	for child in value.getchildren():
		if KEY == shortTag(child):
			return child.text
	return ""

def short_name_child(value):
	global KEY
	for child in value.getchildren():
		if KEY == shortTag(child):
			return child
	return None

def value_key(value):
	return value.tag + ":" + short_name(value)

def merged_features(split_values):
	global KEY
	result = []
	for fragment in split_values:
		result += filter(lambda x: shortTag(x) != KEY, fragment.getchildren())
	return result

def merge_node(parent, to_merge):
	merged = etree.SubElement(parent, to_merge[0].tag)
	short_name_to_set = short_name_child(to_merge[0])
	if short_name_to_set is not None:
		merged.append(short_name_to_set)
	feature_merge(merged, merged_features(to_merge))

def value_merge(parent, values):
	if not values:
		return
	values.sort(key=value_key)
	key = value_key(values[0])
	to_merge = [values[0]]
	for value in values[1:]:
		if key == value_key(value):
			to_merge.append(value)
		else:
			merge_node(parent, to_merge)
			to_merge = [value]
			key = value_key(value)
	merge_node(parent, to_merge)

if __name__ == "__main__":
	etree.register_namespace('', 'http://autosar.org/schema/r4.0')
	if len(sys.argv) < 2:
		exit(1)
	trees = [etree.parse(arg) for arg in sys.argv[1:]]
	if len(trees) == 1:
		trees[0].write(sys.stdout)
	tree = merge(*trees)
	tree.write(sys.stdout)
