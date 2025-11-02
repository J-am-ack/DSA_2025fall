import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

def images_to_pdf(image_folder, output_pdf, images_per_page=2):
    """
    将文件夹中的图片按指定数量每页生成PDF
    :param image_folder: 图片文件夹路径
    :param output_pdf: 输出PDF路径
    :param images_per_page: 每页图片数量（2或3）
    """
    # 支持的图片格式
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    # 获取文件夹中所有图片路径
    image_paths = [
        os.path.join(image_folder, f)
        for f in os.listdir(image_folder)
        if f.lower().endswith(image_extensions)
    ]
    if not image_paths:
        print("文件夹中未找到图片文件！")
        return

    # 创建PDF画布（A4尺寸）
    c = canvas.Canvas(output_pdf, pagesize=A4)
    width, height = A4  # A4尺寸：21cm × 29.7cm
    margin = 1 * cm  # 页边距
    max_img_width = (width - 2 * margin) / (2 if images_per_page in (2,3) else 1)  # 图片最大宽度
    max_img_height = (height - 2 * margin) / (1 if images_per_page <=2 else 2)  # 图片最大高度（3张时分2行）

    for i, img_path in enumerate(image_paths):
        # 每满指定数量图片换一页
        if i % images_per_page == 0:
            if i != 0:
                c.showPage()  # 新建一页
            page_idx = 0  # 重置当前页图片索引

        # 打开图片并处理尺寸（保持比例缩放）
        try:
            with Image.open(img_path) as img:
                # 计算缩放比例
                img_width, img_height = img.size
                scale = min(max_img_width / img_width, max_img_height / img_height)
                new_width = img_width * scale
                new_height = img_height * scale

                # 计算图片位置（根据每页数量排列）
                if images_per_page == 2:
                    # 横向排列2张
                    x = margin + (page_idx % 2) * (max_img_width + 0.5*cm)
                    y = height - margin - new_height
                elif images_per_page == 3:
                    # 2行排列（第一行1张居中，第二行2张）
                    if page_idx == 0:
                        x = width / 2 - new_width / 2
                        y = height - margin - new_height
                    else:
                        x = margin + ((page_idx - 1) % 2) * (max_img_width + 0.5*cm)
                        y = height - margin - new_height - max_img_height - 0.5*cm
                else:
                    raise ValueError("每页图片数量仅支持2或3")

                # 绘制图片到PDF
                c.drawImage(img_path, x, y, width=new_width, height=new_height)
                page_idx += 1
        except Exception as e:
            print(f"处理图片 {img_path} 失败：{e}")

    # 保存PDF
    c.save()
    print(f"PDF已生成：{output_pdf}")

# 配置参数（修改以下路径和数量）
if __name__ == "__main__":
    IMAGE_FOLDER = r"你的图片文件夹路径"  # 例如：r"C:\Photos"
    OUTPUT_PDF = r"输出的PDF路径"        # 例如：r"C:\result.pdf"
    IMAGES_PER_PAGE = 2  # 可选2或3

    images_to_pdf(IMAGE_FOLDER, OUTPUT_PDF, IMAGES_PER_PAGE)