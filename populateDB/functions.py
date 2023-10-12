import os
from PIL import Image
import pytz
import math
from datetime import datetime
from django.conf import settings


def Berlin_time():
    tz = pytz.timezone('Europe/Berlin')
    return datetime.now(tz)

def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def image_grid(img_list, pdf_path, analysis_type):
    temp_path = create_path(os.path.join(settings.MEDIA_ROOT,'temp'))
    width = 600
    hight = 640

    total_images = len(img_list)
    if analysis_type == 'autograt':
        total_pages = math.ceil(total_images / 12)
        width = 600
        hight = 600

        img_from = 0
        img_to = 12

    else:
        total_pages = math.ceil(total_images / 15)
        img_from = 0
        img_to = 15
    page_list=[]
    for page in range(1, total_pages+1):
        if analysis_type == 'autograt':
            new_image =  Image.new(mode="RGB", size=(2400,1958), color='white')
        else:
            new_image =  Image.new(mode="RGB", size=(3000,1958), color='white')
        imgs = img_list[img_from:img_to]
        new_image.save(os.path.join(settings.MEDIA_ROOT,'temp',f'temp_{page}.png'))
        index_second_row_columns = 0
        index_second_row = 1
        index_third_row_columns = 0
        index_third_row = 2
        for i in range(0, len(imgs)):
            img_to_paste = Image.open(imgs[i])
            newsize = (width, hight)
            img_to_paste = img_to_paste.resize(newsize)
            if analysis_type == 'autograt':
                if i < 4:
                    new_image.paste(img_to_paste, (i*width, 100))
                if i >= 4 and i < 8:
                    new_image.paste(img_to_paste, (index_second_row_columns*width, index_second_row*hight+100))
                    index_second_row_columns +=1
                if i >= 8 and i < 12:
                    new_image.paste(img_to_paste, (index_third_row_columns*width, index_third_row*hight+100))
                    index_third_row_columns +=1

            else:
                if i < 5:
                    new_image.paste(img_to_paste, (i*width, 100))
                if i >= 5 and i < 10:
                    new_image.paste(img_to_paste, (index_second_row_columns*width, index_second_row*hight+100))
                    index_second_row_columns +=1
                if i >= 10 and i < 15:
                    new_image.paste(img_to_paste, (index_third_row_columns*width, index_third_row*hight+100))
                    index_third_row_columns +=1

            new_image.save(os.path.join(settings.MEDIA_ROOT,'temp',f'temp_{page}.png'))

        page_path = os.path.join(settings.MEDIA_ROOT,'temp',f'temp_{page}.png')
        page_path = Image.open(page_path)
        page_path = page_path.convert('RGB')
        page_list.append(page_path)
        if analysis_type == 'autograt':
            img_from+=12
            img_to+=12
        else:
            img_from+=15
            img_to+=15

            
    image_1 = Image.open(os.path.join(settings.MEDIA_ROOT,'temp',f'temp_1.png'))
    image_1.save(pdf_path, "PDF", append_images=page_list[1:], save_all=True,resolution=250.0) 
    return page_list
