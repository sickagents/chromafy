from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="chromafy",
    version="1.0.0",
    description="A lightweight, zero-dependency terminal color library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="sickagents",
    url="https://github.com/sickagents/chromafy",
    py_modules=["chromafy"],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Terminals",
    ],
    keywords="terminal color ansi style gradient box table unicode",
    license="MIT",
)
