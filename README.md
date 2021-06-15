# www
### What Went Wrong is a Linux tool that helps you get online assistance right from the terminal
### This tool allows to search for an answer of a given error (exception caugth while running a program) without leaving the terminal

# Installation
git clone <www_repo_link>
pip install -r requirements.txt

# How to run -     
  ## 3 options
    * ./www.sh (no arguments)
    * ./www.sh --q <query to search>
    * ./www.sh <command to run>
    * ./www.sh --h (for help)

# Error parsing 
When running the tool with a given command the tool parses the command and the error message (from stderr) and runs a search

# Web parsing
Currently we support only StackOverFlow, adding support to new website can be done using implementation to Parser class
