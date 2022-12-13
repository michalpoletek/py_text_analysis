import re
# import sys # only needed if passing file from terminal
import operator
import csv

user_count_info = []
user_count_error = []
error_msg = []

with open("syslog.txt", 'r') as f:  # in Linux use sys.argv(1)
    for line in f.readlines():
        if "INFO" in line:
            result = re.search(r"\((\w*.?\w*)\)$", line)
            user_count_info.append(result[1]) # in Linux use >>> user_count_info.append(result.group(1))

        if "ERROR" in line:
            result2 = re.search(r"\((\w*\.?\w*)\)", line)
            user_count_error.append(result2[1]) # in Linux use >>> user_count_error.append(result2.group(1))
            result3 = re.search(r"ERROR ([A-Za-z ']*) \(", line)
            error_msg.append(result3[1]) # in Linux use >>> error_msg.append(result3.group(1))
    f.close()

dict_usr_info = {}
for i in set(user_count_info):
    dict_usr_info[i] = user_count_info.count(i)
dict_usr_error = {}
for i in set(user_count_error):
    dict_usr_error[i] = user_count_error.count(i)
dict_error_msg = {}
for i in set(error_msg):
    dict_error_msg[i] = error_msg.count(i)

# print(dict_usr_info)
# print(dict_usr_error)
# print(dict_usr)


def DictionariesToList(dict_1, dict_2):
    dict_3 = {}
    list_3 = []
    for key in dict_1:
        dict_3[key] = [dict_1[key], 0]
        sublist = [key, dict_1[key]]
        if key in dict_2:
            dict_3[key] = [dict_1[key], dict_2[key]]
            sublist.append(dict_2[key])
        else:
            sublist.append(0)
        list_3.append(sublist)
    for key in dict_2:
        if key not in dict_1:
            dict_3[key] = [0, dict_2[key]]
            sublist = [key, 0, dict_2[key]]
            list_3.append(sublist)
    return list_3


dict_usr_list = DictionariesToList(dict_usr_info, dict_usr_error)
#print(dict_usr_list)

dict_usr_list_sorted = sorted(dict_usr_list)
#print(dict_usr_list_sorted)

dict_error_msg_sorted = sorted(dict_error_msg.items(), key=operator.itemgetter(1), reverse=True)
#print(dict_error_msg_sorted)

fields_usr = ["Username", "INFO", "ERROR"]
with open('user_statistics.csv', 'w', newline='') as f1:
    write = csv.writer(f1)
    write.writerow(fields_usr)
    write.writerows(dict_usr_list_sorted)
    f1.close()

fields_err = ["Error", "Count"]
with open('error_message.csv', 'w', newline='') as f2:
    write = csv.writer(f2)
    write.writerow(fields_err)
    write.writerows(dict_error_msg_sorted)
    f2.close()