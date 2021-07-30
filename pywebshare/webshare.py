import ipaddress

from pywebshare.api import API


__endpoints__ = ['/profile/',
                 '/subscription/',
                 '/proxy/config/',
                 '/proxy/config/reset_password/',
                 '/proxy/list/',
                 '/proxy/replacement/info/',
                 '/proxy/replacement/',
                 '/proxy/replacement/info/refresh/',
                 '/proxy/replacement/',
                 '/proxy/stats/',
                 '/subuser/'
                 ]


class Webshare(API):
    """
    Simple Python Wrapper for Webshare Proxy API

     Implements the API general class and can be invoked with an API Key retrieved
     from 'https://proxy.webshare.io/userapi/keys'

     If no explicit key is provided, by default, the object reads from the env.ini file
     in the current working directory.

     To provide access to the subuser portal, provide the optional 'portal' and 'id' parameters
     >> client = Webshare(API_KEY, portal="subuser", id=1234)

     Otherwise, portal defaults to 'main'

     """

    def get_profile(self):
        """
        Retrieves your Webshare User Profile Object
        :return: profile json object
        """
        r = super().get(url='/profile/')
        return r.json()

    def get_subscription(self):
        """

        :return:
        """
        r = super().get(url='/subscription/')
        return r.json()

    def get_proxy_config(self):
        """ Proxy Config """
        r = super().get(url='/proxy/config/')
        return r.json()

    def get_proxy_list(self, page, **kwargs):
        """ Get Proxy List
        :param page: Current Proxy Page. Defaults to 1
        :param kwargs: Optional Argument: countries
        """
        r = super().get(url='/proxy/list/', page=page, **kwargs)
        return r.json()

    def get_proxy_replacement_info(self):
        """ Get Replacement Info for your subscription """
        r = super().get(url='/proxy/replacement/info/')
        return r.json()

    def get_historical_proxy_replacements(self):
        """ Retrieves all Previous Historical Proxy Replacements """
        r = super().get(url='/proxy/replacement/')
        return r.json()

    def get_proxy_stats(self):
        r = super().get(url='/proxy/stats/')
        return r.json()

    def get_subuser(self, id):
        r = super().get(url='/subuser/', ID=id)
        return r.json()

    def get_all_subusers(self, page):
        """
        :param page:
        :return:
        :raises: HTTPError if Page not Found
        """
        r = super().get(url='/subuser/', page=page)
        return r.json()

    @staticmethod
    def get_endpoints():
        return __endpoints__

    def update_subuser(self, id, **kwargs):
        """ Update Subuser Information
        :param kwargs:
        :return:
        """
        url = "https://proxy.webshare.io/api/subuser/{0}/".format(id)
        r = super().patch(url=url, **kwargs)
        return r.json()

    def update_proxy_config(self, authorized_ips):
        """ Update Config Ting Heh
        :param: authorized_ips: Pee's
        """
        if isinstance(authorized_ips, list):
            if all(ipaddress.ip_address(address) for address in authorized_ips):
                r = super().post(url='/proxy/config/', authorized_ips=authorized_ips)
                return r.json()

    def reset_proxy_password(self, password):
        """ Resets The Proxy Password """
        r = super().post(url='/proxy/config/reset_password/')
        return r.json()

    def refresh_proxy_list(self):
        """ Refreshes Entire List """
        r = super().post(url='/proxy/replacement/info/refresh/')
        return r.json()

    def refresh_subuser_proxy_list(self, id):
        """ Refresh Proxy List of Subuser
        :param id:
        :return:
        """
        url = "https://proxy.webshare.io/api/subuser/{0}/refresh/".format(id)
        r = super().post(url=url)
        return r.json()

    def replace_proxy(self, ip_address):
        """ Replaces Single Proxy From List
        :param: ip_address: Pee Dress
        """
        r = super().post(url='/proxy/replacement/', ip_address=ip_address)
        return r.json()

    def delete_proxy_replacement(self, ip_address):
        """ Delete a Previously Replaced Proxy.
        :return: 204 on Success
        """
        r = super().post(url='/proxy/replacement/', ip_address=ip_address)
        return r.status_code

    def create_subuser(self, label, proxy_limit, **kwargs):
        """ Creates Subuser Client
        :param: label: Name
        :param: proxy_limit:
        :param: kwargs:
        Required: If you wish to gain access to this API, please complete the form at https://proxy.webshare.io/subuser/
        """
        r = super().post(url='/subuser/', label=label, proxy_limit=proxy_limit, **kwargs)
        return r.json()

    def delete_subuser(self, id):
        """ Delete's a subuser
        :param id:
        :return: 204 Status Code on Success
        """
        url = "https://proxy.webshare.io/api/subuser/{0}/".format(id)
        r = super().delete(url=url)
        return r.status_code


# client = Webshare("671454f3bba60745ae754b4ccc8ac2616759cbd0", portal="subuser", id=16527)
client = Webshare("671454f3bba60745ae754b4ccc8ac2616759cbd0")
print(client.portal)
print(client.get_profile())
print(client.get_subscription())
print(client.get_proxy_config())
print(client.get_proxy_list(page=1))
print(client.get_proxy_replacement_info())
print(client.get_proxy_stats())
# print(client.create_subuser(label="Test-User", proxy_limit=0))
# print(client.get_all_subusers(page=1))
# print(client.update_subuser(id=16525, label="Test-User-New"))
# print(client.delete_subuser(id=16526))
