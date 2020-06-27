import datetime
import json
from collections import defaultdict
from tasks import open_file
from dateutil.rrule import rrule, MONTHLY


# get the file and return yield
def get_all_keys(file: 'specific prefix') -> 'yield string':
    data = open_file(file)
    for line in data:
        yield line


# separate date from yiled string
def get_dates(logs) -> 'dates string':
    dates = []
    for i in logs:
        ids = i.split('id=')[1].split('/')[0]
        date = i.split('month=')[1].split('/')[0]
        dates.append((ids, date))
    return dates


# create dict by ids
def create_sorted_dict_by_id(logs) -> 'dates dict':
    dates = get_dates(logs)
    dict_with_dates = defaultdict(list)
    for key, values in dates:
        dict_with_dates[key].append(values)
    return dict_with_dates


def create_last_dict(dict_with_dates_and_ids: dict) -> 'defaultdict list of dicts':
    dd = defaultdict(list)

    for dict_with_dates_and_ids in (dict_with_dates_and_ids, missing_months, max_month_dict, min_month_dict):
        for key, value in dict_with_dates_and_ids.items():
            dd[key].append(value)
    return dd


def dict_to_json(dict_of_dicts: 'data structure dict', name_of_export_file: 'name of file where to save the json'):
    try:
        with open(name_of_export_file, 'w') as fp:
            json.dump(dict_of_dicts, fp)
    except IOError:
        print('cannot save file')
        raise IOError('ERROR')


# create empty dict for max month, min month and missing months
max_month_dict = {}
min_month_dict = {}
missing_months = {}


# upload logs
logs = get_all_keys('./attachements/struc.log')

# save the ids and dates to dict
dict_with_dates_and_ids = create_sorted_dict_by_id(logs)


# main logic of the loop, where I wanna find max and min date and save to dicts
for key, item in dict_with_dates_and_ids.items():
    min_month = datetime.datetime.strptime(min(item), '%Y-%m-%d').date()
    max_month = datetime.datetime.strptime(max(item), '%Y-%m-%d').date()
    dates = [f'{dt:%Y-%m-%d}' for dt in rrule(MONTHLY, dtstart=min_month, until=max_month)]
    dates.remove((str(min_month))) if str(min_month) in dates else None
    dates.remove((str(max_month))) if str(max_month) in dates else None
    missing_months.update({key: {'missing months': dates}})
    max_month_dict.update({key: {'max': str(max_month)}})
    min_month_dict.update({key: {'min': str(min_month)}})


main_dict = create_last_dict(dict_with_dates_and_ids)
dict_to_json(main_dict, './attachements/result.json')


