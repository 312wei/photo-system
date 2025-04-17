import os
from ultralytics import YOLO
import cv2

# 加载预训练的 YOLO 模型
model = YOLO("yolov8n.pt")  # 使用轻量化模型

# 输入图片文件夹路径
input_folder = "F:/biye_work/images"  # 替换为你的图片文件夹路径
output_folder = "F:/biye_work/output"  # 检测结果输出文件夹
os.makedirs(output_folder, exist_ok=True)  # 确保输出文件夹存在

# 支持的图片格式
SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")

# 遍历文件夹中的所有图片
for filename in os.listdir(input_folder):
    # 检查文件是否为支持的图片格式
    if filename.lower().endswith(SUPPORTED_FORMATS):
        image_path = os.path.join(input_folder, filename)
        print(f"Processing: {image_path}")

        # 执行目标检测
        results = model(image_path)

        # 打印检测结果到控制台
        detections = []
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())  # 边界框坐标
            cls = int(box.cls[0])  # 类别索引
            confidence = float(box.conf[0])  # 置信度
            label = model.names[cls]  # 类别名称
            detections.append({
                "label": label,
                "confidence": confidence,
                "bounding_box": {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
            })
        print(f"Detections for {filename}: {detections}")

        # 在图片上绘制边界框
        image = cv2.imread(image_path)
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            cls = int(box.cls[0])
            label = model.names[cls]
            confidence = float(box.conf[0])
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 绿色边界框
            cv2.putText(image, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 保存检测结果图片
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, image)
        print(f"Saved result to: {output_path}")

print("Batch processing completed.")