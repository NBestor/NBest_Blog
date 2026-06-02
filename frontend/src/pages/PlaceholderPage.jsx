function PlaceholderPage({ title, description }) {
  return (
    <section className="page-section">
      <div className="page-heading">
        <h1>{title}</h1>
        <p>{description}</p>
      </div>

      <div className="content-panel">
        <h2>阶段 1 页面框架</h2>
        <p>当前阶段仅完成工程化初始化、路由占位与前后端基础联调。</p>
      </div>
    </section>
  );
}

export default PlaceholderPage;
