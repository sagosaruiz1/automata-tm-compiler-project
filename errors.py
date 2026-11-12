class CompileError(Exception):
    def __init__(self, line_no, message):
        self.line_no = line_no
        self.message = message
        super().__init__(f"Compile error on line {line_no}: {message}")

class TuringRuntimeError(Exception):
    def __init__(self, message, lin_no=None):
        self.message = message
        self.line_no = lin_no
        super().__init__(message)

def format_error(error):
    if isinstance(error, CompileError):
        return f"Runtime error at line {error.line_no}: {error.message}"
    else:
        if error.line_no is not None:
            return f"Runtime error at line {error.line_no}: {error.message}"
        else:
            return f"Runtime error: {error.message}"

