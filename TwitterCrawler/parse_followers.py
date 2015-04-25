import csv
import glob
from datetime import date
import math

class ParseFollowers:
    def __init__(self):
        self.MIN_FOLLOWERS = 10
        self.MAX_FOLLOWERS = 100000
        self.COLLECT_DAY = date(2015, 4, 9)
        self.MIN_TWEETS_PER_DAY = 0.1
        self.already_done = set()

    def __init_already_done(self):
        done_files = glob.glob('crawlLists/archive/*_done')
        for this_file in done_files:
            with open(this_file, 'r') as done_reader:
                all_lines = file.read(done_reader).splitlines()

            for line in all_lines:
                self.already_done.add(line)

    def parse_followers(self):
        self.__init_already_done()

        request_count = 0
        with open("data/chapters/followers/earthhour_hydrated_followers.csv") as csv_file:
            reader = csv.DictReader(csv_file)
            for i in range(1, 345):
                with open("crawlLists/in_list_%04d" % i, 'w') as write_file:
                    counter = 0
                    for row in reader:
                        is_valid = row['protected'] == '0'
                        followers_count = int(row['followers_count'])
                        is_valid = is_valid and followers_count >= self.MIN_FOLLOWERS
                        is_valid = is_valid and followers_count <= self.MAX_FOLLOWERS
                        ca_raw = row['created_at']
                        created_at = date(int(ca_raw[0:4]), int(ca_raw[5:7]), int(ca_raw[8:10]))
                        date_diff = (self.COLLECT_DAY - created_at).days
                        if date_diff > 0:
                            tweets_per_day = float(row['statuses_count']) / date_diff
                        else:
                            tweets_per_day = 0

                        is_valid = is_valid and tweets_per_day > self.MIN_TWEETS_PER_DAY
                        is_valid = is_valid and row['user_id'] not in self.already_done

                        if is_valid:
                            write_file.write("%s\n" % row['user_id'])
                            counter += 1
                            request_count += math.ceil(float(followers_count) / 5000)
                        if counter == 250:
                            break
        print request_count

    def filter_test_in_lists(self):
        self.__init_already_done()

        with open("data/chapters/followers/earthhour_hydrated_followers.csv") as csv_file:
            reader = csv.DictReader(csv_file)
            with open("crawlLists/filtered_test_in_list", 'w') as write_file:
                for row in reader:
                    is_valid = row['protected'] == '0'
                    followers_count = int(row['followers_count'])
                    is_valid = is_valid and followers_count >= self.MIN_FOLLOWERS
                    is_valid = is_valid and followers_count <= self.MAX_FOLLOWERS
                    ca_raw = row['created_at']
                    created_at = date(int(ca_raw[0:4]), int(ca_raw[5:7]), int(ca_raw[8:10]))
                    date_diff = (self.COLLECT_DAY - created_at).days
                    if date_diff > 0:
                        tweets_per_day = float(row['statuses_count']) / date_diff
                    else:
                        tweets_per_day = 0

                    is_valid = is_valid and tweets_per_day > self.MIN_TWEETS_PER_DAY
                    is_valid = is_valid and row['user_id'] in self.already_done

                    if is_valid:
                        write_file.write("%s\n" % row['user_id'])

    def filter_test_out_lists(self):

        with open('crawlLists/filtered_test_in_list', 'r') as filtered_reader:
            all_lines = file.read(filtered_reader).splitlines()

        filtered_list = set()
        for line in all_lines:
            filtered_list.add(line)

        unfiltered_files = glob.glob('data/followersOfFollowers/archive/out_list_[0-9][0-9][0-9].csv')
        for this_file in unfiltered_files:
            file_number = this_file[-7:-4]

            filtered_file = this_file[:-7] + '1' + file_number + '.csv'

            with open(this_file, 'r') as done_reader:
                with open(filtered_file, 'w') as filtered_writer:
                    for line in done_reader:
                        tokens = line.split(',')
                        if tokens[0] in filtered_list:
                            filtered_writer.write(line)

            print file_number

    def get_unique_d2(self):
        already_retrieved = set()
        with open("data/chapters/followers/earthhour_hydrated_followers.csv") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                already_retrieved.add(long(row['user_id']))

        directories = glob.glob('data/followersOfFollowers/d_equals_2_[0-9][0-9][0-9][0-9]')
        directories.sort()

        total_count = 0
        dup_count = 0
        unique_count = 0

        file_number = 0
        write_file = open("crawlLists/hydrated_in_list_%02d" % file_number, 'w')

        for directory in directories:
            files = glob.glob(directory + '/*')
            files.sort()
            for this_file in files:
                with open(this_file, 'r') as read_file:
                    all_lines = file.read(read_file).splitlines()
                for line in all_lines:
                    tokens = line.split(',')
                    user_id = long(tokens[1])
                    total_count += 1

                    if user_id not in already_retrieved:
                        already_retrieved.add(user_id)
                        write_file.write('%s\n' % tokens[1])
                        unique_count += 1
                        if unique_count % 500000 == 0:
                            write_file.close()
                            file_number += 1
                            write_file = open("crawlLists/hydrated_in_list_%02d" % file_number, 'w')
                    else:
                        dup_count += 1

                print 'Finished ' + this_file
            print 'Finished' + directory

        write_file.close()
        print 'Total count is: ' + str(total_count)
        print 'Duplicated count is: ' + str(dup_count)
        print 'Unique count is: ' + str(unique_count)


def extract_location():
    with open('data/users_d2/users_d2.csv', 'r') as users_reader:
        with open('data/users_d2/users_loc_d2.csv', 'w') as loc_writer:
            loc_writer.write('anon_id,location\n')
            csv_reader = csv.DictReader(users_reader)

            line_count = 0
            for row in csv_reader:
                if row['location'] is not None:
                    if len(row['location']) > 0:
                        loc_writer.write('%s,"%s"\n' % (row['anon_id'], row['location']))
                line_count += 1
                if line_count % 500000 == 0:
                    print line_count


def main():
    # p = ParseFollowers()
    # p.parse_followers()
    # p. filter_test_in_lists()
    # p.filter_test_out_lists()
    # p.get_unique_d2()

    extract_location()

if __name__ == "__main__":
    main()
