#!/usr/bin/env make
#
# PEP8 rules are intentionally violated as follows:
# E203 Vertically lining up ',' is preferred to the standard for readability.
# E221 Vertically lining up '=' is preferred to the standard for readability.

# This makefile controls a variety of operations performed on this library
# for use by developers in refactorings, improvements, and bug fixes

__module__     = "Makefile"
__author__     = "Jonathan D. Lettvin"
__copyright__  = "\
Copyright(C) 2016 Jonathan D. Lettvin, All Rights Reserved"
__credits__    = ["Jonathan D. Lettvin"]
__license__    = "GPLv3"
__version__    = "0.0.1"
__maintainer__ = "Jonathan D. Lettvin"
__email__      = "jlettvin@gmail.com"
__contact__    = "jlettvin@gmail.com"
__status__     = "Demonstration"
__date__       = "20161113"


# E202 is thrown when 
PEP8IGNORE=--ignore=E122,E128,E201,E202,E203,E221,E241,E272

PEP8=\
	 UniArray.pep8 \
	 UniClass.pep8 \
	 UniDict.pep8 \
	 UniDigit.pep8 \
	 UniDoc.pep8 \
	 UniGrammar.pep8 \
	 UniTree.pep8

PYFL=\
	 UniArray.pyfl \
	 UniClass.pyfl \
	 UniDict.pyfl \
	 UniDigit.pyfl \
	 UniDoc.pyfl \
	 UniGrammar.pyfl \
	 UniTree.pyfl

GRAMMARS=artifacts/classify16.g4 artifacts/classify21.g4

# keep classify*.g4 as production (TODO move them to artifacts)
ARTIFACTS=\
	$(PEP8) \
	$(PYFL) \
	*Lexer.py \
	*Parser.py \
	*Visitor.py \
	*Listener.py \
	*.tokens \
	*.dot \
	*.js \
	*.pyc \
	*.png \
	*.out

MODULES=UniArray UniClass UniDict UniDigit UniDoc UniTree

antlr4=java -jar /usr/local/lib/antlr-4.5.3-complete.jar

%.pep8 : %.py
	@-pep8 $(PEP8IGNORE) $< > $@ 2>&1
	@./timestamp $@ pep8 checked

%.pyfl : %.py
	@-pyflakes $< > $@ 2>&1
	@./timestamp $@ pyflakes checked

all: $(PEP8) $(PYFL) grammar test report todo Makefile
	@./timestamp $@ finished

.PHONY:
report:
	@./timestamp $@ \
		`wc -c *.pep8 *.pyfl \
		|sed -e 's/  */ /' \
		|cut -d' ' -f2 \
		|tr '\n' '+' \
		|sed -e 's/+$$//' \
		|bc` bytes of error found
	@./timestamp $@ generated

classify16.g4: UniGrammar.py
	@./UniGrammar.py
	@./timestamp $@ generated

grammar: classify16.g4 test_Codepoint.g4
	@$(antlr4) -Dlanguage=Python2 -visitor test_Codepoint.g4
	@./test_Codepoint.py
	@./timestamp $@ tested

.PHONY:
todo:
	@./timestamp $@ "Integrate UniDict replacing"
	@./timestamp $@ "Failing unit test in UniArray top-level block"
	@./timestamp $@ "Add UniTree codepoint cutting replacing dict lookup"

.PHONY:
test:
	@./timestamp $@ $(MODULES)
	@-py.test > py.test.out 2>&1
	@cat py.test.out
	@./timestamp $@ test to graphviz dot to png
	@set -e;\
		for f in $$(ls *.dot|sed -e 's/.dot//');\
		    do dot -Tpng $$f.dot > $$f.png;\
		done
	@./timestamp $@ tested and graphed

.PHONY:
clean:
	@rm -f $(ARTIFACTS)
	@./timestamp $@
