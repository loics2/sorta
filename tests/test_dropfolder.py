import os
import unittest

from sorta.drop_folder import DropFolder


class DropFolderTest(unittest.TestCase):

    def test_initializing_sorta_drops_config_if_path_does_not_exist(self):
        test_dir = os.path.join(os.getcwd(), 'test_dir')
        DropFolder.init_folder(test_dir)

        self.assertIn('.sortaconfig', os.listdir(test_dir))

        test_file = os.path.join(test_dir, '.sortaconfig')
        os.remove(test_file)
        os.rmdir('test_dir')        

    def test_dropfolder_raises_FileNotFoundError_with_bad_path(self):
        with self.assertRaises(FileNotFoundError):
            dropfolder = DropFolder('bad_path')

    def test_dropfolder_raises_FileNotFoundError_with_uninitialized_folder(self):
        os.mkdir('test_folder')
        with self.assertRaises(FileNotFoundError):
            dropfolder = DropFolder('test_folder')

        os.rmdir('test_folder')

if __name__ == "__main__":
    unittest.main()
