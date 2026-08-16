import os
import json

def generate_images_json(output_file='images.json'):
    # Lấy chính xác thư mục chứa file .py này
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        base_dir = os.getcwd()

    # Kiểm tra nếu có thư mục con 'images' thì lấy, không thì lấy thư mục chứa script
    images_dir = os.path.join(base_dir, 'images')
    if not os.path.exists(images_dir):
        images_dir = base_dir

    print(f"Đang quét tại thư mục: {images_dir}")

    # Danh sách đuôi file ảnh
    valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')

    # Lấy danh sách file ảnh
    image_files = [
        f for f in os.listdir(images_dir)
        if os.path.isfile(os.path.join(images_dir, f)) and f.lower().endswith(valid_extensions)
    ]
    image_files.sort()

    # Ghi file JSON vào cùng vị trí chạy script
    output_path = os.path.join(base_dir, output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(image_files, f, ensure_ascii=False, indent=2)

    print(f"Thành công: Đã tìm thấy {len(image_files)} file ảnh và ghi vào '{output_path}'")

if __name__ == '__main__':
    generate_images_json()