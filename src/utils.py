# encoding: UTF-8


import os

import attr
from workflow import web

from src.consts import IP_INFO_URL, ICONS_DIR, APP_STORE_APPSCHEME
from src.consts import ITUNES_SEARCH_URL
from src.models import AppStoreSearchResponse, AppStoreSearchParam, TrackViewUrl
from src.models import IpInfoResponse


def get_ip_info():  # type: () -> IpInfoResponse
    response = web.get(IP_INFO_URL)
    response.raise_for_status()
    data = response.json()
    return IpInfoResponse(**data)


def find_app(term, country):  # type: (unicode, unicode) -> AppStoreSearchResponse
    params = AppStoreSearchParam(term=term, country=country)
    response = web.get(ITUNES_SEARCH_URL, params=attr.asdict(params))
    response.raise_for_status()

    data = response.json()
    return AppStoreSearchResponse(**data)


def get_icon(image_url):  # type: (unicode) -> bytes
    response = web.get(image_url)
    response.raise_for_status()
    return response.content


def save_image(image, identifier):  # type: (bytes, unicode) -> unicode
    extension = u".jpg"
    filepath = os.path.join(ICONS_DIR, identifier + extension)
    with open(filepath, "wb") as image_file:
        image_file.write(image)
        return os.path.realpath(image_file.name)


def get_app_store_appscheme(country, track_view_url):  # type: (unicode, TrackViewUrl) -> unicode
    return APP_STORE_APPSCHEME.substitute(
        country=country.lower(), app_name=track_view_url.app_name, app_id=track_view_url.app_id
    )
