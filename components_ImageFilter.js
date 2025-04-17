import React, { useState } from 'react';

const ImageFilter = ({ onFilter }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [tags, setTags] = useState('');

  const handleFilter = () => {
    const tagList = tags.split(',').map((tag) => tag.trim());
    onFilter(searchTerm, tagList);
  };

  return (
    <div className="image-filter">
      <h2>搜索和筛选</h2>
      <input
        type="text"
        placeholder="搜索图片文件名"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <input
        type="text"
        placeholder="输入标签（用逗号分隔）"
        value={tags}
        onChange={(e) => setTags(e.target.value)}
      />
      <button onClick={handleFilter}>筛选</button>
    </div>
  );
};

export default ImageFilter;