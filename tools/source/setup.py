"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from eager import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=skele', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name='eager',
    version=__version__,
    description='Useful tools for creating and parsing datasets for OpenCV',
    long_description=long_description,
    url='https://github.com/gbarros/hand-detector',
    author='Gabriel Barros',
    author_email='gbbabarros@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Utilities Computer Vision',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='cli, OpenCV, Computer Vision',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=['numpy', 'imutils'],
    extras_require={
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    entry_points={
        'console_scripts': [
            'hand_annotation=eager.hand_annotation:main',
            'jsonmerge=eager.meta_json:merge',
            'jsonclean=eager.meta_json:clean',
            'prepare_sample=eager.prepare_samples:main',
        ],
    },
    cmdclass={'test': RunTests},
)
