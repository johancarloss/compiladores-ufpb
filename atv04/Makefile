CC = gcc
CFLAGS = -Wall -Wextra -std=c99

lexer: main.c lexer.c token.c lexer.h token.h
	$(CC) $(CFLAGS) -o lexer main.c lexer.c token.c

test: lexer
	./run_tests.sh

clean:
	rm -f lexer

.PHONY: test clean
