import os
from PIL import Image
import pytz
import math
from datetime import datetime
from django.conf import settings

# make sure you have the version of PyPDF2==1.26.0

from PyPDF2 import PdfFileReader, PdfFileWriter


def Berlin_time():
    tz = pytz.timezone('Europe/Berlin')
    return datetime.now(tz)

def create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def image_grid(img_list, pdf_path, analysis_type):
    temp_path = create_path(os.path.join(settings.MEDIA_ROOT,'temp'))
    width = 600
    hight = 630

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



def pdf_grid(pdf_list, export_path, analysis_type):
    pdf_writer = PdfFileWriter()
    # creating a list to specify the position of the 15 plots on the page
    # for AutoBat 3 rows and 5 columns
    autoBat_grid = [(0, 500),(240, 500),(480, 500),(720, 500),(960, 500),
                    (0, 250),(240, 250),(480, 250),(720, 250),(960, 250),
                    (0, 0),(240, 0),(480, 0),(720, 0),(960, 0)]

    # for Autograt 3 rows and 4 columns
    autoGat_grid = [(0, 500),(240, 500),(480, 500),(720, 500),
                    (0, 250),(240, 250),(480, 250),(720, 250),
                    (0, 0),(240, 0),(480, 0),(720, 0)]
    pages = 0
    last_position = 200
    """
    if analysis_type == 'comparison':
        start = 0
        end = 14
        total_plots = 0
        for i in range(0, len(pdf_list)):
            total_plots = total_plots + len(i)

        pdf_writer.addBlankPage(width=1224, height=799)
        page.scaleBy(0.70)
        if 0 <= last_position <= 4:
            j+=5
        elif 5 <= last_position <= 9:
            j+=10
        x, y = autoBat_grid[j]
    last_position = j
    """
    for i in range(0, len(pdf_list)):
        if analysis_type == 'autograt':
            start = 0
            end = 11
            total_pages = math.ceil(len(pdf_list[i]) / 12)
        else:
            start= 0
            end = 14
            total_pages = math.ceil(len(pdf_list[i]) / 15)
        total = total_pages + pages
        for indx in range(pages, total):
            #create a new page
            if analysis_type == 'autograt':
                pdf_writer.addBlankPage(width=979, height=799)
            else:
                pdf_writer.addBlankPage(width=1224, height=799)
            # specify the plots that will be printed in each page
            files = pdf_list[i][start:end+1]
            for j, file in enumerate(files):
                pdf_reader = PdfFileReader(file)
                page = pdf_reader.getPage(0)
                if "histogram" in file:
                    x, y = autoGat_grid[9]
                else:
                    page.scaleBy(0.70)
                    if analysis_type == 'autograt':
                        x, y = autoGat_grid[j]
                    else:
                        x, y = autoBat_grid[j]
                pdf_writer.getPage(indx).mergeTranslatedPage(page, x, y)
            if analysis_type == 'autograt':
                start += 12
                end +=12
            else:
                start += 15
                end +=15
        pages+=total_pages
    with open(export_path, 'wb') as export_path:
        pdf_writer.write(export_path)
    return export_path
