# CodeMark CLI 🖥️📝🔍

CodeMark CLI is a command-line interface that helps you manage your coding assignments and tests with the CodeMark cloud service. With this tool, you can easily initialize the configuration, list assignments, fetch and check your code, submit your code for grading, and get AI-powered error recommendations. The tool is designed to simplify your experience with CodeMark and streamline your coding workflow. ⌨️💻👨‍💻

### Website
Visit [here](https://github.com/umeshSinghVerma/codemarkweb/tree/main/codemarkfrontend).

### Download
[<img src="https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white"
     alt="Download from GitHub"
     height="60">](https://github.com/rootCircle/codemark-cli/releases)

## Installation instructions

To install and use CodeMark CLI, follow these steps:

1. Clone the CodeMark CLI repository by running the following command:
 `git clone https://github.com/rootCircle/codemark-cli.git`

2. Install CodeMark CLI by running the following command:

 `pip3 install --editable .`
 
 Note: If pip3 is not installed on your system, use pip instead. If you encounter permission issues, add the `--user` flag at the end of the command.

 Note: If you are a Windows user and encounter issues installing pyrebase, refer to this Stack Overflow post: https://stackoverflow.com/questions/53461316/pyrebase-install-on-windows-python-3-7-fails

3. Verify that CodeMark CLI is installed correctly by running the following command:

 `codemark --help`

 If you encounter any issues, feel free to raise a pull request.

## Usage

To use CodeMark CLI, run the following command:

 `codemark|cmk [OPTIONS] COMMAND [ARGS]...`
 
### Options

- `--help`: Show this message and exit.

### Commands

- `check`: Checks the code against selected test cases and report errors. 🔍🐞
- `doctor`: Fixes any known common issues for the app. 💊🩺
- `get`: Fetches assignments from cloud, based on assignment Code. 🌩️📥
- `init`: Initialize the configuration globally for CodeMark. 🚀🔧
- `list`: Lists all assignments. 📜👀
- `logout`: Logout the user. 🔒👋
- `review`: Let AI review your code and recommend error you might be doing. 🔍💡
- `submit`: Submit the code against selected test cases and report errors. 🚀📝

### Requirements

CodeMark CLI requires a working internet connection to interact with the CodeMark cloud service. Additionally, make sure you have Python installed on your system.

### These fine people helped us with the project

For HackOFiesta v4.0 Submission | Team Silicon Sorcerers

| Name | Username | Role | Key Contributions
| --- | --- | --- | --- |
| Praveen Jaiswal | @rootCircle | Team Lead, CLI Developer | CLI App and Code Integration |
| Umesh Verma | @umeshSinghVerma | Backend Developer | Firebase Integration in Website |
| Vansh Khare | @real-Vansh-Khare | AI & Algorithm Design with frontend web developer | Frontend Pages Designs, Plag Report Detection |
| Yash Agarwal | @Yash7426 | Chief Frontend Developer | All the frontend designs and pages and their integrations with backend |
| Manan Patel | @manan9993 | Blockchain Developer | Web3 based decentralised Storage and management for report of submitted code |

## License

CodeMark CLI is released under the Apache-2.0 License. See LICENSE for details.

## Support

If you have any questions or issues with CodeMark CLI, please raise an issue request. We are here to help! 💬👋

## Walkthrough Videos
[![CodeMark CLI](https://img.youtube.com/vi/tDkEvjWW7QA/0.jpg)](https://www.youtube.com/watch?v=tDkEvjWW7QA "CodeMark CLI")
[![CodeMark Web](https://img.youtube.com/vi/OzlFier3gPE/0.jpg)](https://www.youtube.com/watch?v=OzlFier3gPE "CodeMark CLI")

## Screenshots
![codemark_submit](https://raw.githubusercontent.com/rootCircle/codemark-cli/main/Screenshots/1.png)
![codemark_review](https://raw.githubusercontent.com/rootCircle/codemark-cli/main/Screenshots/2.png)
![cmk_doctor](https://raw.githubusercontent.com/rootCircle/codemark-cli/main/Screenshots/3.png)

## Logo
![CodeMark logo](https://raw.githubusercontent.com/rootCircle/codemark-cli/main/logo.png)

