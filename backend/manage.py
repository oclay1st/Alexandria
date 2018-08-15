import click
from flask.cli import FlaskGroup
from flask.helpers import get_debug_flag

try:
    import better_exceptions
except ImportError:
    pass

from alexandria.factory import create_app
from alexandria.settings.config import DevConfig, ProdConfig

__author__ = 'oclay'


def alexandria_app():
    """
    Setting Flask app context
    :return: a Flask app
    """
    config = DevConfig() if get_debug_flag() else ProdConfig()
    _app = create_app(config)
    ctx = _app.app_context()
    ctx.push()
    return _app


@click.group(cls=FlaskGroup, create_app=lambda request: alexandria_app())
def cli():
    """cli for alexandria application."""


if __name__ == '__main__':
    cli()
else:
    app = alexandria_app()
