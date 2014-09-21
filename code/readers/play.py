#!/usr/bin/env python3


class Play:
    def __init__(self, play_json):
        """ Allows easy access to information contained in a play object.

        args:
            play_json: A play json object.
        """
        self.json = play_json
        # Set up the scoring information
        self.__set_scoring()
        # Get the play number
        self.number = self.json.get("number")

    # Set up the class
    def __set_scoring(self):
        """ Set up scoring information. """
        # Get our dictionary, if we fail then no scoring values can be set so
        # we return
        score_dict = self.json.get("scoring")
        if not score_dict:
            self.is_scoring = False
            self.scoring_type = None
            self.scoring_team = None
            return
        else:
            self.is_scoring = True
        # Set Scoring Type
        self.scoring_type = score_dict.get("type")
        # Set Scoring Team
        self.scoring_team = score_dict.get("team")

    # The play class can be accessed like a dictionary in most respects
    def get(self, key, default=None):
        """ Try to get a value, return default if it doesn't exist. """
        return self.json.get(key, default)

    def __iter__(self):
        """ Returns an iterator to the play object. """
        return self.json.__iter__()

    def __len__(self):
        """ Returns the length of the play JSON object. """
        return self.json.__len__()

    def __getitem__(self, key):
        """ Returns the value associated with the key in the play object. """
        return self.json.__getitem__(key)
