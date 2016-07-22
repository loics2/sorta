#! /usr/bin/python3

import argparse
import configparser
import logging
import os
from shutil import move, Error
from sys import exit
from time import time, sleep


def main():
    """program entry point"""
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)-5.5s]  %(message)s',
                        handlers=[logging.StreamHandler()])

    args = parse_args()

    if not os.path.exists(args.drop_folder):
        create_drop_folder(args.drop_folder)

    config = configparser.ConfigParser()
    # the SafeConfigParser method has been renamed to `ConfigParser` in Python 3.2.

    config.read_file(open(os.path.join(args.drop_folder, '.sortaconfig')))
    # `readfp()` is deprecated and will be removed in future versions

    if args.subcommand == 'sort':
        if args.daemon:
            sort_daemon(args, config)
        else:
            sort_command(args, config)
    elif args.subcommand == 'rm':
        rm_command(args, config)
    else:
        add_command(args, config)

    return 0


def sort_command(args, config):
    """entry point of the sort subcommand"""
    for elt in os.listdir(args.drop_folder):
        if elt == '.sortaconfig':
            continue

        try:
            dest = get_destination(elt, config)
            move(os.path.join(args.drop_folder, elt), dest)
            logging.info("%s moved to %s", elt, dest)
        except LookupError as e:
            logging.warning(str(e))
        except Error:
            logging.warning("error while moving the element {}".format(elt))


def sort_daemon(args, config):
    logging.info("starting sorta daemon...")

    last_time = time()
    try:
        sort_command(args, config)
        while True:
            mtime = os.path.getmtime(args.drop_folder)

            if mtime > last_time:
                sort_command(args, config)
                last_time = mtime

            sleep(config.getfloat('core', 'polling'))
    except KeyboardInterrupt:
        print()
        logging.info("stopping sorta daemon...")


def get_destination(element, config):
    """find the right destination corresponding to the element name"""
    split_prefix = element.split(config.get('core', 'delimiter'))
    split_ext = os.path.splitext(element)

    # dest = None
    # `dest` is never used in the local scope and I commented it out for you.

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


def add_command(args, config):
    """entry point of the add subcommand"""

    if args.element == 'prefix':
        config.set('prefix', args.name, os.path.expanduser(args.destination))
    else:
        config.set('extension', args.name, os.path.expanduser(args.destination))

    with open(os.path.join(args.drop_folder, '.sortaconfig'), mode='w') as configfile:
        config.write(configfile)


def rm_command(args, config):
    """entry point of the rm subcommand"""

    if args.element == 'prefix':
        config.remove_option('prefix', args.name)
    else:
        config.remove('extension', args.name, )

    with open(os.path.join(args.drop_folder, '.sortaconfig'), mode='w') as configfile:
        config.write(configfile)


def parse_args():
    """parse the arguments'"""
    parser = argparse.ArgumentParser(
        description="sorta is a program moving your files in the right folders. sorta chooses the destination of the"
                    " file based on the prefix first, and then on the extension.")
    # PEP 8: Lines shouldn't be longer than 72 characters
    # See `https://www.python.org/dev/peps/pep-0008/#maximum-line-length` for more detailed information

    parser.add_argument('-d', '--drop-folder', dest='drop_folder', type=str,
                        help='path of the folder containing the files to sort', default='~/sorta/')
    subparsers = parser.add_subparsers(dest='subcommand')

    addcmd_parser = subparsers.add_parser('add', help="add a prefix or extension to sorta")
    addcmd_parser.add_argument('element', choices=['prefix', 'ext'], help='type of element to add to the configuration')
    addcmd_parser.add_argument('name', type=str, help='name of the element (the prefix or the extension)')
    addcmd_parser.add_argument('destination', type=str,
                               help='destination of the moved file containing the prefix/extension')

    rmcmd_parser = subparsers.add_parser('rm', help="remove a prefix or extension")
    rmcmd_parser.add_argument('element', choices=['prefix', 'ext'],
                              help='type of element to remove from the configuration')
    rmcmd_parser.add_argument('name', type=str, help='name of the element (the prefix or the extension) to remove')

    sort_parser = subparsers.add_parser('sort', help="sorta file sorting")
    sort_parser.add_argument('-D', '--daemon', action='store_true', help="launch sorta in daemon mode")

    args = parser.parse_args()
    args.drop_folder = os.path.expanduser(args.drop_folder)

    return args


def create_drop_folder(path):
    """create the drop folder and the default config file at the given location"""
    os.mkdir(path)

    config = configparser.ConfigParser()
    config.add_section('core')
    config.set('core', 'delimiter', '--')
    config.set('core', 'polling', '60.0')

    config.add_section('prefix')

    config.add_section('extension')

    with open(os.path.join(path, '.sortaconfig'), mode='w') as configfile:
        config.write(configfile)


if __name__ == '__main__':
    exit(int(main() or 0))
