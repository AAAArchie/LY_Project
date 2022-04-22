import os
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from django.conf import settings
from tensorflow.keras.backend import clear_session
from tensorflow.keras.models import load_model

ROWS = 224
COLS = 224
CHANNELS = 3

label = {
    0: '苗族', 1: '彝族', 2: '革家族', 3: '蒙古族', 4: '朝鲜族',
    5: '藏族', 6: '满族', 7: '汉服', 8: '壮族', 9: '回族',
    10: '羌族', 11: '傣族', 12: '白族', 13: '畲族', 14: '黎族',
}

label2 = {
    0: 'miao', 1: 'yi', 2: 'gejia', 3: 'menggu', 4: 'chaoxian',
    5: 'zang', 6: 'man', 7: 'han', 8: 'zhuang', 9: 'hui',
    10: 'qiang', 11: 'dai', 12: 'bai', 13: 'she', 14: 'li',
}


def read_image(file_path):
    path = Path(file_path)
    img = np.array(Image.open(path))
    img = img[:, :, [2, 1, 0]]
    return cv2.resize(img, (ROWS, COLS), interpolation=cv2.INTER_CUBIC)


def predict():
    test_dir = './media/upload_images/'
    clear_session()  # 清理浏览器的session对象
    model_dir = Path(settings.BASE_DIR) / 'trained_model'
    model_dir.mkdir(exist_ok=True, parents=True)
    model_path = str(model_dir / 'Dense2018983.h5')
    model = load_model(model_path, compile=False)
    test_images = [test_dir + i for i in os.listdir(test_dir)]  # 列表生成式，逐个字母生成路径  os.listdir输出path下的各种文件
    count = len(test_images)
    data = np.ndarray((count, ROWS, COLS, CHANNELS), dtype=np.uint8)  # data-type 数组中元素的类型
    for i, image_file in enumerate(test_images):
        # 获取测试图片文件，并进行处理enumerate() 函数用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标，一般用在 for 循环当中。
        image = read_image(image_file)
        data[i] = image
    test = data

    # 模型预测,输入测试集,输出预测结果  输出预测概率
    predictions = model.predict(test / 127.5 - 1)
    length = len(predictions)
    for i in range(length):
        result = []
        for j in range(3):
            pos = np.argmax(predictions[i])
            result.append(pos)
            predictions[i][pos] = -1
    return result
