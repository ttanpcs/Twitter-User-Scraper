import constants
import standard_requester as sr
import numpy as np
import user_data as ud

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

    def calculate_values(self):
        """Calculates the requested values for all users in user_set
        and returns a list of UserData objects.

        Returns
        -------
        list[UserData]
            list of UserData objects with requested statistics
        """

        pass

    def get_data_name(self):
        """Returns an identifier for the requester type.

        Returns
        -------
        str
            identifier for class
        """

        return "TweetTimeline"
