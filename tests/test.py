from pathlib import Path
from pyclang import CCompiler, SwiftCompiler

c = CCompiler().set_compiler('/usr/bin/cc').add_arg('-O0')
c.compile(Path('test.c'))

swift = SwiftCompiler()
swift.compile(Path('test.swift'))
