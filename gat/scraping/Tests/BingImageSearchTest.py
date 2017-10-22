import sys
sys.path.insert(0, '/home/cheesecake/GAT/gat/scraping/ImageDownloader')

from Bing_Image_Search import BingScraper

BingScraper("north korea", 100).download_images()