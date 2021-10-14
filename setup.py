from setuptools import setup, find_packages


install_requirements=[
    'google-cloud-bigquery',
    'google-cloud-storage',
]

setup(
    name='scielo-dltools',
    version='0.1',
    description="The SciELO Data Lake Tools",
    author="SciELO",
    author_email="scielo-dev@googlegroups.com",
    license="BSD",
    install_requires=install_requirements,
    url="https://github.com/scieloorg/scielo_scholarly_data",
    keywords='data lake',
    maintainer_email='rafael.pezzuto@gmail.com',
    packages=find_packages(),
)
