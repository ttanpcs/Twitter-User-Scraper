from abc import ABC, abstractmethod
import constants
import requests
import user_data as ud

class StandardRequester(ABC):
    """An abstract base class for Requester classes that request to
    Twitter

    ...

    Attributes
    ----------
    bearer_token : str
        The user's bearer token for authorization
    user_set : list[UserData]
        All users information to be included in the request

    Methods
    -------
    authorize_bearer_token()
        Creates the authorization search header with the bearer token
    connect_to_endpoint(index, next_token)
        Connects to the specified endpoint and returns the data as a json object
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

    def __init__(self, bearer_token, user_set = None):
        """
        Parameters
        ----------
        bearer_token : str
            The user's bearer token for authorization
        user_set : list[UserData]
            All users information to be included in the request
        """
        
        self.bearer_token = bearer_token
        self.user_set = user_set

    def authorize_bearer_token(self):
        """Creates the authorization search header with the bearer token.

        Returns
        -------
        dict
            bearer token authorization header
        """

        search_headers = {
            "Authorization": "Bearer {}".format(self.bearer_token)
        }

        return search_headers

    def connect_to_endpoint(self, index, next_token = None):
        """Connects to the specified endpoint and returns the data as a json object.

        Parameters
        ----------
        index : int
            current index to parse in user_set
        next_token : str
            next page token for endpoint

        Returns
        -------
        json
            json with all requested data
        """

        search_params = self.create_search_params(index, next_token)
        search_headers = self.authorize_bearer_token()
        url = self.create_url(index)
        response = requests.request("GET", url, headers = search_headers, params = search_params)
        if (response.status_code != constants.SUCCESS):
            raise Exception(
                "Request failed: {} {}".format(
                    response.status_code, response.text
                )
            )

        return response.json()

    @abstractmethod
    def create_search_params(self, index = None, next_token = None):
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

        return {}

    @abstractmethod
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

        return ""

    @abstractmethod
    def calculate_values(self):
        """Calculates the requested values for all users in user_set
        and returns a list of UserData objects.

        Returns
        -------
        list[UserData]
            list of UserData objects with requested statistics
        """

        return {}

    @abstractmethod
    def get_data_name(self):
        """Returns an identifier for the requester type.

        Returns
        -------
        str
            identifier for class
        """

        return "standard"
