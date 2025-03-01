from setuptools import setup, find_packages

setup(
    name="harness-debugger",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "colorama",
        "tqdm",
        "tabulate",
    ],
    extras_require={
        "dev": [
            "pytest",
            "flake8",
            "mypy",
            "black",
        ],
    },
    entry_points={
        "console_scripts": [
            "harness-debugger=harness_debugger.cli:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A CLI tool for debugging Harness pipeline and delegate issues",
    keywords="harness, devops, debugging",
    python_requires=">=3.6",
) 