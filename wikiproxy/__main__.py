import sys
from importlib.metadata import version

import click
import uvicorn
from fastapi import FastAPI

from wikiproxy.routers import router


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(message=f'wikiproxy {version(__package__)}')
def main():
    """A FutureRestore-compatible firmware key API."""

    sys.tracebacklimit = 0

    app = FastAPI()
    app.include_router(router, prefix='/firmware')

    uvicorn.run(app=app, host='0.0.0.0', port=8888)


if __name__ == '__main__':
    main()
