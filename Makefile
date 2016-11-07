PEPIGNORE=--ignore=E201,E203,E207,E221,E272

all: UniArray.pep8 UniDict.pep8 UniDigit.pep8 UniDoc.pep8 UniTree.pep8

.PHONY:
clean:
	@rm -f *.pep8 *.pyc *.js

UniArray.pep8:	UniArray.py
	@-pep8 $(PEPIGNORE) $< > $@ 2>&1

UniDict.pep8:	UniDict.py
	@-pep8 $(PEPIGNORE) $< > $@ 2>&1

UniDigit.pep8:	UniDigit.py
	@-pep8 $(PEPIGNORE) $< > $@ 2>&1

UniDoc.pep8:	UniDoc.py
	@-pep8 $(PEPIGNORE) $< > $@ 2>&1

UniTree.pep8:	UniTree.py
	@-pep8 $(PEPIGNORE) $< > $@ 2>&1

