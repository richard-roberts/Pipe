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

    ext = None

    def __init__(self, code):
        self.code = code
        self.code_path = ""
        self.last_execution = None

    def run_executable(self, arguments):
        raise NotImplementedError("routines must implement `%s`" % self.run_executable.__name__)
        
    def execute(self, arguments):
        _, self.code_path = tempfile.mkstemp(prefix="pipe", suffix=f".{self.ext}")
        with open(self.code_path, "w") as f:
            f.write(self.code)
            f.seek(0)
            return self.run_executable(arguments)

    def as_json(self):
        return {
            "extension": self.ext,
            "code": self.code
        }


class CRoutine(AbstractRoutine):

    ext = "c"

    def __init__(self, code):
        super(CRoutine, self).__init__(code)

    def run_executable(self, arguments):
        _, exe_path = tempfile.mkstemp(prefix="pipe_exe", suffix=self.ext)
        
        p = subprocess.Popen(
            ["gcc"] + [self.code_path, "-o", exe_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=os.environ.copy()
        )   
        p.wait()
        _, error_bytes = p.communicate()
        p.kill()
        error = error_bytes.decode("utf-8")
        if error: raise SystemError(error)
        result = execute(exe_path, arguments)
        os.remove(exe_path)
        return result


class PythonRoutine(AbstractRoutine):

    ext = "py"

    def __init__(self, code):
        super(PythonRoutine, self).__init__(code)

    def run_executable(self, arguments):
        return execute("python", [self.code_path] + arguments)
        

class RubyRoutine(AbstractRoutine):

    ext = "rb"

    def __init__(self, code):
        super(RubyRoutine, self).__init__(code)

    def run_executable(self, arguments):
        return execute("ruby", [self.code_path] + arguments)


class BashRoutine(AbstractRoutine):

    ext = "sh"

    def __init__(self, code):
        super(BashRoutine, self).__init__(code)

    def run_executable(self, arguments):
        f = open(self.code_path, "r")
        content = f.read()
        f.close()

        with_shebang = "#!/bin/sh\n" + content
        f = open(self.code_path, "w")
        f.write(with_shebang)
        f.close()
        
        os.chmod(self.code_path, os.stat(self.code_path).st_mode | stat.S_IEXEC)

        return execute(self.code_path, arguments)


class BatchRoutine(AbstractRoutine):

    ext = "bat"

    def __init__(self, code):
        super(BatchRoutine, self).__init__(code)

    def run_executable(self, arguments):
        return execute(self.code_path, arguments)


def list_extensions():
    return [
        CRoutine.ext,
        PythonRoutine.ext,
        MayaRoutine.ext,
        RubyRoutine.ext,
        BashRoutine.ext,
        BatchRoutine.ext
    ]


def class_from_extension(ext):
    return {
        CRoutine.ext: CRoutine,
        PythonRoutine.ext: PythonRoutine,
        MayaRoutine.ext: MayaRoutine,
        RubyRoutine.ext: RubyRoutine,
        BashRoutine.ext: BashRoutine,
        BashRoutine.ext: BashRoutine
    }[ext]


def from_extension_and_code(extension, code):
    if extension not in list_extensions():
        raise ValueError("Cannot initialize routine with `%s` extension " % extension)
    return class_from_extension(extension)(code)

    
def from_json(data):
    return from_extension_and_code(data["extension"], data["code"])
