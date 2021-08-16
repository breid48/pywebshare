import collections
import types
import json

from pywebshare import webshare


def get_proxy_list():
    """Returns a complete list of active proxy IP addresses"""
    page = 1
    proxies = list()

    while True:
        print(f"Parsing Proxy Page : {page}")
        proxy_list = client.get_proxy_list(page=page)
        for proxy in proxy_list["results"]:
            proxies.append(proxy["proxy_address"])
        if not proxy_list["next"]:
            return proxies
        page += 1


def query_requests_by_country(country_code):
    """Returns number of requests made by an individual country

    Args:
        country_code (str): ISO 3166-1 Alpha-2 code format
    """
    prx_stats = client.get_proxy_stats()
    countries = prx_stats["request_countries"]
    if country_code in countries.keys():
        return countries[country_code]
    return None


def query_proxy_by_city(pages=1):
    """Returns Collections.Counter Object Containing Proxy City Data"""
    c = list()

    for page in range(1, pages + 1):
        proxy_list = client.get_proxy_list(page=page)
        for config in proxy_list["results"]:
            c.append(config["city_name"])
        if not proxy_list["next"]:
            return collections.Counter(c)


def get_proxy_location(ip_address, pages):
    """Returns a Proxies' Corresponding City and Country Data

    Args:
        ip_address (str): IP Address of the Proxy
        pages (int): Number of pages to search (250 proxies per page)
    """
    for page in range(1, pages + 1):
        print(f"Scanning Proxy Page: {page}")
        proxy_list = client.get_proxy_list(page=page)

        for proxy in proxy_list["results"]:
            if proxy["proxy_address"] == ip_address:
                proxy_city = proxy["city_name"]
                proxy_country_code = proxy["country_code"]
                return types.SimpleNamespace(city=proxy_city, country=proxy_country_code)

        if not proxy_list["next"]:
            return types.SimpleNamespace(city=None, country=None)


def get_retired_proxies_from_iter(_iter, proxy_list=None):
    """Get Retired Proxies from Iterable (Dict / List Support Currently)"""
    if not proxy_list:
        proxy_list = get_proxy_list()

    if isinstance(_iter, dict):
        return {*_iter.values()} - {*proxy_list}
    elif isinstance(_iter, list):
        return {*_iter} - {*proxy_list}
    return None


def get_retired_proxies_from_obj(proxy_json, proxy_list=None):
    """
    Get Retired Proxies from Json Object containing containing "requests" formatted proxies
    example: proxy_json: {server_object: 'http://username:password@ipaddress:port/'}
    """
    if not proxy_list:
        proxy_list = get_proxy_list()

    processed_proxies = set()
    for preprocessed in proxy_json.values():
        processed_proxies.add(preprocessed.split("@")[1].split(":")[0])
    return processed_proxies - {*proxy_list}


def get_unassigned_proxies_from_iter(_iter, proxy_list=None):
    """Get Unassigned Proxies from Iterable"""
    if not proxy_list:
        proxy_list = get_proxy_list()

    if isinstance(_iter, dict):
        return {*_iter.values()} - {*proxy_list}
    elif isinstance(_iter, list):
        return {*_iter} - {*proxy_list}
    return None


def get_unassigned_proxies_from_obj(proxy_json, proxy_list=None):
    """
    Get Unassigned Proxies from Json Object containing "requests" formatted proxies
    example: proxy_json: {server_object: 'http://username:password@ipaddress:port/'}
    """
    if not proxy_list:
        proxy_list = get_proxy_list()

    processed_proxies = set()
    for preprocessed in proxy_json.values():
        processed_proxies.add(preprocessed.split("@")[1].split(":")[0])
    return {*proxy_list} - processed_proxies


client = webshare.Webshare()

