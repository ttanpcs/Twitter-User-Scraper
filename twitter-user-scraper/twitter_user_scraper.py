import math
import numpy as np
import constants
import followers_requester as fr
import timeline_requester as tr
import user_requester as ur

class TwitterUserScraper():
    """A wrapper class to scrape Twitter data with given input parameters.

    ...

    Attributes
    ----------
    bearer_token : str
        The user's bearer token for authorization
    username_set : list[str]
        All usernames to be included in the request
    followers : bool
        Whether to include FollowersRequester
    timeline : bool
        Whether to include TimelineRequester

    Methods
    -------
    parse()
        Parses username_list to return list of UserData objects
    """

    def __init__(self, bearer_token, username_list, followers = True, timeline = True):
        """
        Parameters
        ----------
        bearer_token : str
            The user's bearer token for authorization
        username_set : list[str]
            All usernames to be included in the request
        followers : bool
            Whether to include FollowersRequester
        timeline : bool
            Whether to include TimelineRequester
        """

        self.bearer_token = bearer_token
        num_splits = math.ceil(float(len(username_list)) / constants.MAX_USERNAMES_PER_QUERY)
        self.username_list = []
        for i in range(num_splits):
            self.username_list.append(username_list[ i * constants.MAX_USERNAMES_PER_QUERY : (i + 1) * constants.MAX_USERNAMES_PER_QUERY])
        self.followers = followers
        self.timeline = timeline
    
    def parse(self):
        """Parses username_list to return list of UserData objects.

        Returns
        -------
        list[UserData]
            list of UserData objects with requested statistics
        """

        user_requester = ur.UserRequester(self.bearer_token, self.username_list)
        user_list = user_requester.calculate_values()
        
        if (self.followers):
            followers_requester = fr.FollowersRequester(self.bearer_token, user_list)
            followers_requester.calculate_values()
        if (self.timeline):
            timeline_requester = tr.TimelineRequester(self.bearer_token, user_list)
            timeline_requester.calculate_values()
        
        return user_list

