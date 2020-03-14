from setuptools import setup, find_packages

setup(
    name='libfi',
    version='1.0',
    description='Simple client that scrapes the Swedish Finansinspektionen site https://marknadssok.fi.se/',
    author='jlyheden',
    author_email='github-johan@lyheden.com',
    packages=find_packages(),
    install_requires=[
        "requests",
        "backoff",
        "lxml"
    ],
    )
