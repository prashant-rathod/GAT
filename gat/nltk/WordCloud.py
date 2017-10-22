from os import path
from wordcloud import WordCloud
# https://github.com/amueller/word_cloud
# conda install -c https://conda.anaconda.org/amueller wordcloud

d = path.dirname(__file__)

# Read the whole text.
text = open(path.join(d, 'wordcloud_article.txt')).read()

# Generate a word cloud image
wordcloud = WordCloud(width=1600, height=800).generate(text)

# Display the generated image:
# the matplotlib way:
# import matplotlib.pyplot as plt
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis("off")

# The pil way (if you don't have matplotlib)
image = wordcloud.to_image()
image.show()
