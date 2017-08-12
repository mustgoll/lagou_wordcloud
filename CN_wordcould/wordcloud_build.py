import matplotlib.pyplot as plt
import numpy as np
import jieba
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS

from lagou_wordcloud.CN_wordcould.mysql_totle_str import totle_str


def yun_word(str):
    colormask=np.array(Image.open('muban.jpg'))
    cut_str=' '.join(jieba.cut(str,cut_all=False))
    stopwords = set(STOPWORDS)
    stopwords.update(["要求",'以上学历','进行','常用','产品','以上','职位','描述','开发','岗位职责','任职','优先','岗位','岗位职责','负责'])
    cloud=WordCloud(background_color='#F0F8FF',
                    font_path='Dengb.ttf',
                    mask=colormask,
                    max_words=300,
                    max_font_size=300,
                    random_state=40,
                    stopwords=stopwords
                    ).generate(cut_str)
    image_color=ImageColorGenerator(colormask)
    plt.show(cloud.recolor(color_func=image_color))
    plt.imshow(cloud)
    plt.axis('off')
    plt.show()
    cloud.to_file('detail.png')

str=totle_str()
yun_word(str)