import constants
import standard_requester as sr
import numpy as np
import heapq

class TimelineRequester(sr.StandardRequester):
    """A requester class to calculate Twitter user statistics
    from a user's tweet timeline

    ...

    Attributes
    ----------
    bearer_token : str
        The user's bearer token for authorization
    user_set : list[UserData]
        All users information to be included in the request

    Methods
    -------
    create_search_params(index, next_token)
        Creates the parameters specific to request type
    create_url(index)
        Creates the specific Twitter url for request type
    request_tweets(index)
        Requests the last 3200 for a user.
    is_retweet(tweet)
        Determines if a tweet is a retweet
    fill_statistic_heap(heap, statistic)
        Fills heap with current statistic tuple
    count_tags(tag_dict, tweet, type)
        Fills tag dictionary with counts of each tag
    fill_statistics_tuple(statistics_tuple, current_tweets)
        Analyzes current_tweets to fill tuple
    calculate_values()
        Calculates the requested values for all users in user_set
        and returns a list of UserData objects
    get_data_name()
        Returns an identifier for the requester type
    """

    def create_search_params(self, index, next_token = None):
        """Creates the parameters specific to request type.

        Parameters
        ----------
        index : int
            current index to parse in user_set
        next_token : str
            next page token for endpoint

        Returns
        -------
        dict
            all requested params specific to request type
        """

        current_params = {
            "tweet.fields" : ",".join(constants.TWEET_FIELDS),
            "max_results" : constants.TWEET_MAX_RESULTS
        }
        if (next_token is not None):
            current_params["pagination_token"] = next_token

        return current_params

    def create_url(self, index):
        """Creates the specific Twitter url for request type.

        Parameters
        ----------
        index : int
            current index to parse in user_set

        Returns
        -------
        str
            url string for request type
        """

        return "https://api.twitter.com/2/users/{}/tweets".format(self.user_set[index].get_statistic("User", "id"))

    def request_tweets(self, index):
        """Requests the last 3200 tweets for a given user and 
        returns them as a list of Tweet objects.

        Parameters
        ----------
        index : int
            current index to parse in username_set

        Returns
        -------
        list[Tweets]
            list of Tweet objects with requested statistics
        """
        current_number = 0
        current = self.connect_to_endpoint(index)
        current_number += current.get("meta").get("result_count")
        next_token = current.get("meta").get("next_token")
        tweets = current["data"]

        while (next_token is not None):
            print(str(current_number))
            print(next_token)
            current = self.connect_to_endpoint(index, next_token)
            current_number += current.get("meta").get("result_count")
            next_token = current.get("meta").get("next_token")
            tweets = np.concatenate((current["data"], tweets))

        return tweets

    def is_retweet(self, tweet):
        """Determines if a tweet is a retweet.

        Parameters
        ----------
        tweet : Tweet
            tweet in subject

        Returns
        -------
        bool
            whether tweet is a retweet
        """
        if (tweet.get("referenced_tweets") is not None):
            for referenced_tweet in tweet.get("referenced_tweets"):
                if (referenced_tweet.get("type") == "retweeted"):
                    return True

        return False

    def fill_statistic_heap(self, heap, statistic):
        """Fills heap with current statistic tuple.

        Parameters
        ----------
        heap : list[(int, int)]
            current heap
        statistic : (int, int)
            comparison number and index tuple

        """

        if (len(heap) < constants.NUMBER_TWEETS_SAVED):
            heapq.heappush(heap, statistic)
        else:
            heapq.heappushpop(heap, statistic)
    
    def count_tags(self, tag_dict, tweet, type):
        """Fills tag dicitionary with counts of each tag.

        Parameters
        ----------
        tag_dict : dict
            dictionary to fill
        tweet : Tweet
            tweet to parase tags from
        type : str
            type of tag to parse
        """

        if (tweet.get("entities") is not None and tweet.get("entities").get(type) is not None):
            for tag in tweet.get("entities").get(type):
                if (tag_dict.get(tag["tag"]) is None):
                    tag_dict[tag["tag"]] = 1
                else:
                    tag_dict[tag["tag"]] += 1

    def fill_statistics_tuple(self, statistics_tuple, current_tweets):
        """Fills statistic tuple with current tweet statistics.

        Parameters
        ----------
        statistic_tuple : dict
            dictionary of processed statistics
        current_tweets : list[Tweet]
            all current users tweets (up to 3200)
        """

        hashtag_dict = {}
        cashtag_dict = {}

        for tweet_index in range(len(current_tweets)):
            self.count_tags(hashtag_dict, current_tweets[tweet_index], "hashtags")
            self.count_tags(cashtag_dict, current_tweets[tweet_index], "cashtags")
            retweeted_num_tuple = (current_tweets[tweet_index].get("public_metrics").get("retweet_count"), tweet_index)
            liked_num_tuple = (current_tweets[tweet_index].get("public_metrics").get("like_count"), tweet_index)
            self.fill_statistic_heap(statistics_tuple["most_retweeted_tweets"], (retweeted_num_tuple, tweet_index))
            self.fill_statistic_heap(statistics_tuple["most_liked_tweets"], (liked_num_tuple, tweet_index))
            if (self.is_retweet(current_tweets[tweet_index])):
                self.fill_statistic_heap(statistics_tuple["most_retweeted_retweets"], (retweeted_num_tuple, tweet_index))
                self.fill_statistic_heap(statistics_tuple["most_liked_retweets"], (liked_num_tuple, tweet_index))
        
        statistics_tuple["hashtags"] = heapq.nlargest(constants.NUMBER_TAGS_SAVED, [(hashtag_dict[key], key) for key in hashtag_dict])
        statistics_tuple["cashtags"] = heapq.nlargest(constants.NUMBER_TAGS_SAVED, [(cashtag_dict[key], key) for key in cashtag_dict])

    def calculate_values(self):
        """Calculates the requested values for all users in user_set
        and returns a list of UserData objects.

        Returns
        -------
        list[UserData]
            list of UserData objects with requested statistics
        """

        for user_index in range(len(self.user_set)):
            current_tweets = self.request_tweets(user_index)
            statistics_tuple = {
                "most_retweeted_tweets" : [],
                "most_liked_tweets" : [],
                "most_retweeted_retweets" : [],
                "most_liked_retweets" : [],
                "hashtags" : {},
                "cashtags" : {}
            }
            statistics = {}
            self.fill_statistics_tuple(statistics_tuple, current_tweets)
            
            for statistic in statistics_tuple:
                if (statistic == "hashtags" or statistic == "cashtags"):
                    statistics[statistic] = statistics_tuple[statistic]
                else:
                    statistics[statistic] = [current_tweets[index] for n, index in statistics_tuple[statistic]]
            self.user_set[user_index].add_statistic_set(statistics, self.get_data_name())

        return self.user_set

    def get_data_name(self):
        """Returns an identifier for the requester type.

        Returns
        -------
        str
            identifier for class
        """

        return "TweetTimeline"
