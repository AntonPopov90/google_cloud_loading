import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from apiclient import errors
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
input_file = 'text.txt'


def create_and_upload_file(file_name='test.txt'):
    """Upload one file"""
    try:
        drive = GoogleDrive(gauth)
        my_file = drive.CreateFile({'title': f'{file_name}'})
        my_file.SetContentFile(file_name)
        my_file.Upload()
        return f'File {file_name} was uploaded!Have a good day!'
    except Exception as _ex:
        return _ex


def upload_dir(dir_path=''):
    """Upload all files from directory to new directory in Google Disk"""
    try:
        drive = GoogleDrive(gauth)
        drive.CreateFile()
        for file_name in os.listdir(dir_path):
            my_file = drive.CreateFile({
                'parents': [
                    {"id": 'your_id_from_google_apis'}
                ],
                'title': f'{file_name}',
                'mimeType': 'image/jpeg'
            })
            my_file.SetContentFile(os.path.join(dir_path, file_name))
            my_file.Upload()
            print(f'{file_name} uploaded')
        return 'Succesfully uploaded'
    except Exception as _ex:
        return _ex


def insert_permission(email='insert_your@gmail.com', type='user',role='reader'):
    print(email)
    drive = GoogleDrive(gauth)
    folder = drive.CreateFile({'id': 'your_id_from_google_apis'})
    try:
        folder.InsertPermission({
            'value': email,   ##  вставляем имейл из принятого от ТГ сообщения
            'type': type,
            'role': role
        })
        print('Prava vydany')
    except errors.HttpError as error:
        print(f'An error occurred:{error}')
    return None


def main():
    print(create_and_upload_file(file_name=f'{input_file}'))
    print(upload_dir(dir_path='/your/directictory/for_input/files'))
    print(insert_permission())


if __name__ == '__main__':
    main()
