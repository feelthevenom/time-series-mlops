import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


__version__ = "0.0.0"

REPO_NAME = "Time-Series-Forecasting-Project"
AUTHOR_USER_NAME = "Rahul Ravikumar"
SRC_REPO = "Time-Series-Forecasting-Project"
AUTHOR_EMAIL = "rahul.valli2003@gmail.com"


setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A small python package for time series forecasting",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/feelthevenom/time-series-mlops",
    project_urls={
        "Bug Tracker": f"https://github.com/feelthevenom/time-series-mlops/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)