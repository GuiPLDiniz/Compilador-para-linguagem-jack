class VMWriter:
    def __init__(self):
        self.lines = []

    def write_push(self, segment, index):
        self.lines.append(f"push {segment} {index}")

    def write_pop(self, segment, index):
        self.lines.append(f"pop {segment} {index}")

    def write_arithmetic(self, command):
        self.lines.append(command)

    def write_label(self, label):
        self.lines.append(f"label {label}")

    def write_goto(self, label):
        self.lines.append(f"goto {label}")

    def write_if(self, label):
        self.lines.append(f"if-goto {label}")

    def write_call(self, name, n_args):
        self.lines.append(f"call {name} {n_args}")

    def write_function(self, name, n_locals):
        self.lines.append(f"function {name} {n_locals}")

    def write_return(self):
        self.lines.append("return")

    def get_output(self):
        return "\n".join(self.lines) + "\n"