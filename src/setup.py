from distutils.core import setup
import py2exe
setup(
      name = 'Fontaine',
      version = '0.75',
      windows=[{"script":"Fontaine.py"}],
      options={}
)
