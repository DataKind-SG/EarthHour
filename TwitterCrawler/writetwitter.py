import time
import sys
import json


class WriteTwitter:
    def __init__(self, filename, header, date_string):
        self.file = open(filename, 'w')
        if len(header) > 0:
            self.file.write("%(header)s\n" % locals())

        self.logfilename = 'logs/' + date_string + '-log.txt'
        self.errfilename = 'logs/' + date_string + '-errors.txt'

    def close(self):
        self.file.close()

    def write_to_log(self, filename, n_successful, n_failed):
        with open(self.logfilename, 'a') as log_writer:
            log_writer.write('%s,%s,%s,%s\n' % (filename, str(n_successful), str(n_failed), str(n_successful + n_failed)))

    def write_to_errlog(self, filename, user, status_code):
        with open(self.errfilename, 'a') as err_writer:
            err_writer.write('%s,%s,%s\n' % (filename, user, status_code))

    def write_tweets(self, r, earliest_date):

        is_last = False
        min_id = sys.maxsize

        for tweet in r.get_iterator():
            if 'text' in tweet:
                line = []
                line.append(tweet['user']['id_str'])
                line.append(tweet['id_str'])

                timestamp = time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                if timestamp < earliest_date:
                    is_last = True
                    break

                line.append(time.strftime('%Y-%m-%d %H:%M:%S', timestamp))
                line.append("\"%s\"" % (tweet['text'].replace("\n", "<br>")))
                if tweet['coordinates'] is not None:
                    line.append("%s;%s" % (str(tweet['coordinates']['coordinates'][0]), str(tweet['coordinates']['coordinates'][1])))
                else:
                    line.append('')
                line.append(tweet['lang'])
                line.append(str(tweet['retweet_count']))
                line.append(str(tweet['favorite_count']))
                if tweet['in_reply_to_status_id'] is not None:
                    line.append("%s,%s" % (str(tweet['in_reply_to_status_id']), str(tweet['in_reply_to_user_id'])))
                else:
                    line.append(',')
                if tweet['place'] is not None:
                    place = []
                    for coordinates in tweet['place']['bounding_box']['coordinates'][0]:
                        place.append("[%s;%s]" % (str(coordinates[0]), str(coordinates[1])))
                    line.append(";;".join(place))

                if tweet['id'] < min_id:
                    min_id = tweet['id']

                full_line = ",".join(line).encode('utf8')
                self.file.write("%s\n" % full_line)

        return min_id - 1, is_last

    def write_user_ids(self, r):
        data = json.loads(r.text)
        next_cursor = data['next_cursor']

        for id in data['ids']:
            self.file.write("%s\n" % id)

        return next_cursor

    def write_user_follower_ids(self, r, user):
        data = json.loads(r.text)
        next_cursor = data['next_cursor']

        for id in data['ids']:
            self.file.write("%s,%s\n" % (user, id))

        return next_cursor

    def write_line(self, line):
        self.file.write("%s\n" % line)

    def write_hydrated_users(self, r):
        for user in r.get_iterator():
            line = []
            line.append(user['id_str'])
            line.append("\"%s\"" % user['name'])
            line.append(user['screen_name'])

            created_at = time.strptime(user['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
            line.append(time.strftime('%Y-%m-%d %H:%M:%S', created_at))

            line.append("\"%s\"" % user['description'])
            line.append(user['lang'])
            line.append("\"%s\"" % user['location'])

            if user['profile_location'] is not None:
                print 'PROFILE_LOCATION!!!'

            if user['url'] is not None:
                line.append(user['url'])
            else:
                line.append('')

            line.append(str(user['time_zone']))
            line.append(str(user['utc_offset']))

            line.append(str(user["statuses_count"]))
            line.append(str(user["favourites_count"]))
            line.append(str(user["followers_count"]))
            line.append(str(user["friends_count"]))
            line.append(str(user["listed_count"]))

            if user["contributors_enabled"]:
                line.append("1")
            else:
                line.append("0")

            if user["protected"]:
                line.append("1")
            else:
                line.append("0")

            if user["verified"]:
                line.append("1")
            else:
                line.append("0")

            full_line = ",".join(line).encode('utf8')
            self.file.write("%s\n" % full_line)

