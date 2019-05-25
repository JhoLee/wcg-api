import datetime
import os
from random import random

from PIL import Image
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

from palettable.colorbrewer.qualitative import *


def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return tuple(Dark2_8.colors[random.randint(0, 7)])


class WCG:
    def __init__(self, title, data, font, mask_image_path=None):
        self.mask_image_path = mask_image_path

        self.title = title
        self.data = data
        self.font = font

        if self.mask_image_path is not None:
            self.icon = Image.open(mask_image_path).convert("RGBA")
            self.mask_image = Image.new("RGB", self.icon.size, (255, 255, 255))
            self.mask_image.paste(self.icon, self.icon)
            self.mask_image = np.array(self.mask_image)
        else:
            self.mask_image = None

        self.file_name = "{title}_{font}.png".format(
            title=self.title, font=self.font
        )
        self.save_path = "./images/wordcloud/{file_name}".format(
            title=self.title, font=self.font, file_name=self.file_name
        )
        self.background_color = "white"
        self.result = ""

    def generate(self):
        self.result = WordCloud(background_color=self.background_color, mask=self.mask_image,
                                stopwords=STOPWORDS,
                                max_font_size=300)
        self.result.generate_from_text(self.data)

        if self.mask_image_path is not None:
            coloring = np.array(Image.open(self.mask_image_path))
            image_colors = ImageColorGenerator(coloring)
            image_colors.default_color = [0.6, 0.6, 0.6]
            self.result.recolor(None, image_colors)

        self.result.to_file(self.save_path)

        print('Result saved to \"{}"'.format(self.save_path))


        return self.file_name
