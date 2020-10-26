from setuptools import setup, find_packages

setup(
    name='gsmclient',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/dmnightshade/nightshade-gsm',
    description='Game Server Manager Client',
    install_requires=[
        "PySide2",
        "QtPy",
    ],
)
