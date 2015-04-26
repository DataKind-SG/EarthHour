import csv
import pprint as pp

INDEX_COLUMN_SUBREASON = 14
# COUNT_THRESHOLD_SIGNIFICANT = 2

dict_subscribe_reason = {}

with open('contact.csv') as csvfile:
	spamreader = csv.reader(csvfile)
	headers = next(spamreader)
	for row in spamreader:
		if row[INDEX_COLUMN_SUBREASON] not in dict_subscribe_reason:
			dict_subscribe_reason[row[INDEX_COLUMN_SUBREASON]] = 1
		else:
			dict_subscribe_reason[row[INDEX_COLUMN_SUBREASON]] = dict_subscribe_reason[row[INDEX_COLUMN_SUBREASON]] + 1

# dict_subscribe_reason['Others'] = 0
# dict_subscribe_reason_keys = list(dict_subscribe_reason.keys())
# for key in dict_subscribe_reason_keys:
# 	if (dict_subscribe_reason[key] < COUNT_THRESHOLD_SIGNIFICANT) and (key != 'Others'):
# 		dict_subscribe_reason['Others'] = dict_subscribe_reason['Others'] + 1
# 		dict_subscribe_reason.pop(key)
pp.pprint(dict_subscribe_reason)

with open('parsed_contact.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    spamwriter.writerow(['discover', 'count'])
    for key in dict_subscribe_reason:
    	spamwriter.writerow([key, dict_subscribe_reason[key]])