from pysar import ar

if __name__ == '__main__':
	ar.set_schema('somesar_4.xsd')
	root = ar.AR(ar.read('ecuc.xml'))

	Demo = root.find_first(
		'MODULE_CONFIGURATION', 
		DefinitionRef='/SOMESAR/SomeDefs/Demo')
	print Demo

	DemoGeneral = Demo.getDemoGeneral
	print DemoGeneral
	
	debounce_counter_support = DemoGeneral.getDemoDebounceCounterBasedSupport
	print debounce_counter_support

	status_changed_callbacks = DemoGeneral.getDemoCallbackDTCStatusChanged
	for callback in status_changed_callbacks:
		print callback.getDemoCallbackDTCStatusChangedFnc

	print Demo.getDefinition

	system = root.find_first('SYSTEM')
	print system.getShortName

	system_signal = root.find_first('SYSTEM_SIGNAL')
	print system_signal
	print system_signal.getDynamicLength