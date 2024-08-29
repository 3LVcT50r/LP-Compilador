all:
	antlr4 -Dlanguage=Python3 -no-listener -visitor hm.g4

#visitor:
#	antlr4 -Dlanguage=Python3 -no-listener -visitor hm.g4

tar:
	rm -rf victor.hernandez.LP.tar
	tar -zcvf victor.hernandez.LP.tar hm.g4 hm.py README.md

clean:
	rm -rf *.interp *.tokens hmLexer.py hmParser.py  hmVisitor.py
