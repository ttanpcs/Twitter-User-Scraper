class UserData():
    """A class to store Twitter statistics.

    ...

    Attributes
    ----------
    statistic_library : dict
        All statistic sets included in current user's data

    Methods
    -------
    add_statistic_set(statistic_set, name)
        Adds a statistic set to the UserData
    get_statistic_set(statistic_type)
        Gets the specified statistic set
    get_statistic(statistic_type, statistic_name)
        Gets the specified statistic
    """

    def __init__(self, statistic_set = None, name = "User"):
        """
        Parameters
        ----------
        statistic_set : dict
            The statistic set from the corresponding requester
        name : str
            Name of corresponding requester
        """

        self.statistic_library = {}
        if (statistic_set is not None):
            self.statistic_library[name] = statistic_set

    def add_statistic_set(self, statistic_set, name):
        """ Adds a statistic set to the data set.

        Parameters
        ----------
        statistic_set : dict
            The statistic set from the corresponding requester
        name : str
            Name of corresponding requester
        """

        self.statistic_library[name] = statistic_set

    def get_statistic_set(self, name):
        """Gets the specified statistic set.

        Parameters
        ----------
        name : str
            Name of corresponding requester
        
        Returns
        -------
        dict
            corresponding statistic set
        """

        return self.statistic_library.get(name)

    def get_statistic(self, statistic_type, statistic_name):
        """Gets the specified statistic.

        Parameters
        ----------
        statistic_set : dict
            The statistic set from the corresponding requester
        name : str
            Name of corresponding requester
        
        Returns
        -------
        dict
            corresponding statistic
        """

        return self.statistic_library.get(statistic_type).get(statistic_name)
