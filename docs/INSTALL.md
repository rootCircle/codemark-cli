# Installation Instructions

  
  <h1 style="margin-left: 10px;"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png" alt="Python Logo" height="50" align="center" >Install Python</h1>

A Quick Guide for Installing Python on Common Operating Systems

<br>

1. [Install on Windows](#--windows)
2. [Install on MacOS](#-mac-os)
3. [Install on Linux](#-linux)


 
  <h2 style="margin-left: 20px;" id="windows" > <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Windows_logo_-_2012.svg/132px-Windows_logo_-_2012.svg.png" alt="Windows Logo" height="50" align="center"> Windows</h2>

1. If you have not yet installed Python on your Windows OS, then download and install the latest Python3 installer from [Python Downloads Page](https://www.python.org/downloads/)
   - Make sure to check the box during installation which adds Python to PATH. Labeled something like *Add Python 3.X to PATH*

2. Once Python is installed, you should be able to open a command window, type python, hit ENTER, and see a Python prompt opened. Type quit() to exit it. You should also be able to run the command pip and see its options. If both of these work, then you are ready to go.
  - If you cannot run python or pip from a command prompt, you may need to add the Python installation directory path to the Windows PATH variable
    - The easiest way to do this is to find the new shortcut for Python in your start menu, right-click on the shortcut, and find the folder path for the python.exe file
      - For Python3, this will likely be something like C:\Users\<USERNAME>\AppData\Local\Programs\Python\Python37
    - Open your Advanced System Settings window, navigate to the "Advanced" tab, and click the "Environment Variables" button
    - Create a new system variable:
      - Variable name: PYTHON_HOME
      - Variable value: <your_python_installation_directory>
    - Now modify the PATH system variable by appending the text ;%PYTHON_HOME%\;%PYTHON_HOME%;%PYTHON_HOME%\Scripts\ to the end of it.
    - Close out your windows, open a command window and make sure you can run the commands python and pip
### Setting up Python Environment in Windows

3. **Add Python to the PATH (if necessary)**:
   - If you cannot run `python` or `pip` from a command prompt, you may need to add the Python installation directory path to the Windows PATH variable.

   - **Check Existing PATH Entry**:
     - First, check if the `%USERPROFILE%\AppData\Roaming\Python\Python310\Scripts` path is already in your system's PATH by running this command:
     ```shell
     echo %PATH% | findstr /C:"%USERPROFILE%\AppData\Roaming\Python\Python310\Scripts"
     ```

     - If the path is already in your PATH, no further action is needed. You can use `python` and `pip` without modification.
     - **Separate Paths for Different Versions**:
     - Note that you might have separate paths for different Python versions. Check for the paths     associated with your specific Python version.

     - **Methods of Installation**:
     - Depending on the method of Python installation, the PATH entry may differ. Ensure that you add the correct path associated with your Python installation method.

   - **Add to PATH (if not present)**:

     - **Open Advanced System Settings**:
       - Click the Windows Start button and search for "Advanced System Settings."
       - Select "View advanced system settings."

     - **Access Environment Variables**:
       - In the "System Properties" window, go to the "Advanced" tab.
       - Click the "Environment Variables" button.

     - **Edit the PATH Variable**:
       - In the "Environment Variables" window, locate the "Path" variable under the "System variables" section.
       - Click the "Edit" button to modify the PATH variable.

     - **Add the New Path**:
       - Click "New" in the "Edit Environment Variable" window.
       - Enter the following path similar to: (verify the path)
       ```
       %USERPROFILE%\AppData\Roaming\Python\Python310\Scripts
       ```

     - **Save Changes**:
       - Click "OK" in the "Edit Environment Variable" window.
       - Click "OK" again in the "Environment Variables" window to save your changes.
       - Close the "System Properties" window.

4. **Test Python and pip**:
   - Close and reopen your command prompt to ensure that the changes take effect. You should now be able to run `python` and `pip` from the command prompt.



<div>
  <h2 style="margin-left: 10px;" id="macos" ><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Finder_Icon_macOS_Big_Sur.png/900px-Finder_Icon_macOS_Big_Sur.png?20200704175319" alt="Finder Icon macOS Big Sur" height="50" align="center"> Mac OS</h2>
</div>


MacOS comes with a native version of Python. As of this writing, it comes with a version of Python2, which has been deprecated. In order to use most modern Python applications, you need to install Python3. Python2 and Python3 can coexist on the same machine without problems, and for MacOS it is in fact necessary for this to happen, since MacOS continues to rely on Python2 for some functionality.

### Option 1: Install the official Python release
1. Browse to the [Python Downloads Page](https://www.python.org/downloads/)
2. Click on the "Download Python 3.x.x" button on the page
3. Walk through the steps of the installer wizard to install Python3
4. Once installed, the wizard will open a Finder window with some .command files in it
    - Double-click the Install Certificates.command file and the Update Shell Profile.command file to run each of them
    - Close the windows once they are finished
6. Open your *Terminal* application and run the command python3 to enter the Python interactive command line. Issue the command quit() to exit. Also make sure PIP (the Python package manager) is installed by issuing the command pip3 -V. It should display the current version of PIP as well as Python (which should be some release of Python3)
7. You're all done. Python is installed and ready to use.

### Option 2: Install with Homebrew
[Homebrew](https://brew.sh/) is a MacOS Linux-like package manager. Walk through the below steps to install Homebrew and an updated Python interpreter along with it.
1. Open your *Terminal* application and run: 
```bash 
 xcode-select --install 
``` 
This will open a window. Click *'Get Xcode'* and install it from the app store.
2. Install Homebrew. Run:
```bash
 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" 
 ```
   - You can also find this command on the [Homebrew website](https://brew.sh/)
3. Install latest Python3 with `brew install python`
4. Once Python is installed, you should be able to open your *Terminal* application, type `python3`, hit ENTER, and see a Python 3.X.X prompt opened. Type `quit()` to exit it. You should also be able to run the command `pip3` and see its options. If both of these work, then you are ready to go
   - Here are some additional resources on [Installing Python 3 on Mac OS X](https://docs.python-guide.org/starting/install3/osx/)

<div>
  <h2 style="margin-left: 10px;" id="linux"><img src="https://upload.wikimedia.org/wikipedia/commons/a/af/Tux.png" alt="Tux Linux Mascot"  align="center" height="50"> Linux</h2>
</div>

- *Raspberry Pi OS* may need Python and PIP
  - Install them: `sudo apt install -y python3-pip`
- *Debian (Ubuntu)* distributions may need Python and PIP
  - Update the list of available APT repos with `sudo apt update`
  - Install Python and PIP: `sudo apt install -y python3-pip`
- *RHEL (CentOS)* distributions usually need PIP
  - Install the EPEL package: `sudo yum install -y epel-release`
  - Install PIP: `sudo yum install -y python3-pip`    
- *Fedora* distributions may need Python and PIP
  - Install Python and PIP: `sudo dnf install -y python3 python3-pip`
- *Arch Linux* may need Python and PIP
  - Update the package database: `sudo pacman -Sy`
  - Install Python and PIP: `sudo pacman -S python python-pip`


<div>
  <h1 style="margin-left: 10px;" ><img src="https://raw.githubusercontent.com/rootCircle/codemark-cli/main/logo.png" alt="Codemark CLI Logo" height="50" align="center"> Install Codemark CLI</h1>
</div>

## Installation instructions

To install and use CodeMark CLI, follow these steps:

1. Clone the CodeMark CLI repository by running the following command:
 
    ```bash
    git clone https://github.com/rootCircle/codemark-cli.git
    ```

2. Install CodeMark CLI by running the following commands:

    ```bash
    cd codemark-cli
    pip3 install poetry # use pip if pip3 is not available
    poetry install # python3 -m poetry install
    pip3 install --editable .
    ```

    - **Note:** If pip3 is not installed on your system, use pip instead.
    - **Note:** If you encounter permission issues in `pip3 install --editable .`, add the --user flag at the end of the command.

    - **Note:** Make sure Python's Script library is in System PATH.
    - **Use this to set up:** [https://gist.github.com/martinohanlon/c0abb7281cb9020e75053fba7011daf7](https://gist.github.com/martinohanlon/c0abb7281cb9020e75053fba7011daf7) or [https://realpython.com/add-python-to-path/](https://realpython.com/add-python-to-path)

    - **Note:** If you are a Windows user and encounter issues installing pyrebase, refer to this Stack Overflow post: [https://stackoverflow.com/questions/53461316/pyrebase-install-on-windows-python-3-7-fails](https://stackoverflow.com/questions/53461316/pyrebase-install-on-windows-python-3-7-fails)

    - **Note:** Issues with requests-toolbelt: In some PCs running the latest bleeding edge version of Python may have some issues with pip installation. To fix it, type `pip3 install requests-toolbelt==0.10.1` in your terminal.


3. Verify that CodeMark CLI is installed correctly by running the following command:
    
    ```bash
     poetry run codemark --help # or python -m poetry run codemark --help
     codemark --help # if scripts is on the PATH
    ```

     If you encounter any issues, feel free to raise a issue request.

     *Note:* CodeMark CLI might not work if our Firebase has not been set up yet. for setting it up, religously follow the instructions at [this page](docs/FIREBASE_SETUP.md).

# Running the Code Live

To run CodeMark CLI live, you can follow these steps:

1. Ensure that CodeMark CLI is installed correctly by running the following commands:
   
   ```bash
   poetry run codemark
   ```
   
   If you encounter any issues, please note that CodeMark might not work because our Firebase has not been set up yet. For setting it up, please follow the instructions at [this page](docs/FIREBASE_SETUP.md).
