import os
import shutil

import img2pdf
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


def get_driver():
    options = Options()
    options.add_argument("--headless")
    service = Service(log_path=os.path.devnull)
    return webdriver.Firefox(options=options, service=service)


def img_to_pdf(manga_tom_path, manga_tom_images_path, name, img_save):
    images = [
        f"{manga_tom_images_path}/{img}" for img in
        sorted(os.listdir(manga_tom_images_path), key=lambda x: int(os.path.splitext(x)[0]))
    ]
    with open(f'{manga_tom_path}/{name}.pdf', "wb") as f:
        f.write(img2pdf.convert(images))

    if not img_save:
        shutil.rmtree(manga_tom_images_path)
