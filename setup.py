from setuptools import setup, find_packages

setup(
    name="nsor-grauent-stream-w",
    version="1.0.0",
    description="Neural Stream Gradient Tensor Engine and Distributed Benchmark Pipeline",
    author="Neural Systems Research",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "psutil>=5.9.0",
    ],
)
