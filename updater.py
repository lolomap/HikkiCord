import distutils.dir_util

import requests
import zipfile
import shutil
import os


def main():
    try:
        latest = 'https://github.com/lolomap/HikkiCord/releases/latest/download/New.zip'
        file = requests.get(latest)
        print(file.status_code)
        with open('HikkiCord.zip', 'wb') as f:
            f.write(file.content)
        extract_file = zipfile.ZipFile('New.zip')
        extract_file.extractall('../')

        dir_check_list = [('../', '../New/'), ('../lib/', '../New/lib/'),
                          ('../bin/', '../New/bin/'), ('../bin/lib/', '../New/bin/lib/')]
        for dir_check in dir_check_list:
            del_info = open(dir_check[1]+'delete.txt').read()
            if del_info != '':
                del_list = del_info.split('\n')
                for item in del_list:
                    item_type = item.split(':')[0]
                    item_name = item.split(':')[1]
                    if item_type == 'dir':
                        shutil.rmtree(dir_check[0]+item_name)
                        print(item_name+' deleted')
                    elif item_type == 'file':
                        os.remove(dir_check[0]+item_name)
                        print(item_name+' deleted')
            os.remove(dir_check[1]+'delete.txt')

        distutils.dir_util.copy_tree('../New/', '../')

        shutil.rmtree('../New')

    except Exception as e:
        print('Fail to update: ', e)


if __name__ == '__main__':
    main()


