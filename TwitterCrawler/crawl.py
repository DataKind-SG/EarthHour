import twitteraccess
import datetime
import time
import warnings
import writetwitter as wt
import glob
import os
import multiprocessing

def get_all_chapter_handles():
    with open("earth_hour_chapters.txt", 'r') as chapter_file:
        all_chapters = chapter_file.read().splitlines()
    return all_chapters


class Crawl:
    def __init__(self, app_keys):
        self.ta = twitteraccess.TwitterAccess(app_keys)

    def get_chapter_tweets(self, earliest_date):
        all_chapters = get_all_chapter_handles()
        for chapter in all_chapters:
            self.ta.paginate_user_timeline(chapter, earliest_date)

    # OC: Made untried and untested changes to accommodate modified paginate_followers
    # method (modified for use by get_followers_of_followers)
    def get_chapter_followers(self):
        all_chapters = get_all_chapter_handles()
        for chapter in all_chapters:
            w = wt.WriteTwitter('data/followers/' + chapter + '_followers.csv', '')
            self.ta.paginate_followers(chapter, False, False, w, '')
            w.close()

    def get_followers_of_followers(self):
        input_files = glob.glob(os.getcwd() + '/crawlLists/in_list_[0-9][0-9][0-9][0-9]')
        input_files.sort()
        date_string = datetime.date.today().strftime('%Y-%m-%d')
        for this_file in input_files:
            n_successful = 0
            n_failed = 0
            file_number = this_file[-3:]

            w = wt.WriteTwitter('data/followersOfFollowers/out_list_' + file_number + '.csv', '', date_string)

            with open(this_file, 'r') as file_reader:
                all_lines = file.read(file_reader).splitlines()
                for line in all_lines:
                    try:
                        success = self.ta.paginate_followers(line, True, True, w, file_number)
                    except:
                        success = False
                        w.write_to_errlog(file_number, line, 'UNKNOWN')

                    if success:
                        n_successful += 1
                    else:
                        n_failed += 1
            w.write_to_log(file_number, n_successful, n_failed)
            w.close()
            os.system('mv ' + this_file + ' ' + this_file + '_done')

    # this is broken, need to pass in full path instead of file name
    def get_hydrated_chapter_followers(self):
        all_chapters = get_all_chapter_handles()
        for chapter in all_chapters:
            self.__paginate_hydrated_users(chapter, True)

    def get_hydrated_users(self, lol_file):
        with open(lol_file, 'r') as lol_reader:
            in_lists = file.read(lol_reader).splitlines()

        in_lists.sort()
        for in_list in in_lists:
            file_name = 'crawlLists/' + in_list
            if os.path.isfile(file_name):
                self.__paginate_hydrated_users(file_name, False)

    def paginate_anon_users(self, anon_map):
        header = 'anon_id,created_at,description,lang,location,time_zone,utc_offset,statuses_count,favourites_count,followers_count,friends_count,listed_count,contributors_enabled,protected,verified'

        with open(anon_map, 'r') as id_file:
            all_ids = id_file.read().splitlines()

        n_ids = len(all_ids)

        map = dict()
        for row in all_ids:
            tokens = row.split(',')
            num_id = long(tokens[0])
            map[num_id] = int(tokens[1])

        int_all_ids = map.keys()
        new_counter = 0
        file_name = 'data/anon_users_hashtag_tweets.csv'
        w = wt.WriteTwitter(file_name, header, datetime.date.today().strftime('%Y-%m-%d'))

        while new_counter < n_ids:
            old_counter = new_counter
            new_counter = min(new_counter + 100, n_ids)
            user_ids = ','.join(str(x) for x in int_all_ids[old_counter:new_counter])

            success = False
            while not success:
                success = self.ta.get_hydrated_anon_users(user_ids, w, map)

        w.close()


    def __paginate_hydrated_users(self, in_list, has_header):
        file_number = in_list[-2:]

        header = 'user_id,name,screen_name,created_at,description,lang,location,url,time_zone,utc_offset,statuses_count,favourites_count,followers_count,friends_count,listed_count,contributors_enabled,protected,verified'
        with open(in_list, 'r') as id_file:
            if has_header:
                id_file.readline()
            all_ids = id_file.read().splitlines()

        n_ids = len(all_ids)
        new_counter = 0
        file_name = 'data/users/hydrated_out_list_' + file_number + '.csv'
        w = wt.WriteTwitter(file_name, header, datetime.date.today().strftime('%Y-%m-%d'))

        while new_counter < n_ids:
            old_counter = new_counter
            new_counter = min(new_counter + 100, n_ids)
            user_ids = ",".join(all_ids[old_counter:new_counter])

            success = False
            while not success:
                success = self.ta.get_hydrated_users(user_ids, w)

        w.close()
        os.system('mv ' + in_list + ' ' + in_list + '_done')

    # Hacky hack hack...
    def get_hashtag_tweets(self, hashtags):
        max_id = 581765689498797000
        # for i in range(0, 100):
        max_id = self.ta.paginate_search(max_id, hashtags)

    # Not finished implementing
    def get_retweeter_users(self, directory):
        for i in range(0, 100):
            self.ta.paginate_retweeters(2343)


def worker(i):
    apps_file = 'twitter_apps_consumer_key_' + str(i) + '.secret'
    r = Crawl(apps_file)
    r.get_hydrated_users('lol_' + str(i))


def main():
    earliest_date = time.strptime('2014-03-01', '%Y-%m-%d')
    hashtags = ['EarthHour', 'climatechange', 'yourpower', 'useyourpower']

    jobs = []

    with warnings.catch_warnings():
        warnings.simplefilter('once')
        # for i in range(0, 2):
        #     p = multiprocessing.Process(target=worker, args=(i,))
        #     jobs.append(p)
        #     p.start()

        r = Crawl('twitter_apps_consumer_key_0.secret')
        r.paginate_anon_users('data/hashtag_tweets_user_map.csv')

        # r.get_followers_of_followers()

        # r.get_chapter_tweets(earliest_date)
        # r.get_hashtag_tweets(hashtags)


        # r.get_hydrated_followers()
        # r.get_chapter_followers()

        # r.get_retweeter_users('asdf')



if __name__ == "__main__":
    main()