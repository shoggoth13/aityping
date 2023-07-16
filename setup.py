from setuptools import setup, find_packages

setup(
    name="aityping",
    version="0.0.1",
    description="Fuzzy type hints with AI.",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "pydantic<2",
    ],
)
