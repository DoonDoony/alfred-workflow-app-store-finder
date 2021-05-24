# encoding: UTF-8
import os

import attr
from typing import NoReturn
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


def get_icon(image_url, identifier):  # type: (unicode, unicode) -> unicode
    filepath = _get_icon_filepath(identifier)
    if not os.path.exists(filepath):
        response = web.get(image_url)
        response.raise_for_status()
        _save_image(response.content, filepath)
    return filepath


def _get_icon_filepath(identifier):  # type: (unicode) -> unicode
    return os.path.realpath(os.path.join(ICONS_DIR, identifier + u".jpg"))


def _save_image(image, filepath):  # type: (bytes, unicode) -> NoReturn
    with open(filepath, "wb") as image_file:
        image_file.write(image)


def get_app_store_appscheme(country, track_view_url):  # type: (unicode, TrackViewUrl) -> unicode
    return APP_STORE_APPSCHEME.substitute(
        country=country.lower(), app_name=track_view_url.app_name, app_id=track_view_url.app_id
    )
