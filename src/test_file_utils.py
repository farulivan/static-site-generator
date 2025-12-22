import unittest
import tempfile
import os
import shutil
from file_utils import copy_directory_recursive

class TestFileUtils(unittest.TestCase):
    def setUp(self):
        self.src_dir = tempfile.mkdtemp()
        self.dest_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.src_dir)
        shutil.rmtree(self.dest_dir)

    def test_copy_directory_with_nested_files_and_subdirs(self):
        # Create nested structure in src
        with open(os.path.join(self.src_dir, 'file1.txt'), 'w') as f:
            f.write('content1')
        subdir = os.path.join(self.src_dir, 'subdir')
        os.makedirs(subdir)
        with open(os.path.join(subdir, 'file2.txt'), 'w') as f:
            f.write('content2')
        subsubdir = os.path.join(subdir, 'subsubdir')
        os.makedirs(subsubdir)
        with open(os.path.join(subsubdir, 'file3.txt'), 'w') as f:
            f.write('content3')

        copy_directory_recursive(self.src_dir, self.dest_dir)

        # Assert files copied
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, 'file1.txt')))
        with open(os.path.join(self.dest_dir, 'file1.txt')) as f:
            self.assertEqual(f.read(), 'content1')
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, 'subdir', 'file2.txt')))
        with open(os.path.join(self.dest_dir, 'subdir', 'file2.txt')) as f:
            self.assertEqual(f.read(), 'content2')
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, 'subdir', 'subsubdir', 'file3.txt')))
        with open(os.path.join(self.dest_dir, 'subdir', 'subsubdir', 'file3.txt')) as f:
            self.assertEqual(f.read(), 'content3')

    def test_copy_empty_directory(self):
        copy_directory_recursive(self.src_dir, self.dest_dir)
        self.assertTrue(os.path.exists(self.dest_dir))
        self.assertEqual(os.listdir(self.dest_dir), [])

    def test_copy_nonexistent_source_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            copy_directory_recursive('nonexistent_directory', self.dest_dir)

    def test_destination_cleared_before_copy(self):
        # Add something to dest
        with open(os.path.join(self.dest_dir, 'old_file.txt'), 'w') as f:
            f.write('old content')
        os.makedirs(os.path.join(self.dest_dir, 'old_dir'))

        # Add to src
        with open(os.path.join(self.src_dir, 'new_file.txt'), 'w') as f:
            f.write('new content')

        copy_directory_recursive(self.src_dir, self.dest_dir)

        # Assert old stuff gone, new stuff there
        self.assertFalse(os.path.exists(os.path.join(self.dest_dir, 'old_file.txt')))
        self.assertFalse(os.path.exists(os.path.join(self.dest_dir, 'old_dir')))
        self.assertTrue(os.path.exists(os.path.join(self.dest_dir, 'new_file.txt')))
        with open(os.path.join(self.dest_dir, 'new_file.txt')) as f:
            self.assertEqual(f.read(), 'new content')

    def test_copy_preserves_file_permissions(self):
        # Create file with specific permissions
        test_file = os.path.join(self.src_dir, 'test.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        os.chmod(test_file, 0o644)

        copy_directory_recursive(self.src_dir, self.dest_dir)

        copied_file = os.path.join(self.dest_dir, 'test.txt')
        self.assertTrue(os.path.exists(copied_file))
        # shutil.copy2 preserves permissions, so check
        self.assertEqual(oct(os.stat(copied_file).st_mode)[-3:], '644')


if __name__ == "__main__":
    unittest.main()
