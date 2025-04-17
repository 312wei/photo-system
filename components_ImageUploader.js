import React, { useState } from 'react';
import { uploadImages } from '../api/imageService';

const ImageUploader = ({ onUploadSuccess }) => {
  const [files, setFiles] = useState([]);

  const handleFileChange = (event) => {
    setFiles(event.target.files);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    Array.from(files).forEach((file) => formData.append('files', file));

    const uploadedFiles = await uploadImages(formData);
    onUploadSuccess(uploadedFiles);
  };

  return (
    <div className="image-uploader">
      <h2>上传图片</h2>
      <input type="file" multiple onChange={handleFileChange} />
      <button onClick={handleUpload}>上传</button>
    </div>
  );
};

export default ImageUploader;