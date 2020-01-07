import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="basketball_reference_scraper_vishaalagartha",
    version="0.0.1",
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
    keywords=[
        "NBA",
        "Basketball",
        "Basketball Reference",
        "basketball-reference.com",
        ],
)
