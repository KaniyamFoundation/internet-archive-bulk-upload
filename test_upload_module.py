import unittest
from unittest.mock import patch, MagicMock, call
import os
import shutil
import tempfile
from upload_module import read_metadata, upload_files, print_summary, main

class TestUploadModule(unittest.TestCase):

    @patch('upload_module.csv.DictReader')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='file,identifier,title\nfile1.txt,identifier1,title1\n')
    def test_read_metadata(self, mock_open, mock_dict_reader):
        mock_dict_reader.return_value = [{'file': 'file1.txt', 'identifier': 'identifier1', 'title': 'title1'}]
        metadata = read_metadata('fake.csv')
        self.assertEqual(len(metadata), 1)
        self.assertEqual(metadata[0]['file'], 'file1.txt')

    @patch('upload_module.os.path.isfile', return_value=True)
    @patch('upload_module.shutil.move')
    @patch('upload_module.upload')
    @patch('upload_module.time.sleep')
    def test_upload_files_success(self, mock_sleep, mock_upload, mock_move, mock_isfile):
        metadata = [{'file': 'file1.txt', 'identifier': 'identifier1', 'title': 'title1'}]
        with tempfile.TemporaryDirectory() as upload_folder, tempfile.TemporaryDirectory() as success_folder, tempfile.TemporaryDirectory() as error_folder:
            # Create a dummy file
            open(os.path.join(upload_folder, 'file1.txt'), 'w').close()
            
            success_count, failed_count, errors = upload_files(metadata, upload_folder, success_folder, error_folder)
            
            self.assertEqual(success_count, 1)
            self.assertEqual(failed_count, 0)
            self.assertEqual(len(errors), 0)
            self.assertTrue(os.path.isfile(os.path.join(success_folder, 'file1.txt')))

    @patch('upload_module.os.path.isfile', return_value=True)
    @patch('upload_module.shutil.move')
    @patch('upload_module.upload', side_effect=Exception('Upload error'))
    @patch('upload_module.time.sleep')
    def test_upload_files_failure(self, mock_sleep, mock_upload, mock_move, mock_isfile):
        metadata = [{'file': 'file1.txt', 'identifier': 'identifier1', 'title': 'title1'}]
        with tempfile.TemporaryDirectory() as upload_folder, tempfile.TemporaryDirectory() as success_folder, tempfile.TemporaryDirectory() as error_folder:
            # Create a dummy file
            open(os.path.join(upload_folder, 'file1.txt'), 'w').close()
            
            success_count, failed_count, errors = upload_files(metadata, upload_folder, success_folder, error_folder)
            
            self.assertEqual(success_count, 0)
            self.assertEqual(failed_count, 1)
            self.assertEqual(len(errors), 1)
            self.assertTrue(os.path.isfile(os.path.join(error_folder, 'file1.txt')))

    @patch('upload_module.print')
    def test_print_summary(self, mock_print):
        errors = [('file1.txt', 'Some error')]
        with patch('sys.stdout', new_callable=tempfile.TemporaryFile) as mock_stdout:
            print_summary('fake.csv', 1, 1, errors)
            mock_stdout.seek(0)
            output = mock_stdout.read().decode('utf-8')
            self.assertIn('Summary for CSV file: fake.csv', output)
            self.assertIn('Success count: 1', output)
            self.assertIn('Failed count: 1', output)
            self.assertIn('File: file1.txt - Error: Some error', output)

if __name__ == '__main__':
    unittest.main()
