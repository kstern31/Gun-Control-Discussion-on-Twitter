import numpy as np
from datetime import datetime
from datetime import timedelta
from pymongo import MongoClient

import sys
if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

events = ["#parkland", "#texaschurch", "#lasvegas", "#orlando", "#sanbernardino", "#navyyard", "#sandyhook", "#aurora"]
dates = ["2018-02-14", "2017-11-05", "2017-10-01", "2016-06-12" ,"2015-12-02", "2013-09-16", "2012-12-14", "2012-07-20"]

def getTweets(event):
    hashtags = ["#guncontrol", "#guncontrolnow", "#gunreform", "#gunreformnow", "#gunsense", "#gunrights", "#2a", "#nra"]
    index = events.index(event)
    hashtags.append("%s gun" % event)
    date = dates[index]
    ##get day of event, as well as 6 days afterward
    format_date = datetime.strptime(date, "%Y-%m-%d")
    week = []
    week.append(date)
    for day in range(1,7):
        date = format_date+timedelta(days=day)
        week.append(date.strftime("%Y-%m-%d"))
    ###get tweets with each combination of date/hashtag
    tweetList = []
    for hashtag in hashtags:
        for day in week:
            startdate = day
            enddate = (datetime.strptime(day, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(hashtag).setSince(startdate).setUntil(enddate).setMaxTweets(1500)
            tweets = got.manager.TweetManager.getTweets(tweetCriteria)
            for tweet in tweets:
                t = {}
                t['username'] = tweet.username
                t['retweets'] = tweet.retweets
                t['text'] = tweet.text
                t['date'] = tweet.date
                t['favorites'] = tweet.favorites
                t['ID'] = tweet.id
                t['event'] = event.strip("#")
                tweetList.append(t)
    return tweetList

tweets = getTweets("#aurora")

client = MongoClient()

db = client.gunControl
col = db.tweets

col.insert_many(tweets)
