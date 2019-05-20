import datetime
from random import random

from PIL import Image
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from matplotlib import pyplot as plt

from palettable.colorbrewer.qualitative import *


def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return tuple(Dark2_8.colors[random.randint(0, 7)])


class WCG:
    def __init__(self, title, data, font, mask_image):
        self.title: str = title
        self.data: list = data
        self.font: str = font

        icon = Image.open(icon_path).comvert("RGBA")
        self.mask_image = Image.new("RGB", icon.size, (255, 255, 255))
        self.mask_image.paste(icon, icon)
        self.mask_image = mask_image.array(mask_image)

        self.save_path = "./images/wordcloud/{title}_{font}.png".format(
            title=self.title, font=self.font
        )
        self.result = ""
        self.background_color = "white"

    def generate(self):
        self.result = WordCloud(font_path=self.font, background_color=self.background_color, mask=self.mask_image,
                                stopwords=STOPWORDS,
                                max_font_size=300)
        coloring = np.array(Image.open(self.mask_image))
        image_colors = ImageColorGenerator(coloring)
        image_colors.default_color = [0.6, 0.6, 0.6]

        self.result.generate_from_text(self.data)
        self.result.recolor(None, image_colors)
        self.result.to_file(self.save_path)

        print('Result saved to \"{}"'.format(self.save_path))

        plt.imshow(self.result, interpolation='bilinear')
        plt.axis("off")
        plt.figure()
        plt.show()
