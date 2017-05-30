"""This module contains everything needed to represent a Sorta drop folder."""

import configparser
import logging
import os
from shutil import move, Error


CONFIG_FILE_NAME = ".sortaconfig"

class DropFolder(object):
    """This class is the representation of a Sorta drop folder.

    A Sorta drop folder is a folder managed by Sorta. It must contain a .sortaconfig file. 
    The DropFolder object cannot be instantiated with an invalid drop folder
         (it will raise a FileNotFoundError).
    """

    def __init__(self, path):
        """Initialize a DropFolder object.

        :param str path: Path of the drop folder
        :raises FileNotFoundError:If the folder is not correctly initialized 
             (the given path or the .sortaconfig  doesn't exist)
        """
        self.path = path
        self.config_path = os.path.join(path, CONFIG_FILE_NAME)

        self.config = configparser.ConfigParser()
        if (not os.path.exists(self.path)) or (not os.path.exists(self.config_path)):
            raise FileNotFoundError("this folder is not correctly initialized")
        else:
            self.config.read_file(open(self.config_path))

        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)-5.5s]  %(message)s',
                        handlers=[logging.StreamHandler()])


    def _get_destination(self, element):
        """Find the right destination corresponding to the element (file or folder) name.

        :param str element: Name of the element to get the destination
        :returns str dest: The path corresponding to the prefix or extension of the element 
        :raises LookupError: If no destination has been found for the element in the config
        """
        split_prefix = element.split(self.config.get('core', 'delimiter'))
        split_ext = os.path.splitext(element)

        try:
            if len(split_prefix) == 2:
                dest = os.path.join(self.config.get('prefix', split_prefix[0]), split_prefix[1])
            elif len(split_ext) == 2:
                dest = os.path.join(self.config.get('extension', split_ext[1][1:]), element)
            else:
                raise LookupError("no destination found for the element {}".format(element))
        except configparser.NoOptionError:
            raise LookupError("no destination found for the element {}".format(element))

        return dest
    

    @staticmethod
    def init_folder(path):
        """Initialize a drop folder.

        This function creates the folder at the given path if needed, and write the default
        .sortaconfig file. If a .sortaconfig file already exists, it will be resetted
        """
        if not os.path.exists(path):
            os.mkdir(path)

        config = configparser.ConfigParser()
        config.add_section('core')
        config.set('core', 'delimiter', '--')
        config.set('core', 'polling', '60.0')

        config.add_section('prefix')

        config.add_section('extension')

        with open(os.path.join(path, CONFIG_FILE_NAME), mode='w') as configfile:
            config.write(configfile)


    def sort(self):
        """Sort the files inside the drop folder."""
        for elt in os.listdir(self.path):
            if elt == CONFIG_FILE_NAME:
                continue

            try:
                dest = self._get_destination(elt)
                move(os.path.join(self.path, elt), dest)
                logging.info("%s moved to %s", elt, dest)
            except LookupError as e:
                logging.warning(str(e))
            except Error:
                logging.warning("error while moving the element %s", elt)


    def add_rule(self, element_type, name, value):
        """Add a sorting rule to the .sortaconfig file.

        :param str element_type: Type of rule to add (['prefix'|'ext'])
        :param str name: Name of the rule
        :param str value: Destination path of the rule
        """       
        if element_type == 'prefix':
            self.config.set('prefix', name, value)
        else:
            self.config.set('extension', name, value)

        with open(self.config_path, mode='w') as configfile:
            self.config.write(configfile)


    def remove_rule(self, element_type, name):
        """Remove a rule from the .sortaconfig file.

        :param str element_type ['prefix'|'ext']) : Type of rule to add (['prefix|'ext'])
        :param name: Name of the rule

        """
        if element_type == 'prefix':
            self.config.remove_option('prefix', name)
        else:
            self.config.remove_option('extension', name)

        with open(self.config_path, mode='w') as configfile:
            self.config.write(configfile)

