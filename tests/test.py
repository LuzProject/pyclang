from pathlib import Path
from pyclang import CCompiler, SwiftCompiler

c = CCompiler().set_compiler('/usr/bin/cc').add_arg('-O0')
c.compile(Path('test.c'), 'test-c.o')

swift = SwiftCompiler()
swift.compile(Path('test.swift'), 'test-swift.o')
