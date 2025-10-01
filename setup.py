from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-sudoku",
    version="1.0.0",
    author="Nestor Wheelock",
    author_email="nestor@example.com",
    description="Reusable Django app for Sudoku puzzle game with REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nestorwheelock/django-sudoku",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment :: Puzzle Games",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Django>=4.0,<6.0",
        "djangorestframework>=3.14,<4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-django>=4.5",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
