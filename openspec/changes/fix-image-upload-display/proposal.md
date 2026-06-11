## Why

部署到服务器后，上传的图片（文章配图、头像、照片墙等）无法正常显示。容器内 `/app/static/uploads/` 下已有图片文件，Nginx 也配置了 `/static/` 反向代理到 `backend:8000`，但浏览器端请求图片返回失败。

## What Changes

- **诊断**：在服务器上分别测试 Nginx (80) → Backend (8000) 的 `/static/` 路径，确认是 Nginx 转发问题还是后端 StaticFiles 服务问题
- **修复**：根据诊断结果调整 Nginx 配置或后端静态文件路径
- **验证**：上传一张新图片确认前端可正常显示

## Capabilities

### New Capabilities

- 无

### Modified Capabilities

- `static-file-serving`: 修复生产环境中静态文件（上传图片等）的 Nginx 代理或后端服务路径

## Impact

- 后端：可能需要调整 `config.py` 中 `static_dir` 路径或 Dockerfile 中的目录结构
- 部署：可能需要修改 `nginx.conf` 中的 `/static/` location 配置
- 仅影响部署层，不涉及业务逻辑变更