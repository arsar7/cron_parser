import logging
from typing import Dict, Generator

from cron_parser import CronParser

_INPUT_TIMES = dict(

    min_time=0,
    max_hrs=23,
    max_min=59
)


class CronNextRun(CronParser):

    def __init__(self):

        self.min_time = _INPUT_TIMES['min_time']
        self.max_hrs = _INPUT_TIMES['max_hrs']
        self.max_min = _INPUT_TIMES['max_min']

        super(CronNextRun, self).__init__(logger=logging.Logger('Cron Next Run Times'))

    def get_next_runtime(
            self, input_time: str, config_path: str
    ) -> Generator:
        """
        :param input_time: str
        :param config_path: str
        :return: generator
        """

        _valid_input_time: Dict = self._check_input_time(input_time)

        if config_path:
            configs = self.load_parsed_data(config_path)

            for item in configs:
                runtime = self._next_cron_run_time(item, _valid_input_time)

                yield (
                    self._concat_hrs_mins(runtime['hour'], runtime['minute']),
                    runtime['day'], item['job_path']
                )

        else:
            logging.error(
                "No config path was specified"
            )

    def _check_input_time(self, input_time: str) -> Dict:
        """
        :param input_time: string containing time (ex. "15:30")
        :return: dictionary
        """

        hour, minute = tuple(map(int, input_time.split(":")))

        if 0 <= hour <= self.max_hrs and 0 <= minute <= self.max_min:

            return {
                'hour': hour,
                'minute': minute
            }

        else:
            logging.error(
                f"Incorrect time -{input_time} was passed, make sure time corresponds HH:MM format"
            )

    @staticmethod
    def _time_delta(
            line_dict: Dict, valid_input: Dict, freq: str
    ) -> int:

        """
          :param line_dict: dictionary
          :param valid_input: dictionary
          :param freq: frequency
          :return: int
          """

        if str(line_dict[freq]).strip() != '*':
            var = int(line_dict[freq]) - (valid_input[freq])
        else:
            var = 0

        return var

    @staticmethod
    def _concat_hrs_mins(hour: int, minute: int):
        """
        :param: hour: int
        :param: minute: int
        :return: str: A formatted time string hr in HH:MM format
        """

        return ':'.join([str(hour), str(minute).zfill(2)])

    def _next_cron_run_time(
            self, line_dict, valid_input
    ):

        """
        :param line_dict: dictionary
        :param valid_input: dictionary
        :return: next cron run time
        """

        # TODO: Optimise this using calendar
        #  package and perhaps timedelta for the intervals

        input_hr: int = line_dict['hour']
        input_min: int = line_dict['minute']
        valid_hr: int = valid_input['hour']
        valid_min: int = valid_input['minute']

        hrs_diff: int = self._time_delta(line_dict, valid_input, freq='hour')
        mins_diff: int = self._time_delta(line_dict, valid_input, freq='minute')

        # double * means program should run today every hr/min
        if input_hr == '*' and input_min == '*':

            run_hr = valid_hr
            run_min = valid_min
            run_day = 'today'

        # running every hrs
        elif input_hr == '*':

            if mins_diff < 0:

                if valid_hr == self.max_hrs:

                    run_hr = 0
                    run_day = 'tomorrow'

                else:
                    run_hr = valid_hr + 1
                    run_day = 'today'

            else:
                run_hr = valid_hr
                run_day = 'today'

            run_min = input_min

        # running every min
        elif input_min == '*':

            if hrs_diff < 0:
                run_min = 0
                run_day = 'tomorrow'

            elif hrs_diff == 0:
                run_min = valid_min
                run_day = 'today'

            else:
                run_min = 0
                run_day = 'today'

            run_hr = input_hr

        else:

            if hrs_diff < 0:
                run_day = 'tomorrow'
            elif hrs_diff == 0:
                if mins_diff < 0:
                    run_day = 'tomorrow'
                else:
                    run_day = 'today'
            else:
                run_day = 'today'

            run_hr = input_hr
            run_min = input_min

        return {
            'day': run_day,
            'hour': run_hr,
            'minute': run_min
        }
