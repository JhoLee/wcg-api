import datetime
from random import random

from PIL import Image
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

from palettable.colorbrewer.qualitative import *


def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return tuple(Dark2_8.colors[random.randint(0, 7)])


current_datetime = datetime.datetime.now().strftime("%y%m%d_%H%M%S")

image = 'apple1'
icon_path = "./img/" + image + ".png"
font = "BMHANNA_11yrs_otf"
font_path = "./otf/" + font + ".otf"
data = "sample4"
data_path = "./data/" + data + ".txt"
background_color = "white"

save_path = "./result/" + image + "_" + font + "_" + data + "_" + background_color + "_" + current_datetime + ".png"
with open(data_path) as f:
    message = f.read()
    print(message)

icon = Image.open(icon_path).convert("RGBA")
mask = Image.new("RGB", icon.size, (255, 255, 255))
mask.paste(icon, icon)
mask = np.array(mask)

print(type(STOPWORDS))
STOPWORDS.add('있습니다')
STOPWORDS.add('또는')
STOPWORDS.add('귀하의')
STOPWORDS.add('귀하는')
STOPWORDS.add('귀하가')
STOPWORDS.add('다른')
STOPWORDS.add('있다')
STOPWORDS.add('있는')
STOPWORDS.add('jpg')
STOPWORDS.add('한다')
STOPWORDS.add('이러한')
STOPWORDS.add('모든')
STOPWORDS.add('경우')
STOPWORDS.add('합니다')
STOPWORDS.add('서비스')



wc = WordCloud(font_path=font_path, background_color=background_color, mask=mask, stopwords=STOPWORDS,
               max_font_size=300)

coloring = np.array(Image.open(icon_path))
image_colors = ImageColorGenerator(coloring)
image_colors.default_color = [0.6, 0.6, 0.6]

wc.generate_from_text(message)
wc.recolor(None, image_colors)
wc.to_file(save_path)
print('Result saved to \"{}"'.format(save_path))


