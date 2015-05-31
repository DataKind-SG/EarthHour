import csv
import pprint as pp

INDEX_COLUMN_UNSUBREASON = 1
COUNT_THRESHOLD_SIGNIFICANT = 2

dict_unsubscribe_reason = {}

with open('unsubscribe.csv') as csvfile:
	spamreader = csv.reader(csvfile)
	headers = next(spamreader)
	for row in spamreader:
		if row[INDEX_COLUMN_UNSUBREASON] not in dict_unsubscribe_reason:
			dict_unsubscribe_reason[row[INDEX_COLUMN_UNSUBREASON]] = 1
		else:
			dict_unsubscribe_reason[row[INDEX_COLUMN_UNSUBREASON]] = dict_unsubscribe_reason[row[INDEX_COLUMN_UNSUBREASON]] + 1

dict_unsubscribe_reason['Other Reasons'] = 0
dict_unsubscribe_reason_keys = list(dict_unsubscribe_reason.keys())
for key in dict_unsubscribe_reason_keys:
	if dict_unsubscribe_reason[key] < COUNT_THRESHOLD_SIGNIFICANT:
		dict_unsubscribe_reason['Other Reasons'] = dict_unsubscribe_reason['Other Reasons'] + 1
		dict_unsubscribe_reason.pop(key)
pp.pprint(dict_unsubscribe_reason)

with open('parsed_unsubscribe.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
    spamwriter.writerow(['unsubreason', 'count'])
    for key in dict_unsubscribe_reason:
    	spamwriter.writerow([key, dict_unsubscribe_reason[key]])