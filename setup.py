# setup.py
from setuptools import find_packages, setup

setup(
    name="obsidian_cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "obs=obs.cli:main",
        ],
    },
)
