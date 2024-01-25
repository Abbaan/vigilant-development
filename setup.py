from setuptools import setup, find_packages

# Read the contents of requirements file
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='vigilant_dev',
    version='0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=required,
    author='Abbaan Nassar',
    author_email='abbaan31@hotmail.com',
    description='A package for visualizing personal development using NLP clustering and 3D visualization.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
