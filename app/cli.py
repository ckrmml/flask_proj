import os
import click


def register(app):
    @app.cli.group()
    def db():
        """Database operations."""
        pass

    @db.command()
    def init():
        """Initialize the database."""
        os.system('flask db upgrade')

    @db.command()
    @click.option('-m', '--message', default=None, help='Revision message')
    def revision(message):
        """Create a new revision."""
        if os.system(
                f'alembic -c "migrations/alembic.ini" revision --autogenerate -m "{message}"'):
            raise RuntimeError('revision command failed')

    @db.command()
    @click.option('-r', '--revision', default='head', help='Revision message')
    def upgrade(revision):
        """Upgrade database"""
        if os.system(f'alembic -c "migrations/alembic.ini" upgrade {revision}'):
            raise RuntimeError('upgrade command failed')
