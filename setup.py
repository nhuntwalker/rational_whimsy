"""Setup file for my website."""
from setuptools import setup

setup(
    name="rational-whimsy",
    author="Nicholas Hunt-Walker",
    author_email="nhuntwalker@gmail.com",
    description="This is my main website for blogs, projects, you name it.",
    install_requires=["ipython", "django", "psycopg2"],
    extras_require={
        "test": ["pytest", "pytest-cov", "pytest-watch", "tox", "factory_boy"]
    },
    license="MIT",
    version=0.1,
)
