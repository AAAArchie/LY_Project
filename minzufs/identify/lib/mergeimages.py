import shutil
import tempfile
from pathlib import Path
from typing import Dict

import cv2
import matplotlib.pyplot as plt
import numpy as np
import paddlehub as hub
from PIL import Image

from minzufs import settings
from .changeface import merge_face

"""
  本脚本完成了放入头像、服饰图片后，进行共同背景的替换

"""


def change_face_and_extract(template_path, extract_path, dst_path: Path):
    """
    【调用】换脸
    face_result_path 变脸存放路径
    :param template_path:
    :param extract_path:
    :param dst_path: 之後的路徑
    """
    face_path = dst_path.parent / f'{dst_path.stem}-face.png'
    merge_face(template_path, extract_path, 100, face_path)  # 将变脸返回值（变脸存放路径）赋值给 face_result_path
    # 【调用】图像分割
    test_img_path = [str(face_path)]  # 已经换脸但是待分割人像
    module = hub.Module(name="deeplabv3p_xception65_humanseg")  # 预加载图像分割模型
    input_dict = {"image": test_img_path}
    # execute predict and print the result
    results = module.segmentation(data=input_dict)  # 根据图像分割模型对待分割图像进行分割  并通过 data 保存
    for result in results:
        for key in result.keys():
            if key == "processed":
                shutil.copy(result[key], dst_path)
                # humanseg_output_path = result[key]  # 输出分割后的人像图片路径


def blend_images(fg_image: Path, bg_image: Path, ratio, pos=None, align_bottom=True):
    """
    将抠出的人物图像换背景
    :param fg_image: 前景图片，抠出的人物图片
    :param bg_image: 背景图片
    :param ratio: 调整前景的比例
    :param pos: 前景放在背景的位置的，格式为左上角坐标
    :param align_bottom: 默认使用底边对齐
    :return:
    """
    fg_image, bg_image = str(fg_image), str(bg_image)
    fg_img = cv2.imread(fg_image)  # read foreground image
    bg_img = cv2.imread(bg_image)  # read images_bg image
    height_fg, width_fg, _ = fg_img.shape  # get height and width of foreground image
    height_bg, width_bg, _ = bg_img.shape  # get height and width of images_bg image
    if ratio > (height_bg / height_fg):
        print(f'ratio is too large, use maximum ratio {(height_bg / height_fg): .2}')
        ratio = round((height_bg / height_fg), 1)
    if ratio < 0.1:
        print('ratio < 0.1, use minimum ratio 0.1')
        ratio = 0.1
    # if no pos arg input, use this as default
    if not pos:
        pos = (height_bg - int(ratio * height_fg), width_bg // 4)  # 底边对齐：hb-hf为纵坐标，//整除,背景图的1//4宽为横坐标
    elif align_bottom:
        pos = (height_bg - int(ratio * height_fg), pos[1])

    roi = bg_img[pos[0]: pos[0] + int(height_fg * ratio), pos[1]: pos[1] + int(width_fg * ratio)]  # 背景图片编辑
    cv2.imwrite("roi.jpg", roi)
    bg_image = Image.open('roi.jpg').convert('RGB')
    fg_image = Image.open(fg_image).resize(bg_image.size)
    # 图片加权合成
    scope_map = np.array(fg_image)[:, :, -1] / 255
    scope_map = scope_map[:, :, np.newaxis]
    scope_map = np.repeat(scope_map, repeats=3, axis=2)
    res_image = np.multiply(scope_map, np.array(fg_image)[:, :, :3]) + np.multiply((1 - scope_map),
                                                                                   np.array(bg_image))
    bg_img[pos[0]: pos[0] + roi.shape[0], pos[1]: pos[1] + roi.shape[1]] = np.uint8(res_image)[:, :, ::-1]
    return bg_img


def merge_fn_path(person_extract_path: Path, src: Path, ratio, pos, del_image, dst: Path):
    """
    保存最终合成图片
    :param person_extract_path: 切割出来的人像路径（要合成到背景的图片路径）
    :param src: 背景图片路径
    :param ratio: 调整前景的比例
    :param pos: 前景放在背景的位置的，格式为左上角坐标
    :param del_image:下一张图片合到同一张背景时，是否覆盖前一张
    :param dst: 合成后的图像的生成位置
    :return: 返回背景替换后的路径
    """
    plt.figure(figsize=(10, 10))
    img = blend_images(person_extract_path, src, ratio, pos, align_bottom=True)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.axis('off')  # 去坐标轴
    plt.savefig(dst, bbox_inches='tight', pad_inches=-0.1)
    return dst


BACKGROUND_IMAGE_DIR = Path(settings.MEDIA_ROOT) / 'background-image'
BACKGROUND_LIST: Dict[str, Path] = {f'bg{i}': BACKGROUND_IMAGE_DIR / f'bg{i}.png' for i in range(1, 7)}


def merge_images(template_path1: str, extract_path1: str, template_path2: str, extract_path2: str,
                 background_name: str):
    """
    合成两张人像分割结果图片到背景
    :param template_path1: 第一个接受换人脸的图片路径
    :param extract_path1: 第一个提取的人脸图片路径
    :param template_path2: 第二个接受换人脸的图片路径
    :param extract_path2: 第二个提取的人脸图片路径
    :param background_name: 背景图片的名称，只能再有限的给定的选项中进行选择
    :return: 二进制的图片数据
    """

    with tempfile.TemporaryDirectory(prefix='minzufs-merge-image') as directory:
        directory = Path(directory)

        # 分割后的人像图片存放路径（前景图片）
        face_1_output_path = directory / 'face1.png'
        change_face_and_extract(template_path1, extract_path1, face_1_output_path)
        face_2_output_path = directory / 'face2.png'
        change_face_and_extract(template_path2, extract_path2, face_2_output_path)  # 分割后的人像图片存放路径（前景图片）

        src, dst = BACKGROUND_LIST[background_name], directory / 'first.png'
        ratio = 0.5
        pos = (50, 230)
        merge_fn_path(face_1_output_path, src, ratio, pos, False, dst)
        src, dst = dst, directory / 'second.png'
        ratio = 0.7
        pos = (50, 80)
        merge_fn_path(face_2_output_path, src, ratio, pos, True, dst)
        with open(dst, 'rb') as f:
            content = f.read()
    return content


def test():
    # 背景提供列表,增加相应路径字段即可
    face_template_path1 = "clothes1.png"  # 这里再调整成数据库提取出来的路径 把face_extract_path的脸换到face_template_path图片中的脸上去
    face_extract_path1 = "face1.png"
    face_template_path2 = "clothes2.png"  # 这里再调整成数据库提取出来的路径 把face_extract_path的脸换到face_template_path图片中的脸上去
    face_extract_path2 = "face2.png"
    content = merge_images(face_template_path1, face_extract_path1, face_template_path2, face_extract_path2, 'sea')
    with open('result.png', 'wb') as f:
        f.write(content)


if __name__ == '__main__':
    test()
