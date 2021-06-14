# WWW
[![License](https://img.shields.io/badge/License-MIT-red.svg)](https://www.mit.edu/~amini/LICENSE.md)
### What Went Wrong is a Linux tool that helps you get online assistance right from the terminal

## Installation:
    git clone <www_repo_link>
    pip install -r requirements.txt

## How to run:
  ### The following commands are available to use in the terminal:
    * ./www.sh (no arguments)
    * ./www.sh --q <query to search>
    * ./www.sh <command to run>
    * ./www.sh --h (for help)

## Parsing:
  ### Errors
    When running the tool with a given command the tool parses the command and the error message (from stderr) and runs a search.

  ### Web
    Currently we support only Stack OverFlow, adding support to a different website can be done by writing an implementation for the Parser class.

## Notes for contributors:
* This tool requires [Python 3](https://www.python.org/downloads/) and [pip](https://pypi.org/project/pip/) to run.
* This tool requires an internet connection to work properly.
* Every change in the code, requires a proper and well documented pull request, which will only be accepted after being reviewed and approved by all main authors of the app.

## Main Authors:
[Koral Haham](https://github.com/The-Kor) [Dor Probstein](https://github.com/dorpro13)
