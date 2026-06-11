## Tasks

- [x] ① 诊断：在服务器上测试 Nginx(80) → Backend(8000) 的 `/static/` 路径
  - Nginx 返回 HTTP 200 + 正确 Content-Type，图片文件正常返回
  - 结论：图片服务链路完全正常

- [x] ② 重新构建前端（`docker compose up -d --build frontend`）

- [x] ③ 验证：重启前后端容器，数据不丢失，图片正常访问

- [x] ④ 清理：本地临时文件、服务器端诊断脚本已删除
