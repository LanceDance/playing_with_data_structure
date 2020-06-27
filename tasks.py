import re
import tracemalloc


def open_file(file):
    try:
        with open(file) as f:
            readed_data = f.readlines()
        return readed_data
    except IOError:
        print('File doesnt exist')
        raise IOError('ERROR')


# 1st task
# I would say there is lot's of modules how to measure memory in Python, tracemalloc is in build in module
# so there is no need to install other packages
# as an example I tracking one function
# and there si command ps in bash which can tell us outside the code how is memory
# ps -m -o %cpu,%mem,command - do the trick

def check_memory():
    tracemalloc.start()
    open_file('web.log')
    current, peak = tracemalloc.get_traced_memory()
    result = f"Current memory usage is {current / 10**6}MB"
    tracemalloc.stop()
    return result


# 2nd task
def find_in_generator():
    # (int(s) for s in str.split() if s.isdigit())

    string_to_set = set(generator().split(" "))
    numb = list((filter(lambda x: x.isdigit(), string_to_set)))
    json = list(filter(lambda x: '.json' in x or '.csv' in x ,string_to_set))
    date = list(filter(lambda x: re.search(r'\d{4}-\d{2}-\d{2}', x), string_to_set))
    result = numb + json + date
    return result


def generator(string='h3110 23 cat rabbit 11 2 dog eng.json efv.csv , 2019-05-27 23'):
    return string
########################################################


# 3th task
def find_intersection(d):
    if d:
        return set(d[0]).intersection(*d)

########################################################


# 4th task
def count_logs(file):
    data = open_file(file)
    li = []
    for line in data:
        endpoint = line.split('"')[1]
        without_method = endpoint.split(" H")[0]
        li.append(without_method)
    endpoints = [[x, li.count(x)] for x in set(li)]
    result = ' '
    for i in endpoints:
        result.join(str(i))
        result += f"\n{i[0]} was hitted {i[1]} time(s)\n"

    return result

# 4.b
# I tried to create algorithm in that way, that it doesnt matter if logs are sorted or not
# I copied/pasted twice the example of logs to web.log file
#
# 4.c I just can think of some log tools for example splunk or Vsphere, where you can play with some filters or write in
# other language :)

#######################################################

