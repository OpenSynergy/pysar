from lxml import etree
from lxml import objectify
import types

from ar_mm import MMHelper

AR_NAMESPACE = '{http://somesar.org/schema/r4.0}'
AR_NS_LEN = len(AR_NAMESPACE)
AR_PARSER = None

class AR:
    msg = 'Too many {} values with definition: {} in: {}'

    def __init__(self, obj, parent=None):
        self.obj = obj
        self.parent = parent
        self.ar_type = obj.tag[AR_NS_LEN:]
        self.children = {}
        self.wrap_self()

    def get_root_obj(self):
        crt = self
        nxt = crt.parent
        while nxt:
            crt = nxt
            nxt = crt.parent
        return crt

    def get_identifiable(self, uri):
        if not isinstance(uri, str):
            uri = str(uri)
        segments = uri.split('/')
        length = len(segments)
        i = 0
        root = self.get_root_obj()
        if 0 == length:
            return root
        if '' == segments[0]:
            i = 1
        crt = root
        child = None
        while i < length:
            children = crt.all_children()
            named_children = filter(
                lambda e: has_short_name(e, segments[i]), 
                children)
            if len(named_children) == 1:
                child = named_children[0]
                crt = child
                i += 1
            else:
                break
        return child

    def find(self, ar_type, **kwargs):
        def find_aux(obj, ar_type, result):
            if isinstance(obj, AR):
                for child in obj.all_children():
                    if isinstance(child, AR) and is_type(child, ar_type):
                        if MMHelper.attrib_match(child, kwargs):
                            result.append(child)
                    find_aux(child, ar_type, result)
            return result
        ar_type = MMHelper.maps(ar_type)
        result = []
        return find_aux(self, ar_type, result)

    def find_first(self, ar_type, **kwargs):
        lst = self.find(ar_type, **kwargs)
        if len(lst) > 0:
            return lst[0]

    def all_children(self):
        result = []
        for key, val in self.children.items():
            if isinstance(val, list):
                result += val
            else:
                result.append(val)
        return result

    def wrap_self(self, parent=None):
        for feature in self.obj.getchildren():
            grand_children = feature.getchildren()
            attr = feature.tag[AR_NS_LEN:]
            lower_attr = MMHelper.wrap_name(attr)
            if grand_children:
                filtered = filter(lambda e: e.tag != 'comment', grand_children)
                grand_children_wrappers = [AR(grand_child, self) for grand_child in filtered]
                self.children[lower_attr] = grand_children_wrappers
            else:
                if lower_attr == MMHelper.WRAP_DEFINITION_REF:
                    self.children[MMHelper.wrap_name('DEFINITION')] = types.MethodType(
                                                    MMHelper.get_definition(),
                                                    self, type(self))
                self.children[lower_attr] = types.MethodType(
                                                    MMHelper.single_attr(attr), 
                                                    self, type(self))

    def get_container_value(self, attr):
        feature = MMHelper.WRAP_SUB_CONTAINERS
        if is_type(self, 'MODULE_CONFIGURATION'):
            feature = MMHelper.WRAP_CONTAINERS
        if self.children.has_key(feature):
            cont_vals = self.children[feature]
            vals = filter(
                        lambda e: MMHelper.has_definition(e, attr), 
                        cont_vals)
            if [] == vals:
                return None
            val = vals[0]
            def_uri = MMHelper.get_definition_uri(val)
            definition = self.get_identifiable(def_uri)
            wrap_upper_multi_inf = MMHelper.WRAP_UPPER_MULTIPLICITY_INFINITE
            if hasattr(definition, wrap_upper_multi_inf):
                if getattr(definition, wrap_upper_multi_inf):
                    return vals
            wrap_upper_multi = MMHelper.WRAP_UPPER_MULTIPLICITY
            if 1 == getattr(definition, wrap_upper_multi):
                if len(vals) > 1:
                   raise AttributeError(self.msg.format('container', def_uri, self))
                else:
                    return val
            else:
                return vals

    def get_parameter_value(self, attr):
        wrap_parameter_values = MMHelper.WRAP_PARAMETER_VALUES
        if self.children.has_key(wrap_parameter_values):
            par_vals = self.children[wrap_parameter_values]         
            vals = filter(lambda e: MMHelper.has_definition(e, attr), par_vals)
            if [] == vals:
                return None
            val = vals[0]
            def_uri = MMHelper.get_definition_uri(val)
            definition = self.get_identifiable(def_uri)
            wrap_upper_multi_inf = MMHelper.WRAP_UPPER_MULTIPLICITY_INFINITE
            if hasattr(definition, wrap_upper_multi_inf):
                if getattr(definition, wrap_upper_multi_inf):
                    return vals
            wrap_upper_multi = MMHelper.WRAP_UPPER_MULTIPLICITY
            wrap_value = MMHelper.WRAP_VALUE
            if 1 == getattr(definition, wrap_upper_multi):
                if len(vals) > 1:
                    raise AttributeError(self.msg.format('parameter', def_uri, self))
                else:
                    return getattr(val, wrap_value)
            else:
                return [getattr(v, wrap_value) for v in vals]

    def __str__(self):
        name = ''
        if hasattr(self, MMHelper.WRAP_SHORT_NAME):
            name = ': ' + getattr(self, MMHelper.WRAP_SHORT_NAME)
        return "AR({0} {1})".format(self.ar_type, name)
    
    def __repr__(self):
        return str(self)

    def __getattr__(self, attr):
        attr = MMHelper.maps(attr)
        if self.children.has_key(attr):
            child = self.children[attr]
            if isinstance(child, list):
                return child
            else:
                result = child()
                if isinstance(result, objectify.StringElement):
                    return str(result)
                return result
        if self.ar_type.startswith('MACC_'):
            g = self.get_parameter_value(attr)
            if g is not None:
                return g
            g = self.get_container_value(attr)
            if g is not None:
                return g
        raise AttributeError(attr)

def init_parser(schema_file):
    parser = AR_PARSER
    f = open(schema_file, "r")
    schema = etree.XMLSchema(file=f)
    parser = objectify.makeparser(schema = schema)
    return parser

def set_schema(schema_file):
    global AR_PARSER
    AR_PARSER = init_parser(schema_file)

def read(arxml_file):
    parser = AR_PARSER
    g = open(arxml_file, "r")
    config = g.read()
    somesar = objectify.fromstring(config, parser=parser)
    return somesar

def findall(root, element_type):
    return root.findall('.//' + AR_NAMESPACE + element_type)

def has_short_name(element, short_name):
    wrap_SHORT_NAME = MMHelper.WRAP_SHORT_NAME
    return (hasattr(element, wrap_SHORT_NAME)
        and getattr(element, wrap_SHORT_NAME) == short_name)

def is_type(ar_obj, ar_type):
    ar_type = MMHelper.maps(ar_type)
    return ar_obj.obj.tag == AR_NAMESPACE + ar_type