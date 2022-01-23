USER_FIELDS = [
    "name",
    "username",
    "id",
    "created_at",
    "description",
    "public_metrics",
    "location"
]

USER_SUB_FIELDS = {
    "public_metrics" : [
        "followers_count",
        "following_count",
        "tweet_count",
        "listed_count"
    ]
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