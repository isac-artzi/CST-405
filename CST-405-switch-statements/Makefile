CC = gcc
LEX = flex
YACC = bison
CFLAGS = -g -Wall

TARGET = minicompiler
OBJS = lex.yy.o parser.tab.o main.o ast.o symtab.o semantic.o codegen.o tac.o

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

lex.yy.c: scanner.l parser.tab.h
	$(LEX) scanner.l

parser.tab.c parser.tab.h: parser.y
	$(YACC) -d parser.y

lex.yy.o: lex.yy.c
	$(CC) $(CFLAGS) -c lex.yy.c

parser.tab.o: parser.tab.c
	$(CC) $(CFLAGS) -c parser.tab.c

main.o: main.c ast.h semantic.h codegen.h tac.h
	$(CC) $(CFLAGS) -c main.c

ast.o: ast.c ast.h
	$(CC) $(CFLAGS) -c ast.c

symtab.o: symtab.c symtab.h
	$(CC) $(CFLAGS) -c symtab.c

semantic.o: semantic.c semantic.h ast.h symtab.h
	$(CC) $(CFLAGS) -c semantic.c

codegen.o: codegen.c codegen.h ast.h symtab.h tac.h
	$(CC) $(CFLAGS) -c codegen.c

tac.o: tac.c tac.h ast.h
	$(CC) $(CFLAGS) -c tac.c

clean:
	rm -f $(TARGET) $(OBJS) lex.yy.c parser.tab.c parser.tab.h *.s *.tac

test: $(TARGET)
	./$(TARGET) test.c test.s
	@echo "\n=== Generated MIPS Code ==="
	@cat test.s

# Run the if-statement test and display generated MIPS assembly.
# Expected output when run in a MIPS simulator: 1 2 3 4 5 6 6 6 6 6 6 7 8
test-if: $(TARGET)
	./$(TARGET) test_if.c test_if.s
	@echo "\n=== Generated MIPS Code (if-statement test) ==="
	@cat test_if.s

# Run the switch-statement test and display generated MIPS assembly.
# Expected output when run in a MIPS simulator:
#   20  (case 2 body)
#   0   (default body — x=99 matches no case)
#   30  (case 3 body — fall-through from case 3: print(30))
#   40  (chained: case 4 body after fall-through grouping)
#   99  (switch inside function returns correctly)
test-switch: $(TARGET)
	./$(TARGET) test_switch.c test_switch.s
	@echo "\n=== Generated MIPS Code (switch-statement test) ==="
	@cat test_switch.s

.PHONY: all clean test test-if test-switch