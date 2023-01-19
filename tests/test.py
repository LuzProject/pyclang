from pyclang import CCompiler

c = CCompiler().set_compiler('/usr/bin/cc').add_arg('-O0')
c.compile('test.c')