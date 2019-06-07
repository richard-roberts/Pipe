import os
import stat
import subprocess
import tempfile
import json


class Execution:

    def __init__(self, command, args):
        call = [command] + args
        stdout = subprocess.PIPE
        stderr = subprocess.PIPE
        env = os.environ.copy()
        process_result = subprocess.Popen(call, stdout=stdout, stderr=stderr, env=env)
        process_result.wait()
        self.output, self.error = process_result.communicate()
        process_result.kill()

    def get_error(self):
        return self.error.decode("utf-8")
    
    def raise_if_errored(self):
        if self.error:
            raise ValueError(self.get_error())

    def get_output(self):
        return self.output.decode("utf-8")


class AbstractRoutine(object):

    def __init__(self, code, extension):
        self.code = code
        self.extension = extension
        self.code_path = "./pipe_%s_code.%s" % (self.extension, self.extension) # TODO: make temporary file
        self.last_execution = None

    def write_code(self):
        f = open(self.code_path, "w")
        f.write(self.code)
        f.close()

    def prepare_executable(self):
        pass

    def compile(self):
        self.prepare_executable()

    def run_executable(self, arguments):
        raise NotImplementedError("routines must implement `%s`" % self.run_executable.__name__)
        
    def run(self, arguments):
        self.run_executable(arguments)
        self.last_execution.raise_if_errored()
        return self.last_execution.get_output()

    def execute(self, arguments):
        self.write_code()
        self.compile()
        return self.run(arguments)

    def as_json(self):
        return {
            "extension": self.extension,
            "code": self.code
        }


class CRoutine(AbstractRoutine):

    def __init__(self, code):
        super(CRoutine, self).__init__(code, "c")
        self.exe_path = "./pipe_%s_exe" % (self.extension)

    def prepare_executable(self):
        e = Execution("gcc", [self.code_path, "-o", self.exe_path])
        e.raise_if_errored()

    def run_executable(self, arguments):
        self.last_execution = Execution(self.exe_path, arguments)


class PythonRoutine(AbstractRoutine):

    def __init__(self, code):
        super(PythonRoutine, self).__init__(code, "py")

    def prepare_executable(self):
        pass

    def run_executable(self, arguments):
        self.last_execution = Execution("python3", [self.code_path] + arguments)


class RubyRoutine(AbstractRoutine):

    def __init__(self, code):
        super(RubyRoutine, self).__init__(code, "rb")

    def prepare_executable(self):
        pass

    def run_executable(self, arguments):
        self.last_execution = Execution("ruby", [self.code_path] + arguments)


class BashRoutine(AbstractRoutine):

    def __init__(self, code):
        super(BashRoutine, self).__init__(code, "sh")

    def prepare_executable(self):
        f = open(self.code_path, "r")
        content = f.read()
        f.close()

        with_shebang = "#!/bin/sh\n" + content
        f = open(self.code_path, "w")
        f.write(with_shebang)
        f.close()
        
        os.chmod(self.code_path, os.stat(self.code_path).st_mode | stat.S_IEXEC)

    def run_executable(self, arguments):
        self.last_execution = Execution(self.code_path, arguments)


class BatchRoutine(AbstractRoutine):

    def __init__(self, code):
        super(BatchRoutine, self).__init__(code, "batch")

    def prepare_executable(self):
        os.chmod(self.code_path, os.stat(self.code_path).st_mode | stat.S_IEXEC)

    def run_executable(self, arguments):
        self.last_execution = Execution(self.code_path, arguments)


def from_extension_and_code(extension, code):
    types = {
        "c": CRoutine,
        "py": PythonRoutine,
        "rb": RubyRoutine,
        "sh": BashRoutine,
        "bat": BatchRoutine
    }
    if extension not in types.keys():
        raise ValueError("Cannot initialize routine with `%s` extension " % extension)
    return types[extension](code)

    
def from_json(data):
    return from_extension_and_code(data["extension"], data["code"])
