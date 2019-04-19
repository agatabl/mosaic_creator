from flask import send_file, render_template, Response
import requests
from PIL import Image
from io import BytesIO
from random import shuffle
from werkzeug import FileWrapper


def urls_to_list(urls, order):
    urls_list = urls.split(',')
    if order:
        try:
            if int(order) == 1:
                shuffle(urls_list)
        finally:
            return urls_list
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


def get_image(img_url):
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        return img


def get_croped_image(image, index, source_height, source_width):

        img_w, img_h = image.size

        width_ratio = img_w / source_width
        height_ratio = img_h / source_height

        ratio = min(width_ratio, height_ratio)

        new_height = ratio * source_height
        new_width = ratio * source_width

        height_diff = img_h - new_height
        width_diff = img_w - new_width

        left = 0 + (width_diff / 2)
        upper = 0 + (height_diff / 2)
        right = img_w - (width_diff / 2)
        down = img_h - (height_diff / 2)

        crop_img = image.crop((left, upper, right, down))

        return crop_img


def get_result(res, images_lst):
    result = Image.new("RGB", (res[0], res[1]))
    result_w, result_h = result.size
    final_height = img_height(images_lst, result_h)
    final_width = img_width(images_lst, result_w)

    for index, image in enumerate(images_lst):
        img = get_image(image)
        if index == (len(images_lst) - 1) and index != 0 and index % 2 == 0:
            final_width = 2 * final_width
        crop_img = get_croped_image(img, index, final_height, final_width)
        final_photo = crop_img.resize((final_width, final_height))
        # calculating position of image
        x = index % 2 * final_width
        y = index // 2 * final_height
        # psting image onto canvas of result
        result.paste(final_photo, (x, y))
    return result


def send_result(resolution, images):
    try:
        result = get_result(resolution, images)
        bytes_result = BytesIO()
        result.save(bytes_result, 'JPEG', quality=70)
        bytes_result.seek(0)
        file = FileWrapper(bytes_result)
        return Response(file, mimetype='image/jpeg', direct_passthrough=True)
        # return send_file(bytes_result, mimetype='image/jpeg')
    except requests.exceptions.RequestException as e:
        print(e)
        return render_template('error.html')
