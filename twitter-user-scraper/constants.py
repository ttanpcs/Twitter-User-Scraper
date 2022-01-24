USER_FIELDS = {
    "name" : None,
    "username" : None,
    "id" : None,
    "created_at" : None,
    "description" : None,
    "public_metrics" : [
        "followers_count",
        "following_count",
        "tweet_count",
        "listed_count"
    ],
    "location" : None
}

MAX_FOLLOWERS = 1000

FOLLOWS_FIELDS = {
    "user.fields" : "id",
    "max_results" : "1000"
}

TWEET_FIELDS = {
    "id" : None,
    "text" : None,
    "public_metrics" : None,
    "created_at" : None,
    "entities.hashtags.tag" : None,
    "entities.cashtags.tag" : None,
    "referenced_tweets" : None
}

SUCCESS = 200