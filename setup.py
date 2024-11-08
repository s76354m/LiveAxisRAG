from setuptools import setup, find_packages

setup(
    name="swarmrag",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'sqlalchemy',
        'pyodbc',
        'python-dotenv'
    ]
) 