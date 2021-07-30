import requests
import json

from tenacity import (retry, stop_after_delay,
                      stop_after_attempt, wait_fixed)



MAX_DELAY = 10
MAX_RETRIES = 5
MAX_WAIT = 2


class API:
    """
    Generalized API Wrapper Method Calls with Optional Sub-Arguments

    """
    def __init__(self, _api_key=None, portal="main", id=None):
        self.base_url = "https://proxy.webshare.io/api"
        self._api_key = _api_key
        self.headers = dict()
        self.portal = portal
        self.id = id # SubUser Portal Use Only

    @retry(stop=(stop_after_delay(MAX_DELAY) | stop_after_attempt(MAX_RETRIES)), wait=wait_fixed(MAX_WAIT))
    def get(self, url, **kwargs):
        """ Fulfill Get Request """
        data = {key: kwargs[key] for key in kwargs}
        url = self.base_url + url

        if self.portal == "main":
            headers = self.get_headers()
        if self.portal == "subuser":
            headers = self.get_subuser_headers()
        try:
            r = requests.get(url, params=data, headers=headers)
            r.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print("Connection Error: {!r}".format(e))
        except requests.exceptions.Timeout as e:
            print("Request Timeout: {!r}".format(e))
        except requests.exceptions.HTTPError as e:
            print("Credentials Error: {!r}".format(e))
        else:
            return r

    @retry(stop=(stop_after_delay(MAX_DELAY) | stop_after_attempt(MAX_RETRIES)), wait=wait_fixed(MAX_WAIT))
    def post(self, url, **kwargs):
        """ Fulfill Post Request """
        data = {key: kwargs[key] for key in kwargs}
        url = self.base_url + url

        if self.portal == "main":
            headers = self.get_headers()
        if self.portal == "subuser":
            headers = self.get_subuser_headers()
        try:
            r = requests.post(url, data=data, headers=headers)
            r.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print("Connection Error: {!r}".format(e))
        except requests.exceptions.Timeout as e:
            print("Request Timeout: {!r}".format(e))
        except requests.exceptions.HTTPError as e:
            print("Credentials Error: {!r}".format(e))
        else:
            return r

    @retry(stop=(stop_after_delay(MAX_DELAY) | stop_after_attempt(MAX_RETRIES)), wait=wait_fixed(MAX_WAIT))
    def patch(self, url, **kwargs):
        """ Fulfill Patch Request """
        data = {key: kwargs[key] for key in kwargs}
        url = self.base_url + url

        if self.portal == "main":
            headers = self.get_headers()
        if self.portal == "subuser":
            headers = self.get_subuser_headers()
        try:
            r = requests.patch(url, data=data, headers=headers)
            r.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print("Connection Error: {!r}".format(e))
        except requests.exceptions.Timeout as e:
            print("Request Timeout: {!r}".format(e))
        except requests.exceptions.HTTPError as e:
            print("Credentials Error: {!r}".format(e))
        else:
            return r

    @retry(stop=(stop_after_delay(MAX_DELAY) | stop_after_attempt(MAX_RETRIES)), wait=wait_fixed(MAX_WAIT))
    def delete(self, url, **kwargs):
        """ Fulfill Delete Request """
        data = {key: kwargs[key] for key in kwargs}
        url = self.base_url + url

        if self.portal == "main":
            headers = self.get_headers()
        if self.portal == "subuser":
            headers = self.get_subuser_headers()
        try:
            r = requests.delete(url, params=data, headers=headers)
            r.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            print("Connection Error: {!r}".format(e))
        except requests.exceptions.Timeout as e:
            print("Request Timeout: {!r}".format(e))
        except requests.exceptions.HTTPError as e:
            print("Credentials Error: {!r}".format(e))
        else:
            return r

    def get_headers(self):
        """ Authorization Headers """
        headers = {"Authorization": "Token {}".format(self._api_key)}
        return headers

    def get_subuser_headers(self):
        """ Masquerade as Sub-User """
        headers = {"X-Webshare-SubUser": "{}".format(self.id),
                   "Authorization": "Token {}".format(self._api_key)}

        return headers


