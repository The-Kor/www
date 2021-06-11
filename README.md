# www
### What Went Wrong is a Linux tool that helps you get online assistance right from the terminal

# Installation - 
    git clone <www_repo_link>
    pip install -r requirements.txt
# How to run -     
  ## 3 options
    * ./www.sh (no arguments)
    * ./www.sh --q <query to search>
    * ./www.sh <command to run>
    * ./www.sh --h (for help)


# Demo
![image](https://user-images.githubusercontent.com/44695990/121691478-b47c0600-cacf-11eb-9f6c-6bed425547c1.png)

# Error parsing 
    When running the tool with a given command the tool parses the command and the error message (from stderr) and runs a search

# Web parsing
    Currently we support only StackOverFlow, adding support to new website can be done using implementation to Parser class
