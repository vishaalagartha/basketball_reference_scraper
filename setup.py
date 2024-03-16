import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="basketball_reference_scraper",
    version="2.0.0",
    author="Vishaal Agartha",
    author_email="vishaalagartha@gmail.com",
    license="MIT",
    description="A Python client for scraping stats and data from Basketball Reference",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vishaalagartha/basketball_reference_scraper",
    packages=setuptools.find_packages(),
    package_data={'basketball_reference_scraper': ['*.txt']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        'beautifulsoup4',
        'bs4',
        'lxml',
        'numpy',
        'pandas',
        'python-dateutil',
        'pytz',
        'requests',
        'six',
        'soupsieve',
        'Unidecode',
        'selenium'
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
