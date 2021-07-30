import collections

from pywebshare import webshare
from pywebshare import config

def query_requests_by_country(country_code):
    """
    Number of requests made by individual country
    :param country_code:
    :return:
    """
    prx_stats = client.get_proxy_stats()
    rq_countries = prx_stats["request_countries"]
    if country_code in rq_countries.keys():
        return rq_countries[country_code]
    return None


def query_proxy_by_city(pages=1):
    """
    Proxy By City Data
    :param pages: Number of Pages to Scan, defaults to 1
    :return: Collections.counter Object
    """
    ct = list()

    for page in range(1, pages + 1):
        proxy_list = client.get_proxy_list(page=page)
        for config in proxy_list["results"]:
            ct.append(config["city_name"])
        if not proxy_list["next"]:
            return collections.Counter(ct)


config = config.Config()
client = webshare.Webshare(config.get_key())

