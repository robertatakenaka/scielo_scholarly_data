from setuptools import setup, find_packages


setup(
    name='scielo-scholarly-data',
    version='0.1',
    description="The SciELO Scholarly Data Standardizer, Normalizer and Deduplicator Tools",
    author="SciELO",
    author_email="scielo-dev@googlegroups.com",
    license="BSD",
    url="https://github.com/scieloorg/scielo_scholarly_data",
    keywords='scholarly data, normalization, deduplication, disambiguation, preprocessing',
    maintainer_email='rafael.pezzuto@gmail.com',
    packages=find_packages(),
)