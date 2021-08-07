from setuptools import setup, find_packages
from mageia import __version__, __email__, __author__, __package__

with open("README.md", 'r', encoding="utf8") as f:
    long_description = f.read()

parse_requirements = ['SQLAlchemy', 'PyMySQL']

setup(
    name=__package__,
    version=__version__,
    description="Simple DataBase tools for MySQL . Read Write Splitting Load Balance .",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache",
    url="https://github.com/stefanlei",
    author=__author__,
    author_email=__email__,
    packages=find_packages(),
    install_requires=parse_requirements,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]

)
