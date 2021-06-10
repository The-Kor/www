# WWW - What Went Wrong
WWW is a Linux tool that helps you get online assistance right from the terminal.

## Table of Contents  
- [Installation](#Installation)  
- [How to run](#run)
- [Error parsing](#err)  
- [Web parsing](#web)
- [How To Contribute?](#howtocontribute)  

### Installation - 
    git clone <www_repo_link>
    pip install -r requirements.txt

<a name="run"/>

### How to run -     
#### 3 options
* ./www.sh (no arguments)
* ./www.sh --q <query to search>
* ./www.sh <command to run>
* ./www.sh --h (for help)

<a name="err"/>

#### Error parsing 
    When running the tool with a given command the tool parses the command and the error message (from stderr) and runs a search

<a name="web"/>

#### Web parsing
    Currently we support only StackOverFlow, adding support to new website can be done using implementation to Parser class

<a name="howtocontribute"/>

### How to Contribute
* Fork this repo.
* Open a new branch (locally) and start working on it.
* Push it.
* Create a new pull request. (Thank you! ❤️)
