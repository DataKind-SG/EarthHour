import csv


def parse_followers():
    with open("data/chapters/followers/earthhour_hydrated_followers.csv") as csv_file:
        reader = csv.DictReader(csv_file)
        for i in range(1, 50):
            with open("crawlLists/in_list_%03d" % i, 'w') as write_file:
                counter = 0
                for row in reader:
                    if row['protected'] == '0':
                        write_file.write("%s\n" % row['user_id'])
                        counter += 1
                    if counter == 100:
                        break

parse_followers()

