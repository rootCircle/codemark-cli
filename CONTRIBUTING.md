# CONTRIBUTING
@TODO

## Installation instructions

To install and use CodeMark CLI, follow these steps:

1. Clone the CodeMark CLI repository by running the following command:
 `git clone https://github.com/rootCircle/codemark-cli.git`

2. Install CodeMark CLI by running the following commands:

     `cd codemark-cli`

     `pip3 install poetry`

     `poetry install`

     `pip3 install --editable .`

     Note: If pip3 is not installed on your system, use pip instead. If you encounter permission issues, add the `--user` flag at the end of the command. 

     Make sure Python's Script library is in System PATH

     Use this to setup: https://gist.github.com/martinohanlon/c0abb7281cb9020e75053fba7011daf7 or https://realpython.com/add-python-to-path/

     Note: If you are a Windows user and encounter issues installing pyrebase, refer to this Stack Overflow post: https://stackoverflow.com/questions/53461316/pyrebase-install-on-windows-python-3-7-fails

  Issues with requests-toolbelt: In some PCs running latest bleeding edge version of Python may have some issues with pip installation. To fix it type `pip3 install requests-toolbelt==0.10.1` in your terminal.

3. Verify that CodeMark CLI is installed correctly by running the following command:
     `poetry run codemark --help`

     `codemark --help`

     If you encounter any issues, feel free to raise a pull request.

