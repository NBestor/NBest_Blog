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

const SUMMARY_STYLES = [
  { key: 'formal', label: '📋 正式公告', desc: '严谨正式的公告式简介' },
  { key: 'marketing', label: '📢 营销吸睛', desc: '夸张吸引眼球的营销风格' },
  { key: 'academic', label: '🎓 学术简洁', desc: '学术论文摘要风格' },
  { key: 'casual', label: '💬 轻松娱乐', desc: '轻松口语化风格' },
  { key: 'humorous', label: '🤪 幽默搞笑', desc: '幽默玩梗风格' },
  { key: 'custom', label: '✏️ 自定义', desc: '自己输入提示词' },
];

const POLISH_STYLES = [
  { key: 'formatting', label: '📐 仅优化排版', desc: '只调整格式，严禁修改文字' },
  { key: 'typo', label: '🔍 仅改错别字/重复', desc: '只修正错字和重复' },
  { key: 'academic', label: '🎓 学术规范', desc: '学术化改写' },
  { key: 'youth_lit', label: '🌸 青春文学', desc: '文艺清新风格' },
  { key: 'custom', label: '✏️ 自定义', desc: '自己输入提示词' },
];

function AIModePanel({ title, options, onSelect, onClose, isOpen, isLoading: panelLoading }) {
  const [customPrompt, setCustomPrompt] = useState('');
  const [selectedCustom, setSelectedCustom] = useState(false);

  if (!isOpen) return null;

  function handleOptionClick(option) {
    if (option.key === 'custom') {
      setSelectedCustom(true);
    } else {
      onSelect(option.key, null);
    }
  }

  function handleCustomSubmit() {
    const prompt = customPrompt.trim();
    if (!prompt) return;
    onSelect('custom', prompt);
    setCustomPrompt('');
    setSelectedCustom(false);
  }

  return (
    <div className="ai-mode-backdrop" onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="ai-mode-panel">
        <div className="ai-mode-header">
          <h3>{title}</h3>
          <button className="text-button" type="button" onClick={onClose}>✕</button>
        </div>
        {selectedCustom ? (
          <div className="ai-mode-custom">
            <textarea
              value={customPrompt}
              onChange={(e) => setCustomPrompt(e.target.value)}
              placeholder="输入自定义提示词，告诉 AI 你想要什么风格..."
              rows={4}
            />
            <div className="editor-actions" style={{ justifyContent: 'flex-end' }}>
              <button className="secondary-button" type="button" onClick={() => setSelectedCustom(false)}>返回</button>
              <button type="button" onClick={handleCustomSubmit} disabled={!customPrompt.trim() || panelLoading}>
                提交
              </button>
            </div>
          </div>
        ) : (
          <div className="ai-mode-options">
            {options.map((option) => (
              <button
                className="ai-mode-option"
                key={option.key}
                type="button"
                onClick={() => handleOptionClick(option)}
                disabled={panelLoading}
              >
                <strong>{option.label}</strong>
                <span>{option.desc}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function PolishResultModal({ content, onApply, onClose }) {
  async function handleCopy() {
    try { await navigator.clipboard.writeText(content); } catch { /* fallback */ }
  }

  return (
    <div className="ai-mode-backdrop" onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}>
      <div className="ai-mode-panel" style={{ width: 'min(90vw, 900px)', maxHeight: 'min(85vh, 750px)' }}>
        <div className="ai-mode-header">
          <h3>✨ 润色结果</h3>
          <button className="text-button" type="button" onClick={onClose}>✕</button>
        </div>
        <div className="ai-polish-preview">
          <pre className="markdown-source" style={{ maxHeight: '50vh' }}>{content}</pre>
        </div>
        <div className="editor-actions" style={{ justifyContent: 'flex-end', marginTop: 12 }}>
          <button className="secondary-button" type="button" onClick={handleCopy}>📋 复制</button>
          <button type="button" onClick={onApply}>✅ 覆盖原文</button>
        </div>
      </div>
    </div>
  );
}

function BlogEditPage() {
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const articleId = searchParams.get('articleId');
  const draftId = articleId ? null : searchParams.get('draftId');
  const isPublishedMode = Boolean(articleId);
  const plugins = useMemo(() => [gfm(), math({ katexOptions: { strict: false } }), highlight()], []);
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
  const [aiPanelMode, setAiPanelMode] = useState(null);
  const [polishedResult, setPolishedResult] = useState(null);
  const [enableNiubaoComment, setEnableNiubaoComment] = useState(false);

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
    if (!draftId && !articleId) {
      setFormData({
        title: '',
        summary: '',
        content: '# 新草稿\n\n开始写点什么吧。',
        category_id: '',
        visible_type: 'self',
        tags: '',
      });
      setCurrentDraftId(null);
      setSearchParams({});
      setIsLoading(false);
      setMessage('');
    }
  }, [draftId, articleId]);

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

  function cleanContent(text) {
    if (!text) return text;
    return text.replace(/[\u200b\u200c\u200d\u2060\u2061\u2062\u2063\ufeff\u00a0\u2028\u2029]/g, '');
  }

  function getPayload() {
    return {
      title: formData.title.trim(),
      summary: formData.summary.trim() || null,
      content: cleanContent(formData.content.trim()),
      category_id: formData.category_id ? Number(formData.category_id) : null,
      visible_type: formData.visible_type,
      tags: formData.tags
        .split(',')
        .map((tag) => tag.trim())
        .filter(Boolean),
    };
  }

  async function handleAISummary(style, customPrompt) {
    setAiPanelMode(null);
    const content = formData.content.trim();
    if (!content) {
      setMessage('请先编写文章内容');
      return;
    }

    setMessage('');
    setAiLoading(true);
    setAiModel(null);

    try {
      const requestBody = { content };
      if (style) {
        requestBody.style = style;
        if (customPrompt) {
          requestBody.custom_prompt = customPrompt;
        }
      }
      const response = await httpClient.post('/ai/summary', requestBody);
      setFormData((currentData) => ({ ...currentData, summary: response.data.summary }));
      setAiModel(response.data.model);
    } catch (error) {
      const detail = error.response?.data?.detail || 'AI 生成失败，请稍后重试';
      setMessage(detail);
    } finally {
      setAiLoading(false);
    }
  }

  async function handleAIPolish(style, customPrompt) {
    setAiPanelMode(null);
    const content = formData.content.trim();
    if (!content) {
      setMessage('请先编写文章内容');
      return;
    }

    setMessage('');
    setAiLoading(true);

    try {
      const requestBody = { content, style: style || 'formatting' };
      if (customPrompt) {
        requestBody.custom_prompt = customPrompt;
      }
      const response = await httpClient.post('/ai/polish', requestBody);
      setPolishedResult(response.data.polished);
    } catch (error) {
      const detail = error.response?.data?.detail || 'AI 润色失败，请稍后重试';
      setMessage(detail);
    } finally {
      setAiLoading(false);
    }
  }

  function handleApplyPolish() {
    setFormData((currentData) => ({ ...currentData, content: polishedResult }));
    setPolishedResult(null);
    setMessage('润色内容已覆盖原文');
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
      if (enableNiubaoComment) {
        setEnableNiubaoComment(false);
        try {
          await httpClient.post('/ai/comment', {
            content: payload.content,
            target_type: 'article',
            target_id: parseInt(articleId),
          });
        } catch {
          // AI comment failure is silent
        }
      }
      navigate(`/blog/detail/${articleId}`);
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

      const publishResponse = await httpClient.post(`/articles/drafts/${response.data.id}/publish`);
      const publishedId = publishResponse.data.id;
      if (enableNiubaoComment) {
        setEnableNiubaoComment(false);
        try {
          await httpClient.post('/ai/comment', {
            content: payload.content,
            target_type: 'article',
            target_id: publishedId,
          });
        } catch {
          // AI comment failure is silent
        }
      }
      navigate(`/blog/detail/${publishedId}`);
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
            onClick={() => {
              if (!formData.content.trim()) {
                setMessage('请先编写文章内容');
                return;
              }
              setAiPanelMode('summary');
            }}
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
          <label className="file-button" title="选择图片文件，上传后将自动插入到正文末尾">
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
          <button
            className="secondary-button"
            type="button"
            onClick={() => setAiPanelMode('polish')}
            disabled={aiLoading || !formData.content.trim()}
          >
            🤖 AI 润色
          </button>
          {formData.content.length > 8000 && (
            <span className="ai-hint">⚠️ 文章较长，仅润色前8000字符</span>
          )}
          <label className="todo-check">
            <input
              type="checkbox"
              checked={enableNiubaoComment}
              onChange={(e) => setEnableNiubaoComment(e.target.checked)}
            />
            🤖 牛宝评论
          </label>
          {message && <p className="form-message">{message}</p>}
        </div>
        {aiLoading && (
          <div className="ai-mode-backdrop">
            <div className="ai-mode-panel" style={{ textAlign: 'center', padding: '40px 20px' }}>
              <p style={{ fontSize: 18, color: '#555' }}>🤖 AI 正在思考...</p>
              <p style={{ color: '#888', fontSize: 14 }}>请稍候，这可能需要几秒钟</p>
            </div>
          </div>
        )}
        {polishedResult && (
          <PolishResultModal
            content={polishedResult}
            onApply={handleApplyPolish}
            onClose={() => setPolishedResult(null)}
          />
        )}
      </div>

      <AIModePanel
        title="选择简介风格"
        options={SUMMARY_STYLES}
        onSelect={handleAISummary}
        onClose={() => setAiPanelMode(null)}
        isOpen={aiPanelMode === 'summary'}
        isLoading={aiLoading}
      />

      <AIModePanel
        title="选择润色模式"
        options={POLISH_STYLES}
        onSelect={handleAIPolish}
        onClose={() => setAiPanelMode(null)}
        isOpen={aiPanelMode === 'polish'}
        isLoading={aiLoading}
      />
    </section>
  );
}

export default BlogEditPage;