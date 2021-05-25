import sys
import utils

if __name__ == '__main__':
    run_args = utils.get_run_info(sys.argv)
    while (True):
        run_args = utils.run(run_args)

        # check action and do what needed
