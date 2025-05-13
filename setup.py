from setuptools import setup, find_packages

setup(
    name="post_ranker",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "python-dotenv",
    ],
    author="Marcos Santos",
    author_email="@marcosogs",
    description="A package for fetching and analyzing posts from different platforms",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/marcosogsantos/post_ranker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
) 