from setuptools import setup, find_packages

setup(
    name="win-matrix-core",
    version="1.0.0",
    description="Windows Matrix Benchmark & Compute Runtime for Distributed Pipelines",
    author="Neural Systems Research",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "psutil>=5.9.0",
    ],
)
