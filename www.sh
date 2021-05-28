#!/bin/bash
run_cmd(){
      case "$1" in
        -q )
        python main.py q "${@:2}"

        ;;
        *)
        "$@" 2>tmp_err.txt
        python main.py "$@" tmp_err.txt
        ;;
    esac
}

run_cmd "$@"