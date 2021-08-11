import configparser

from os.path import abspath, join, dirname


class Config():
    """
    Configuration object containing authorization credentials and optional portal parameters
    """

    def __init__(self, filepath="env.ini"):
        self.filepath = filepath
        self.config = None
        self.config_options = ['auth']

    def parse_config(self):
        """
        Generates object of type ConfigParser
            Query ->  value = self.config.get(section, key)

        """
        if not self.config:
            self.config = configparser.ConfigParser()
            abs_path = self.get_abs_path(filepath=self.filepath)
            self.config.read(abs_path)

            if not all(option in self.config.sections() for option in self.config_options):
                raise IllegalConfigException("invalid config arguments supplied")

        return self.config

    def get_endpoint_keys(self):
        if self.config:
            return [k for k in self.config["endpoints"]]

    def get_all_endpoints(self):
        if self.config:
            return [v for k, v in self.config["endpoints"].items()]

    def get_endpoint(self, endpoint_key):
        if self.config:
            return self.config.get("endpoints", endpoint_key)

    def get_key(self):
        if self.config:
            return self.config.get("auth", "API_KEY")

    def get_subuser_id(self):
        if self.config:
            return self.config.get("auth", "user_id")

    def get_abs_path(self, filepath):
        return join(dirname(abspath(__file__)), filepath)


class IllegalConfigException(ValueError):
    """
    Exception class for handling omitted config arguments
    """
    pass

