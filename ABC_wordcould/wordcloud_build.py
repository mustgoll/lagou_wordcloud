import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS

from lagou_wordcloud.ABC_wordcould.mysql_totle_str import totle_str


def yun_word(str):
    colormask=np.array(Image.open('muban.jpg'))
    stopwords = set(STOPWORDS)
    stopwords.add("Python")
    cloud=WordCloud(background_color='#F0F8FF',
                    font_path='Dengb.ttf',
                    mask=colormask,
                    max_words=300,
                    max_font_size=300,
                    random_state=40,
                    stopwords=stopwords
                    ).generate(str)
    image_color=ImageColorGenerator(colormask)
    plt.show(cloud.recolor(color_func=image_color))
    plt.imshow(cloud)
    plt.axis('off')
    plt.show()
    cloud.to_file('detail.png')

str=totle_str()
yun_word(str)