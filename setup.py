from setuptools import setup, find_packages

setup(
    name='second_project',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'pytest',
        'sphinx',
    ],
)
