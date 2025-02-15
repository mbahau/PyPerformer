from setuptools import setup, find_packages

setup(
    name="md_features",
    version="0.1",
    description="Utility functions for managing dataframes",
    py_modules=["md_features"],
    install_requires=["pandas", "numpy"],  # Add dependencies if needed
)
