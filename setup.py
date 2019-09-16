import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycocks",
    version="0.0.1",
    author="Carlton Shepherd",
    author_email="carlton@linux.com",
    description="An implementation of Cocks' identity-based encryption (IBE) scheme",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CarltonShepherd/pycocks",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
        "Intended Audience :: Science/Research",
        "Development Status :: 3 - Alpha"
    ],
    keywords='cocks,encryption,decryption,ibe,identity, based,crypto,cryptography,security,privacy',
    install_requires=[
        "gmpy2>=2.0.0",
    ]
)