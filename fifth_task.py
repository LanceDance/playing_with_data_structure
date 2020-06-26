import json
from collections import defaultdict
from tasks import open_file


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
        return 0


# create empty dict for max month, min month and missing months
max_month_dict = {}
min_month_dict = {}
missing_months = {}


# upload logs
logs = get_all_keys('struc.log')

dict_with_dates_and_ids = create_sorted_dict_by_id(logs)


# main logic of the loop, where I wanna find max and min date and save to dicts
for key, item in dict_with_dates_and_ids.items():
    v = []
    year = 0
    for i in item:
        a = i.split('-')[1]
        v.append(int(a))
        year = i.split('-')[0]
    min_month = min(item)
    maxi_month = max(item)
    missing_dates = []
    for x in range(min(v), max(v)):
        if x <= 9:
            num = '-0'
        else:
            num = '-'
        if x in v:
            pass
        else:
            created_date = f"{year}{num}{x}-01"
            missing_dates.append(created_date)
            missing_months.update({key: {'missing months': missing_dates}})
    max_month_dict.update({key: {'max': maxi_month}})
    min_month_dict.update({key: {'min': min_month}})

di = create_last_dict(dict_with_dates_and_ids)

dict_to_json(di, 'result.json')


