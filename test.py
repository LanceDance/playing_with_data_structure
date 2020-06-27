import unittest
from unittest.mock import patch, mock_open
from tasks import *
from fifth_task import *

LIST_OF_LISTS = [[1, 2, 3, 4, 8], [1, 2, 3, 5, 8, 13], [2, 4, 6, 8], [0, 2, 5, 8, 10]]
LOG = ['s3://my-bucket/xxx/yyy/zzz/def/id=333/month=2019-11-01/86002333-cccd-715b-57aa-726238199139.ndjson.gz']


class TestTasks(unittest.TestCase):
    def test_aswer(self):
        assert find_intersection(LIST_OF_LISTS) == {2, 8}
        assert find_intersection([]) is None

    def test_count_logs(self):
        file = count_logs('web.log')
        self.assertIn('GET',file)

    def test_open_file(self):
        with patch("builtins.open", mock_open(read_data="data")) as mock_file:
            assert open("struc.log").read() == "data"
            mock_file.assert_called_with("struc.log")


class TestFifthTask(unittest.TestCase):
    def test_yields(self):
        yields = get_all_keys('struc.log')
        for i in yields:
            self.assertIn('s3://', i)

    def test_parsed_date(self):
        dates = get_dates(LOG)
        self.assertIsInstance(dates[0],tuple)

    def test_sorted_dict(self):
        inst = create_sorted_dict_by_id(LOG)
        self.assertIn('333', inst)

