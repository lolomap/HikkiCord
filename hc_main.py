from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from pywinauto import Application
import pypresence as discord


def update(presence, anime_name, is_anime):
    if is_anime:
        watching_info = 'Смотрит: ' + anime_name
        presence.update(details=watching_info, instance=False)
    else:
        watching_info = 'Ничего не смотрит'
        presence.update(details=watching_info, instance=False)


def process_url(url, browser):
    if url.find('https://yummyanime.club/catalog/item/') >= 0:
        browser.get(url)
        name = browser.find_element_by_tag_name('h1').text
        print(name)
        return name
    else:
        return ''


def get_url():
    try:
        app = Application(backend='uia')
        app.connect(title_re=".*Opera.*")
        dlg = app.top_window()
        url = dlg.child_window(title="Поле адреса", control_type="Edit").get_value()
        return url
    except Exception:
        return ''


def main():

    path_driver = 'phantomjs.exe'
    browser = webdriver.PhantomJS(executable_path=path_driver)
    presence = discord.Presence('697438501473615942')
    presence.connect()

    anime_name = ''
    url = ''
    last_url = ''

    while True:
        last_url = url
        url = get_url()
        if last_url == url:
            continue
        print(url)
        anime_name = process_url(url, browser)
        if anime_name == '':
            update(presence, anime_name, False)
        else:
            update(presence, anime_name, True)


    input()

    presence.close()


if __name__ == '__main__':
    main()
