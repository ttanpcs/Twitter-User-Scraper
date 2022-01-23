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

        current_users = "usernames=" + ",".join(self.users_info_set[index])
        user_fields = "user.fields=" + ",".join(constants.USER_FIELDS)
        url = "https://api.twitter.com/2/users/by?{}&{}".format(current_users, user_fields)

        return url

    def calculate_values(self):
        """Calculates the requested values and returns a UserData object.

        Returns
        -------
        list[UserData]
            list of UserData object with requested statistics
        """            
        raw_user_data = []
        for index in range(len(self.users_info_set)):
            raw_user_data = np.concatenate((self.connect_to_endpoint(index).get("data"), raw_user_data))
        user_data = []
        for user in raw_user_data:
            processed_user = {}
            for key in constants.USER_FIELDS:
                if (constants.USER_SUB_FIELDS.get(key) is None):
                    processed_user[key] = user.get(key)
                else:
                    for subkey in constants.USER_SUB_FIELDS.get(key):
                        processed_user[subkey] = user.get(key).get(subkey)
            user_data.append(ud.UserData(processed_user))

        return user_data

    def get_data_name(self):
        """Returns an identifier for the requester type.

        Returns
        -------
        str
            identifier for class
        """

        return "user"
