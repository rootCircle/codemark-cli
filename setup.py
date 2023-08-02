from setuptools import setup, find_packages

setup(
    name='codemark',
    version='0.2.1',
    description='CodeMark CLI is a command-line interface that helps you manage your coding assignments and tests.\nWith this tool, you can easily initialize the configuration, list assignments, fetch and check your code, submit your code for grading, and get AI-powered error recommendations.',
    author='rootCircle',
    url='https://github.com/rootCircle/codemark-cli',
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
        'requests-toolbelt==0.10.1',
        'trogon',
        'termcolor'
    ],
    entry_points={
        'console_scripts': [
            'codemark = codemark.scripts.cm_cli:cli',
            'cmk = codemark.scripts.cm_cli:cli',
        ],
    },
    package_data={'codemark': ['firebase/res/service-account-file.json']}
)
