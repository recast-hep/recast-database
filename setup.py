from setuptools import setup, find_packages

setup(
  name = 'recast-database',
  version = '0.1.0',
  description = 'database code for RECAST',
  author = 'Lukas Heinrich',
  packages = find_packages(),
  install_requires = [
    'Flask-SQLAlchemy'
  ]
)