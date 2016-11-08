PEP8IGNORE=--ignore=E201,E203,E207,E221,E272
PEP8=UniArray.pep8 UniDict.pep8 UniDigit.pep8 UniDoc.pep8 UniTree.pep8
PYFL=UniArray.pyfl UniDict.pyfl UniDigit.pyfl UniDoc.pyfl UniTree.pyfl

all: $(PEP8) $(PYFL)

.PHONY:
clean:
	@rm -f *.pep8 *.pyfl *.pyc *.js

UniArray.pep8: UniArray.py
	@-pep8 $(PEP8IGNORE) $< > $@ 2>&1

UniArray.pyfl: UniArray.py
	@-pyflakes $< > $@ 2>&1

UniDict.pep8: UniDict.py
	@-pep8 $(PEP8IGNORE) $< > $@ 2>&1

UniDict.pyfl: UniDict.py
	@-pyflakes $< > $@ 2>&1

UniDigit.pep8: UniDigit.py
	@-pep8 $(PEP8IGNORE) $< > $@ 2>&1

UniDigit.pyfl: UniDigit.py
	@-pyflakes $< > $@ 2>&1

UniDoc.pep8: UniDoc.py
	@-pep8 $(PEP8IGNORE) $< > $@ 2>&1

UniDoc.pyfl: UniDoc.py
	@-pyflakes $< > $@ 2>&1

UniTree.pep8: UniTree.py
	@-pep8 $(PEP8IGNORE) $< > $@ 2>&1

UniTree.pyfl: UniTree.py
	@-pyflakes $< > $@ 2>&1
