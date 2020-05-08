import pywinauto
from discord_api import DiscAPI
import vk
import getpass

from win32api import Sleep

USER_NAME = getpass.getuser()


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
    if settings[5].split(':')[1] == 'True':
        is_vk_online = True
    else:
        is_vk_online = False

    user_id = settings[6].split(':')[1]

    disc = None

    while True:
        try:
            disc = DiscAPI('697438501473615942')
            disc.connect()
            break
        except Exception as e:
            print(e)
            continue

    vk_session = None
    if is_vk_online:
        vk_session = \
            vk.create_session('', '')
    is_disc_closed = False
    title = ''
    while True:
        try:
            if is_vk_online:
                user = vk.get_user(user_id, vk_session['session'])
                print(user)
                print(user[0]['online'])
                if user[0]['online']:
                    disc.update(DiscAPI.ContentType.VK_Online, True)
                else:
                    disc.update(DiscAPI.ContentType.VK_Online, False)

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
                if is_disc_closed:
                    disc.connect()
                    is_disc_closed = False
                disc.update(DiscAPI.ContentType.YT_Video, title['title'])
            elif title['win_name'].find('смотреть онлайн') >= 0 and is_anime:
                if is_disc_closed:
                    disc.connect()
                    is_disc_closed = False
                disc.update(DiscAPI.ContentType.Anime, title['title'], 'yummyanime')
            elif title['title'] == 'Смотреть онлайн' and is_anime:
                if is_disc_closed:
                    disc.connect()
                    is_disc_closed = False
                disc.update(DiscAPI.ContentType.Anime, service='nekomori')
            else:
                disc.update(DiscAPI.ContentType.No_Action)
                disc.close()
                is_disc_closed = True

            Sleep(delay)
        except Exception as e:
            print(e)
            continue
    disc.close()


if __name__ == '__main__':
    main()
