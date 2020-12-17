import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="basketball_reference_scraper",
    version="1.0.21",
    author="Vishaal Agartha",
    author_email="vishaalagartha@gmail.com",
    license="MIT",
    description="A Python client for scraping stats and data from Basketball Reference",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vishaalagartha/basketball_reference_scraper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        'beautifulsoup4==4.8.2',
        'bs4==0.0.1',
        'lxml==4.4.2',
        'numpy==1.18.1',
        'pandas==0.25.3',
        'python-dateutil==2.8.1',
        'pytz==2019.3',
        'requests==2.22.0',
        'six==1.13.0',
        'soupsieve==1.9.5'
    ],
    extras_require={
        'test': ['unittest'],
    },
    keywords=[
        "nba",
        "sports",
        "data mining",
        "basketball",
        "basketball reference",
        "basketball-reference.com",
        ],
)
