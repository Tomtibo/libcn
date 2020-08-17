import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'libcn',
    packages = setuptools.find_packages(),
    version = '0.0.1',
    description = 'Unofficial cyphernode library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'Tom Tibo',
    author_email = 'tomtibeau@gmail.com',
    url = 'https://github.com/tomtibo/libcn',
    keywords = ['cyphernode', 'bitcoin', 'api'], 
    install_requires=[
        'argparse',
        'configparser',
        'requests',
        'urllib3',
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
    ],
    python_requires='>=3.6',
)