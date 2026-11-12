from dataclasses import dataclass
from typing import Optional

from errors import CompileError
from tape import is_valid_symbol

OPERAND_COUNT = {
    "GOTO": 1,
    "IF": 3,
    "WRITE": 1,
    "RIGHT": 0,
    "LEFT": 0,
    "HALT": 0
}

@dataclass
class Instruction:

    name: str
    line_no: int
    symbol: Optional[str] = None
    target: Optional[str] = None

def read_source(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"Program file not found: {path}")

def tokenize_line(line, line_no):
    if "#" in line:
        line = line.split("#")[0]
    words = line.split()
    if not words:
        return None, []

    label = None
    if words[0].endswith(":"):
        label_text = words[0][:-1]
        if not label_text.replace("_", "").isalnum():
            raise CompileError(line_no, f"Invalid label '{words[0]}'")

        label = label_text.lower()
        words = words[1:]

    return label, words

def collect_labels(tokenized):
    labels = {}
    errors = []
    position = 0

    for line_no, label, words in tokenized:
        if label is not None:
            if label in labels:
                errors.append(CompileError(line_no, f"duplicate label '{label}'"))
            else:
                labels[label] = position

        if words:
            position += 1

    return labels, errors

def check_symbol(symbol, line_no):
    if not is_valid_symbol(symbol):
        raise CompileError(line_no, f"Invalid symbol '{symbol}'")

def check_operands(name, operands, line_no):
    expected = OPERAND_COUNT[name]
    if len(operands) != expected:
        raise CompileError(line_no, f"{name} expects {expected} operand(s), got {len(operands)}")

    if name == "IF":
        check_symbol(operands[0], line_no)
        if operands[1] != "GOTO":
            raise CompileError(line_no, "IF must be written as: IF <symbol> GOTO <label>")

        if name == "WRITE":
            check_symbol(operands[0], line_no)


def parse_line(words, line_no):
    name = words[0]
    operands = words[1:]

    if name not in OPERAND_COUNT:
        raise CompileError(line_no, f"unknown instruction '{name}'")

    check_operands(name, operands, line_no)

    if name == "GOTO":
        return Instruction(name, line_no, target=operands[0].lower())
    if name == "IF":
        return Instruction(name, line_no, symbol=operands[0], target=operands[2].lower())
    if name == "WRITE":
        return Instruction(name, line_no, symbol=operands[0])
    return Instruction(name, line_no)

def check_labels(program, labels):
    errors = []
    for ins in program:
        if ins.target is not None and ins.target not in labels:
            errors.append(CompileError(ins.line_no, f"undefined label '{ins.target}'"))
    return errors

def compile_program(lines):
    errors = []
    tokenized = []

    for line_no, text in enumerate(lines, start=1):
        try:
            label, words = tokenize_line(text, line_no)
            tokenized.append((line_no, label, words))
        except CompileError as e:
            errors.append(e)

    labels, label_errors = collect_labels(tokenized)
    errors += label_errors

    program = []
    for line_no, label, words in tokenized:
        if words:
            try:
                program.append(parse_line(words, line_no))
            except CompileError as e:
                errors.append(e)

    errors += check_labels(program, labels)

    errors.sort(key=lambda e: e.line_no)

    return program, labels, errors