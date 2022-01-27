import user_data as ud
import json

class UserDataHandler():
    """A class to parse and jsonify UserData objects.

    ...

    Methods
    -------
    load_user_json(file_path)
        Adds a statistic set to the UserData
    get_statistic(statistic_type, statistic_name)
        Gets the specified statistic
    """

    def load_user_json(self, file_path):
        """Loads json into a list of UserData

        Parameters
        ----------
        file_path : str
            string file path
        
        Returns
        -------
        list[UserData]
            list of UserData with loaded data
        """

        user_list = json.load(file_path)
        user_data_list = []

        for user in user_list:
            current = ud.UserData()
            current.statistic_library = user
            user_data_list.append(current)
        
        return user_data_list 
            
    def write_users_to_file(self, user_list, file_path):
        """Writes UserData objects to file path

        Parameters
        ----------
        user_list : list[UserData]
            list of users statistics

        file_path : str
            string file path
        """

        with open(file_path, "w") as outfile:
            json.dump([user.statistic_library for user in user_list], outfile, indent = 4)
