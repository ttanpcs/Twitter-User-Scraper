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
    create_search_params()
        Creates the parameters specific to request type
    create_url(index)
        Creates the specific Twitter url for request type
    calculate_values()
        Calculates the requested values for all users in user_set
        and returns a list of UserData objects
    get_data_name()
        Returns an identifier for the requester type
    """

    def create_search_params(self, index):
        """Creates the parameters specific to request type.

        Parameters
        ----------
        index : int
            current index to parse in user_set

        Returns
        -------
        dict
            all requested params specific to request type
        """

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
        
        pass

    def get_data_name(self):
        """Returns an identifier for the requester type.

        Returns
        -------
        str
            identifier for class
        """

        return "follows"
