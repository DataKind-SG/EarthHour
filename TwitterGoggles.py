

#TODO: https://dev.twitter.com/docs/using-search add double quotes

#set language to english

# run cron jobs

# set result type to mixed - check duplication



# tid, entity_id (get this id from wikipedia), createtime, text, lat, lon, uid, screenname, name, profile_image_url, time when the tweet is crawled

# entity_id, entity_name, 



import argparse, collections, configparser, json, math, mysql.connector as sql, os, requests, sys, time

from datetime import datetime

from mysql.connector import errorcode

from requests import HTTPError

from requests import ConnectionError

from requests_oauthlib import OAuth1

import pprint

import urllib

import urlparse



def url_fix(s, charset='utf-8'):

    if isinstance(s, unicode):

        s = s.encode(charset, 'ignore')

    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)

    path = urllib.quote(path, '/%')

    qs = urllib.quote_plus(qs, '&=')

    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))



NUM_TWEETS_TOP_MAX = 10

# WEIGHTS_



# Print strings in verbose mode

def verbose(info) :

	try:

		if args.verbose:

			printUTF8(info)

	except UnicodeDecodeError:

		pass



def printUTF8(info) :

	print(info.encode('ascii', 'replace').decode())



# Connect to MySQL using config entries

def connect() :

	config = configparser.ConfigParser()

	script_dir = os.path.dirname(__file__)

	config_file = os.path.join(script_dir, 'config/settings.cfg')

	config.read(config_file)



	db_params = {

		'user'        : config["MySQL"]["user"],

		'password'    : config["MySQL"]["password"],

		'host'        : config["MySQL"]["host"],

		'port'        : int(config["MySQL"]["port"]),

		'database'    : config["MySQL"]['database'],

		'charset'     : 'utf8',

		'collation'   : 'utf8_general_ci',

		'use_unicode' : True,

		'buffered'    : True

	}



	return sql.connect(**db_params)



# Get all jobs from the database

def getJobs(conn) :

	cursor = conn.cursor() 



	query = ("SELECT job_id, zombie_head, state, query, since_id_str, description, book_id, page_id, start, end, last_tried, \
oauth.oauth_id, consumer_key, consumer_secret, access_token, access_token_secret \
FROM job, oauth \
WHERE job.state > 0 AND job.oauth_id = oauth.oauth_id AND zombie_head = %s \
ORDER BY last_tried")



	cursor.execute(query,[args.head])

	return cursor



# Append default values to the job's query string

def getFullQuery(query, since_id) :

	#Put the query in quotes so that the API searches for tweets containing the exact query phrase

	# query = '"' + query + '"'



	#query is unicode  query_arry is a list of string

	try:
		query_array = eval(query)
	except:
		return -1



	# print(query_array);

	query_string = '"'+query_array[0].decode('utf-8')+'"'

	max_index = None

	if len(query_array) >= 2:

		max_index = 2

	else:

		max_index = len(query_array)

	for i in range(1, max_index):

		query_string += ' OR '+ '"'+query_array[i].decode('utf-8')+'"'

	

	if (not query_string.startswith("q=")) :

		query_string = "q=" + query_string



	#returns unicode

	return "?" + query_string + "&since_id=" + since_id + "&count=100&lang=en"



# Query Twitter's Search 1.1 API

def search(query, oauth) :

	if query == -1:
		return -1

	verbose("Query: " + query)



	attempt = 1

	while attempt <= 3 :

		try :

			r = requests.get(url_fix("https://api.twitter.com/1.1/search/tweets.json" + query), auth=oauth)

			# print "https://api.twitter.com/1.1/search/tweets.json" + urllib.quote(query)

			# print r.text

			return json.loads(r.text)



		except (ConnectionError, HTTPError) as err :

			sleep_time = 2**(attempt - 1)

			verbose("Connection attempt " + str(attempt) + " failed. "

				"Sleeping for " + str(sleep_time) + " second(s).")

			time.sleep(sleep_time)

			attempt = attempt + 1



	print("***** Error: Unable to query Twitter. Terminating.")

	sys.exit(1)

def does_tweet_have_link_or_image(tweet):
	if 'entities' in tweet:

	return False


# Add a tweet to the DB

def addTweet(conn, job_id, tweet, job_query) :

	cursor = conn.cursor()

	prefix = "INSERT INTO tweets (tid, createtime, text, uid, screenname, name, profileurl, timestamp, job_id"

	suffix = ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s"

	lat = "NULL"

	lon = "NULL"

	pprint.pprint(tweet)

	if (tweet['coordinates']):

		lat = tweet["coordinates"]["coordinates"][1]

		lon = tweet["coordinates"]["coordinates"][0]

	values = [

		tweet["id"],

		datetime.strptime(tweet["created_at"], '%a %b %d %H:%M:%S +0000 %Y').strftime('%Y-%m-%d %H:%M:%S'),

		tweet["text"].encode('utf-8'),

		tweet["user"]["id"],

		tweet["user"]["screen_name"],

		tweet["user"]["name"],

		tweet["user"]["profile_image_url"],

		datetime.now().strftime('%Y-%m-%d %H:%M:%S'),

		job_id

	]

	# Optionally include the geo data

	if tweet['coordinates'] is not None and tweet['coordinates']['type'] == "Point" :		

		prefix = prefix + ", lat, lon"

		suffix = suffix + ", %s, %s"

		values.extend([

			lat,

			lon

		])



	suffix = suffix + ")"

	query = (prefix + suffix)

	

	try :

		cursor.execute(query, values)

		conn.commit()

		compareAndAddTweetToTopTweetTable(job_id, tweet, job_query, conn)

		return True

	except sql.IntegrityError:
		compareAndAddTweetToTopTweetTable(job_id, tweet, job_query, conn)
		return True
	except sql.Error as err :

		verbose("")

		verbose(">>>> Warning: Could not add Tweet: " + str(err))

		verbose("     Query: " + cursor.statement)

		return False

	finally :

		cursor.close()



def flatten_job_query_and_remove_duplicates(job_query):

	modified_job_query = []

	# print "job_query = ",  job_query

	# print "Length of job query is ", len(job_query)

	weighted_keywords_dict = {}

	weight_current = 0.5

	for i in range(0, len(job_query)):

		query_string = job_query[i].decode('utf-8')

		# print "query_string = ", query_string.encode('utf-8')

		for word in query_string.split(" "):

			if word not in modified_job_query:

				modified_job_query.append(word)

				weighted_keywords_dict[word] = weight_current

		weight_current = weight_current / 2

	# print "Flattened job query = ", modified_job_query

	return weighted_keywords_dict



def get_keyword_score(job_query, keywords):

	num_keywords_in_query = 0

	tweet_text_in_lower_case = job_query.lower()

	keywords_lower_case = {}

	for keyword in keywords:

		keywords_lower_case[keyword.lower()] = keywords[keyword]

	for keyword in keywords_lower_case:

		if keyword in tweet_text_in_lower_case:

			num_keywords_in_query = num_keywords_in_query + keywords_lower_case[keyword]

	return num_keywords_in_query



def compute_rank_of_tweet(tweet, job_query):

	len_tweet = len(tweet["text"])

	tweet_len_score = 0.3 * len_tweet / 140.0

	# print tweet["text"]

	# print len_tweet

	keywords = flatten_job_query_and_remove_duplicates(job_query)

	# print keywords

	# print tweet["text"]

	keyword_score = 0.7 * get_keyword_score(tweet["text"], keywords)

	# print keyword_score

	score = tweet_len_score + keyword_score

	return score



def get_tweet_with_lowest_rank_score(top_tweets):

	min_rank_score = 10

	tweet_with_lowest_rank_score = None

	for top_tweet in top_tweets:

		if top_tweet[1] < min_rank_score:

			min_rank_score = top_tweet[1]

			tweet_with_lowest_rank_score = top_tweet

	return top_tweet



def replace_a_top_tweet_if_needed(top_tweets, rank_score_new_tweet, new_tweet, job_id):

	cursor = conn.cursor()

	if len(top_tweets) < NUM_TWEETS_TOP_MAX:

		query = "INSERT INTO top_tweet (job_id, tid, rank_score, text) VALUES(%s, %s, %s, %s);"

		values = [job_id, new_tweet["id"], rank_score_new_tweet, new_tweet["text"].encode('utf-8')]

		cursor.execute(query, values)

		# print "Text: ", new_tweet["text"].encode('utf-8'), "Rank Score = ", rank_score_new_tweet

	else:

		top_tweet_with_lowest_rank_score = get_tweet_with_lowest_rank_score(top_tweets)

		rank_score_top_tweet = top_tweet_with_lowest_rank_score[1]

		if rank_score_top_tweet < rank_score_new_tweet:

			query = "UPDATE top_tweet SET tid = %s, rank_score = %s, text = %s WHERE tid=%s;"

			values = [new_tweet["id"], rank_score_new_tweet, new_tweet["text"].encode('utf-8'), top_tweet_with_lowest_rank_score[0]]

			cursor.execute(query, values)

			# print "Text: ", new_tweet["text"].encode('utf-8'), "Rank Score = ", rank_score_new_tweet

	conn.commit()

	cursor.close()



def compareAndAddTweetToTopTweetTable(job_id, new_tweet, job_query, conn):

	cursor_fetch = conn.cursor()

	rank_score_new_tweet = compute_rank_of_tweet(new_tweet, job_query)

	top_tweets = []

	try:

		cursor_fetch.execute("SELECT * FROM top_tweet WHERE job_id = %s", (job_id,))

		top_tweets=cursor_fetch.fetchall()

		replace_a_top_tweet_if_needed(top_tweets, rank_score_new_tweet, new_tweet, job_id)

	except sql.Error as err :

		verbose("")

		verbose(">>>> Warning: Could not fetch top tweet(s): " + str(err))

		verbose("     Query: " + cursor_fetch.statement)

	finally :

		cursor_fetch.close()

	cursor_fetch.close()



# Add hashtag entities to the DB

def addHashtags(conn, job_id, tweet) :

	cursor = conn.cursor()



	query = "INSERT INTO hashtag (tweet_id, job_id, text, index_start, index_end) VALUES(%s, %s, %s, %s, %s)"



	for hashtag in tweet['entities']['hashtags'] :

		values = [

			tweet["id_str"], 

			job_id, 

			hashtag["text"], 

			hashtag["indices"][0],

			hashtag["indices"][1] 

		]



		try :

			cursor.execute(query, values)

			conn.commit()

		except sql.Error as err :

			verbose("")

			verbose(">>>> Warning: Could not add Hashtag: " + str(err))

			verbose("     Query: " + cursor.statement)

	

	cursor.close()



# Add user mention entities to the DB

def addUserMentions(conn, job_id, tweet) :

	cursor = conn.cursor()



	query = "INSERT INTO mention (tweet_id, job_id, screen_name, name, id_str, index_start, index_end) VALUES(%s, %s, %s, %s, %s, %s, %s)"



	for mention in tweet['entities']['user_mentions'] :

		values = [

			tweet["id_str"], 

			job_id, 

			mention["screen_name"], 

			mention["name"], 

			mention["id_str"], 

			mention["indices"][0],

			mention["indices"][1] 

		]



		try :

			cursor.execute(query, values)

			conn.commit()

		except sql.Error as err :

			verbpse("")

			verbose(">>>> Warning: Could not add User Mention: " + str(err))

			verbose("     Query: " + cursor.statement)

	

	cursor.close



# Add all URL entities to the DB

def addURLS(conn, job_id, tweet) :

	cursor = conn.cursor()



	query = "INSERT INTO url (tweet_id, job_id, url, expanded_url, display_url, index_start, index_end) VALUES(%s, %s, %s, %s, %s, %s, %s)"



	for url in tweet['entities']['urls'] :

		values = [

			tweet["id_str"], 

			job_id, 

			url["url"], 

			expandURL(url["expanded_url"]) if "expanded_url" in url else "", 

			url["display_url"] if "display_url" in url else "", 

			url["indices"][0],

			url["indices"][1] 

		]



		try :

			cursor.execute(query, values)

			conn.commit()

		except sql.Error as err :

			verbose("")

			verbose(">>>> Warning: Could not add URL: " + str(err))

			verbose("     Query: " + cursor.statement)

	

	cursor.close()



def expandURL(url) :

	headers = {'User-agent': 'TwitterGoggles v1.0'}

	r = requests.get("http://api.longurl.org/v2/expand?format=json&url=" + url, headers = headers)	

	response = json.loads(r.text)



	if "long-url" in response :

		return response["long-url"]

	else :

		return url



# Update the stored job's since_id to prevent retrieving previously processed tweets

def updateSinceId(conn, job_id, max_id_str, total_results) :

	cursor = conn.cursor()



	query = "UPDATE job SET since_id_str=%s, last_count=%s, last_run=%s WHERE job_id=%s"



	values = [

		max_id_str,

		total_results,

		datetime.now().strftime('%Y-%m-%d %H:%M:%S'),

		job_id

	]



	try :

		cursor.execute(query, values)

		conn.commit()

	except sql.Error as err :

		verbose(">>>> Warning: Could not update job: " + str(err))

		verbose("     Query: " + cursor.statement)

	finally:

		cursor.close()



# Add an entry into the job history table

def addHistory(conn, job_id, oauth_id, success, total_results = 0) :

	cursor = conn.cursor()



	query = "INSERT INTO history (job_id, oauth_id, timestamp, status, total_results) VALUES(%s, %s, %s, %s, %s)"



	values = [

		job_id,

		oauth_id,

		datetime.now().strftime('%Y-%m-%d %H:%M:%S'),

		"success" if success else "failure",

		total_results

	]



	try :

		cursor.execute(query, values)

		conn.commit()

	except sql.Error as err :

		verbose(">>>> Warning: Could not add history entry: " + str(err))

		verbose("     Query: " + cursor.statement)

	finally:

		cursor.close()



# Main function

if __name__ == '__main__' :

	# Handle command line arguments

	parser = argparse.ArgumentParser(description="A Python adaptation of the PHP program Twitter Zombie\", originally developed for the Twitter Search API version 1.0. This new project is built for the Twitter Search API version 1.1.")

	parser.add_argument('head', type=int, help="Specify the head #")

	parser.add_argument('-v','--verbose', default=False, action="store_true", help="Show additional logs")

	parser.add_argument('-d','--delay', type=int, default=0, help="Delay execution by DELAY seconds")

	args = parser.parse_args()



	# Display startup info

	print("vvvvv Start:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

	verbose("Verbose Mode: Enabled")

	print("Head:", args.head)

	print("Delay:", args.delay)



	epoch_min = math.floor(time.time() / 60)

	verbose("Epoch Minutes: " + str(epoch_min))



	if (args.delay > 0) :

		time.sleep(args.delay)



	print("Connecting to database...")



	try :

		run_total_count = 0

		conn = connect()

		print("Connected")



		# Get all of the jobs for this head

		jobs = getJobs(conn)



		if not jobs.rowcount :

			print("\nUnable to find any jobs to run. Please make sure there are entries in the 'job'"

				+ " table that have an oauth_id corresponding to an entry in the 'oauth', the 'zombie_head'"

				+ " value matches {}, and the 'state' value is greater than 0.\n".format(args.head))



		for (job_id, zombie_head, state, query, since_id_str, description, book_id, page_id, start, end, last_tried, oauth_id, consumer_key, consumer_secret, access_token, access_token_secret) in jobs :

			conn.cursor().execute("UPDATE job SET last_tried=%s WHERE job_id=%s", (time.strftime('%Y-%m-%d %H:%M:%S'), job_id))

			conn.commit()

			print((job_id, zombie_head, state, query, since_id_str, description, book_id, page_id, start, end, last_tried, oauth_id, 

				consumer_key, consumer_secret, access_token, access_token_secret))



			# Throttle the job frequency

			if (epoch_min % state != 0) :

				verbose("Throttled frequency for job: " + str(job_id))

				continue

			

			printUTF8("+++++ Job ID:" + str(job_id) + "\tDescription:" + description + "\tQuery:" + query + "\tOAuth ID:" + str(oauth_id))



			oauth = OAuth1(client_key=consumer_key,

						client_secret=consumer_secret,

						resource_owner_key=access_token,

						resource_owner_secret=access_token_secret)



			since_id_str = since_id_str.decode('utf8')


			total_results = 0
			# print(getFullQuery(query, since_id_str).encode('utf-8'))

			# Get the Tweets

			try:
				if len(eval(query)) == 0:
					continue
			except SyntaxError:
				continue
			except TypeError:
				continue
			results = search(getFullQuery(query, since_id_str), oauth)
			if results == -1:
				continue



			# Make sure that we didn't receive an error instead of an actual result

			if "errors" in results :

				for error in results["errors"] :

					print(error)

					verbose("      Error response received: " + error["message"])



				print("***** Error: Unable to query Twitter. Ending job.")

				addHistory(conn, job_id, oauth_id, False)

				continue



			tweets = collections.deque()



			tweets.extend(results["statuses"])



			# Search results are returned in a most-recent first order, so we only need the inital max

			max_id_str =  results["search_metadata"]["max_id_str"]

			verbose("Max ID: " + str(max_id_str))

			count = 1

			total = len(tweets)

			while tweets :

				print "Max ID Str: ", max_id_str

				total_results = total_results + 1

				tweet = tweets.popleft()



				# Insert the tweet in the DB

				success = addTweet(conn, job_id, tweet, eval(query))



				# Show status logging

				if args.verbose :

					sys.stdout.write("\rProgress: " + str(count) + "/" + str(total))

				count = count + 1



				# Insert the tweet entities in the DB

				if success :

					addHashtags(conn, job_id, tweet)

					addUserMentions(conn, job_id, tweet)

					# addURLS(conn, job_id, tweet)



				# If we have no more tweets to process, but Twitter says there are more to get

				if not tweets and "next_results" in results["search_metadata"] :

					next_results = results["search_metadata"]["next_results"]

					query_new = next_results + "&since_id=" + since_id_str + "&count=100"

					

					verbose("\nFetching more results...")

					results = search(query_new, oauth)



					# Make sure that we didn't receive an error instead of an actual result

					if "errors" in results :

						for error in results["errors"] :

							verbose("      Error response received:" + error["message"])



						print("***** Error: Unable to query Twitter. Ending job.")



						# End this job early, since we've probably hit rate limits

						break



					# Add the newly retrieved tweets to the processing queue

					tweets.extend(results["statuses"])



					# Update logging

					total = len(tweets)

					count = 1



			verbose("")

			print("Total Results:", total_results)

			run_total_count = run_total_count + total_results



			# Update the since_id to use for future tweets

			updateSinceId(conn, job_id, max_id_str, total_results)

			addHistory(conn, job_id, oauth_id, True, total_results)

					

	except sql.Error as err :

		print(err)

		print("Terminating.")

		sys.exit(1)

	else :

		conn.close()

	finally :

		print("$$$$$ Run total count: " + str(run_total_count))

		print("^^^^^ Stop:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

