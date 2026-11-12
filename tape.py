BLANK = "_"
SYMBOL = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
TAPE_SYMBOLS = SYMBOL + BLANK

def is_valid_symbol(symbol):
    return len(symbol) == 1 and symbol in TAPE_SYMBOLS

def make_tape(input_string):
    tape = {}
    for i, ch in enumerate(input_string):  
        if ch not in SYMBOL:
            raise ValueError(f"Invalid symbol: {ch} at position {i}")
        tape[i] = ch
    return tape

def read_symbol(tape, head):
    if head in tape:
        return tape[head]
    else:
        return BLANK

def write_symbol(tape, head, symbol):
    if symbol == BLANK:
        if head in tape:
            del tape[head]
        else:
            tape[head] = symbol

def move_head(head, direction):
    if direction == "RIGHT":
        return head + 1
    elif direction == "LEFT":
        if head == 0:
            raise ValueError("moved off the start of the tape")
        return head - 1

def format_tape(tape, head):
    positions_used = list(tape.keys()) + [head]
    low = min(positions_used)
    high = max(positions_used)

    symbols_line = ""
    marker_line = ""
    for p in range(low, high + 1):
        symbols_line += read_symbol(tape, p) + " "
        if p == head:
            marker_line += "^ "
        else:
            marker_line += "  "
    return symbols_line, marker_line


