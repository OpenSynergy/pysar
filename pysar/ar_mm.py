class MMHelper:
    @staticmethod
    def wrap_name(attr):
        names = [part.capitalize() for part in attr.split('_')]
        return MMHelper.GETTER_PREFIX + ''.join(names)

    @staticmethod
    def definition_name(getter):
        prefix = MMHelper.GETTER_PREFIX
        if not getter.startswith(prefix):
            return getter
        return getter[len(prefix):]

    @staticmethod
    def has_definition(e, getter):
        return MMHelper.get_definition_uri(e).endswith(
                            '/' + MMHelper.definition_name(getter))

    @staticmethod
    def single_attr(attr):
        return lambda self: getattr(self.obj, attr)

    @staticmethod
    def attrib_match(element, kwargs):
        for attr, value in kwargs.items():
            getter = MMHelper.GETTER_PREFIX + attr
            if not hasattr(element, getter):
                return False
            if getattr(element, getter) != value:
                return False
        return True

    @staticmethod
    def get_definition_uri(definable):
        ref = getattr(definable, MMHelper.WRAP_DEFINITION_REF)
        if not ref:
            return None
        return str(ref)

    @staticmethod
    def maps(attr):
        return (MMHelper.mapped.has_key(attr) and
                MMHelper.mapped[attr] or
                attr)

    @staticmethod
    def get_definition():
        return lambda self: self.get_identifiable(getattr(self, MMHelper.WRAP_DEFINITION_REF))

    @staticmethod
    def init():
        MMHelper.mapped = {
            'MODULE_CONFIGURATION': 'MACC_MODULE_CONFIGURATION_VALUES',
            'MODULE_DEFINITION': 'MACC_MODULE_DEF',
        }
        MMHelper.GETTER_PREFIX='get' 
        wrapped_attrs = ['SHORT_NAME', 'DEFINITION_REF', 
        'CONTAINERS', 'SUB_CONTAINERS', 'UPPER_MULTIPLICITY',
        'UPPER_MULTIPLICITY_INFINITE', 'PARAMETER_VALUES', 'VALUE']
        for attr in wrapped_attrs:
            setattr(MMHelper, 'WRAP_' + attr.upper(), MMHelper.wrap_name(attr))

MMHelper.init()
