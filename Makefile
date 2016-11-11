#!/usr/bin/env make
#
# PEP8 rules are intentionally violated as follows:
# E203 Vertically lining up ',' is preferred to the standard for readability.
# E221 Vertically lining up '=' is preferred to the standard for readability.
PEP8IGNORE=--ignore=E202,E203,E221,E241,E272
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
	*.pyc \
	*.js \
	*.out

MODULES=UniArray UniClass UniDict UniDigit UniDoc UniTree

antlr4=java -jar /usr/local/lib/antlr-4.5.3-complete.jar

%.pep8 : %.py
	@-pep8 $(PEP8IGNORE) $< > $@ 2>&1

%.pyfl : %.py
	@-pyflakes $< > $@ 2>&1

all: $(PEP8) $(PYFL) grammar Makefile
	@echo "Ran Quality Control checks with pep8 and pyflakes."
	@echo \
		`wc -c *.pep8 *.pyfl \
		|sed -e 's/  */ /' \
		|cut -d' ' -f2 \
		|tr '\n' '+' \
		|sed -e 's/+$$//' \
		|bc` bytes of error found

classify16.g4: UniGrammar.py
	@./UniGrammar.py

grammar: classify16.g4 test_Codepoint.g4
		@$(antlr4) -Dlanguage=Python2 -visitor test_Codepoint.g4
		@./test_Codepoint.py

.PHONY:
todo:
	@echo "TODO: Integrate UniDict in place of self.__dict__ = self dict"
	@echo "TODO: Unit tests need to be improved."
	@echo "TODO: Unit test for UniArray top-level block replacement fails.

.PHONY:
test:
	@echo "Run unit tests on $(MODULES)."
	@py.test > py.test.out 2>&1
	@cat py.test.out

.PHONY:
clean:
	@echo "Remove intermediate files not used in the git repository."
	@rm -f $(ARTIFACTS)
