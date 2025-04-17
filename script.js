document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("upload-form");
    const fileInput = document.getElementById("file-input");
    const progressContainer = document.getElementById("progress-container");
    const gallery = document.getElementById("image-gallery");

    // Fetch and display uploaded images
    const fetchImages = async () => {
        try {
            const response = await fetch("/images");
            const data = await response.json();
            gallery.innerHTML = ""; // 清空图片展示区域
            data.images.forEach((image) => {
                const img = document.createElement("img");
                img.src = image.url; // 设置图片 URL
                img.alt = image.filename;
                img.className = "gallery-image";
                gallery.appendChild(img);
            });
        } catch (error) {
            console.error("Error fetching images:", error);
        }
    };

    // Upload files with progress
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        const files = fileInput.files;
        if (files.length === 0) {
            alert("Please select files to upload.");
            return;
        }

        progressContainer.innerHTML = ""; // 清空进度条

        Array.from(files).forEach((file) => {
            const progressItem = document.createElement("div");
            progressItem.className = "progress-item";

            const progressBar = document.createElement("div");
            progressBar.className = "progress-bar";

            const progressBarInner = document.createElement("div");
            progressBarInner.className = "progress-bar-inner";

            progressBar.appendChild(progressBarInner);
            progressItem.appendChild(progressBar);
            progressContainer.appendChild(progressItem);

            const formData = new FormData();
            formData.append("files", file);

            const xhr = new XMLHttpRequest();
            xhr.open("POST", "/upload");

            xhr.upload.onprogress = (event) => {
                if (event.lengthComputable) {
                    const percent = (event.loaded / event.total) * 100;
                    progressBarInner.style.width = percent + "%";
                }
            };

            xhr.onload = () => {
                if (xhr.status === 200) {
                    fetchImages(); // 上传完成后刷新图片
                } else {
                    alert("Failed to upload " + file.name);
                }
            };

            xhr.send(formData);
        });
    });

    fetchImages(); // 页面加载时加载图片
});