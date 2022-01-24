import constants
import standard_requester as sr
import numpy as np
import user_data as ud

class FollowsRequester(sr.StandardRequester):
    """A requester class to calculate Twitter user follows statistics

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
        if (next_token is not None):
            current_params = constants.FOLLOWS_FIELDS
            current_params["pagination_token"] = next_token
            return current_params

        return constants.FOLLOWS_FIELDS

    def create_url(self, index):
        """Creates the specific Twitter url for request type.

        Parameters
        ----------
        index : int
            current index to parse in username_set

        Returns
        -------
        str
            url string for request type
        """

        return "https://api.twitter.com/2/users/{}/followers".format(self.user_set[index].get_statistic("user", "id"))

    def calculate_values(self):
        """Calculates the requested values for all users in user_set
        and returns a list of UserData objects.

        Returns
        -------
        list[UserData]
            list of UserData object with requested statistics
        """
        
        for i in range(len(self.user_set)):
            current_number = 0
            current = self.connect_to_endpoint(i)
            current_number += current.get("meta").get("result_count")
            next_token = current.get("meta").get("next_token")
            followers = current["data"]

            while (next_token is not None and current_number < constants.MAX_FOLLOWERS):
                current = self.connect_to_endpoint(i, next_token)
                current_number += current.get("meta").get("result_count")
                next_token = current.get("meta").get("next_token")
                followers = np.concatenate((current["data"], followers))

            self.user_set[i].add_statistic_set(followers, self.get_data_name())

        return self.user_set

    def get_data_name(self):
        """Returns an identifier for the requester type.

        Returns
        -------
        str
            identifier for class
        """

        return "follows"
