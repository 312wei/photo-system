import React, { useState, useEffect } from 'react';
import ImageUploader from './components/ImageUploader';
import ImageList from './components/ImageList';
import ImageFilter from './components/ImageFilter';
import TagManager from './components/TagManager';
import './styles/styles.css';
import { fetchImages } from './api/imageService';

function App() {
  const [images, setImages] = useState([]);
  const [filteredImages, setFilteredImages] = useState([]);
  const [selectedTags, setSelectedTags] = useState([]);

  useEffect(() => {
    // Fetch images from server
    fetchImages().then((data) => {
      setImages(data.images);
      setFilteredImages(data.images);
    });
  }, []);

  const handleUploadSuccess = (newImages) => {
    setImages([...images, ...newImages]);
    setFilteredImages([...images, ...newImages]);
  };

  const handleFilter = (searchTerm, tags) => {
    const filtered = images.filter((image) => {
      const matchesTags = tags.every((tag) => image.tags.includes(tag));
      const matchesSearch = image.filename.toLowerCase().includes(searchTerm.toLowerCase());
      return matchesTags && matchesSearch;
    });
    setFilteredImages(filtered);
  };

  return (
    <div className="app-container">
      <h1>图片素材管理系统</h1>
      <ImageUploader onUploadSuccess={handleUploadSuccess} />
      <ImageFilter onFilter={handleFilter} />
      <ImageList images={filteredImages} />
    </div>
  );
}

export default App;