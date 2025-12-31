# === Python Modules ===
import setuptools
from pathlib import Path

# === Read the README for the long description on PyPI/GitHub ===
long_description = Path("README.md").read_text(encoding = "utf-8")

# === Package Version ===
__version__ = "0.0.1"

# === Project Metadata ===
REPO_NAME = "Probabilistic-Trading-System"
AUTHOR_USER_NAME = "RawatRahul14"
SRC_REPO = "probtrade"
AUTHOR_EMAIL = "rahulrawat272chd@gmail.com"

# === Main Setup Function ===
setuptools.setup(
    ## === Package name users will install as:  pip install quantfin ===
    name = SRC_REPO,

    ## === Version number of your package ===
    version = __version__,

    ## === Author information ===
    author = AUTHOR_USER_NAME,
    author_email = AUTHOR_EMAIL,

    ## === Short description ===
    description = "Multi-Timeframe Sector Rotation with Momentum Breakout",

    ## === Long description (README.md) ===
    long_description = long_description,
    long_description_content_type = "text/markdown",

    ## === GitHub links ===
    url = f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls = {
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },

    ## === Package Discovery ===
    package_dir = {"": "src"},

    packages = setuptools.find_packages(where = "src"),

    # === Minimum Python Version Required ===
    python_requires = ">=3.11"
)