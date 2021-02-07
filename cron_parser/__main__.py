import logging
import sys

from cron_next_run import CronNextRun

if __name__ == '__main__':

    if len(sys.argv) != 2:
        logging.error(
            """
            Syntax error - run the file using an example like this: 
            MAC OS - python3 parser 20:00 < config
            Windows -parser 20:00 < config.txt  
        """
        )
        sys.exit()

    ob: object = CronNextRun()

    for cron in ob.get_next_runtime(
        input_time=sys.argv[1], config_path=sys.stdin
    ):
        print(' '.join(cron))
