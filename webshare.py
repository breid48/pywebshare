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

    

web = Webshare("671454f3bba60745ae754b4ccc8ac2616759cbd0")
#print(web.get_profile())
#print(web.get_subscription())
#print(web.get_proxy_config())
#print(web.get_proxy_list(page=21))
print(web.get_proxy_replacement_info())
