from setuptools import setup, find_packages

setup(
    name="jnks-cli",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",          # For CLI interface
        "pyyaml>=6.0.0",         # For YAML file handling
        "python-jenkins>=1.8.0",  # For Jenkins API
        "requests>=2.25.0",       # For HTTP requests with SSL support
        "tabulate>=0.9.0",       # For table formatting
        "urllib3>=2.0.0",        # For SSL warning management
    ],
    entry_points={
        "console_scripts": [
            "jnks=jenkins_cli.cli:cli",
        ],
    },
    python_requires='>=3.7',  # Adding minimum Python version requirement
    description="A command-line interface for managing Jenkins jobs",
    author="Jenkins CLI Team",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)