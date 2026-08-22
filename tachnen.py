import os
from pathlib import Path
from PIL import Image
from rembg import remove, new_session

# 1. Cấu hình đường dẫn
CURRENT_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = CURRENT_DIR / "output_nobg"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 2. Cấu hình kích thước mong muốn
TARGET_WIDTH = 400

# 3. Khởi tạo session AI (Ưu tiên GPU NVIDIA RTX A2000)
# 'birefnet-general' hoặc 'u2net' tách nền caro giả rất sạch
session = new_session(
    model_name="birefnet-general",
    providers=["CUDAExecutionProvider", "CPUExecutionProvider"]
)

# Các định dạng ảnh hỗ trợ
VALID_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

# Lấy danh sách file ảnh cần xử lý
files = [
    f for f in CURRENT_DIR.iterdir()
    if f.is_file() 
    and f.suffix.lower() in VALID_EXTENSIONS 
    and not f.stem.endswith("_nobg")
]

total_files = len(files)
print(f"=== Bắt đầu xử lý {total_files} ảnh tại: {CURRENT_DIR} ===\n")

for index, file_path in enumerate(files, start=1):
    try:
        output_file_name = f"{file_path.stem}_nobg.png"
        output_path = OUTPUT_DIR / output_file_name

        with Image.open(file_path) as img:
            # Bước 1: Tách nền bằng AI
            img_nobg = remove(img, session=session)

            # Bước 2: Tính toán tỷ lệ chiều cao theo chiều rộng 400px
            orig_w, orig_h = img_nobg.size
            if orig_w != TARGET_WIDTH:
                target_height = int((TARGET_WIDTH / orig_w) * orig_h)
                # Dùng Resampling.LANCZOS để giữ độ sắc nét cao nhất
                img_resized = img_nobg.resize((TARGET_WIDTH, target_height), Image.Resampling.LANCZOS)
            else:
                img_resized = img_nobg
                target_height = orig_h

            # Bước 3: Lưu file PNG (kèm cờ optimize giảm dung lượng)
            img_resized.save(output_path, format="PNG", optimize=True)

        print(f"[{index}/{total_files}] OK: {file_path.name} -> {output_file_name} ({TARGET_WIDTH}x{target_height}px)")

    except Exception as e:
        print(f"[{index}/{total_files}] Lỗi tại {file_path.name}: {e}")

print(f"\n=== Hoàn thành! Kết quả lưu tại: {OUTPUT_DIR} ===")