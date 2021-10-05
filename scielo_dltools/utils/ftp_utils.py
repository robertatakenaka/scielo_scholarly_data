# coding=utf-8
from ftplib import FTP
import os


def get_files(server, user, password, local_path,
              timeout=30,
              remote_path=None, prefix=None, delete_remote=False,
              ):
    if not os.path.isdir(local_path):
        os.makedirs(local_path)
    os.chdir(local_path)

    with FTP(server, user, password, timeout=timeout) as ftp:

        # muda de diretório se não é na raiz
        if remote_path:
            ftp.cwd(remote_path)

        # filtra documentos
        files_or_folders = ftp.nlst()
        if prefix:
            files_or_folders = [
                item
                for item in files_or_folders
                if item.startswith(prefix)
            ]

        # transfere e apaga os arquivos
        transfered_files = []
        for file_name in files_or_folders:
            try:
                ftp.retrbinary(
                    f'RETR {file_name}', open(file_name, 'wb').write)

                local_file_path = os.path.join(local_path, file_name)
                if _is_transfered(ftp, local_file_path, file_name):
                    transfered_files.append(local_file_path)
                    if delete_remote:
                        ftp.delete(file_name)
            except IOError:
                pass
        return transfered_files


def put_file(server, user, password, local_file_path,
             timeout=30,
             remote_path=None,
             ):

    try:
        with FTP(server, user, password, timeout) as ftp:
            # muda de diretório se não é na raiz
            if remote_path:
                ftp.cwd(remote_path)

            # remote name
            remote_name = os.path.basename(local_file_path)

            # transfer
            with open(local_file_path, 'rb') as fp:
                ftp.storbinary(f'STOR {remote_name}', fp)

            # return True if transfered
            return _is_transfered(ftp, local_file_path, remote_name)
    except IOError:
        return False


def _is_transfered(ftp, local_file_path, remote_name):
    try:
        statinfo = os.stat(local_file_path)
        return statinfo.st_size == ftp.size(remote_name)
    except IOError:
        return False


