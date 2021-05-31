#!/bin/bash
run_cmd(){
      if [ ! -n "$1" ]
      then
        python main.py e
      fi
      case "$1" in
        --q )
        python main.py q "${@:2}"
        ;;
        --h )
        python main.py h
        ;;
        *)
        "$@" 2>tmp_err.txt
        python main.py "$@" tmp_err.txt
        ;;
    esac
}
#TODO add "www" support - ask for query in menu
run_cmd "$@"