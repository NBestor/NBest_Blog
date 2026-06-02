import gfm from '@bytemd/plugin-gfm';
import highlight from '@bytemd/plugin-highlight';
import math from '@bytemd/plugin-math';
import { Editor } from '@bytemd/react';
import { useEffect, useMemo, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

import 'bytemd/dist/index.css';
import 'github-markdown-css/github-markdown-light.css';
import 'highlight.js/styles/github.css';
import 'katex/dist/katex.css';

import httpClient from '../api/http-client';

function BlogEditPage() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const articleId = searchParams.get('articleId');
  const draftId = articleId ? null : searchParams.get('draftId');
  const isPublishedMode = Boolean(articleId);
  const plugins = useMemo(() => [gfm(), math(), highlight()], []);
  const [formData, setFormData] = useState({
    title: '',
    summary: '',
    content: '# 新草稿\n\n开始写点什么吧。',
    category_id: '',
    visible_type: 'self',
    tags: '',
  });
  const [categories, setCategories] = useState([]);
  const [newCategoryName, setNewCategoryName] = useState('');
  const [currentDraftId, setCurrentDraftId] = useState(draftId);
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(Boolean(draftId || articleId));
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiModel, setAiModel] = useState(null);

  useEffect(() => {
    if (isPublishedMode) {
      let isMounted = true;

      async function fetchArticle() {
        try {
          const response = await httpClient.get(`/articles/${articleId}`);
          if (isMounted) {
            setFormData({
              title: response.data.title,
              summary: response.data.summary || '',
              content: response.data.content,
              category_id: response.data.category_id ? String(response.data.category_id) : '',
              visible_type: response.data.visible_type || 'self',
              tags: response.data.tags.join(', '),
            });
          }
        } catch {
          if (isMounted) {
            setMessage('文章加载失败');
          }
        } finally {
          if (isMounted) {
            setIsLoading(false);
          }
        }
      }

      fetchArticle();

      return () => {
        isMounted = false;
      };
    }
  }, [articleId, isPublishedMode]);

  useEffect(() => {
    if (isPublishedMode) return;

    let isMounted = true;

    async function fetchDraft() {
      if (!draftId) {
        setIsLoading(false);
        return;
      }

      try {
        const response = await httpClient.get(`/articles/drafts/${draftId}`);
        if (isMounted) {
          setFormData({
            title: response.data.title,
            summary: response.data.summary || '',
            content: response.data.content,
            category_id: response.data.category_id ? String(response.data.category_id) : '',
            visible_type: response.data.visible_type || 'self',
            tags: response.data.tags.join(', '),
          });
          setCurrentDraftId(String(response.data.id));
        }
      } catch {
        if (isMounted) {
          setMessage('草稿读取失败');
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    fetchDraft();

    return () => {
      isMounted = false;
    };
  }, [draftId]);

  useEffect(() => {
    let isMounted = true;

    async function fetchCategories() {
      try {
        const response = await httpClient.get('/article-categories');
        if (isMounted) {
          setCategories(response.data.items);
        }
      } catch {
        if (isMounted) {
          setMessage('分类加载失败');
        }
      }
    }

    fetchCategories();

    return () => {
      isMounted = false;
    };
  }, []);

  function handleChange(event) {
    const { name, value } = event.target;
    setFormData((currentData) => ({ ...currentData, [name]: value }));
  }

  function getPayload() {
    return {
      title: formData.title.trim(),
      summary: formData.summary.trim() || null,
      content: formData.content.trim(),
      category_id: formData.category_id ? Number(formData.category_id) : null,
      visible_type: formData.visible_type,
      tags: formData.tags
        .split(',')
        .map((tag) => tag.trim())
        .filter(Boolean),
    };
  }

  async function handleAIGenerateSummary() {
    const content = formData.content.trim();
    if (!content) {
      setMessage('请先编写文章内容');
      return;
    }

    setMessage('');
    setAiLoading(true);
    setAiModel(null);

    try {
      const response = await httpClient.post('/ai/summary', { content });
      setFormData((currentData) => ({ ...currentData, summary: response.data.summary }));
      setAiModel(response.data.model);
    } catch (error) {
      const detail = error.response?.data?.detail || 'AI 生成失败，请稍后重试';
      setMessage(detail);
    } finally {
      setAiLoading(false);
    }
  }

  async function handleCreateCategory() {
    const categoryName = newCategoryName.trim();
    if (!categoryName) {
      return;
    }

    try {
      const response = await httpClient.post('/article-categories', { name: categoryName });
      setCategories((currentCategories) => {
        const exists = currentCategories.some((category) => category.id === response.data.id);
        return exists ? currentCategories : [response.data, ...currentCategories];
      });
      setFormData((currentData) => ({ ...currentData, category_id: String(response.data.id) }));
      setNewCategoryName('');
      setMessage('分类已创建');
    } catch {
      setMessage('分类创建失败');
    }
  }

  async function handleImageUpload(event) {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }

    const imageFormData = new FormData();
    imageFormData.append('image', file);

    try {
      const response = await httpClient.post('/articles/images', imageFormData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      const imageMarkdown = `\n\n![图片](http://127.0.0.1:8000${response.data.url})`;
      setFormData((currentData) => ({
        ...currentData,
        content: `${currentData.content}${imageMarkdown}`,
      }));
      setMessage('图片已插入正文');
    } catch {
      setMessage('图片上传失败，请选择 jpg、png 或 webp 图片');
    } finally {
      event.target.value = '';
    }
  }

  async function handleSaveDraft() {
    setMessage('');
    setIsSubmitting(true);

    try {
      const payload = getPayload();
      const response = currentDraftId
        ? await httpClient.put(`/articles/drafts/${currentDraftId}`, payload)
        : await httpClient.post('/articles/drafts', payload);

      setCurrentDraftId(String(response.data.id));
      setSearchParams({ draftId: String(response.data.id) });
      setMessage('草稿已保存');
    } catch {
      setMessage('保存失败，请检查标题和正文');
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleSaveArticle() {
    setMessage('');
    setIsSubmitting(true);

    try {
      const payload = getPayload();
      await httpClient.put(`/articles/${articleId}`, payload);
      setMessage('保存成功');
    } catch {
      setMessage('保存失败，请检查标题和正文');
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handlePublish() {
    setMessage('');
    setIsSubmitting(true);

    try {
      const payload = getPayload();
      const response = currentDraftId
        ? await httpClient.put(`/articles/drafts/${currentDraftId}`, payload)
        : await httpClient.post('/articles/drafts', payload);

      await httpClient.post(`/articles/drafts/${response.data.id}/publish`);
      navigate('/blog/draft');
    } catch {
      setMessage('发布失败，请先完善标题和正文');
    } finally {
      setIsSubmitting(false);
    }
  }

  if (isLoading) {
    return (
      <section className="page-section">
        <div className="content-panel">正在读取草稿...</div>
      </section>
    );
  }

  return (
    <section className="page-section">
      <div className="page-heading">
        <h1>文章编辑器</h1>
        <p>{isPublishedMode ? '正在编辑已发布文章。' : '使用 Markdown 写作，实时预览，并保存到云端草稿。'}</p>
      </div>

      <div className="content-panel editor-shell">
        <label>
          标题
          <input name="title" value={formData.title} onChange={handleChange} maxLength={120} required />
        </label>
        <label>
          简介
          <textarea
            name="summary"
            value={formData.summary}
            onChange={handleChange}
            maxLength={300}
            rows={3}
            placeholder="不写简介时，会自动取正文开头作为词条简介"
          />
          <span className="field-hint">{formData.summary.length}/300</span>
        </label>
        <div className="ai-summary-row">
          <button
            className="secondary-button"
            type="button"
            onClick={handleAIGenerateSummary}
            disabled={aiLoading}
          >
            {aiLoading ? '🤖 AI 生成中...' : '🤖 AI 生成'}
          </button>
          {!formData.summary.trim() && !aiLoading && !aiModel && (
            <span className="ai-hint">用 AI 帮你生成？</span>
          )}
          {aiModel && (
            <span className="ai-model-label">由 {aiModel} 生成</span>
          )}
        </div>
        <div className="article-meta-grid">
          <label>
            分类
            <select name="category_id" value={formData.category_id} onChange={handleChange}>
              <option value="">无分类</option>
              {categories.map((category) => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>
          </label>
          <label>
            可见范围
            <select name="visible_type" value={formData.visible_type} onChange={handleChange}>
              <option value="public">公开</option>
              <option value="friend">好友可见</option>
              <option value="self">仅自己可见</option>
            </select>
          </label>
          <label>
            标签
            <input name="tags" value={formData.tags} onChange={handleChange} placeholder="React, FastAPI" />
          </label>
        </div>
        <div className="article-tool-row">
          <input
            value={newCategoryName}
            onChange={(event) => setNewCategoryName(event.target.value)}
            placeholder="新分类名称"
          />
          <button className="secondary-button" type="button" onClick={handleCreateCategory}>
            新建分类
          </button>
          <label className="file-button">
            上传图片
            <input type="file" accept="image/png,image/jpeg,image/webp" onChange={handleImageUpload} />
          </label>
        </div>
        <div className="markdown-editor-wrap">
          <Editor
            mode="split"
            plugins={plugins}
            value={formData.content}
            onChange={(value) => setFormData((currentData) => ({ ...currentData, content: value }))}
          />
        </div>
        <div className="editor-actions">
          {isPublishedMode ? (
            <button type="button" onClick={handleSaveArticle} disabled={isSubmitting}>
              保存修改
            </button>
          ) : (
            <>
              <button type="button" onClick={handleSaveDraft} disabled={isSubmitting}>
                保存草稿
              </button>
              <button className="secondary-button" type="button" onClick={handlePublish} disabled={isSubmitting}>
                发布
              </button>
            </>
          )}
          {message && <p className="form-message">{message}</p>}
        </div>
      </div>
    </section>
  );
}

export default BlogEditPage;
