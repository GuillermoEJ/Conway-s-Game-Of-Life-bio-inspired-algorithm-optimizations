from setuptools import setup

setup(
    name="game-of-life-optimization",
    version="1.0.0",
    description="Game of Life optimization with evolutionary algorithms",
    author="Guillermo",
    python_requires=">=3.7",
    install_requires=[
        "numpy>=1.21.0",
        "matplotlib>=3.4.0",
        "scipy>=1.7.0",
        "inspyred>=1.0.1",
        "networkx>=2.6",
    ],
)
