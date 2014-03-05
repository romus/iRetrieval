__author__ = 'romus'


from setuptools import setup, find_packages
from os.path import join, dirname
import iRetrieval


setup(
    name="iRetrieval",
    version=iRetrieval.__version__,
    test_suite="iRetrieval.test",
    include_package_data=True,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), "README.md")).read(),
    description="Information retrieval "
                "Python packages",
    author="romus",
    author_email="vkromus@gmail.com",
    license="GPL v3", requires=['statistic4text', 'pymongo', 'docx']
)