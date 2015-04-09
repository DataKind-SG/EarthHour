from TwitterAPI import TwitterAPI
import time
import writetwitter as wt
import math


class TwitterAccess:
    def __init__(self, apps_file):
        self.current_app_index = 0
        self.status = []
        self.app = []
        with open(apps_file, 'r') as apps_file_reader:
            all_lines = file.read(apps_file_reader).splitlines()

        for line in all_lines:
            tokens = line.split(',')
            self.app.append(TwitterAPI(tokens[0], tokens[1], auth_type='oAuth2'))
            self.status.append(dict())

        self.n_app = len(self.app)
        self.__query_rate_limit_status()

    # OC: This API endpoint isn't very stable. Wasn't working over the weekend but it is now.
    def __query_rate_limit_status(self):
        count = 0
        for app in self.app:
            request = app.request('application/rate_limit_status',
                                  {'resources': 'application,statuses,search,followers,users'})
            for item in request:
                self.status[count]['rate'] = item['resources']['application']['/application/rate_limit_status']['remaining']
                self.status[count]['retweeters'] = item['resources']['statuses']['/statuses/retweeters/ids']['remaining']
                self.status[count]['retweets'] = item['resources']['statuses']['/statuses/retweets/:id']['remaining']
                self.status[count]['timeline'] = item['resources']['statuses']['/statuses/user_timeline']['remaining']
                self.status[count]['search'] = item['resources']['search']['/search/tweets']['remaining']
                self.status[count]['users'] = item['resources']['users']['/users/lookup']['remaining']
                self.status[count]['followers'] = item['resources']['followers']['/followers/ids']['remaining']
                self.status[count]['app'] = item['rate_limit_context']['application']
            count += 1
        return self.status

    # OC: The call to __query_rate_limit_status doesn't always work as intended if the API isn't working. Make sure
    # your code can allow for it not to work.
    def __update_current_app(self, endpoint, count_needed):
        if self.status[self.current_app_index][endpoint] < count_needed:
            self.current_app_index += 1
            if self.current_app_index == self.n_app:
                self.current_app_index = 0

            while self.status[self.current_app_index][endpoint] < count_needed:
                print 'Going to sleep for 2 minutes... zzz...'
                time.sleep(60 * 2)
                self.__query_rate_limit_status()

    # OC: Made some untried and untested changes to this...
    def paginate_user_timeline(self, username, earliest_date):
        endpoint = 'timeline'
        self.__update_current_app(endpoint, 16)

        header = "user_id,tweet_id,created_at,text,coordinates,lang,retweet_count,favorite_count,in_reply_to_tweet_id,in_reply_to_user_id,place"
        w = wt.WriteTwitter('data/chapters/tweets/' + username + '_tweets.csv', header)

        args = {'screen_name': username,
                'count': 200,
                'trim_user': 't'}

        next_max_id = -999
        counter = 0
        is_last = False
        while not is_last:
            if counter > 0:
                args['max_id'] = next_max_id

            r = self.app[self.current_app_index].request('statuses/user_timeline', args)
            self.status[self.current_app_index][endpoint] = int(r.headers._store['x-rate-limit-remaining'][1])

            if r.status_code != 200:
                print 'WARNING: status not 200!!!'
                self.__update_current_app(endpoint, 16 - counter)
            else:
                next_max_id, is_last = w.write_tweets(r, earliest_date)

            counter += 1

            if self.status[self.current_app_index][endpoint] == 0:
                self.__update_current_app(endpoint, 1)

        w.close()

    # OC: Made some untried and untested changes to this...
    def paginate_search(self, max_id, hashtags):
        endpoint = 'search'
        self.__update_current_app(endpoint, 300)

        header = "user_id,tweet_id,created_at,text,coordinates,lang,retweet_count,favorite_count,in_reply_to_tweet_id,in_reply_to_user_id,place"
        w = wt.WriteTwitter('data/hashtags/' + str(max_id) + '_tweets.csv', header)

        html_hashtags = "%20OR%20%23".join(hashtags)
        html_hashtags = "%23" + html_hashtags
        args = {'q': html_hashtags,
                'count': 100,
                'max_id': max_id,
                'include_entities': 'false'}
        earliest_date = time.strptime('2000-01-01', '%Y-%m-%d')

        while self.status[self.current_app_index][endpoint] > 1:
            args['max_id'] = max_id

            r = self.app[self.current_app_index].request('search/tweets', args)
            self.status[self.current_app_index][endpoint] = int(r.headers._store['x-rate-limit-remaining'][1])

            if r.status_code != 200:
                print 'WARNING: status not 200!!!'
                self.__update_current_app(endpoint, 300)
            else:
                max_id, temp = w.write_tweets(r, earliest_date)

        w.close()
        return max_id

    # OC: not finished implementing
    def paginate_retweeters(self, tweet_id, retweet_count):
        self.__update_current_app('retweeters', math.ceil(retweet_count / 100))

        w = wt.WriteTwitter('data/retweets/' + str(max_id) + '_tweets.csv', header)

        next_cursor = -1
        args = {'id': tweet_id,
                'cursor': next_cursor,
                'stringify_ids': 'true'}

        while self.status[self.current_app_index]["retweeters"] > 0 and next_cursor != 0:
            # args['max_id'] = max_id

            # r = self.app[self.current_app_index].request('search/tweets', args)
            self.status[self.current_app_index]["retweeters"] -= 1

            if r.status_code != 200:
                print 'WARNING: status not 200!!!'

            else:
                next_cursor = w.write_retweeters(r)

        w.close()

    def paginate_followers(self, user, is_id, include_root, w, filename):
        endpoint = 'followers'
        self.__update_current_app(endpoint, 1)

        next_cursor = -1
        args = {'cursor': next_cursor,
                'stringify_ids': 'true',
                'count': 5000}
        if is_id:
            args['user_id'] = user
        else:
            args['screen_name'] = user

        while next_cursor != 0:
            args['cursor'] = next_cursor

            try:
                r = self.app[self.current_app_index].request('followers/ids', args)
            except:
                w.write_to_errlog(filename, user, 'TwitterRequestError')
                return False

            try:
                self.status[self.current_app_index][endpoint] = int(r.headers._store['x-rate-limit-remaining'][1])
            except:
                self.status[self.current_app_index][endpoint] -= 1

            if r.status_code != 200:
                w.write_to_errlog(filename, user, str(r.status_code))
                return False
            else:
                if include_root:
                    next_cursor = w.write_user_follower_ids(r, user)
                else:
                    next_cursor = w.write_user_ids(r)

            if self.status[self.current_app_index][endpoint] == 0:
                self.__update_current_app(endpoint, 1)

        return True

    def get_hydrated_users(self, user_ids, w):
        endpoint = 'users'
        self.__update_current_app(endpoint, 1)

        args = {'user_id': user_ids,
                'include_entities': 'true'}

        r = self.app[self.current_app_index].request('users/lookup', args)
        self.status[self.current_app_index][endpoint] = int(r.headers._store['x-rate-limit-remaining'][1])

        if r.status_code != 200:
            print 'WARNING: status not 200!!!'
            self.status[self.current_app_index][endpoint] = 0
            success = False
        else:
            w.write_hydrated_users(r)
            success = True

        return success