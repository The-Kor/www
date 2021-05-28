import sys
import utils

if __name__ == '__main__':
    run_args = {}
    if sys.argv[1] == "q":
        run_args['query'] = " ".join(sys.argv[2:])
    else:
        run_args = utils.get_run_info(sys.argv)
        run_args['query'] = utils.get_query(run_args['command'], run_args['error'])
    run_args = utils.run(run_args)

    # check action and do what needed
