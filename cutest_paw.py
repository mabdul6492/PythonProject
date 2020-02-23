import csv
import urllib
import time
import cv2
import os

from bs4 import BeautifulSoup
from requests_html import HTMLSession


def scrape(index, url):
    all_cats_list = []

    if not os.path.exists(f'page_folders/page_folder_{index + 1}'):
        os.makedirs(f'page_folders/page_folder_{index + 1}')

    csv_file = open(f"page_folders/page_folder_{index + 1}/cats.csv", 'w')
    csv_writer = csv.writer(csv_file, lineterminator='\n')
    csv_writer.writerow(['Title', 'Image', 'Hyperlink'])

    session = HTMLSession()
    response = session.get(url).html
    source = response.html

    soup = BeautifulSoup(source, 'lxml')
    box = soup.find('div', id="photos")
    all_cats = box.find_all('a')

    for cats in all_cats:
        try:
            image = cats.find('img')['src']
            title = cats.attrs['title']
            hyperlink = cats.attrs['href']
        except:
            pass
        all_cats_list.append((title, image, hyperlink))
        csv_writer.writerow([title, image, hyperlink])

    csv_file.close()
    return all_cats_list


def download_image(index, all_cats_list):

    if not os.path.exists(f'page_folders/page_folder_{index + 1}/images'):
        os.makedirs(f'page_folders/page_folder_{index + 1}/images')

    for i in range(len(all_cats_list)):
        try:
            urllib.request.urlretrieve(all_cats_list[i][1], f"page_folders/page_folder_{index + 1}/images/{all_cats_list[i][0]}.jpg")
        except:
            pass


def process_image(index, all_cats_list):
    # face_cascade = cv2.CascadeClassifier("classifiers/haarcascade_frontalcatface.xml")
    face_cascade = cv2.CascadeClassifier("classifiers/haarcascade_frontalcatface_extended.xml")

    if not os.path.exists(f'page_folders/page_folder_{index + 1}/filter_images'):
        os.makedirs(f'page_folders/page_folder_{index + 1}/filter_images')

    csv_file = open(f"page_folders/page_folder_{index + 1}/cats_filter.csv", 'w')
    csv_writer = csv.writer(csv_file, lineterminator='\n')
    csv_writer.writerow(['Title', 'Image', 'Hyperlink'])

    for i in range(len(all_cats_list)):
        img = cv2.imread(f"page_folders/page_folder_{index + 1}/images/{all_cats_list[i][0]}.jpg", 1)
        try:
            grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        except:
            continue
        faces = face_cascade.detectMultiScale(grey_img,
                                              scaleFactor=1.05,
                                              minNeighbors=3)

        for x, y, w, h in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + w), (0, 255, 0), 3)

        if faces != ():
            csv_writer.writerow([all_cats_list[i][0], all_cats_list[i][1], all_cats_list[i][2]])
            j = 1
            for x, y, w, h in faces:
                cropped_image = img[y:y+h, x:x+w]
                cv2.imwrite(f'page_folders/page_folder_{index + 1}/filter_images/{all_cats_list[i][0]}_croppedFace_{j}.jpg', cropped_image)
                j += 1

        cv2.imshow("Image Window", img)
        cv2.waitKey(100)
        cv2.destroyAllWindows()

    csv_file.close()


if __name__ == "__main__":

    urls = []
    pages = int(input('Enter the Number of Pages you want to Scrape: '))

    for i in range(1, pages + 1):
        urls.append(f'http://www.cutestpaw.com/tag/cats/page/{i}/')

    print(f'Urls of all the Pages : {urls}')

    for index, url in enumerate(urls):
        start = time.time()
        print(f'Page {index + 1}: {url}')
        all_cats_list = scrape(index, url)
        download_image(index, all_cats_list)
        process_image(index, all_cats_list)
        end = time.time()
        print(end - start)

    print("Thank You for Scraping with us")
