import React from 'react';

const ImageList = ({ images }) => {
  return (
    <div className="image-list">
      <h2>图片列表</h2>
      <ul>
        {images.map((image) => (
          <li key={image.filename}>
            <img src={`http://localhost:8000/images/${image.filename}`} alt={image.filename} />
            <p>{image.filename}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ImageList;