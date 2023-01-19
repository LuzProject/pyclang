# module imports
from functools import reduce
from os import path
from subprocess import run

# local imports
from .utils import cmd_in_path


class CCompiler:
    def __init__(self):
        # set clang and clang_args
        self.clang_path = cmd_in_path('clang')
        self.clang_args = []

    def __format_command(self, file: str, outfile: str = None, args: list = []):
        outfileF = outfile if outfile else f'{file.replace(".c", "")}.o'
        argsF = reduce(lambda a, b: a + " " + str(b), args) if args else ''
        clang_argsF = reduce(lambda a, b: a + " " + str(b),
                             self.clang_args) if self.clang_args else ''
        return f'{self.clang_path} {argsF} {clang_argsF} {file} -o {outfileF}'.split(' ')

    def set_compiler(self, compiler: str):
        """Set compiler to use.
        
        :param str compiler: Compiler to use
        """
        if not cmd_in_path(compiler):
            raise FileNotFoundError(f'Compiler "{compiler}" not found in PATH')
        # set clang path
        self.clang_path = cmd_in_path(compiler)
        return self

    def add_arg(self, arg: str):
        """Add an argument to the compiler.
        
        :param str arg: Argument to add
        """
        self.clang_args.append(arg)
        return self

    def add_args(self, args: list):
        """Add arguments to the compiler.
        
        :param list args: Arguments to add
        """
        self.clang_args.extend(args)
        return self

    def compile(self, file: str, outfile: str = None, args: list = []):
        # ensure compiler exists
        if self.clang_path is None:
            raise FileNotFoundError(
                'No compiler was manually set, and "clang" was not found in path.')
        # ensure file exists
        if not path.exists(file):
            raise FileNotFoundError(
                f'Passed file to compile "{file}" does not exist')
        # run compile command
        run(self.__format_command(file, outfile, args), shell=False)