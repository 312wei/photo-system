from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
from ultralytics import YOLO
import os
import cv2
from pathlib import Path
from collections import defaultdict

# 初始化 FastAPI 应用
app = FastAPI()

# 加载 YOLO 模型
model = YOLO("yolov8n.pt")  # 替换为实际模型路径

# 文件夹路径
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "static/outputs"  # 静态文件目录下保存检测图片
TEMPLATES_DIR = BASE_DIR / "templates"

# 确保必要的文件夹存在
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 挂载静态文件和模板目录
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """返回上传页面"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/images")
async def get_images():
    """获取已上传和检测的图片列表"""
    images = []
    output_dir = OUTPUT_DIR.glob("*")  # 遍历 outputs 文件夹
    for category_folder in output_dir:
        # 检查是否是目录
        if category_folder.is_dir():
            for image_file in category_folder.glob("*.*"):
                images.append({
                    "url": f"/static/outputs/{category_folder.name}/{image_file.name}",
                    "filename": image_file.name
                })
    return {"images": images}

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """处理上传文件并按类别分类存储"""
    results = []
    category_folders = defaultdict(list)  # 记录每个类别的文件路径

    for file in files:
        # 保存上传的文件
        upload_path = UPLOAD_DIR / file.filename
        with open(upload_path, "wb") as buffer:
            buffer.write(await file.read())

        # 执行目标检测
        detection_results = model(str(upload_path))

        # 提取检测结果
        detections = []
        image = cv2.imread(str(upload_path))
        for box in detection_results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            cls = int(box.cls[0])
            label = model.names[cls]
            confidence = float(box.conf[0])
            detections.append({"label": label, "confidence": confidence})
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, f"{label} {confidence:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # 分类存储：为每个类别创建单独的文件夹
            category_folder = OUTPUT_DIR / label
            category_folder.mkdir(parents=True, exist_ok=True)
            category_file_path = category_folder / file.filename
            cv2.imwrite(str(category_file_path), image)  # 按类别保存图片
            category_folders[label].append(str(category_file_path))

        # 保存检测结果图片到输出文件夹（不分类）
        output_path = OUTPUT_DIR / file.filename
        cv2.imwrite(str(output_path), image)

        # 添加检测结果到结果列表
        results.append({
            "filename": file.filename,
            "detections": detections,
            "output_url": f"/static/outputs/{file.filename}"
        })

    return {"results": results, "categories": dict(category_folders)}