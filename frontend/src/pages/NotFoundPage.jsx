import { Link } from 'react-router-dom';

function NotFoundPage() {
  return (
    <section className="page-section">
      <div className="page-heading">
        <h1>404</h1>
        <p>页面不存在或仍未开放。</p>
      </div>
      <Link className="primary-link" to="/">
        返回首页
      </Link>
    </section>
  );
}

export default NotFoundPage;
