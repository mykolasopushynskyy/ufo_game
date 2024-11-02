from setuptools import setup, find_packages
import pathlib
import pkg_resources


with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name='Neural network test',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'start=application.application:main',
        ]
    },
    install_requires=install_requires
)