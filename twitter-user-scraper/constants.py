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

TWEET_FIELDS = [
    "id",
    "text",
    "public_metrics",
    "created_at",
    "entities.hashtags.tag",
    "entities.cashtags.tag",
    "referenced_tweets"
]

SUCCESS = 200