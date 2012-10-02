from setuptools import setup

setup(
    name = "Treatment",
    version = "0.1",
    author = "Christopher Poole",
    author_email = "mail@christopherpoole.net",
    description = "Read Tomotherapy treatment plan archives",
    keywords = "radiotherapy, tomotherapy, archive",
    url = "http://github.com/christopherpoole/Treatment",
    packages = ["Treatment"],    
    long_description=open("README.md").read(),
)
