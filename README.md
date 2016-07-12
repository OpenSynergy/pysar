# PySAR

## Rationale

PySAR was created in my spare time as a proof of concept framework for model access and code generation using Python. 

Code generation based on some type of model or IDL is a very important technique in complex contemporary software systems. Some particularly relevant fields are: avionics, automotive and telecom.

Existing model access and code generation solutions are usually very heavyweight. In the Eclipse world, they typically rely at least on: EMF and its myriad of related frameworks and components, and, in the automotive/[AUTOSAR](http://www.autosar.org/) domain, ARTOP. Development using these technologies is not always easy, so a reasonably good living can be earned as a model-driven tooling expert. These experts can easily become a bottleneck for embedded development, if things aren't kept in check. In addition to being complex, these technologies are sometimes over-engineered and buggy. Consider also that a significant number of companies that are based to a degree on preserving this status quo --- because it earns them consulting and customer "tailoring" projects --- and therefore have little financial incentive to properly "fix" the deeper architectural problems.

PySAR aims to show that such complex Eclipse/EMF solutions are not the only ones to be considered when it comes to open source model-driven tooling.

Specifically, it tries to support the vision of a kind of 'code generation socialism' --- I think that it would be ideal if embedded developers were to control the means of code generation :-) This allows embedded developers to perform quick fixes and improvements that also involve the generators, and can eliminate the bottleneck on the model engineer. Obviously, this may not be suited to all use-cases of AUTOSAR MDE --- for some of these, the rich validation frameworks and graphical components have their place, and PySAR does not aim to replace ARTOP/Sphinx/EMF/Eclipse altogether. Instead, I would try to keep it small, comprehensible and extensible.

## The Means...

Therefore, working in Python, I am using lxml.objectify instead of EMF, using Jinja2 templates instead of Xtend templates for code generation, and some custom code to dynamically populate objects with extra utility methods (for example, for the AUTOSAR ECUC-like objects such as module configurations and containers --- e.g., in the slides, DemoGeneral.getDemoDebounceCounterBasedSupport). The name "Demo" could be thought of as corresponding to an AUTOSAR BSW module, but it is entirely hypothetical.

The code does not depend on AUTOSAR consortium artifacts by design, due to license restrictions. The included examples work on an XML "model" document and corresponding XML Schema that are AUTOSAR-like, but limited to the narrow scope of this model. However, it is almost trivial for a skilled AUTOSAR model engineer to change it so that it supports processing standard AUTOSAR models based on the published schemata. The two scripts: 'transform_arxml.py' and 'transform_schema.py', aim to ease this 'translation' of AUTOSAR artifacts to the format supported by PySAR. Additionally, adjustments have to be done to the pysar/ar_mm module, to replace the necessary strings with their AUTOSAR counterparts.

The initial feature set is small (no splittable support, no fancy optimizations, no remote model repositories) and the code is fairly "rough around the edges (and maybe in-between too)" but the framework is very easily extensible --- as you expect from a ~300 lines Python codebase ;-)

To the observing reader with safety-related concerns (considering domains such as automotive or avionics), I would say that on the one hand it is true that Python being dynamically typed can be a question mark. However my belief is that the ability to easily change/fix the code of the clients/generators and of the framework itself can be more important for the resulting overall safety and correctness. That said, the applicable license for PySAR, is found in the accompanying "LICENSE" file and it includes the standard disclaimers for BSD-licensed software.

The distribution notably includes:
- the pysar package with the ar, ar_mm, and ar_cg modules
- the templates folder with Jinja2 codegen templates for the examples (also using template inheritance --- as an application to standardized C header generation)
- the model_access.py and code_gen.py files that demo model access and code generation, respectively.
- unit tests in the 'test_pysar.py' file (to be run with py.test).

Enjoy, and know that your feedback is highly appreciated.

I'd also like to thank OpenSynergy, Inc.'s management for the permission to publish this as open source under the company's "umbrella".

Cheers,
Cornel

(cornel dot izbasa at openberrysynergy dot com minus fruit)

## P.S. (for whomever may care)

To paraphrase the esteemed Alan J. Perlis, 
"This _code_ is dedicated, in respect and admiration, to the spirit that lives in the computer."

I feel this quote from Structure and Interpretation of Computer Programs is still very relevant nowadays, although we're starting to move away from the nascent phase of computer programming [SICP](https://mitpress.mit.edu/sicp/full-text/sicp/book/book.html):
-------------8<----------------------
``I think that it's extraordinarily important that we in computer science keep fun in computing. When it started out, it was an awful lot of fun. Of course, the paying customers got shafted every now and then, and after a while we began to take their complaints seriously. We began to feel as if we really were responsible for the successful, error-free perfect use of these machines. I don't think we are. I think we're responsible for stretching them, setting them off in new directions, and keeping fun in the house. I hope the field of computer science never loses its sense of fun. Above all, I hope we don't become missionaries. Don't feel as if you're Bible salesmen. The world has too many of those already. What you know about computing other people will learn. Don't feel as if the key to successful computing is only in your hands. What's in your hands, I think and hope, is intelligence: the ability to see the machine as more than when you were first led up to it, that you can make it more.''
-- Alan J. Perlis (April 1, 1922-February 7, 1990)
-------------8<----------------------