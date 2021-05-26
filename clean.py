# encoding: utf-8
import sys

sys.path.append("./lib")

import glob  # noqa: E402
import os.path  # noqa: E402

from typing import NoReturn  # noqa: E402
from workflow import Workflow3  # noqa: E402

from src.consts import ICONS_DIR  # noqa: E402


def main(wf):  # type: (Workflow3) -> NoReturn
    pattern = os.path.join(ICONS_DIR, "*")
    for icon in glob.glob(pattern):
        os.remove(icon)
    wf.logger.info(pattern)
    wf.clear_cache()


if __name__ == u"__main__":
    workflow = Workflow3()
    workflow.run(main)
