import sys
from importlib.metadata import version
from typing import Annotated

import typer
import uvicorn
from fastapi import FastAPI
from loguru import logger

from wikiproxy.routers import router


def _version_callback(val: bool) -> None:
    if val:
        print(' '.join(__package__, version(__package__)))
        raise typer.Exit()


app = typer.Typer()


@app.command(context_settings={'help_option_names': ['-h', '--help']})
def cli(
    verbose: Annotated[
        bool, typer.Option('--verbose', '-v', help='Enable verbose logging.')
    ] = False,
    version: Annotated[
        bool | None, typer.Option('--version', callback=_version_callback)
    ] = None,
) -> None:
    """A FutureRestore-compatible firmware key API."""

    if verbose:
        logger.remove()
        logger.add(
            sys.stderr,
            level='DEBUG',
            format='[{time:MMM D YYYY - hh:mm:ss A zz}] {level} | {module}:{function}:{line} {message}',
        )
        logger.enable(__package__)
        logger.enable('plykos')
    else:
        sys.tracebacklimit = 0

    app = FastAPI()
    app.include_router(router, prefix='/firmware')

    uvicorn.run(app=app, host='0.0.0.0', port=8888)


if __name__ == '__main__':
    app()
