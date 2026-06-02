import { useEffect, useState } from 'react';

import httpClient from '../api/http-client';
import { useAuth } from '../contexts/use-auth';

const sourceLabels = {
  avatar: '头像',
  article: '文章插图',
  upload: '照片',
};

const visibleLabels = {
  public: '公开',
  self: '仅自己可见',
};

function getImageUrl(url) {
  return url.startsWith('http') ? url : `http://127.0.0.1:8000${url}`;
}

function PhotoPage() {
  const { isAuthenticated } = useAuth();
  const [photos, setPhotos] = useState([]);
  const [selectedPhoto, setSelectedPhoto] = useState(null);
  const [visibleType, setVisibleType] = useState('self');
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  async function getPhotos() {
    const response = await httpClient.get('/photos');
    return response.data.items;
  }

  useEffect(() => {
    let isMounted = true;

    async function loadPhotos() {
      try {
        const items = await getPhotos();
        if (isMounted) {
          setPhotos(items);
        }
      } catch {
        if (isMounted) {
          setMessage('照片加载失败');
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadPhotos();

    return () => {
      isMounted = false;
    };
  }, []);

  async function refreshPhotos() {
    setMessage('');
    setIsLoading(true);

    try {
      setPhotos(await getPhotos());
    } catch {
      setMessage('照片加载失败');
    } finally {
      setIsLoading(false);
    }
  }

  async function handleUpload(event) {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }

    const formData = new FormData();
    formData.append('image', file);
    formData.append('visible_type', visibleType);

    try {
      await httpClient.post('/photos', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      await refreshPhotos();
      setMessage('照片已上传');
    } catch {
      setMessage('照片上传失败，请选择 jpg、png 或 webp 图片');
    } finally {
      event.target.value = '';
    }
  }

  async function handleVisibleChange(photo, nextVisibleType) {
    try {
      await httpClient.put(`/photos/${photo.id}`, { visible_type: nextVisibleType });
      await refreshPhotos();
    } catch {
      setMessage('可见范围修改失败');
    }
  }

  async function handleDelete(photo) {
    try {
      await httpClient.delete(`/photos/${photo.id}`);
      await refreshPhotos();
      if (selectedPhoto?.id === photo.id) {
        setSelectedPhoto(null);
      }
    } catch {
      setMessage('照片删除失败');
    }
  }

  async function handleCopyLink(photo) {
    const imageUrl = getImageUrl(photo.url);

    try {
      await navigator.clipboard.writeText(imageUrl);
      setMessage('图片链接已复制');
    } catch {
      setMessage(`复制失败，请手动复制：${imageUrl}`);
    }
  }

  return (
    <section className="page-section">
      <div className="page-heading">
        <h1>照片墙</h1>
        <p>浏览公开照片，管理自己上传的图片资源。</p>
      </div>

      {isAuthenticated ? (
        <div className="content-panel photo-upload-panel">
          <select value={visibleType} onChange={(event) => setVisibleType(event.target.value)}>
            <option value="self">仅自己可见</option>
            <option value="public">公开</option>
          </select>
          <label className="file-button">
            上传照片
            <input type="file" accept="image/png,image/jpeg,image/webp" onChange={handleUpload} />
          </label>
        </div>
      ) : null}

      {message ? <p className="form-message photo-message">{message}</p> : null}
      {isLoading ? <div className="content-panel">正在加载照片...</div> : null}
      {!isLoading && photos.length === 0 ? (
        <div className="content-panel">
          <p className="empty-text">暂无可见照片。</p>
        </div>
      ) : null}

      <div className="photo-grid">
        {photos.map((photo) => (
          <article className="photo-card" key={photo.id}>
            <button type="button" onClick={() => setSelectedPhoto(photo)}>
              <img src={getImageUrl(photo.url)} alt={sourceLabels[photo.source_type] || '照片'} />
            </button>
            <div className="photo-card-body">
              <strong>{photo.author_nickname}</strong>
              <span>
                {sourceLabels[photo.source_type] || photo.source_type} · {visibleLabels[photo.visible_type]}
              </span>
              {photo.can_manage ? (
                <div className="photo-actions">
                  <select
                    value={photo.visible_type}
                    onChange={(event) => handleVisibleChange(photo, event.target.value)}
                  >
                    <option value="self">仅自己可见</option>
                    <option value="public">公开</option>
                  </select>
                  <button className="secondary-button" type="button" onClick={() => handleCopyLink(photo)}>
                    复制链接
                  </button>
                  <button className="secondary-button" type="button" onClick={() => handleDelete(photo)}>
                    删除
                  </button>
                </div>
              ) : null}
            </div>
          </article>
        ))}
      </div>

      {selectedPhoto ? (
        <div className="photo-preview" role="dialog" aria-modal="true">
          <button className="photo-preview-backdrop" type="button" onClick={() => setSelectedPhoto(null)} />
          <div className="photo-preview-content">
            <img src={getImageUrl(selectedPhoto.url)} alt="照片预览" />
            <div className="photo-preview-info">
              <strong>{selectedPhoto.author_nickname}</strong>
              <span>
                {sourceLabels[selectedPhoto.source_type] || selectedPhoto.source_type} ·{' '}
                {visibleLabels[selectedPhoto.visible_type]}
              </span>
              <code>{getImageUrl(selectedPhoto.url)}</code>
            </div>
            <div className="photo-preview-actions">
              {selectedPhoto.can_manage ? (
                <button type="button" onClick={() => handleCopyLink(selectedPhoto)}>
                  复制链接
                </button>
              ) : null}
              <button type="button" onClick={() => setSelectedPhoto(null)}>
                关闭
              </button>
            </div>
          </div>
        </div>
      ) : null}
    </section>
  );
}

export default PhotoPage;
