#!/bin/bash
run_cmd(){
      if [ ! -n "$1" ]
      then
        python3 main.py e
      fi
      case "$1" in
        --q )
        python3 main.py q "${@:2}"
        ;;
        --h )
        python3 main.py h
        ;;
        *)
        "$@" 2>tmp_err.txt
        python3 main.py "$@" tmp_err.txt
        ;;
    esac
}
run_cmd "$@"