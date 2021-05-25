run_cmd(){
  "$@" 2>tmp_err.txt
  python main.py "$@" tmp_err.txt
}

run_cmd "$@"