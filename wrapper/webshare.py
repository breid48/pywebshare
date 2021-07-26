import ipaddress

import endpoints

from api import API


class Webshare(API):
    """ Webshare API Stuffs """
    def get_profile(self):
        """ Profile """
        r = super().get(url=endpoints.PROFILE)
        return r.json()

    def get_subscription(self):
        """ Subscription """
        r = super().get(url=endpoints.SUBSCRIPTION)
        return r.json()

    def get_proxy_config(self):
        """ Proxy Config """
        r = super().get(url=endpoints.GET_CONFIG)
        return r.json()

    def get_proxy_list(self, page, **kwargs):
        """ Get Proxy List
        :param page: Current Proxy Page. Defaults to 1
        :param kwargs: Optional Argument: countries
        """
        r = super().get(url=endpoints.PROXY_LIST, data=page, **kwargs)
        return r.json()

    def get_proxy_replacement_info(self):
        """ Get Replacement Info for your subscription """
        r = super().get(url=endpoints.REPLACEMENT_INFO)
        return r.json()

    def get_historical_proxy_replacements(self):
        """ Retrieves all Previous Historical Proxy Replacements """
        r = super().get(url=endpoints.REPLACEMENT_HISTORY)
        return r.json()

    def get_proxy_stats(self):
        r = super().get(url=endpoints.STATS)
        return r.json()

    def get_subuser(self, id):
        r = super().get(url=endpoints.SUBUSER, ID=id)
        return r.json()

    def get_all_subusers(self, page):
        """
        :param page:
        :return:
        :raises: HTTPError if Page not Found
        """
        r = super().get(url=endpoints.SUBUSER, page=page)
        return r.json()

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
                r = super().post(url=endpoints.UPDATE_CONFIG, authorized_ips=authorized_ips)
                return r.json()

    def reset_proxy_password(self, password):
        """ Resets The Proxy Password """
        r = super().post(url=endpoints.RESET_PASSWORD)
        return r.json()

    def refresh_proxy_list(self):
        """ Refreshes Entire List """
        r = super().post(url=endpoints.REFRESH_LIST)
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
        r = super().post(url=endpoints.REPLACE_PROXY, ip_address=ip_address)
        return r.json()

    def delete_proxy_replacement(self, ip_address):
        """ Delete a Previously Replaced Proxy.
        :return: 204 on Success
        """
        r = super().post(url=endpoints.DELETE_REPLACEMENT, ip_address=ip_address)
        return r.status_code

    def create_subuser(self, label, proxy_limit, **kwargs):
        """ Creates Subuser Client
        :param: label: Name
        :param: proxy_limit:
        :param: kwargs:
        Required: If you wish to gain access to this API, please complete the form at https://proxy.webshare.io/subuser/
        """
        r = super().post(url=endpoints.SUBUSER, label=label, proxy_limit=proxy_limit, **kwargs)
        return r.json()

    def delete_subuser(self, id):
        """ Delete's a subuser
        :param id:
        :return: 204 Status Code on Success
        """
        url = "https://proxy.webshare.io/api/subuser/{0}/".format(id)
        r = super().delete(url=url)
        return r.status_code



web_sub = Webshare("671454f3bba60745ae754b4ccc8ac2616759cbd0", portal="subuser", id=16527)
web_main = Webshare("671454f3bba60745ae754b4ccc8ac2616759cbd0")
#print(web.portal)
#print(web.get_profile())
#print(web.get_subscription())
#print(web.get_proxy_config())
#print(web.get_proxy_list(page=1))
#print(web_main.get_proxy_list(page=1))
#print(web.get_proxy_replacement_info())
#print(web.get_proxy_stats())
#print(web.create_subuser(label="Test-User", proxy_limit=0))
#print(web.get_all_subusers(page=1))
#print(web.update_subuser(id=16525, label="Test-User-New"))
#print(web.delete_subuser(id=16526))
