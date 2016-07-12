from pysar import ar

ar.set_schema('somesar_4.xsd')

somesar = ar.read('ecuc.xml')

class TestModel:
	def test_system_signal(self):
		system_signals = ar.findall(somesar, 'SYSTEM_SIGNAL')
		assert system_signals
		assert len(system_signals) == 1
		system_signal = system_signals[0]
		assert system_signal is not None
		assert hasattr(system_signal, 'DYNAMIC_LENGTH')
		assert system_signal.DYNAMIC_LENGTH == False

	def find_Demo_module_config(self):
		module_configs = ar.findall(somesar, 'MACC_MODULE_CONFIGURATION_VALUES')
		assert module_configs
		assert len(module_configs) == 1
		module_config = module_configs[0]
		assert module_config is not None
		assert hasattr(module_config, 'SHORT_NAME')
		assert module_config.SHORT_NAME == 'Demo'
		return module_config
		
	def test_module_config_wrap(self):
		Demo = self.find_Demo_module_config()
		Demo_w = ar.AR(Demo)
		assert Demo_w is not None
		assert Demo_w.getShortName == 'Demo'
		print Demo_w
		assert Demo_w.getDefinitionRef == '/SOMESAR/SomeDefs/Demo'
		containers = Demo_w.getContainers
		assert containers is not None
		assert len(containers) == 2
		assert ar.is_type(containers[0], 'MACC_CONTAINER_VALUE')
		assert ar.is_type(containers[1], 'MACC_CONTAINER_VALUE')

	def test_find_Demo_config_wrapped_model(self):
		root = ar.AR(somesar)
		assert isinstance(root, ar.AR)
		res = root.find('MODULE_CONFIGURATION', DefinitionRef='/SOMESAR/SomeDefs/Demo')
		assert isinstance(res, list)
		assert len(res) == 1
		Demo = res[0]
		assert isinstance(Demo, ar.AR)
		containers = Demo.getContainers
		assert isinstance(containers, list)
		assert 'Demo' == Demo.getShortName
		def_uri = Demo.getDefinitionRef
		assert '/SOMESAR/SomeDefs/Demo' == def_uri
		Demo_def = root.get_identifiable(def_uri)
		assert isinstance(Demo_def, ar.AR)
		assert ar.is_type(Demo_def, 'MACC_MODULE_DEF')
		Demo_def = Demo.get_identifiable(def_uri)
		assert isinstance(Demo_def, ar.AR)
		assert ar.is_type(Demo_def, 'MACC_MODULE_DEF')
		Demo_def = Demo.getDefinition
		assert isinstance(Demo_def, ar.AR)
		assert ar.is_type(Demo_def, 'MODULE_DEFINITION')

	def test_find_Demo_definition_wrapped_model(self):
		root = ar.AR(somesar)
		res = root.find('MACC_MODULE_DEF', ShortName='Demo')
		assert isinstance(res, list)
		assert len(res) == 1
		Demo_def = res[0]
		assert isinstance(Demo_def, ar.AR)
		assert 'Demo' == Demo_def.getShortName
		containers = Demo_def.getContainers
		assert isinstance(containers, list)
		assert len(containers) == 1
		names = [container.getShortName for container in containers]
		assert 'DemoGeneral' in names
