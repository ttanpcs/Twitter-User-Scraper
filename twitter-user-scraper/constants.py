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

FOLLOWERS_FIELDS = {
    "user.fields" : "id",
    "max_results" : "1000"
}

TWEET_FIELDS = {
    "id",
    "text",
    "public_metrics",
    "created_at",
    "entities",
    "referenced_tweets"
}

MAX_TWEETS = 3200

MAX_USERNAMES_PER_QUERY = 100

TWEET_MAX_RESULTS = 100

NUMBER_TAGS_SAVED = 3

NUMBER_TWEETS_SAVED = 5

SUCCESS = 200