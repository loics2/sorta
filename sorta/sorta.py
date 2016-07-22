#! /usr/bin/python3

import configparser
import click
import logging
import os
from shutil import move, Error
from sys import exit
from time import time, sleep

CONFIG_FILE_NAME = ".sortaconfig"

@click.group()
def cli():
    """Sorta is a tool helping you to manage your files."""
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)-5.5s]  %(message)s',
                        handlers=[logging.StreamHandler()])

@cli.command()
@click.option('--path', default=".", type=click.Path(exists=False,
                                                     file_okay=False,
                                                     dir_okay=True,
                                                     writable=True,
                                                     readable=True,
                                                     resolve_path=True))
def sort(path):
    """Sort the files in the drop folder."""

    config_path = os.path.join(path, CONFIG_FILE_NAME)
    config = get_config(config_path)

    for elt in os.listdir(path):
        if elt == CONFIG_FILE_NAME:
            continue

        try:
            dest = get_destination(elt, config)
            move(os.path.join(path, elt), dest)
            logging.info("%s moved to %s", elt, dest)
        except LookupError as e:
            logging.warning(str(e))
        except Error:
            logging.warning("error while moving the element %s", elt)

@cli.command()
@click.argument('element_type', type=click.Choice(['prefix', 'ext']))
@click.argument('name', type=click.STRING)
@click.argument('value', type=click.Path(exists=True,
                                         file_okay=False,
                                         dir_okay=True,
                                         writable=True,
                                         readable=True,
                                         resolve_path=True))
@click.option('--path', default=".", type=click.Path(exists=False,
                                                     file_okay=False,
                                                     dir_okay=True,
                                                     writable=True,
                                                     readable=True,
                                                     resolve_path=True))
def add(element_type, name, value, path):
    """Add an entry to the sorting rules."""
    config_path = os.path.join(path, CONFIG_FILE_NAME)
    config = get_config(config_path)

    if element_type == 'prefix':
        config.set('prefix', name, value)
    else:
        config.set('extension', name, value)

    with open(config_path, mode='w') as configfile:
        config.write(configfile)

@cli.command()
@click.argument('element_type', type=click.Choice(['prefix, ext']))
@click.argument('name', type=click.STRING)
@click.option('--path', default=".", type=click.Path(exists=False,
                                                     file_okay=False,
                                                     dir_okay=True,
                                                     writable=True,
                                                     readable=True,
                                                     resolve_path=True))
def rm(element_type, name, path):
    """Remove an entry from the sorting rules."""
    config_path = os.path.join(path, CONFIG_FILE_NAME)
    config = get_config(config_path)

    if element_type == 'prefix':
        config.remove('prefix', name)
    else:
        config.set('extension', name)

    with open(config_path, mode='w') as configfile:
        config.write(configfile)

@cli.command()
@click.option('--path', default=".", type=click.Path(exists=False,
                                                     file_okay=False,
                                                     dir_okay=True,
                                                     writable=True,
                                                     readable=True,
                                                     resolve_path=True))
def init(path):
    """Create an empty Sorta drop folder or reinitialize an existing one."""
    if not os.path.exists(path):
        os.mkdir(path)

    config = configparser.ConfigParser()
    config.add_section('core')
    config.set('core', 'delimiter', '--')
    config.set('core', 'polling', '60.0')

    config.add_section('prefix')

    config.add_section('extension')

    with open(os.path.join(path, '.sortaconfig'), mode='w') as configfile:
        config.write(configfile)

def get_config(path):
    """Parse the config file and return a ConfigParser object."""
    config = configparser.ConfigParser()
    config.read_file(open(path))

    return config

def get_destination(element, config):
    """Find the right destination corresponding to the element name."""
    split_prefix = element.split(config.get('core', 'delimiter'))
    split_ext = os.path.splitext(element)

    try:
        if len(split_prefix) == 2:
            dest = os.path.join(config.get('prefix', split_prefix[0]), split_prefix[1])
        elif len(split_ext) == 2:
            dest = os.path.join(config.get('extension', split_ext[1][1:]), element)
        else:
            raise LookupError("no destination found for the element {}".format(element))
    except configparser.NoOptionError:
        raise LookupError("no destination found for the element {}".format(element))

    return dest
