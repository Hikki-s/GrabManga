from app.manga_scripts.сlasses.manga import Manga, Characteristic, MangaVolume
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests as requests
from tkinter import messagebox
import re

pattern = re.compile(r'[\\/:*?"<>.|~]')


class MangaVolumeLib(MangaVolume):
    def search_page(self, driver):
        driver.get(url=self.volume_url)
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        count_pages = \
            soup.find('label', class_='button reader-pages__label reader-footer__btn').find('span').text.split()[-1]
        for page_nuber in range(1, int(count_pages) + 1):
            driver.get(url=f"{self.volume_url}&page={page_nuber}")
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            page_img_url = soup.select("div.reader-view__wrap:not(.hidden) img").pop()['src']
            self.page_list.append(requests.get(page_img_url).content)


class MangaLib(Manga):
    def get_info_by_url(self, url):
        with self.driver as driver:
            driver.get(url=url)
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            tags = soup.find('div', class_='media-sidebar')

            self.title = pattern.sub('', soup.find('div', class_='media-name__main').text)

            media_info = list(zip([item.text for item in tags.findAll('div', class_='media-info-list__title')],
                                  [item.text.strip() for item in tags.findAll('div', class_='media-info-list__value')]))
            first_value_manga_url = tags.find('div', class_='media-sidebar__buttons').find('a')['href']

            driver.get(url=first_value_manga_url)
            element = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/div")
            element.click()
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            manga_book_list = reversed(
                [MangaVolumeLib((pattern.sub('', " ".join(item.text.split()))).strip(), f'{url.rsplit("/", 1)[0]}{item["href"]}') for item in
                 soup.findAll('a', class_='menu__item')])
            self.manga_volume_append(*manga_book_list)

            for property_title, description in media_info:
                characteristic = Characteristic(property_title, description)
                match property_title:
                    case 'Тип':
                        self.type = characteristic
                    case 'Формат выпуска':
                        self.format = characteristic
                    case 'Год релиза':
                        self.release_date = characteristic
                    case 'Статус тайтла':
                        self.status = characteristic
                    case 'Статус перевода':
                        self.translate_status = characteristic
                    case 'Художник':
                        self.artist = characteristic
                    case 'Издательство':
                        self.publishing = characteristic
                    case 'Возрастной рейтинг':
                        self.age_rating = characteristic
                    case 'Альтернативные названия':
                        self.alter_name = characteristic
        messagebox.showinfo('Alert', f'Download {self.title} finished')


