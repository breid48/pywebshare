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
    """Simple Python Wrapper for Webshare Proxy's API <https://www.webshare.io/>.

     Implements the API() general class and can be invoked with an API Key retrieved
     from <https://proxy.webshare.io/userapi/keys>.

     A direct representation of the api_key can be passed to the constructor,
     else, instantiate the object through a configuration file. Currently Supports .ini file format.
     By default, the object reads from the env.ini file in the current working directory.
     A different absolute filepath to the configuration file can be specified with <config_path> parameter.

     To provide access to the subuser portal, provide the optional <portal> and <id> parameters.
     >> client = Webshare(API_KEY, portal="subuser", id=1234)

     Requests can be made to the Proxy Configuration, Proxy List and Proxy Stats APIs as a subuser

     Otherwise, portal defaults to 'main'

     """

    def get_profile(self):
        """ Returns your Webshare User Profile Object.

        Returns:
            r.json(): profile json object.
        """
        r = super().get(url='/profile/')
        return r.json()

    def get_subscription(self):
        """ Returns your Webshare User Subscription Object.

        Returns:
            r.json(): subscription json object.
        """
        r = super().get(url='/subscription/')
        return r.json()

    def get_proxy_config(self):
        """ Returns your Webshare User Proxy Configuration Object

        Returns:
            r.json(): subscription json object.
        """
        r = super().get(url='/proxy/config/')
        return r.json()

    def get_proxy_list(self, page=1, **kwargs):
        """ Returns your Webshare User Proxy List.

        This API is paginated and returns multiple proxy list objects.

        Args:
            page: Proxy Page (Offsets by 250). Defaults to 1.

        Keyword Args:
            countries (dict of str: int): Dictionary containing country codes in
                                          in ISO 3166-1 Alpha-2 code format and number
                                          of proxies.
        """
        r = super().get(url='/proxy/list/', page=page, **kwargs)
        return r.json()

    def get_proxy_replacement_info(self):
        """ Returns your Webshare User Proxy Replacement Object.

        Returns:
            r.json(): proxy replacement object.
        """
        r = super().get(url='/proxy/replacement/info/')
        return r.json()

    def get_historical_proxy_replacements(self):
        """ Returns a list containing your historical proxy replacement objects.

        Returns:
            r.json() (list of dicts): List of Historical Proxy Replacements
        """
        r = super().get(url='/proxy/replacement/')
        return r.json()

    def get_proxy_stats(self):
        """ Returns your Webshare User Proxy Stats Object.

        Returns:
            r.json(): proxy stats object.
        """
        r = super().get(url='/proxy/stats/')
        return r.json()

    def get_subuser(self, user_id):
        """ Returns your a Sub-users proxy configuration object.

        Args:
            user_id (int):  ID of the Sub-User.

        Returns:
            r.json(): sub-user's proxy configuration object.
        """
        r = super().get(url='/subuser/', ID=user_id)
        return r.json()

    def get_all_subusers(self, page=1):
        """ Returns all Sub-Users in the System.

        Args:
            page (int): Page

        Returns:
            r.json(): Sub-User's object.
        """
        r = super().get(url='/subuser/', page=page)
        return r.json()

    def update_subuser(self, user_id, **kwargs):
        """ Update Subuser Information in the System.

        Args:
            user_id (int): Subuser ID
            **kwargs: Optional Keyword Arguments.

        Keyword Args:
            label (str): Unique user identifier
            proxy_username (str): The username to connect to the Webshare Proxy.
            proxy_password (str): The password to connect to the Webshare Proxy.
            proxy_countries (dict of str: int): Dictionary containing country codes in
                                                in ISO 3166-1 Alpha-2 code format and number
                                                of proxies.
            proxy_limit (int): The user proxy limit in GBs. You can set to 0 in order to get
                               unlimited bandwidth.
            max_thread_count (int): The maximum number of proxy request concurrency this subuser
                                    can have.
        """
        url = "/subuser/{0}/".format(user_id)
        r = super().patch(url=url, **kwargs)
        print(r.text)
        return r.json()

    def update_proxy_config(self, authorized_ips):
        """Updates your Webshare User Proxy Configuration.

        Args:
            authorized_ips (list(str)): List of IP Authorized IP Addresses
                                        [IPs authorized to make requests to Webshare Proxy.]

        Returns:
            r.json(): updated proxy configuration object.
        """
        if isinstance(authorized_ips, list):
            if all(ipaddress.ip_address(address) for address in authorized_ips):
                r = super().post(url='/proxy/config/', authorized_ips=authorized_ips)
                return r.json()

    def reset_proxy_password(self):
        """ Resets your Proxy Password.

        Returns:
            r.json(): updated proxy object.
        """
        r = super().post(url='/proxy/config/reset_password/')
        return r.json()

    def refresh_proxy_list(self):
        """ Refresh your entire proxy list. You can only perform this
        action if you have on_demand_refreshes_available available.

        Returns:
            r.json(): updated proxy refresh object.
        """
        r = super().post(url='/proxy/replacement/info/refresh/')
        return r.json()

    def refresh_subuser_proxy_list(self, user_id):
        """ Refresh the proxy list of a user. You can only perform this
        action if the user has a custom proxy list.

        Args:
            user_id (int): target sub-user ID

        Returns:
            r.json(): updated sub-user proxy refresh object.
        """
        url = "/subuser/{0}/refresh/".format(user_id)
        r = super().post(url=url)
        return r.json()

    def replace_proxy(self, ip_address):
        """ Replace a specific proxy from your active proxy list.

        Args:
            ip_address (int): The IP address replaced. May be presented in CIDR
                              format (with / at the end). If CIDR is missing, assume /32.

        Returns:
            r.json(): proxy replacement object.
        """
        r = super().post(url='/proxy/replacement/', ip_address=ip_address)
        return r.json()

    def delete_proxy_replacement(self, ip_address):
        """ Delete a previously replaced proxy.

        Args:
            ip_address (int): The IP address replaced. May be presented in CIDR
                              format (with / at the end). If CIDR is missing, assume /32.

        Returns:
            r.status_code: 204 on Success
        """
        r = super().post(url='/proxy/replacement/', ip_address=ip_address)
        return r.status_code

    def create_subuser(self, label, proxy_limit, **kwargs):
        """ Creates a new Sub-user Client

        Args:
            label (str): Unique user identifier
            proxy_limit (int): The user proxy limit in GBs. You can set to 0 in order to get
                               unlimited bandwidth.

        Keyword Arguments:
            **max_thread_count (int): The maximum number of proxy request concurrency this subuser
                                    can have.
            **proxy_countries (dict of str: int): Dictionary containing country codes in
                                                in ISO 3166-1 Alpha-2 code format and number
                                                of proxies.

        """
        r = super().post(url='/subuser/', label=label, proxy_limit=proxy_limit, **kwargs)
        return r.json()

    def delete_subuser(self, user_id):
        """ Delete's a Sub-User

        Args:
            user_id (int): Sub-User ID

        Returns:
            r.status_code: 204 on Success
        """
        url = "/subuser/{0}/".format(id)
        r = super().delete(url=url)
        return r.status_code

    @staticmethod
    def get_endpoints():
        return __endpoints__

