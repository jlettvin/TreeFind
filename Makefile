#!/usr/bin/env make
#
# PEP8 rules are intentionally violated as follows:
# E203 Vertically lining up ',' is preferred to the standard for readability.
# E221 Vertically lining up '=' is preferred to the standard for readability.

# This makefile controls a variety of operations performed on this library
# for use by developers in refactorings, improvements, and bug fixes

# Legal block
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


# Definitions
MODULES=UniArray UniClass UniDict UniDigit Self UniGrammar UniTree
PEP8=$(patsubst %, %.pep8, $(MODULES))
PYFL=$(patsubst %, %.pyfl, $(MODULES))
PLNT=$(patsubst %, %.plnt, $(MODULES))

GRAMMARS=artifacts/classify16.g4 artifacts/classify21.g4

# keep classify*.g4 as production (TODO move them to artifacts)
ARTIFACTS=\
	$(PEP8) \
	$(PYFL) \
	$(PLNT) \
	*Lexer.py \
	*Parser.py \
	*Visitor.py \
	*Listener.py \
	test/*.dot \
	test/*.png \
	*.tokens \
	*.dot \
	*.js \
	*.pyc \
	*.png \
	*.out

# Disable some PEP8 checks because the preferred style for Uni is different.
# Uni prefers vertical alignment of like code elements.
# E122:  continuation line missing indentation or outdented
# E128:  continuation line under-indented for visual indent
# E201:  whitespace after ‘(‘
# E202:  whitespace before ‘)’
# E203:  whitespace before ‘:’
# E221:  multiple spaces before operator
# E241:  multiple spaces after ‘,’
# E272:  multiple spaces before keyword
PEP8IGNORE=--ignore=E122,E128,E201,E202,E203,E221,E241,E272

# Disable some pylint checks because the preferred style for Uni is different
# bad-whitespace:  Uni prefers vertical alignment of like code elements
# attribute-defined-outside-init:  Uni does not follow RAII rules
# no-member:  Uni uses special rules to turn dict indices into instance members
# invalid-name:  External libraries do not follow pylint rules
# super-init-not-called:  Same as no-member, empty dicts do not need super
# superfluous-parends:  print in python 3 requires them
# relative-import:  TODO this is worth refining
# too-many-instance-attributes:  we need more than pylint allows
# too-many-locals:  same as too-many-instance-attributes
PYLINTIGNORE=\
bad-whitespace \
attribute-defined-outside-init \
no-member \
invalid-name \
super-init-not-called \
superfluous-parens \
relative-import \
too-many-instance-attributes \
too-many-locals

PYLINTDISABLE=$(patsubst %, --disable=%, $(PYLINTIGNORE))

antlr4=java -jar /usr/local/lib/antlr-4.5.3-complete.jar

timestamp=echo `date '+%Y/%m/%d %H:%M:%S'` $(1)

%.pep8 : %.py
	@-pep8 $(PEP8IGNORE) $< > $@ 2>&1
	@$(call timestamp,$@ checked)

%.pyfl : %.py
	@-pyflakes $< > $@ 2>&1
	@$(call timestamp,$@ checked)

%.plnt : %.py
	@-pylint $(PYLINTDISABLE) $< > $@ 2>&1
	@$(call timestamp,$@ checked)

all: $(PEP8) $(PYFL) $(PLNT) grammar unittest graphviz report todo Makefile
	@$(call timestamp,$@ finished)

.PHONY:
report:
	@$(call timestamp,$@ \
		`wc -c *.pep8 *.pyfl \
		|sed -e 's/  */ /' \
		|cut -d' ' -f2 \
		|tr '\n' '+' \
		|sed -e 's/+$$//' \
		|bc` bytes of error found)
	@$(call timestamp,$@ generated)

classify16.g4: UniGrammar.py
	@./UniGrammar.py
	@$(call timestamp,$@ generated)

grammar: classify16.g4 test_Codepoint.g4
	@$(antlr4) -Dlanguage=Python2 -visitor test_Codepoint.g4
	@./test_Codepoint.py
	@$(call timestamp,$@ tested)

.PHONY:
todo:
	@$(call timestamp,$@ Integrate UniDict replacing)
	@$(call timestamp,$@ Failing unit test in UniArray top-level block)
	@$(call timestamp,$@ Replace UniTree dict lookup with CPT)

.PHONY:
unittest:
	@$(call timestamp,$@ begins)
	@pytest > pytest.out 2>&1
	@cat pytest.out
	@$(call timestamp,$@ end)

SUBDIRS=test
.PHONY: subdirs $(SUBDIRS)

.PHONY:
$(SUBDIRS):
	@$(call timestamp,$@ begins)
	@$(MAKE) -C $@
	@$(call timestamp,$@ ends)

graphviz:
	@$(call timestamp,$@ dot to png begins)
	@set -e;\
		for f in $$(ls test/*.dot|sed -e 's/.dot//');\
		    do dot -Tpng $$f.dot > $$f.png;\
		done
	@$(call timestamp,$@ dot to png ends)

.PHONY:
clean:
	@rm -f $(ARTIFACTS)
	@$(call timestamp,$@)
