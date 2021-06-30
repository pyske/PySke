import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyske",
    version="0.5",
    author="Frederic Loulergue",
    author_email="frederic.loulergue@univ-orleans.fr",
    description="The Python Skeleton Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pyske/pyske",
    project_urls={
        "Bug Tracker": "https://github.com/pyske/pyske/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD-2-Clause",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.8",
)
