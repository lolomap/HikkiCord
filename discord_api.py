import pypresence as discord


class DiscAPI:
    class ContentType:
        Anime = 1
        YT_Video = 2
        IDE = 3
        No_Action = 0

    def __init__(self, app_id: str):
        self.app_id = app_id
        self.presence = None

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
                self.presence.update(details=watching_info, state=name[5:], instance=False)
            elif service == 'nekomori':
                watching_info = 'Смотрит аниме на nekomori'
                self.presence.update(details=watching_info, instance=False)
            else:
                watching_info = 'Смотрит аниме'
                self.presence.update(details=watching_info, instance=False)
            return True
        elif content_type == DiscAPI.ContentType.YT_Video:
            name = name.split(' - YouTube')[0]
            watching_info = 'Смотрит видео: '
            print(name, watching_info)
            self.presence.update(details=watching_info, state=name, instance=False)
            return True
        elif content_type == DiscAPI.ContentType.IDE:
            watching_info = 'Работает в:'
            self.presence.update(details=watching_info, state=name, instance=False)
        elif content_type == DiscAPI.ContentType.No_Action:
            watching_info = 'Ничего не делает'
            self.presence.update(details=watching_info, instance=False)
            return True
        else:
            return False
