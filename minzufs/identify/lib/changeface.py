import base64
import json
from pathlib import Path

import requests
import simplejson


def find_face(img_path):
    """
    :param img_path: 图片的地址
    :return: 一个字典类型的人脸关键点 如：{'top': 156, 'left': 108, 'width': 184, 'height': 184}
    """
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'  # 获取人脸信息的接口
    data = {
        "api_key": "x2NyKaa6vYuArYwat4x0-NpIbM9CrwGU",  # 访问url所需要的参数
        "api_secret": "OuHx-Xaey1QrORwdG7QetGG5JhOIC8g7",  # 访问url所需要的参数
        "image_url": img_path,  # 图片地址
        "return_landmark": 1
    }

    files = {'image_file': open(img_path, 'rb')}  # 定义一个字典存放图片的地址
    response = requests.post(http_url, data=data, files=files)
    res_con1 = response.content.decode('utf-8')
    res_json = simplejson.loads(res_con1)
    faces = res_json['faces']
    list1 = faces[0]
    rectangle = list1['face_rectangle']
    return rectangle


def merge_face(image_template, image_extract, number, dst_path: Path):
    """
    :param image_template: 被换脸的图片路径
    :param image_extract: 换脸的图片路径
    :param number: 换脸的相似度
    :param dst_path: 運行后的結果輸出位置
    """
    # 首先获取两张图片的人脸关键点
    face_template = find_face(image_template)
    face_extract = find_face(image_extract)
    # 将人脸转换为字符串的格式
    rectangle1 = str(
        str(face_template['top']) + "," + str(face_template['left']) + "," + str(face_template['width']) + "," + str(
            face_template['height']))
    rectangle2 = str(
        str(face_extract['top']) + "," + str(face_extract['left']) + "," + str(face_extract['width']) + "," + str(
            face_extract['height']))
    # 读取两张图片
    f1 = open(image_template, 'rb')
    f1_64 = base64.b64encode(f1.read())
    f1.close()
    f2 = open(image_extract, 'rb')
    f2_64 = base64.b64encode(f2.read())
    f2.close()

    url_add = 'https://api-cn.faceplusplus.com/imagepp/v1/mergeface'  # 实现换脸的接口
    data = {
        "api_key": "x2NyKaa6vYuArYwat4x0-NpIbM9CrwGU",
        "api_secret": "OuHx-Xaey1QrORwdG7QetGG5JhOIC8g7",
        "template_base64": f1_64,
        "template_rectangle": rectangle1,
        "merge_base64": f2_64,
        "merge_rectangle": rectangle2,
        "merge_rate": number
    }
    response1 = requests.post(url_add, data=data)
    res_con1 = response1.content.decode('utf-8')
    res_dict = json.JSONDecoder().decode(res_con1)
    result = res_dict['result']
    imgdata = base64.b64decode(result)
    # 固定变脸后的图片存放路径
    with open(dst_path, 'wb') as file:
        file.write(imgdata)
