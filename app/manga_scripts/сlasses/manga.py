import os
import re
import shutil
import threading

from PyPDF2 import PdfMerger
import img2pdf
from app.config.config import config
from app.manga_scripts.tools.tools import get_driver


class Characteristic:
    def __init__(self, property_title, description):
        self.property_title = property_title
        self.description = description


class MangaVolume:
    def __init__(self, volume_title, volume_url):
        self.volume_title = volume_title
        self.volume_url = volume_url
        self.page_list = []

    def search_page(self, driver):
        ...

    def download_pages(self, volume_index, manga_path):

        manga_volume_path = f'{manga_path}/{volume_index}'
        manga_volume_image_path = f'{manga_volume_path}/images'

        if not os.path.isdir(manga_volume_path):
            os.mkdir(manga_volume_path)

        if not os.path.isdir(manga_volume_image_path):
            os.mkdir(manga_volume_image_path)

        for index in range(0, len(self.page_list)):
            with open(f'{manga_volume_image_path}/{index}.jpg', 'wb') as file:
                file.write(self.page_list[index])

            if False:
                with open(f'{manga_volume_path}/{self.volume_title}.cfg', 'wb') as file:
                    file.writelines(f'{page}\t\n')


class Manga:

    def __init__(self, url):
        self.url = url
        self.title = None
        self.type = None
        self.format = None
        self.release_date = None
        self.status = None
        self.translate_status = None
        self.publishing = None
        self.age_rating = None
        self.author = None
        self.artist = None
        self.genre = None
        self.volumes = None
        self.alter_name = None
        self.manga_volume_list = []
        self.manga_path = config.get('Settings', 'save_path')
        self.driver = get_driver()
        self.get_info_by_url(url)

    def get_info_by_url(self, url):
        ...

    def manga_volume_append(self, *manga_volume: MangaVolume):
        for index, volume in enumerate(manga_volume, start=1):
            self.manga_volume_list.append(volume)
            self.download_manga(index, volume)
            print(index)

    def download_manga(self, index, volume):
        volume.search_page(self.driver)
        volume.download_pages(index, self.manga_path)
        process = threading.Thread(target=self.img_to_pdf, args=(index,))
        process.start()

    def img_to_pdf(self, volume_index):
        manga_volume_path = os.path.join(self.manga_path, str(volume_index))
        manga_volume_image_path = os.path.join(manga_volume_path, 'images')
        images = [
            os.path.join(manga_volume_image_path, img) for img in
            sorted(os.listdir(manga_volume_image_path), key=lambda x: int(os.path.splitext(x)[0]))
        ]
        with open(os.path.join(manga_volume_path, f'{volume_index}-{self.title}.pdf'), 'wb') as f:
            f.write(img2pdf.convert(images))

        if not config.getboolean('Settings', 'save_images'):
            shutil.rmtree(manga_volume_image_path)

    def pdf_merge(self):

        if not config.getboolean('Settings', 'pdf_merge'):
            return
        merger = PdfMerger()
        allpdfs = [os.path.join(self.manga_path, str(index), f'{index}-{self.title}.pdf') for index in
                   os.listdir(self.manga_path)]
        allpdfs.sort(key=lambda f: int(re.sub('\D', '', f)))
        [merger.append(pdf) for pdf in allpdfs]
        with open(os.path.join(self.manga_path, f'Full_{self.title}.pdf'), "wb") as new_file:
            merger.write(new_file)

    def create_manga_dir(self):
        if not os.path.isdir(self.manga_path):
            os.mkdir(self.manga_path)

    def create_manga_info(self):
        with open(os.path.join(self.manga_path, 'info.txt'), 'w+', encoding='utf-8') as file:
            file.writelines(f'{str(self)}')

    def __str__(self):
        return f'{self.title}\nLink: {self.url}\n\n' + \
            '\n'.join('{}:\n{}\n'.format(val.property_title, val.description) for key, val in self.__dict__.items()
                      if val is not None and isinstance(val, Characteristic)) + \
            '\n' + '\n'.join('{}:\n{}\n'.format(item.volume_title, item.volume_url) for item in self.manga_volume_list)
