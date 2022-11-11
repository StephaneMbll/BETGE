from setuptools import setup, find_packages

setup(
        name="betge",
        version="1.2.0",
        packages=find_packages(include=['betge', 'betge.*']),
        package_data={'betge': ['data/*']}
        )

