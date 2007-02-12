.PHONY: all clean


all: parser.py lexer.py walker.py


lexer.py: java.g
	antlr java.g


parser.py: java.g
	antlr java.g


walker.py: walker.g lexer.py
	antlr walker.g


clean:
	rm -f *.pyo
	rm -f *.pyc
	rm -rf lexer.py
	rm -rf parser.py
	rm -rf walker.py
	rm -rf walkerTokenTypes.txt
	rm -rf JavaTokenTypes.txt
