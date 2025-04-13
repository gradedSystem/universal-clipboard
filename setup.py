from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("version.txt", "r", encoding="utf-8") as fh:
    version = fh.read().strip()

setup(
    name="universal-clipboard",
    version=version,
    author="gradedSystem",
    author_email="homesiknessgerald@gmail.com",
    description="Cross-platform clipboard synchronization between Windows and Mac",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gradedSystem/universal-clipboard",
    project_urls={
        "Bug Tracker": "https://github.com/gradedSystem/universal-clipboard/issues",
        "Documentation": "https://github.com/gradedSystem/universal-clipboard#readme",
        "Source Code": "https://github.com/gradedSystem/universal-clipboard",
    },
    packages=find_packages(include=["universal_clipboard", "universal_clipboard.*"]),
    package_data={
        "universal_clipboard": ["py.typed"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    python_requires=">=3.8",
    install_requires=[
        "websockets>=11.0.3",
        "cryptography>=41.0.3",
        "Pillow>=10.0.0",
    ],
    extras_require={
        "windows": ["pywin32>=306"],
        "mac": ["pyobjc>=9.2"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "types-cryptography>=3.3.23",
        ],
    },
    entry_points={
        "console_scripts": [
            "universal-clipboard=universal_clipboard.cli:main",
        ],
    },
    zip_safe=False,
) 