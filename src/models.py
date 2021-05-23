# encoding: UTF-8
from urllib import quote

import attr
import furl
from typing import Any, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from furl import furl


def _to_search_result(raw_results):  # type: (List[Dict[unicode, Any]]) -> List[AppStoreSearchResult]
    return [
        AppStoreSearchResult(
            artworkUrl60=result[u"artworkUrl60"],
            description=result[u"description"],
            trackCensoredName=result[u"trackCensoredName"],
            trackViewUrl=TrackViewUrl.from_url(result[u"trackViewUrl"])
        )
        for result in raw_results
    ]


def _to_track_view_url(raw_url):  # type: (str) -> TrackViewUrl
    url = furl.furl(raw_url)
    return TrackViewUrl.from_url(url)


@attr.s
class AppStoreSearchParam(object):
    term = attr.ib(type=unicode)
    country = attr.ib(type=unicode)
    media = attr.ib(type=unicode, default=u"software")
    limit = attr.ib(type=int, default=10)
    entity = attr.ib(type=unicode, default=u"macSoftware")


@attr.s
class TrackViewUrl(object):
    app_id = attr.ib(type=unicode)
    app_name = attr.ib(type=unicode)

    @classmethod
    def from_url(cls, url):  # type: (unicode) -> "TrackViewUrl"
        _url = furl.furl(url)
        app_id = _url.path.segments[-1]
        app_name = _url.path.segments[-2]
        app_name = quote(app_name)
        return cls(app_id=app_id, app_name=app_name)


@attr.s
class AppStoreSearchResult(object):
    artworkUrl60 = attr.ib(type=unicode)
    description = attr.ib(type=unicode)
    trackCensoredName = attr.ib(type=unicode)
    trackViewUrl = attr.ib(type=TrackViewUrl)


@attr.s
class AppStoreSearchResponse(object):
    resultCount = attr.ib(type=int)
    results = attr.ib(type=list, converter=_to_search_result)  # type: List[AppStoreSearchResult]


@attr.s
class IpInfoResponse(object):
    city = attr.ib(type=unicode)
    country = attr.ib(type=unicode)
    ip = attr.ib(type=unicode)
    loc = attr.ib(type=unicode)
    org = attr.ib(type=unicode)
    postal = attr.ib(type=unicode)
    readme = attr.ib(type=unicode)
    region = attr.ib(type=unicode)
    timezone = attr.ib(type=unicode)


@attr.s
class WorkflowItem(object):
    title = attr.ib(type=unicode)
    subtitle = attr.ib(type=unicode)
    arg = attr.ib(type=unicode)
    icon = attr.ib(type=unicode)
    valid = attr.ib(type=bool, default=True)
