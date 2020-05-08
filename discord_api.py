import pypresence as discord


class DiscAPI:
    class ContentType:
        Anime = 1
        YT_Video = 2
        IDE = 3
        VK_Online = 4
        No_Action = 0

    def __init__(self, app_id: str):
        self.app_id = app_id
        self.presence = None
        self.vk_online = False

    def set_app_id(self, app_id: str):
            self.app_id = app_id

    def get_app_id(self):
        return self.app_id

    def connect(self):
        self.presence = discord.Presence(self.app_id)
        self.presence.connect()

    def close(self):
        self.presence.close()

    def reconnect(self):
        self.close()
        self.connect()

    def update(self, content_type: int, name='', service=None):
        if content_type == DiscAPI.ContentType.Anime:
            if service == 'yummyanime':
                name = name.split(' смотреть онлайн')[0]
                watching_info = 'Смотрит аниме: '
                if self.vk_online:
                    self.presence.update(details=watching_info, state=name[5:], large_image='yummy',
                                         instance=False, small_image='vk_online', small_text='Онлайн в VK')
                else:
                    self.presence.update(details=watching_info, state=name[5:], large_image='yummy',
                                         instance=False, small_image='vk_offline')
            elif service == 'nekomori':
                watching_info = 'Смотрит аниме на nekomori'
                if self.vk_online:
                    self.presence.update(details=watching_info, large_image='neko',
                                         instance=False, small_image='vk_online', small_text='Онлайн в VK')
                else:
                    self.presence.update(details=watching_info, large_image='neko',
                                         instance=False, small_image='vk_offline')
            else:
                watching_info = 'Смотрит аниме'
                if self.vk_online:
                    self.presence.update(details=watching_info, large_image='hc_icon',
                                         instance=False, small_image='vk_online', small_text='Онлайн в VK')
                else:
                    self.presence.update(details=watching_info, large_image='hc_icon',
                                         instance=False, small_image='vk_offline')
            return True
        elif content_type == DiscAPI.ContentType.YT_Video:
            name = name.split(' - YouTube')[0]
            watching_info = 'Смотрит видео: '
            print(name, watching_info)
            if self.vk_online:
                self.presence.update(details=watching_info, state=name, large_image='youtube',
                                     instance=False, small_image='vk_online', small_text='Онлайн в VK')
            else:
                self.presence.update(details=watching_info, state=name, large_image='youtube',
                                     instance=False, small_image='vk_offline')
            return True
        elif content_type == DiscAPI.ContentType.IDE:
            watching_info = 'Работает в:'
            image = ''
            if name == 'PyCharm':
                image = 'pycharm'
            elif name == 'Qt Creator':
                image = 'qt'
            elif name == 'Visual Studio':
                image = 'visual_studio'
            elif name == 'Unity':
                image = 'unity'
            elif name == 'Sublime Text':
                image = 'sublime'

            if self.vk_online:
                self.presence.update(details=watching_info, state=name, large_image=image,
                                     instance=False, small_image='vk_online', small_text='Онлайн в VK')
            else:
                self.presence.update(details=watching_info, state=name, large_image=image,
                                     instance=False, small_image='vk_offline')
        elif content_type == DiscAPI.ContentType.VK_Online:
            if name:
                self.vk_online = True
            else:
                self.vk_online = False
        elif content_type == DiscAPI.ContentType.No_Action:
            watching_info = 'Ничего не делает'
            self.presence.update(details=watching_info, large_image='hc_icon',
                                 instance=False, small_image='vk_offline')
            return True
        else:
            return False
