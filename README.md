# WWW
### What Went Wrong is a Linux tool that helps you get online assistance right from the terminal

## Table of Contents  
- [Installation](#installation)  
- [How to run](#run)
- [Web parsing](#web_parsing)
- [How To Contribute?](#contribute)  

<a name="installation"/>

# Installation 
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
Currently we support only StackOverFlow, adding support to new website can be done by implementing the `Parser` class and updating `parser_factory.py`

<a name="contribute"/>

# How to Contribute
* Fork this repo.
* Open a new branch (locally) and start working on it.
* Push it.
* Create a new pull request. (Thank you! ❤️)