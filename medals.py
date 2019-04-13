import numpy as np
import requests
import os
from bs4 import BeautifulSoup
from PIL import Image
from tqdm import tqdm

class Medals:
    def __init__(self, gamename):
        allowed_gamenames = ["Halo 2", "Halo 3", "Halo 4", "Halo 5", "Halo Reach"]
        if gamename not in allowed_gamenames:
            raise KeyError(f"gamename must be one of {allowed_gamenames}")

        self.gamename = gamename
        self.medal_folder = "medals"
        self._lookup_website = {"Halo 2": "https://www.halopedia.org/Category:Halo_2_Multiplayer_Medal_Images",
                                "Halo 3": "https://halo.fandom.com/wiki/Halo_3_medals",
                                "Halo 4": "https://halo.fandom.com/wiki/Halo_4_Medals",
                                "Halo Reach": "https://halo.fandom.com/wiki/Halo:_Reach_Medals",
                                "Halo 5": "http://halotracker.com/h5/db/medals"}
        self.medal_res = 100
        self.format = "PNG"

    def _get_from_fandom(self, soup):
        soup_parsed = soup.find_all(class_="image image-thumbnail")
        images_url = [tag["href"] for tag in soup_parsed]

        return images_url

    def _get_from_halopedia(self, soup):
        soup_parsed = soup.find_all("img")
        images_url = ["https://www.halopedia.org" + tag["src"] for tag in soup_parsed if "class" not in tag.attrs]

        return images_url

    def _get_from_halotracker(self, soup):
        raise NotImplementedError

    def download_medals(self):
        if not os.path.isdir(f"{self.medal_folder}/{self.gamename}"):
            print("Getting medals...")
            os.mkdir(f"{self.medal_folder}/{self.gamename}")

            r = requests.get(self._lookup_website[self.gamename])
            soup = BeautifulSoup(r.text, 'html.parser')

            # Parse appropriately
            if "fandom" in self._lookup_website[self.gamename]:
                images_url = self._get_from_fandom(soup)
            elif "halopedia" in self._lookup_website[self.gamename]:
                images_url = self._get_from_halopedia(soup)
            else:
                images_url = self._get_from_halotracker(soup)

            # Download all images and get average colour for later checking
            average_colour = np.zeros((len(images_url), 4))
            for i, url in enumerate(tqdm(images_url)):
                if "svg" not in url:
                    im = Image.open(requests.get(url, stream=True).raw).convert('RGBA')
                    im_resized = im.resize((self.medal_res, self.medal_res))
                    im_resized.save(f"{self.medal_folder}/{self.gamename}/{i}.{self.format}", self.format)

                    average_colour[i, :] = np.array(im).mean(axis=(0, 1))
            np.savetxt(fname=f"{self.medal_folder}/{self.gamename}/colours.txt",
                       X=average_colour)
