CC = gcc
CFLAGS = -Wall -Wextra -std=c99

lexer: main.c
	$(CC) $(CFLAGS) -o lexer main.c

test:
	./run_tests.sh

clean:
	rm -f lexer

.PHONY: test clean
