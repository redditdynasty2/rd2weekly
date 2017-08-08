from setuptools import setup

from rd2weekly.version import __version__

__author__ = "Simon Swanson"
__email__ = "nomiswanson@gmail.com"
__copyright__ = "Copyright 2017, Simon Swanson"


setup(
    name = "rd2weekly",
    version = __version__,
    packages = [],
    package_dir = { "": "rd2weekly" },
    url = "https://github.com/swanysimon/rd2weekly",
    license = "MIT",
    author = __author__,
    author_email = __email__,
    maintainer = __author__,
    maintainer_email = __email__,
    description = "A tool for generating weekly summaries for CBS fantasy baseball leagues",
    install_requires = [
        "beautifulsoup4",
        "chromedriver_installer",
        "selenium"
    ]
)
