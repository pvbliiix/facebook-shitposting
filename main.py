import facebook
from os import listdir
from datetime import datetime
from PIL import Image
import time
import random

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


srcimages = listdir('src')
templates = sorted(listdir('templates'))

token = read_token()

fb = facebook.GraphAPI(access_token=token)

posted = 0

#what are the sizes of blank boxes you can paste images in?
#sizes = []

#insert top-left points of blank boxes here
#points = []
          
#how many source images can your template hold?
#max_srcs = []


def post_image():
    tempid = random.randint(0, len(templates) - 1)
    srcid = random.randint(0, len(srcimages) - 1)
    src = Image.open("src/" + srcimages[srcid])
    template = Image.open("templates/" + templates[tempid])
    out = Image.open("templates/" + templates[tempid])
    print("src: ", srcimages[srcid])
    print("template: ", templates[tempid])
    size_x = sizes[tempid][0]
    size_y = sizes[tempid][1]

    if max_srcs[tempid] == 1:
        if src.size[0] > size_x or src.size[1] > size_y:
            print("THUMBNAIL")
            src.thumbnail((size_x, size_y), Image.LANCZOS)
        else:
            print("RESIZE")
            hpercent = size_y / src.size[1]
            wsize = int(src.size[0] * hpercent)
            src = src.resize((wsize, size_y))

            if src.size[0] > size_x  :
                wpercent = size_x / src.size[0]
                hsize = int(src.size[1] * wpercent)
                src = src.resize((size_x, hsize))

        top_left = points[tempid]

        print("top_left: ", top_left)

        blank_x = size_x - src.size[0]
        blank_y = size_y - src.size[1]
        print("blank x: ", blank_x, "blank y: ", blank_y)
        out.paste(src, (int(top_left[0] + blank_x / 2), int(top_left[1] + blank_y / 2)))
    elif max_srcs[tempid] > 1:
        print("multi template")
        for i in range(max_srcs[tempid]):
            srcid = random.randint(0, len(srcimages) - 1)
            src = Image.open("src/" + srcimages[srcid])
            print("src: ", srcimages[srcid])
            if src.size[0] > size_x or src.size[1] > size_y:
                print("THUMBNAIL")
                src.thumbnail((size_x, size_y), Image.LANCZOS)
            else:
                print("RESIZE")
                hpercent = size_y / src.size[1]
                wsize = int(src.size[0] * hpercent)
                src = src.resize((wsize, size_y))

                if src.size[0] > size_x:
                    wpercent = size_x / src.size[0]
                    hsize = int(src.size[1] * wpercent)
                    src = src.resize((size_x, hsize))

            top_left = points[tempid][i]

            print("top_left: ", top_left)

            blank_x = size_x - src.size[0]
            blank_y = size_y - src.size[1]
            print("blank x: ", blank_x, "blank y: ", blank_y)
            out.paste(src, (int(top_left[0] + blank_x / 2), int(top_left[1] + blank_y / 2)))

    out.paste(template, (0, 0), template)
    out.save("meme.png")
    fb.put_photo(image=open('meme.png', 'rb'))


while True:
    curtime = datetime.now()
    minutes = int(time.strftime("%M"))

    if minutes % 30 == 0 and posted == 0:
        post_image()
        posted = 1
    if minutes % 30 != 0:
        posted = 0
