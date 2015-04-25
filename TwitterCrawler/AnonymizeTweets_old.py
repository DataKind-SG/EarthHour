import csv
import glob
import numpy as np

class AnonymizeTweets:
    def __init__(self):
        self.map_file = 'data/final/map/test_map.csv'
        self.hashtag_dir = 'data/hashtags/*_tweets.csv'
        self.chapter_dir = 'data/chapters/tweets/*_tweets.csv'
        self.hashtag_tweet_file = 'data/final/hashtag_tweets.csv'
        self.chapters_tweet_file = 'data/final/chapters_tweets.csv'
        self.log_file = 'data/final/tweet_log.csv'
        self.new_map_file = 'data/final/map/tweet_map.csv'

        self.map = dict()
        self.__read_map()
        self.rand = np.random.permutation(range(70000000, 80000000))
        self.counter = 0
        self.tweet_header = 'anon_id,created_at,text,coordinates,lang,retweet_count,favorite_count,is_reply,in_reply_to_user_id,place\n'

    def __read_map(self):
        with open(self.map_file, 'r') as map_reader:
            map_reader.readline()
            csv_map = csv.reader(map_reader)
            for row in csv_map:
                self.map[long(row[0])] = int(row[1])

    def __get_anon_value(self, user_id):
        num_id = long(user_id)
        if num_id not in self.map:
            self.map[num_id] = self.rand[self.counter]
            self.counter += 1
            did_exist = False
        else:
            did_exist = True
        return str(self.map[num_id]), did_exist

    def anon_hashtag_tweets(self):
        tweet_files = glob.glob(self.hashtag_dir)
        tweet_files.sort()

        log_writer = open(self.log_file, 'w')
        log_writer.write('file,line count,self.counter\n')
        tweet_writer = open(self.hashtag_tweet_file, 'w')
        tweet_writer.write(self.tweet_header)

        for tweet_file in tweet_files:
            with open(tweet_file, 'r') as tweet_reader:
                tweet_reader.readline()
                csv_reader = csv.reader(x.replace('\0', '\n') for x in tweet_reader)
                line_count = 0

                for row in csv_reader:
                    line_count += self.__process_tweet_row(row, tweet_writer)

            log_writer = open(self.log_file, 'a')
            log_writer.write('%s,%s,%s\n' % (tweet_file, str(line_count), str(self.counter)))
            log_writer.close()

            print 'Finished ' + tweet_file

        tweet_writer.close()
        print 'Finished anon_hashtag_tweets'

    def anon_chapter_tweets(self):
        tweet_files = glob.glob(self.chapter_dir)
        tweet_files.sort()

        tweet_writer = open(self.chapters_tweet_file, 'w')
        tweet_writer.write(self.tweet_header)

        for tweet_file in tweet_files:
            with open(tweet_file, 'r') as tweet_reader:
                tweet_reader.readline()
                csv_reader = csv.reader(x.replace('\0', '\n') for x in tweet_reader)
                line_count = 0

                for row in csv_reader:
                    line_count += self.__process_tweet_row(row, tweet_writer)

            log_writer = open(self.log_file, 'a')
            log_writer.write('%s,%s,%s\n' % (tweet_file, str(line_count), str(self.counter)))
            log_writer.close()

            print 'Finished ' + tweet_file

        tweet_writer.close()
        print 'Finished anon_hashtag_tweets'

    def __process_tweet_row(self, row, tweet_writer):
        anon_id, did_exist = self.__get_anon_value(row[0])
        if not did_exist:
            map_writer = open(self.new_map_file, 'a')
            map_writer.write('%s,%s\n' % (row[0], str(anon_id)))
            map_writer.close()

        if len(row) >= 10:
            row[9] = ''
            if len(row[9]) != 0:
                in_reply_to_anon_id, did_exist = self.__get_anon_value(row[9])
                row[9] = in_reply_to_anon_id
                if not did_exist:
                    map_writer = open(self.new_map_file, 'a')
                    map_writer.write('%s,%s\n' % (row[0], str(anon_id)))
                    map_writer.close()

        line = '%s,%s,"%s",%s\n' % (anon_id, row[2], row[3], ','.join(row[4:]))
        tweet_writer.write(line)
        return 1


def main():
    at = AnonymizeTweets()
    at.anon_hashtag_tweets()
    at.anon_chapter_tweets()

if __name__ == '__main__':
    main()


