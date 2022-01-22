from abc import ABC, abstractmethod
import requests

class StandardRequester(ABC):
    """An abstract base class for Requester classes that request to
    Twitter

    ...

    Attributes
    ----------
    bearer_token : str
        The user's bearer token for authorization
    users_info_set : list[list[str]]
        All users information to be included in the request

    Methods
    -------
    authorize_bearer_token()
        Creates the authorization search header with the bearer token
    connect_to_endpoint()
        Connects to the specified endpoint and returns the data as a json file
    create_search_params()
        Creates the parameters specific to request type
    create_url(index)
        Creates the specific Twitter url for request type
    calculate_values()
        Calculates the requested values and returns a UserData object
    get_data_name()
        Returns an identifier for the requester type
    """

    def __init__(self, bearer_token, users_info_set):
        """
        Parameters
        ----------
        bearer_token : str
            The user's bearer token for authorization
        users_info_set : list[object]
            All users information to be included in the request
        """
        
        self.bearer_token = bearer_token
        self.users_info_set = users_info_set

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

    def connect_to_endpoint(self, index):
        """Connects to the specified endpoint and returns the data as a json file.

        Parameters
        ----------
        index : int
            current index to parse in users_info_set

        Returns
        -------
        json
            json with all requested data
        """

        search_params = self.create_search_params()
        search_headers = self.authorize_bearer_token()
        url = self.create_url(index)
        response = requests.request("GET", url, headers = search_headers, params = search_params)
        if (response.status_code != 200):
            raise Exception(
                "Request failed: {} {}".format(
                    response.status_code, response.text
                )
            )

        return response.json()

    @abstractmethod
    def create_search_params(self):
        """Creates the parameters specific to request type.

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
            current index to parse in users_info_set

        Returns
        -------
        str
            url string for request type
        """

        return ""

    @abstractmethod
    def calculate_values(self):
        """Calculates the requested values and returns a UserData object.

        Returns
        -------
        UserData
            UserData object with requested statistics
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
