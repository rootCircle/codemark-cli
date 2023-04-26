from setuptools import setup, find_packages

setup(
    name='codemark',
    version='0.2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pyrebase4',
        'firebase_admin',
        'openai',
        'keyring',
        'appdirs',
        'tabulate',
        'fuzzywuzzy',
        'python-Levenshtein',
        'psutil',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'codemark = codemark.scripts.cm_cli:cli',
        ],
    },
)