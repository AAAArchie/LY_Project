import time
from .predict import *
from PIL import Image


class BatchRename:
    def __init__(self):
        self.path = './media/upload_images/'  # 表示需要命名处理的文件夹

    def rename(self):
        file_list = os.listdir(self.path)  # 获取文件路径
        old_time = time.time()
        result = predict()
        for item in file_list:
            portion = list(os.path.splitext(item))  # os.path.splitext分离文件与扩展名
            if portion[1] == '.jpg' or '.png' or '.jpeg' or '.tiff' or '.raw' or '.bmp':
                src = os.path.join(os.path.realpath(self.path), item)
                for j in range(14):
                    if label[result[0]] == label[j]:
                        save_path = './media/upload_sort' + '/save_' + label2[j]
                        if not os.path.exists(os.path.realpath(save_path)):  # 若没有文件夹建造文件夹
                            os.makedirs(os.path.realpath(save_path))
                        file_list_save_num = len(os.listdir(save_path))  # 获取文件长度（个数）
                        if file_list_save_num == 0:
                            i = 0  # 表示文件的命名是从1开始的
                        else:
                            i = file_list_save_num
                        dst = os.path.join(os.path.realpath(save_path),
                                           label2[j]+'_' + str(i) + portion[1])
            os.rename(src, dst)
            # 裁剪图片大小
            im = Image.open(dst)
            # 重新设定大小
            region = im.resize((400, 400))
            region.save(dst)
            i = i + 1
            new_time = time.time()
            time_consuming = round(new_time - old_time, 2)

        return label[result[0]], label[result[1]], label[result[2]], dst, time_consuming
