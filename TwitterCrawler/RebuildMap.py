import csv
import glob
import itertools


class AnonymizeTweets:
    def __init__(self):
        self.hashtag_dir = 'data/hashtags/*_tweets.csv'
        self.anon_hashtag_tweet_file = 'data/hashtag_tweets.csv'
        self.log_file = 'data/hashtag_tweets_user_log.csv'
        self.new_map_file = 'data/hashtag_tweets_user_map.csv'

        self.map = dict()
        self.written_users = set()
        self.counter = 0

    def gen_user_map_from_hashtag_tweets(self):
        tweet_files = glob.glob(self.hashtag_dir)
        tweet_files.sort()

        log_writer = open(self.log_file, 'w')
        log_writer.write('file,line count,user count\n')
        log_writer.close()

        user_writer = open(self.new_map_file, 'w')
        user_writer.write('user_id,anon_id\n')

        with open(self.anon_hashtag_tweet_file, 'r') as anon_tweet_reader:
            anon_tweet_reader.readline()
            anon_csv_tweet_reader = csv.reader(anon_tweet_reader)
            for tweet_file in tweet_files:
                with open(tweet_file, 'r') as tweet_reader:
                    tweet_reader.readline()
                    csv_reader = csv.reader(x.replace('\0', '\n') for x in tweet_reader)
                    user_count = 0
                    line_count = 0

                    while 1 == 1:
                        slice = itertools.islice(csv_reader, 0, 1)
                        anon_slice = itertools.islice(anon_csv_tweet_reader, 0, 1)
                        for anon_row in anon_slice:
                            if '\n' in anon_row[2]:

                        for row in slice:

                            if anon_row
                            user_count += self.__process_tweet(row, anon_row, user_writer)
                        line_count += 1

                log_writer = open(self.log_file, 'a')
                log_writer.write('%s,%s,%s\n' % (tweet_file, str(line_count), str(user_count)))
                log_writer.close()

                print 'Finished ' + tweet_file

        user_writer.close()
        print 'Finished user_hashtag_tweets'

    def __process_tweet(self, row, anon_row, user_writer):

        if '#ActOnClimate' in anon_row[2]:
            print anon_row
        # check they are same row
        if row[2] != anon_row[1] or row[3] not in anon_row[2]:
            raise NameError('shit')

        users_added = 0

        # find retweet column
        for i in range(6, 20):
            try:
                a = int(row[i])
                retweet_count_col = i
                break
            except:
                continue

        # find retweet column
        for i in range(5, 20):
            try:
                a = int(anon_row[i])
                anon_retweet_count_col = i
                break
            except:
                continue

        users_added += self.__try_add(row[0], anon_row[0], user_writer)

        in_reply_to_user_id_col = retweet_count_col + 3
        in_reply_to_anon_user_id_col = anon_retweet_count_col + 3
        if len(row) >= in_reply_to_user_id_col + 1:
            if len(row[in_reply_to_user_id_col]) != 0:
                users_added += self.__try_add(row[in_reply_to_user_id_col], anon_row[in_reply_to_anon_user_id_col], user_writer)

        return users_added

    def __try_add(self, user_id, anon_id, user_writer):
        int_user_id = int(user_id)
        if int_user_id not in self.written_users:
            self.written_users.add(int_user_id)
            user_writer.write('%s,%s\n' % (user_id, anon_id))
            return 1
        else:
            return 0

def main():
    at = AnonymizeTweets()
    at.gen_user_map_from_hashtag_tweets()

if __name__ == '__main__':
    main()


