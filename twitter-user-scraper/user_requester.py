import standard_requester as sr

class UserRequester(sr.StandardRequester):
    """A requester class to calculate Twitter user PII statistics

    ...

    Attributes
    ----------
    bearer_token : str
        The user's bearer token for authorization
    usernames : list[str]
        All usernames to be included in the request

    Methods
    -------
    create_search_params()
        Creates the parameters specific to request type
    create_url(index)
        Creates the specific Twitter url for request type
    calculate_values()
        Calculates the requested values and returns a UserData object
    get_data_name()
        Returns an identifier for the requester type
    """

    def create_search_params(self):
        """Creates the parameters specific to request type.

        Returns
        -------
        dict
            all requested params specific to request type
        """

        return None

    def create_url(self, index):
        """Creates the specific Twitter url for request type.

        Parameters
        ----------
        index : int
            current index to parse in users_info_set

        Returns
        -------
        str
            url string for request type
        """

    def calculate_values(self):
        """Calculates the requested values and returns a UserData object.

        Returns
        -------
        UserData
            UserData object with requested statistics
        """

        return {}

    def get_data_name(self):
        """Returns an identifier for the requester type.

        Returns
        -------
        str
            identifier for class
        """

        return "user"
