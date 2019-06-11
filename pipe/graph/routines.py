import os
import stat
import subprocess
import tempfile
import json


def execute(command, args):
    p = subprocess.Popen(
        [command] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=os.environ.copy()
    )
    p.wait()
    output_bytes, error_bytes = p.communicate()
    p.kill()
    error = error_bytes.decode("utf-8")
    if error:
        raise ValueError(error)
    return output_bytes.decode("utf-8")


class AbstractRoutine(object):

    def __init__(self, code, extension):
        self.code = code
        self.extension = extension
        self.code_path = ""
        self.last_execution = None

    def prepare_executable(self):
        pass        

    def run_executable(self, arguments):
        raise NotImplementedError("routines must implement `%s`" % self.run_executable.__name__)
        
    def execute(self, arguments):
        _, self.code_path = tempfile.mkstemp(prefix="pipe", suffix=f".{self.extension}")
        with open(self.code_path, "w") as f:
            f.write(self.code)
            f.seek(0)
            self.prepare_executable()
            return self.run_executable(arguments)

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
        execute("gcc", [self.code_path, "-o", self.exe_path])

    def run_executable(self, arguments):
        return execute(self.exe_path, arguments)


class PythonRoutine(AbstractRoutine):

    def __init__(self, code):
        super(PythonRoutine, self).__init__(code, "py")

    def prepare_executable(self):
        pass

    def run_executable(self, arguments):
        return execute("python", [self.code_path] + arguments)


class RubyRoutine(AbstractRoutine):

    def __init__(self, code):
        super(RubyRoutine, self).__init__(code, "rb")

    def prepare_executable(self):
        pass

    def run_executable(self, arguments):
        return execute("ruby", [self.code_path] + arguments)


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
        return execute(self.code_path, arguments)


class BatchRoutine(AbstractRoutine):

    def __init__(self, code):
        super(BatchRoutine, self).__init__(code, "bat")

    def prepare_executable(self):
        pass

    def run_executable(self, arguments):
        return execute(self.code_path, arguments)


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
