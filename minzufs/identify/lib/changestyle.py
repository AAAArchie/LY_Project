import cv2
import matplotlib.pyplot as plt
import paddlehub as hub


class DIY(object):
    def __init__(self, old_path, style_path):
        self.old_path = old_path
        self.style_path = style_path

    def change(self):
        stylepro_artistic = hub.Module(name="stylepro_artistic")  # 加载预训练模型 stylepro_artistic
        self.result = stylepro_artistic.style_transfer(
            images=[{
                'content': cv2.imread(self.old_path),  # 提取内容特征
                'styles': [cv2.imread(self.style_path)]  # 提取风格特征
            }],  # 利用模型中的已定义的style_transfer将content（待转换图片）与作为底色的图片相结合，
            visualization=True)  # 是否将结果保存为图片，默认为False，此处为yes

    def show(self):
        old = plt.imread(self.old_path)  # 读取old图片图像
        style = plt.imread(self.style_path)  # 读取style图片图像
        new = self.result[0]['data']
        # 展示old图片
        new = new[:, :, [2, 1, 0]]
        plt.imshow(new)
        plt.axis('off')
        plt.savefig('img.jpg', bbox_inches='tight', pad_inches=-0.1)
        plt.show()


if __name__ == '__main__':
    old_path = 'blend_res_img.jpg'
    style_path = 'nahan.jpg'
    a = DIY(old_path, style_path)
    a.change()
    a.show()
