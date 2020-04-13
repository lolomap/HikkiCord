import os
import sys

import winshell
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pywinauto import Application
import pypresence as discord
import getpass
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


def update_anime(presence, anime_name, is_anime, url=None):
    if is_anime:
        watching_info = 'Смотрит аниме: ' + anime_name
        if url is None:
            return
        presence.update(details=watching_info, instance=False)
    else:
        watching_info = 'Ничего не делает'
        presence.update(details=watching_info, instance=False)


def update_ytvideo(presence, video_name, is_video, url=None):
    if is_video:
        watching_info = 'Смотрит видео: ' + video_name
        if url is None:
            return
        presence.update(details=watching_info, instance=False)
    else:
        watching_info = 'Ничего не делает'
        presence.update(details=watching_info, instance=False)


def process_url(url, browser, client):
    if url.find('yummyanime.club/catalog/item/') >= 0:
        browser.get(url)
        name = browser.find_element_by_tag_name('h1').text
        print(name)

        return {'name': name, 'type': 'anime'}
    elif url.find('youtube.com/watch?') >= 0:
        browser.get(url)
        hname = browser.find_elements_by_tag_name('h1')
        print(hname)
        if client == 'opera':
            name = hname[1].text
        elif client == 'chrome':
            name = hname[0].text
        else:
            return None
        print(name)
        return {'name': name, 'type': 'yt_video'}
    else:
        return None


def get_url(client):
    try:
        if client == 'opera':
            app = Application(backend='uia')
            app.connect(title_re=".*Opera.*")
            dlg = app.top_window()
            url = dlg.child_window(title="Поле адреса", control_type="Edit").get_value()
            if url is None:
                return ''
            return url
        elif client == 'chrome':
            app = Application(backend='uia')
            app.connect(title_re=".*Google Chrome.*")
            dlg = app.top_window()
            url = dlg.child_window(title="Адресная строка и строка поиска", control_type="Edit").get_value()
            if url is None:
                return ''
            return url
    except Exception as e:
        print(e)
        return None


def main():
    add_to_startup()

    settings = open('settings.txt')
    client = settings.read()

    if client == 'opera':
        path_driver = 'phantomjs.exe'
        browser = webdriver.PhantomJS(executable_path=path_driver, service_log_path=None)
    elif client == 'chrome':
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--window-size=1920x1080')
        path_driver = 'chromedriver.exe'
        browser = webdriver.Chrome(executable_path=path_driver, service_log_path=None, options=chrome_options)
    else:
        return

    presence = discord.Presence('697438501473615942')

    url = ''
    closed = True
    while True:
        last_url = url
        url = get_url(client)
        if last_url == url:
            continue
        if url is None and not closed:
            presence.close()
            closed = True
            continue
        elif closed:
            presence.connect()
            closed = False
        print(url)
        if url is None:
            continue
        if client == 'opera':
            anime_info = process_url(url, browser, client)
        elif client == 'chrome':
            anime_info = process_url('http://'+url, browser, client)
        else:
            return
        name = None
        content_type = None
        if anime_info is not None:
            name = anime_info['name']
            content_type = anime_info['type']
        if name is None:
            update_anime(presence, name, False)
        elif content_type == 'anime':
            update_anime(presence, name, True, url)
        elif content_type == 'yt_video':
            update_ytvideo(presence, name, True, url)
        else:
            continue

    presence.close()


if __name__ == '__main__':
    main()
