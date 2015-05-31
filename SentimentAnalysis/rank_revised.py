import pandas as pd
import matplotlib.pyplot as plt
import vaderSentiment
from vaderSentiment.vaderSentiment import sentiment as va
scores = list()
ranks = list()
# tweets_df = pd.read_csv('./DKSG-EarthHour/tweets/test1.csv')
# tweets_df = pd.read_csv('hashtag_tweets - nocomma - checked_remap.csv')
tweets_df = pd.read_csv('EH Chapter tweets.csv')

for tweet in tweets_df['text']:
        vs = va(tweet)
        score = vs.__getitem__("compound")
        if score <= -0.56:
            score1 = 'very neg'
        else:
            if score > -0.56 and score <= -0.11:
                score1 = 'neg'
            else:
                if score > -0.11 and score <= 0.09:
                    score1 = 'neu'
                else:
                    if score > 0.09 and score <= 0.54:
                         score1 = 'pos'
                    else:
                         score1 = 'very pos'
        scores.append(str(score))
        ranks.append(str(score1))

score_df = pd.DataFrame(scores)
rank_df  = pd.DataFrame(ranks)
tweets_df['compound'] = score_df
tweets_df['rank'] = rank_df
tweets_df['cnt'] = 1
# tweets_df.to_csv('EH_tweet_rank_20150523.csv')
tweets_df.to_csv('Chapter_tweet_rank_20150523.csv')