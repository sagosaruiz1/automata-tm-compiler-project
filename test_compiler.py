import compiler
from errors import format_error

lines = compiler.read_source("examples/append_one.tm")
program, labels, errors = compiler.compile_program(lines)

if errors:
    for e in errors:
        print(format_error(e))
else:
    print("Compiled OK")
    print(labels)
    for ins in program:
        print(ins)