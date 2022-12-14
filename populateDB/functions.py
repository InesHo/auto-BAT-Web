import os
from PIL import Image
import pytz
from datetime import datetime
from django.conf import settings


def Berlin_time():
    tz = pytz.timezone('Europe/Berlin')
    return datetime.now(tz)

def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def image_grid(img_list, pdf_path):
    new_image =  Image.new(mode="RGB", size=(3000,1958), color='white')
    temp_path = create_path(os.path.join(settings.MEDIA_ROOT,'temp'))
    #new_image.save(os.path.join(temp_path, 'temp.png'))
    new_image.save(os.path.join(settings.MEDIA_ROOT,'temp','temp.png'))
    width = 600
    hight = 640

    index_second_row_columns = 0
    index_second_row = 1

    index_third_row_columns = 0
    index_third_row = 2

    for i in range(0, len(img_list)):
        img_to_paste = Image.open(img_list[i])
        newsize = (width, hight)
        img_to_paste = img_to_paste.resize(newsize)
        if i < 5:
            new_image.paste(img_to_paste, (i*width, 100))
        if i >= 5 and i < 10:
            new_image.paste(img_to_paste, (index_second_row_columns*width, index_second_row*hight+100))
            index_second_row_columns +=1
        if i >= 10 and i < 15:
            new_image.paste(img_to_paste, (index_third_row_columns*width, index_third_row*hight+100))
            index_third_row_columns +=1
        
        new_image.save(os.path.join(settings.MEDIA_ROOT,'temp','temp.png'))
        
    new_image.save(pdf_path, "PDF" ,resolution=250.0)