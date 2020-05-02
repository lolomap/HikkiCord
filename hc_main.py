import os
import sys

import winshell
import pywinauto
from discord_api import DiscAPI
import getpass

from win32api import Sleep

USER_NAME = getpass.getuser()


def add_to_startup():
    try:
        startFile = os.path.abspath(sys.argv[0])
        startup = winshell.startup()
        winshell.CreateShortcut(
            Path=os.path.join(startup, "hikkicord.lnk"),
            Target=startFile,
            Icon=(startFile, 0),
            Description="HikkiCord",
            StartIn=os.path.abspath(None)
        )
    except Exception:
        pass


def get_title(win_name):
    try:
        win = pywinauto.findwindows.find_elements(title_re='.*'+win_name+'.*')[0]
        title = win.name
        title = title.split(' - '+win_name)[0]
        return {'title': title, 'win_name': win.name}
    except IndexError:
        return None


def get_win(win_name):
    try:
        win = pywinauto.findwindows.find_elements(title_re='.*' + win_name + '.*')[0]
        print(win)
        return True
    except IndexError:
        return False


def check_win_list(win_list):
    for item in win_list:
        if get_title(item):
            return item
    return None


def main():
    # add_to_startup()
    settings = open('settings.txt').read().split('\n')
    client_str = settings[0].split(':')[1]
    delay = int(settings[1].split(':')[1])*1000

    if settings[2].split(':')[1] == 'True':
        is_yt = True
    else:
        is_yt = False
    if settings[3].split(':')[1] == 'True':
        is_anime = True
    else:
        is_anime = False
    if settings[4].split(':')[1] == 'True':
        is_ide = True
    else:
        is_ide = False
    print(is_yt, is_anime, is_ide)

    disc = DiscAPI('697438501473615942')
    disc.connect()
    title = ''
    while True:
        if is_ide:
            ide = check_win_list(['Qt Creator', 'Visual Studio', 'Unity', 'Sublime Text', 'PyCharm'])
            if ide is not None:
                disc.update(DiscAPI.ContentType.IDE, ide)
                continue
        last_title = title
        title = get_title(client_str)
        if title == last_title or title is None:
            continue
        print(title)
        if title['win_name'].find('YouTube') >= 0 and is_yt:
            print('here')
            disc.update(DiscAPI.ContentType.YT_Video, title['title'])
        elif title['win_name'].find('смотреть онлайн') >= 0 and is_anime:
            disc.update(DiscAPI.ContentType.Anime, title['title'], 'yummyanime')
        elif title['title'] == 'Смотреть онлайн' and is_anime:
            disc.update(DiscAPI.ContentType.Anime, service='nekomori')
        else:
            disc.update(DiscAPI.ContentType.No_Action)

        Sleep(delay)
    disc.close()


if __name__ == '__main__':
    main()
