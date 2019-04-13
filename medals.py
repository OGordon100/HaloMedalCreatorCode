import numpy as np
import requests
import os
from bs4 import BeautifulSoup
from PIL import Image
from tqdm import tqdm


class Medals:
    def __init__(self, gamename, medal_res=150):
        allowed_gamenames = ["Halo2", "Halo3", "Halo4", "HaloReach", "all"]
        if gamename == ["all"]:
            self.gamenames = allowed_gamenames[:-1]
        else:
            self.gamenames = gamename

        self.medal_folder = "medals"
        self._lookup_website = {"Halo2": "https://www.halopedia.org/Category:Halo_2_Multiplayer_Medal_Images",
                                "Halo3": "https://halo.fandom.com/wiki/Halo_3_medals",
                                "Halo4": "https://halo.fandom.com/wiki/Halo_4_Medals",
                                "HaloReach": "https://halo.fandom.com/wiki/Halo:_Reach_Medals",
                                "Halo5": "http://halotracker.com/h5/db/medals"}
        self.medal_res = medal_res
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

    def download_medals(self, gamename):
        print(f"Downloading medals for {gamename}:")
        os.mkdir(f"{self.medal_folder}/{gamename}")

        r = requests.get(self._lookup_website[gamename])
        soup = BeautifulSoup(r.text, 'html.parser')

        # Parse appropriately
        if "fandom" in self._lookup_website[gamename]:
            images_url = self._get_from_fandom(soup)
        elif "halopedia" in self._lookup_website[gamename]:
            images_url = self._get_from_halopedia(soup)
        else:
            images_url = self._get_from_halotracker(soup)

        # Download all images and get average colour for later checking
        average_colour = np.zeros((len(images_url), 4))
        for i, url in enumerate(tqdm(images_url)):
            if "svg" not in url:
                im = Image.open(requests.get(url, stream=True).raw).convert('RGBA')
                im_resized = im.resize((self.medal_res, self.medal_res))
                im_resized.save(f"{self.medal_folder}/{gamename}/{i}.{self.format}", self.format)

                average_colour[i, :] = np.array(im).mean(axis=(0, 1))
        np.savetxt(fname=f"{self.medal_folder}/{gamename}/colours.txt",
                   X=average_colour)

    def load_medals(self):
        tot_files = 0
        for gamename in self.gamenames:
            if not os.path.isdir(f"{self.medal_folder}/{gamename}"):
                self.download_medals(gamename)

            tot_files += len(os.listdir(f"{self.medal_folder}/{gamename}")) - 1

        output_images = np.zeros((tot_files, self.medal_res, self.medal_res, 4))
        output_averages = np.zeros((0, 4))

        # Load all images as stacked numpy
        i = 0  # Can't be bothered to use itertools
        print("Loading game images into memory: ")
        with tqdm(total=tot_files) as pbar:
            for gamename in self.gamenames:
                output_averages = np.vstack((output_averages, np.loadtxt(f"{self.medal_folder}/{gamename}/colours.txt")))
                for image in os.listdir(f"{self.medal_folder}/{gamename}")[:-1]:
                    image = Image.open(f"{self.medal_folder}/{gamename}/{image}")
                    output_images[i, :, :, :] = np.array(image.getdata()).reshape(self.medal_res, self.medal_res, 4)
                    i += 1
                    pbar.update(1)

        # Return
        return output_images, output_averages
