import csv
import glob
from datetime import date
import math

def parse_followers():

    MIN_FOLLOWERS = 10
    MAX_FOLLOWERS = 100000
    TODAY = date.today()
    MIN_TWEETS_PER_DAY = 0.1

    already_done = set()

    done_files = glob.glob('crawlLists/*_done')
    for this_file in done_files:
        with open(this_file, 'r') as done_reader:
            all_lines = file.read(done_reader).splitlines()

        for line in all_lines:
            already_done.add(line)

    request_count = 0
    with open("data/chapters/followers/earthhour_hydrated_followers.csv") as csv_file:
        reader = csv.DictReader(csv_file)
        for i in range(1, 345):
            with open("crawlLists/in_list_%04d" % i, 'w') as write_file:
                counter = 0
                for row in reader:
                    is_valid = row['protected'] == '0'
                    followers_count = int(row['followers_count'])
                    is_valid = is_valid and followers_count >= MIN_FOLLOWERS
                    is_valid = is_valid and followers_count <= MAX_FOLLOWERS
                    ca_raw = row['created_at']
                    created_at = date(int(ca_raw[0:4]), int(ca_raw[5:7]), int(ca_raw[8:10]))
                    date_diff = (TODAY - created_at).days
                    if date_diff > 0:
                        tweets_per_day = float(row['statuses_count']) / date_diff
                    else:
                        tweets_per_day = 0

                    is_valid = is_valid and tweets_per_day > MIN_TWEETS_PER_DAY
                    is_valid = is_valid and row['user_id'] not in already_done

                    if is_valid:
                        write_file.write("%s\n" % row['user_id'])
                        counter += 1
                        request_count += math.ceil(float(followers_count) / 5000)
                    if counter == 250:
                        break
    print request_count
parse_followers()

