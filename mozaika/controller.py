from flask import send_file
import requests
from PIL import Image
from io import BytesIO
from random import shuffle


def urls_to_list(urls, order):
    urls_list = urls.split(',')
    if order:
        if int(order) == 1:
            shuffle(urls_list)
    return urls_list


def resolution_params(given_params):
    if given_params:
        param = given_params.split('x')
        n_param = [int(p) for p in param]
    else:
        n_param = [2048, 2048]
    return n_param


def img_height(images_lst, parent_height):
    if len(images_lst) % 2 == 0:
        row_num = len(images_lst) // 2
    else:
        row_num = len(images_lst) // 2 + 1
    return int(parent_height / row_num)


def img_width(images_lst, parent_width):
    if len(images_lst) == 1:
        col_num = 1
    else:
        col_num = 2
    return int(parent_width / col_num)


def get_result(res, images_lst):
    result = Image.new("RGB", (res[0], res[1]))
    for index, image in enumerate(images_lst):
        img = Image.open(BytesIO(requests.get(image).content))
        w, h = result.size
        # calculating height and width of  image depending of number of images
        resize_height = img_height(images_lst, h)
        resize_width = img_width(images_lst, w)
        resized_img = img.resize((resize_width, resize_height))

        # calculating position of image
        x = index % 2 * resize_width
        y = index // 2 * resize_height

        # psting image onto canvas of result
        result.paste(resized_img, (x, y))
    return result


def send_result(resolution, images):
    result = get_result(resolution, images)
    bytes_result = BytesIO()
    result.save(bytes_result, 'JPEG', quality=70)
    bytes_result.seek(0)
    return send_file(bytes_result, mimetype='image/jpeg')
