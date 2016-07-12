from pysar import ar
from pysar import ar_cg

def gen_cfg_h(module):
	def_name = module.getDefinition.getShortName
	cg = ar_cg.CodeGen('bsw/' + def_name + '_Cfg_h.j2')
	return cg.generate(
		header_base = def_name.upper(),
		Demo=module)

if __name__ == '__main__':
	ar.set_schema('somesar_4.xsd')
	root = ar.AR(ar.read('ecuc.xml'))
	Demo = root.find_first(
				'MODULE_CONFIGURATION', 
				DefinitionRef='/SOMESAR/SomeDefs/Demo')
	print gen_cfg_h(Demo)