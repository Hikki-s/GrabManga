import os


class Characteristic:
    def __init__(self, property_title, description):
        self.property_title = property_title
        self.description = description


class MangaVolume:
    def __init__(self, volume_url, volume_title):
        self.volume_url = volume_url
        self.volume_title = volume_title
        self.page_list = []

    def search_page(self):
        ...

    def download_pages(self, manga_path, sv_conf_volume):

        manga_volume_path = f'{manga_path}/{self.volume_title}'
        manga_volume_image_path = f'{manga_volume_path}/images'

        if not os.path.isdir(manga_volume_path):
            os.mkdir(manga_volume_path)

        if not os.path.isdir(manga_volume_image_path):
            os.mkdir(manga_volume_image_path)

        for page_nuber, page in self.page_list:
            with open(f"{manga_volume_image_path}/{page_nuber}.jpg", 'wb') as file:
                file.write(page)
            if sv_conf_volume:
                with open(f"{manga_volume_path}/{self.volume_title}.cfg", 'wb') as file:
                    file.writelines(f"{page}\t\n")


class Manga:
    def __init__(self, url):
        self.url = url
        self.title = None
        self.type: Characteristic | None = None
        self.format: Characteristic | None = None
        self.release_date: Characteristic | None = None
        self.status: Characteristic | None = None
        self.author: Characteristic | None = None
        self.artist: Characteristic | None = None
        self.genre: Characteristic | None = None
        self.volumes: Characteristic | None = None
        self.alter_name: Characteristic | None = None
        self.manga_volume_list = []

        self.get_info_by_url(url)

    def get_info_by_url(self, url):
        ...

    def manga_volume_append(self, *manga_volume: MangaVolume):
        for volume in manga_volume:
            self.manga_volume_list.append(volume)

    def create_manga_dir(self, manga_path):
        if not os.path.isdir(manga_path):
            os.mkdir(manga_path)

        with open(manga_path + "/info.txt", 'w+', encoding="utf-8") as file:
            file.writelines(f"{self.title}:\n")
            file.writelines(f"Link: {self.url}\n\n")
            file.writelines('\n'.join('{}:\n{}'.format(val.property_title, val.description) for key, val in self.__dict__.items() if (val is not None and isinstance(val, Characteristic))))
            file.writelines('\n'.join(self.manga_volume_list))

    def __str__(self):
        return f'{self.title}\nLink: {self.url}\n\n' + '\n'.join('{}:\n{}'.format(val.property_title, val.description) for key, val in self.__dict__.items() if val is not None and isinstance(val, Characteristic)) + '\n'.join(self.manga_volume_list)
