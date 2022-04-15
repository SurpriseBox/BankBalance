
import importlib
import logging
import os
import typing as t

from fastapi import APIRouter


def get_apps_router():
    apps_router = APIRouter()

    app_dirs: t.Set[os.DirEntry] = set(filter(
        lambda file_: os.path.isdir(file_) and not file_.name.startswith("__"),
        os.scandir(os.path.abspath(__name__))
    ))

    for app_dir in app_dirs:
        app = importlib.import_module(f".{app_dir.name}", package=__name__)
        if not hasattr(app, 'app_router'):
            logging.getLogger('uvicorn').warning(f"App {app_dir.name} has no router.")
            continue
        apps_router.include_router(app.router.app_router)

    return apps_router
