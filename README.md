# WWW
### What Went Wrong is a Linux tool that helps you get online assistance right from the terminal
[![License](https://img.shields.io/badge/License-MIT-red.svg)](https://www.mit.edu/~amini/LICENSE.md)

## Table of Contents  
- [Installation](#installation)  
- [How to run](#run)
- [Web parsing](#web_parsing)
- [How To Contribute?](#contribute)  

<a name="installation"/>

# Installation 
* Windows users - please install WSL in order to be able to run this project, for more info click [here](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

1. Clone the repository via `git clone <www_repo_link>`
    
2. (Recommended) setup a Python virtual environment as follows:
    
```shell
   python3 -m venv venv
   . ./venv/bin/activate
```
    
3. Install the dependencies via `pip install -r requirements.txt`
4. Make the shell script executable via `chmod +x ./www.sh`

<a name="run"/>

# How to run

To see all available options for CLI, type `./www.sh --h`

There are mainly 3 ways of running this tool:

* Interactively, by running 

  `./www.sh` (no arguments)

* By supplying a query directly:

  `./www.sh --q <query to search>`
 
   For example `./www.sh --q no such file`

* By executing a terminal command:

  `./www.sh <command to run>`
  
  This will execute the command and use the resulting stderr, along with the
  command itself as the query.

  For example, `./www.sh python demo_error_1.py`

<a name="web_parsing"/>

# Web parsing
Currently we support StackOverFlow Threads and GitHub Issues, adding support to new website can be done by implementing the `Parser` class (that can be found in site_parser.py) and adding the new implemented class to parsers list in  `main.py`

<a name="contribute"/>

# How to Contribute
* Fork this repo.
* Open a new branch (locally) and start working on it.
* Push it.
* Create a new pull request. (Thank you! ❤️)
####    Notes for contributors:
*   This tool requires [Python 3](https://www.python.org/downloads/) and [pip](https://pypi.org/project/pip/) to run.
*   This tool requires an internet connection to work properly.
*   Every change in the code, requires a proper and well documented pull request, which will only be accepted after being reviewed and approved by all main authors of the app.
