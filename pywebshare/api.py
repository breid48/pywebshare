import requests
import os

from tenacity import (retry, stop_after_delay, stop_after_attempt, wait_fixed)
from configparser import NoOptionError

import pywebshare.config as cfg

MAX_DELAY = 10
MAX_RETRIES = 3
MAX_WAIT = 2


class API:
    """
    Generalized requests HTTP Wrapper Method Calls with Optional Sub-Arguments
    """

    def __init__(self, api_key=None, config_path=None, portal="main", user_id=None):
        self.api_key = api_key
        self.config_path = config_path
        self.headers = dict()
        self.portal = portal
        self.user_id = user_id  # Sub-user Portal
        self.base_url = "https://proxy.webshare.io/api"

        if not self.api_key:
            # If an api_key is not explicitly given to the constructor, invoke it from the configuration file
            self.__invoke_config(config_path=config_path, portal=portal)

    def __invoke_config(self, config_path, portal):

        if not config_path:
            # Fallback to current working directory
            fallback = os.path.join(os.getcwd(), "env.ini")

            if os.path.exists(fallback) and os.path.getsize(fallback) > 0:
                config_path = fallback
            else:
                # Fallback to the file root directory
                fallback = os.path.join(os.path.dirname(__file__), "env.ini")

                if os.path.exists(fallback) and os.path.getsize(fallback) > 0:
                    config_path = fallback

        if not config_path:
            raise FileNotFoundError("unable to locate config file")

        config = cfg.Config(filepath=config_path)
        config.parse_config()

        self.api_key = config.get_key()

        if portal == "subuser":
            try:
                self.user_id = config.get_subuser_id()
            except NoOptionError:
                self.user_id = None

    @retry(reraise=True,
           stop=(stop_after_delay(MAX_DELAY) | stop_after_attempt(MAX_RETRIES)),
           wait=wait_fixed(MAX_WAIT))
    def get(self, url, **kwargs):
        """Fulfills a HTTP GET Request."""
        data = {key: kwargs[key] for key in kwargs}
        url = self.base_url + url

        if self.portal == "main":
            headers = self._get_headers()
        if self.portal == "subuser":
            headers = self._get_subuser_headers()
        try:
            r = requests.get(url, params=data, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise requests.exceptions.HTTPError("Authentication Credentials Error: {!r}".format(e))
        else:
            return r

    @retry(reraise=True,
           stop=(stop_after_delay(MAX_DELAY) | stop_after_attempt(MAX_RETRIES)),
           wait=wait_fixed(MAX_WAIT))
    def post(self, url, **kwargs):
        """Fulfills a HTTP POST Request."""
        data = {key: kwargs[key] for key in kwargs}
        url = self.base_url + url

        if self.portal == "main":
            headers = self._get_headers()
        if self.portal == "subuser":
            headers = self._get_subuser_headers()
        try:
            r = requests.post(url, data=data, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise requests.exceptions.HTTPError("Authentication Credentials Error: {!r}".format(e))
        else:
            return r

    @retry(reraise=True,
           stop=(stop_after_delay(MAX_DELAY) | stop_after_attempt(MAX_RETRIES)),
           wait=wait_fixed(MAX_WAIT))
    def patch(self, url, **kwargs):
        """Fulfills a HTTP PATCH Request."""
        data = {key: kwargs[key] for key in kwargs}
        url = self.base_url + url

        if self.portal == "main":
            headers = self._get_headers()
        if self.portal == "subuser":
            headers = self._get_subuser_headers()
        try:
            r = requests.patch(url, json=data, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise requests.exceptions.HTTPError("Authentication Credentials Error: {!r}".format(e))
        else:
            return r

    @retry(reraise=True,
           stop=(stop_after_delay(MAX_DELAY) | stop_after_attempt(MAX_RETRIES)),
           wait=wait_fixed(MAX_WAIT))
    def delete(self, url, **kwargs):
        """Fulfills a HTTP DELETE Request."""
        data = {key: kwargs[key] for key in kwargs}
        url = self.base_url + url

        if self.portal == "main":
            headers = self._get_headers()
        if self.portal == "subuser":
            headers = self._get_subuser_headers()
        try:
            r = requests.delete(url, params=data, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise requests.exceptions.HTTPError("Authentication Credentials Error: {!r}".format(e))
        else:
            return r

    def _get_headers(self):
        """Main Portal Headers"""
        headers = {"Authorization": "Token {}".format(self.api_key)}
        return headers

    def _get_subuser_headers(self):
        """Sub-User Portal Headers"""
        headers = {"X-Webshare-SubUser": "{}".format(self.user_id),
                   "Authorization": "Token {}".format(self.api_key)}

        return headers
