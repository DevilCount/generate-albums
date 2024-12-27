import os
from PIL import Image
from jinja2 import Template

# 定义图片目录
photos_dir = 'photos'  # 原始图片目录
thumb_dir = 'index/images/thumbs'  # 缩略图目录
full_dir = 'index/images/fulls'    # 原图目录

# 创建缩略图和原图目录
os.makedirs(thumb_dir, exist_ok=True)
os.makedirs(full_dir, exist_ok=True)

# 获取图片文件列表（支持子目录）
images = []
for root, dirs, files in os.walk(photos_dir):
    for filename in files:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            original_path = os.path.join(root, filename)
            thumb_path = os.path.join(thumb_dir, filename)
            full_path = os.path.join(full_dir, filename)

            # 生成缩略图
            with Image.open(original_path) as img:
                img.thumbnail((200, 200))  # 缩略图大小为 200x200
                img.save(thumb_path, quality=95)  # 提高压缩质量

            # 复制原图到 fulls 目录
            img = Image.open(original_path)
            img.save(full_path, quality=95)  # 提高压缩质量

            # 添加图片信息
            images.append({
                'full_path': full_path.replace('\\', '/'),  # 替换反斜杠为正斜杠
                'thumb_path': thumb_path.replace('\\', '/'),  # 替换反斜杠为正斜杠
                'title': os.path.splitext(filename)[0],  # 使用文件名作为标题
                'description': f"Description for {filename}"  # 可以替换为实际描述
            })

# 分页设置
images_per_page = 12
total_pages = (len(images) + images_per_page - 1) // images_per_page

# 将图片列表分页
paged_images = [images[i:i + images_per_page] for i in range(0, len(images), images_per_page)]

# 读取HTML模板
with open('template.html', 'r', encoding='utf-8') as file:
    template_content = file.read()

# 使用Jinja2模板引擎
template = Template(template_content)

# 生成每页的 HTML 内容
for page_num, page_images in enumerate(paged_images, start=1):
    html_content = template.render(images=page_images, current_page=page_num, total_pages=total_pages)
    if page_num == 1:
        output_file = 'index/index.html' 
    else:
        output_file = f'index/index-{page_num}.html'
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)
    print(f"相册第 {page_num} 页已生成，保存为 {output_file}")