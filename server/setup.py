from setuptools import setup, find_packages

setup(
    name='gsmserver',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/dmnightshade/nightshade-gsm',
    description='Game Server Manager Server',
    install_requires=[
        "PySignal",
    ],
)
