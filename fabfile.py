# encoding: UTF-8
import os

from fabric import task
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from invoke import Context

HOME = os.path.expanduser("~")
DESTINATION = "dist"
POETRY_PATH = os.path.join(HOME, ".poetry/bin/poetry")


class Command(object):
    make_destination_dir = "mkdir -p dist/src dist/icons"

    ensure_pip = "/usr/bin/python -m ensurepip --user 2>&1 > /dev/null"
    export_dependencies = POETRY_PATH + " export -f requirements.txt --without-hashes > requirements.txt"
    download_dependencies = "python -m pip install -q --target lib -r requirements.txt"
    compile_python_files = "python -m compileall -q -x 'fabfile.py|_next_gen.py|__version__.py' ."

    delete_redundant_vendor_files = "find lib -name '*.py' ! -name '__version__.py' ! -delete"
    delete_redundant_vendor_directories = "find lib -name '*dist-info' | xargs rm -rf"

    copy_target_files = "cp ./{main.pyc,clean.pyc,info.plist} dist/"
    copy_source_files = "cp -r src/*.pyc dist/src/"
    copy_assets = "cp assets/* dist/"
    copy_dependencies = "cp -r lib dist/"

    archive_workflow = "cd dist && zip -r ../appstorefinder.alfredworkflow ."

    clear_compiled_python_files = "find . -name '*.pyc' -delete"
    delete_spin_offs = "rm -rf lib dist requirements.txt"
    delete_pip = "/usr/bin/python -m pip uninstall pip -y -q"


@task
def _create_destination_dir(c):  # type: (Context) -> None
    print("Start building...")
    if not os.path.exists(DESTINATION):
        c.run(Command.make_destination_dir)


@task(pre=[_create_destination_dir])
def _ensure_pip(c):  # type: (Context) -> None
    c.run(Command.ensure_pip)


@task(pre=[_ensure_pip])
def _download_dependencies(c):  # type: (Context) -> None
    c.run(Command.export_dependencies)
    c.run(Command.download_dependencies)


@task(pre=[_download_dependencies])
def _precompile(c):  # type: (Context) -> None
    c.run(Command.compile_python_files)


@task(pre=[_precompile])
def _tree_shaking(c):  # type: (Context) -> None
    c.run(Command.delete_redundant_vendor_files)
    c.run(Command.delete_redundant_vendor_directories)


@task(pre=[_tree_shaking])
def _collect_files(c):  # type: (Context) -> None
    c.run(Command.copy_target_files)
    c.run(Command.copy_source_files)
    c.run(Command.copy_assets)
    c.run(Command.copy_dependencies)


@task(pre=[_collect_files])
def _archive(c):  # type: (Context) -> None
    c.run(Command.archive_workflow)


@task(pre=[_archive])
def _cleanup(c):  # type: (Context) -> None
    c.run(Command.delete_spin_offs)
    c.run(Command.delete_pip)
    c.run(Command.clear_compiled_python_files)


@task(pre=[_cleanup])
def build(c):  # type: (Context) -> None
    print("Complete")
