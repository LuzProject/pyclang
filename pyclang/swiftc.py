# module imports
from functools import reduce
from multiprocessing import Lock
from os import environ
from pathlib import PosixPath
from subprocess import check_output

# local imports
from .utils import cmd_in_path


class SwiftCompiler:
    def __init__(self, lock: Lock = None):
        # set swift and swift_args
        self.swift_path = cmd_in_path('swiftc')
        self.swift_args = []
        self.lock = lock

    def __format_command(self, file: str, outfile: str = None, args: list = []):
        returnValue = ''
        outfileF = outfile if outfile else f'{file.replace(".swift", "")}.o'
        argsF = reduce(lambda a, b: a + " " + str(b), args) if args else ''
        swift_argsF = reduce(lambda a, b: a + " " + str(b),
                             self.swift_args) if self.swift_args else ''
        if self.swift_args is not None and self.swift_args != []:
            returnValue = f'{self.swift_path} {argsF} {swift_argsF} {file} -o {outfileF}'
        else:
            returnValue = f'{self.swift_path} {argsF} {file} -o {outfileF}'
        return returnValue

    def set_compiler(self, compiler: str):
        """Set compiler to use.
        
        :param str compiler: Compiler to use
        """
        if not cmd_in_path(compiler):
            raise FileNotFoundError(f'Compiler "{compiler}" not found in PATH')
        # set swift path
        self.swift_path = cmd_in_path(compiler)
        return self

    def add_arg(self, arg: str):
        """Add an argument to the compiler.
        
        :param str arg: Argument to add
        """
        self.swift_args.append(arg)
        return self

    def add_args(self, args: list):
        """Add arguments to the compiler.
        
        :param list args: Arguments to add
        """
        self.swift_args.extend(args)
        return self

    def compile(self, file: PosixPath, outfile: str = None, args: list = []):
        # ensure compiler exists
        if self.swift_path is None:
            raise FileNotFoundError(
                'No compiler was manually set, and "swift" was not found in path.')
        # ensure file exists
        if type(file) is not list:
            file = [file]

        # loop files
        files_to_compile = ''
        for f in file:
            if not f.exists():
                raise FileNotFoundError(
                    f'Passed file to compile "{f}" does not exist')
            files_to_compile += f'{f} '
        # run compile command
        if self.lock is not None:
            with self.lock:
                return check_output(self.__format_command(files_to_compile, outfile, args),
                                    env=environ.copy(), shell=True)
        else:
            check_output(self.__format_command(files_to_compile, outfile, args),
                        env=environ.copy(), shell=True)
