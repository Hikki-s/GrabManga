
def main_router(url):

    match url.rsplit('/', 1)[0]:
        case "https://mangalib.me":
            return "Download start"
        case _:
            return "This site is not supported or\nthere is an error in the link.\nCheck the correctness of its writing!"
