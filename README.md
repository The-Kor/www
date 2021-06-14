# www
### What Went Wrong is a Linux tool that helps you get online assistance right from the terminal

# Installation - 
    git clone <www_repo_link>
    pip install -r requirements.txt

# Contribution
Inside github, fork the upstream repository.

Clone your own fork of the project.

Before starting to implement a new feature or fixing a bug, make sure to pull master (or develop) branch from the upstream repository, and only then create your branch.

Push your code and open a PR against the upstream repository develop branch.

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
