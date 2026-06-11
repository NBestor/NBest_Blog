# 🚀 阿里云部署指南（零基础版）

> 从零开始，把你的博客部署到阿里云服务器上，让全世界都能访问。

---

## 📦 本文档包含的文件

| 文件 | 用途 |
|------|------|
| `deploy/Dockerfile.backend` | 后端 FastAPI 容器镜像 |
| `deploy/Dockerfile.frontend` | 前端 React + Nginx 容器镜像 |
| `deploy/nginx.conf` | Nginx 反向代理配置 |
| `deploy/.env.production` | 生产环境变量模板 |
| `docker-compose.yml` | 一键编排前后端服务 |

---

## 🗺️ 整体流程概览

```
你现在在这 → Step 1 → Step 2 → Step 3 → Step 4 → Step 5 → Step 6 → Step 7
    ↓          ↓        ↓        ↓        ↓        ↓        ↓        ↓
  阅读本指南  买服务器  连服务器  装Docker  传代码   配环境   启动服务  访问网站
```

---

## Step 1：购买阿里云服务器

### 1.1 注册账号
打开 [aliyun.com](https://www.aliyun.com)，用支付宝/淘宝扫码注册并实名认证。

### 1.2 购买轻量应用服务器（推荐新手）
1. 搜索「轻量应用服务器」
2. 点击「立即购买」
3. 选择以下配置：

| 配置项 | 推荐选择 |
|--------|----------|
| **地域** | 离你最近的（华东1/华东2/华北2） |
| **镜像** | 系统镜像 → **Ubuntu 22.04** |
| **套餐** | 2核2G（~50元/月）起步即可 |
| **时长** | 先买1个月试用，满意再续费 |

4. 点击「立即购买」→ 付款

### 1.3 获取服务器信息
购买成功后，在「轻量应用服务器」控制台找到你的实例，记录：
- **公网 IP**（例如 `123.456.789.0`）
- **用户名**：默认是 `root`
- **密码**：点击「重置密码」设置一个强密码（务必记住！）

---

## Step 2：连接服务器

> **Windows 用户**：打开命令行（Win+R → 输入 `cmd`）

```bash
ssh root@你的服务器IP
# 例如: ssh root@123.456.789.0
```

首次连接会提示：
```
Are you sure you want to continue connecting (yes/no)?
```
输入 `yes` 回车，然后输入你设置的密码。

> 💡 **提示**：SSH 输入密码时不显示任何字符，这是正常的，输完直接回车。

---

## Step 3：安装 Docker

连接上服务器后，一键安装 Docker：

```bash
# 一键安装脚本
curl -fsSL https://get.docker.com | bash

# 启动 Docker
systemctl start docker
systemctl enable docker

# 安装 Docker Compose 插件
apt install -y docker-compose-plugin
```

验证安装：
```bash
docker --version
docker compose version
```

---

## Step 4：上传代码到服务器

### 方式A：Git 推送（推荐）
在你的**本地电脑**上执行：
```bash
# 将代码推送到 GitHub
git add -A
git commit -m "添加 Docker 部署配置"
git push

# 在服务器上克隆
# 先连上服务器，然后：
git clone https://github.com/NBestor/NBest_Blog.git
cd NBest_Blog
```

### 方式B：直接压缩上传
在**本地电脑**上执行：
```bash
# 打包项目（排除不需要的文件）
tar -czf blog.tar.gz \
    --exclude=node_modules \
    --exclude=.venv \
    --exclude=frontend/dist \
    --exclude=.git \
    .

# 上传到服务器
scp blog.tar.gz root@你的服务器IP:/root/

# 然后在服务器上解压
ssh root@你的服务器IP
tar -xzf /root/blog.tar.gz -C /root/
mv /root/project /root/NBest_Blog    # 如果目录名不对则重命名
cd /root/NBest_Blog
```

---

## Step 5：配置环境变量

在**服务器上**执行：

```bash
cd /root/NBest_Blog   # 或你的项目目录

# 复制生产环境配置
cp deploy/.env.production backend/.env

# 编辑配置文件
nano backend/.env
```

需要修改 3 个地方：

```bash
# 1. 替换为你的服务器 IP（访问 http://IP 查看）
FRONTEND_ORIGIN=http://你的服务器IP

# 2. 数据库路径（使用容器内路径，不用改）
DATABASE_URL=sqlite:///app/data/private-blog.db

# 3. 生成一个安全的 JWT 密钥（必须改！）
JWT_SECRET_KEY=随机字符串  # 见下方生成方法
```

**生成 JWT 密钥**（在服务器上执行）：
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
# 把输出的字符串复制到 JWT_SECRET_KEY=
```

保存：`Ctrl+O` → 回车 → `Ctrl+X`

---

## Step 6：启动服务

```bash
cd /root/NBest_Blog

# 构建并启动
docker compose up -d --build
```

等待 3-5 分钟（首次需要下载镜像），看到：
```
✔ Container blog-backend  Started
✔ Container blog-frontend  Started
```

查看运行状态：
```bash
docker compose ps
# 两个容器都应该是 Up 状态

docker compose logs -f --tail=20
# 查看日志，按 Ctrl+C 退出
```

---

## Step 7：访问你的网站 🎉

打开浏览器，输入：
```
http://你的服务器IP
```

看到博客首页就代表部署成功！

默认管理员账号：
- 用户名：`NBest`
- 密码：`NBest666`

---

## 🔧 日常维护命令

```bash
# 查看运行状态
docker compose ps

# 查看日志
docker compose logs -f backend    # 后端日志
docker compose logs -f frontend   # 前端日志

# 停止服务
docker compose stop

# 重启服务（修改代码后）
docker compose restart

# 重新构建并启动（修改代码后）
docker compose up -d --build

# 完全停止并删除容器（数据不会丢失，存在 Docker Volume 里）
docker compose down
docker compose up -d
```

---

## 🌐 绑定域名 + HTTPS（可选但推荐）

### 前提条件
1. 拥有一个域名（可在阿里云、腾讯云等购买）
2. 域名已完成 ICP 备案（国内服务器必须备案）
3. 免费 SSL 证书（Let's Encrypt）

### 待你准备好域名后，我可以帮你：
- 配置 DNS 解析
- 配置 Nginx + Let's Encrypt 自动续签 SSL
- 添加 `docker-compose.yml` 中的 Certbot 服务

---

## 🐛 常见问题

**Q: 访问服务器 IP 没反应？**
A: 检查阿里云防火墙是否放行 80 端口：
   轻量应用服务器 → 你的实例 → 防火墙 → 添加规则：
   - 端口：80
   - 协议：TCP
   - 来源：0.0.0.0/0

**Q: 构建失败？**
A: 通常是网络问题，重试 `docker compose up -d --build`

**Q: 如何备份数据库？**
A: 
   ```bash
   docker cp blog-backend:/app/data/private-blog.db ./backup-$(date +%Y%m%d).db
   ```

---

## 📞 需要帮助？

在过程中的任何一步遇到问题，随时告诉我：
1. 你在哪一步
2. 报了什么错误信息
3. 我会帮你排查