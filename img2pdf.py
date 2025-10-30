import os
import img2pdf
from PIL import Image

def images_to_pdf(image_folder, output_pdf="output.pdf"):
    """
    将文件夹中的所有图片合并为一个PDF
    :param image_folder: 图片文件夹路径
    :param output_pdf: 输出PDF文件名
    """
    # 支持的图片格式
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
    
    # 获取文件夹中所有图片路径，并按文件名排序
    image_paths = []
    for filename in sorted(os.listdir(image_folder)):
        if filename.lower().endswith(image_extensions):
            img_path = os.path.join(image_folder, filename)
            image_paths.append(img_path)
    
    if not image_paths:
        print("错误：未找到图片文件！")
        return
    
    # 处理图片（确保格式兼容，转换为RGB避免透明通道问题）
    processed_images = []
    for img_path in image_paths:
        try:
            with Image.open(img_path) as img:
                # 转换为RGB（png透明图会转为白色背景）
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new(img.mode[:-1], img.size, (255, 255, 255))
                    background.paste(img, img.split()[-1])
                    img = background
                # 保存为临时JPG（避免格式问题）
                temp_path = f"temp_{os.path.basename(img_path)}.jpg"
                img.convert('RGB').save(temp_path)
                processed_images.append(temp_path)
        except Exception as e:
            print(f"处理图片 {img_path} 失败：{e}")
    
    # 生成PDF
    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(processed_images))
    
    # 清理临时文件
    for temp in processed_images:
        if os.path.exists(temp):
            os.remove(temp)
    
    print(f"PDF生成成功：{os.path.abspath(output_pdf)}")

# 使用示例（替换为你的图片文件夹路径）
if __name__ == "__main__":
    image_folder = input("请输入图片文件夹路径：").strip()
    images_to_pdf(image_folder)
    


# useless

