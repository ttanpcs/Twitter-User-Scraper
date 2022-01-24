USER_FIELDS = [
    "name",
    "username",
    "id",
    "created_at",
    "description",
    "public_metrics",
    "location"
]

MAX_FOLLOWERS = 1000

FOLLOWS_FIELDS = {
    "user.fields" : "id",
    "max_results" : "1000"
}

TWEET_FIELDS = {
    "id",
    "text",
    "public_metrics",
    "created_at",
    "entities.hashtags.tag",
    "entities.cashtags.tag",
    "referenced_tweets"
}

SUCCESS = 200