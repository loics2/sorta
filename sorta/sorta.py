#! /usr/bin/python3
import click
from .drop_folder import DropFolder

@click.group()
def cli():
    """Sorta is a tool helping you to sort your files."""


@cli.command()
@click.option('--path', default=".", type=click.Path(exists=True,
                                                     file_okay=False,
                                                     dir_okay=True,
                                                     writable=True,
                                                     readable=True,
                                                     resolve_path=True))
def sort(path):
    """Sort the files in the drop folder."""
    folder = DropFolder(path)
    folder.sort()


@cli.command()
@click.argument('element_type', type=click.Choice(['prefix', 'ext']))
@click.argument('name', type=click.STRING)
@click.argument('value', type=click.Path(exists=True,
                                         file_okay=False,
                                         dir_okay=True,
                                         writable=True,
                                         readable=True,
                                         resolve_path=True))
@click.option('--path', default=".", type=click.Path(exists=True,
                                                     file_okay=False,
                                                     dir_okay=True,
                                                     writable=True,
                                                     readable=True,
                                                     resolve_path=True))
def add(element_type, name, value, path):
    """Add an entry to the sorting rules."""
    folder = DropFolder(path)
    folder.add_rule(element_type, name, value)


@cli.command()
@click.argument('element_type', type=click.Choice(['prefix', 'ext']))
@click.argument('name', type=click.STRING)
@click.option('--path', default=".", type=click.Path(exists=True,
                                                     file_okay=False,
                                                     dir_okay=True,
                                                     writable=True,
                                                     readable=True,
                                                     resolve_path=True))
def rm(element_type, name, path):
    """Remove an entry from the sorting rules."""
    folder = DropFolder(path)
    folder.remove_rule(element_type, name)


@cli.command()
@click.option('--path', default=".", type=click.Path(exists=False,
                                                     file_okay=False,
                                                     dir_okay=True,
                                                     writable=True,
                                                     readable=True,
                                                     resolve_path=True))
def init(path):
    """Create an empty Sorta drop folder or reinitialize an existing one."""
    DropFolder.init_folder(path)
