# encoding: utf-8
import sys
from multiprocessing.pool import ThreadPool

sys.path.append("./lib")

from typing import TYPE_CHECKING  # noqa: E402

import attr  # noqa: E402
from workflow import Workflow3  # noqa: E402

from src.models import WorkflowItem  # noqa: E402
from src.utils import find_app, get_ip_info, get_icon, get_app_store_appscheme  # noqa: E402

if TYPE_CHECKING:
    from src.models import IpInfoResponse, AppStoreSearchResult  # noqa: E402

tasks = []


def create_workflow_item(ip_info, app):  # type: (IpInfoResponse, AppStoreSearchResult) -> WorkflowItem
    icon = get_icon(app.artworkUrl60, app.trackViewUrl.app_id)
    arg = get_app_store_appscheme(ip_info.country, app.trackViewUrl)
    return WorkflowItem(title=app.trackCensoredName, subtitle=app.description, arg=arg, icon=icon)


def main(wf):  # type: (Workflow3) -> int
    query = wf.args[0]
    ip_info = wf.cached_data("ip_info", get_ip_info, max_age=60 * 24)
    apps = find_app(query, ip_info.country)
    pool = ThreadPool(processes=apps.resultCount)
    for app in apps.results:
        task = pool.apply_async(create_workflow_item, args=(ip_info, app))
        tasks.append(task)

    pool.close()
    pool.join()

    for task in tasks:
        workflow_item = task.get()
        wf.add_item(**attr.asdict(workflow_item))

    wf.send_feedback()
    return 0


if __name__ == "__main__":
    workflow = Workflow3()
    workflow.run(main)
