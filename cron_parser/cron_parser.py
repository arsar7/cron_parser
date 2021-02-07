import logging
from typing import List, Dict, Union, Generator


class CronParser:

    def __init__(self, logger=None, **kwargs):

        self.logger = logger
        self.logger.setLevel(logging.ERROR)

    def load_parsed_data(self, path) -> List[Dict]:
        """
        :param path: path of the parsed filed
        :return: list of dicts
        """

        lines: List = self._parse_file_data(path)

        return self._map_data(lines)

    def _map_data(self, input_data: List) -> List[Dict]:
        """
        :param input_data: List
        :return: List of dictionaries
        """
        output_data = list()

        for i in input_data:
            output_data.append(
                {
                    'hour': self._get_return_type(i[1], max_range='hour'),
                    'minute': self._get_return_type(i[0], max_range='minute'),
                    'job_path': i[2]

                }
            )

        return output_data

    @staticmethod
    def _parse_file_data(file: List) -> List:

        try:

            list_of_rows: Generator = (x.strip(u'\n') for x in file)

            return [
                i.strip().split() for i in list_of_rows
            ]

        except Exception as e:
            logging.error(e)

    @staticmethod
    def _get_return_type(
            value_to_check, max_range: str
    ) -> Union[str, int, None]:
        """

        :param value_to_check: input value Ex (1, 30, * etc.)
        :param max_range: Max number of hrs/min
        :return:
        """

        if max_range not in ('hour', 'minute'):
            raise ValueError("Invalid entity type")

        # 23 is max hrs in a day - 1 and 59 max min in an hour - 1
        max_val: int = 23 if max_range == 'hour' else 59

        if str(value_to_check) == '*':
            return str(value_to_check)
        elif 0 <= int(value_to_check) <= max_val:
            return int(value_to_check)
        else:
            return None
