import constants
import standard_requester as sr
import numpy as np
import user_data as ud

class UserRequester(sr.StandardRequester):
    """A requester class to calculate Twitter user PII statistics

    ...

    Attributes
    ----------
    bearer_token : str
        The user's bearer token for authorization
    username_set : list[list[str]]
        All usernames to be included in the request

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

    def __init__(self, bearer_token, username_set):
        """
        Parameters
        ----------
        bearer_token : str
            The user's bearer token for authorization
        username_set : list[list[str]]
            All usernames to be included in the request
        """

        super().__init__(bearer_token)
        self.username_set = username_set

    def create_search_params(self, index = None, next_token = None):
        """Creates the parameters specific to request type.

        Parameters
        ----------
        index : int
            current index to parse in username_set
        next_token : str
            next page token for endpoint

        Returns
        -------
        dict
            all requested params specific to request type
        """

        return {
            "usernames" : ",".join(self.username_set[index]),
            "user.fields" : ",".join(constants.USER_FIELDS)
        }

    def create_url(self, index = None):
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

        return "https://api.twitter.com/2/users/by"

    def calculate_values(self):
        """Calculates the requested values for all users in user_set
        and returns a list of UserData objects.

        Returns
        -------
        list[UserData]
            list of UserData objects with requested statistics
        """

        raw_user_data = []
        for index in range(len(self.username_set)):
            raw_user_data = np.concatenate((self.connect_to_endpoint(index).get("data"), raw_user_data))
        user_data = [ud.UserData(user) for user in raw_user_data]

        return user_data

    def get_data_name(self):
        """Returns an identifier for the requester type.

        Returns
        -------
        str
            identifier for class
        """

        return "User"
