# HotNews - 热搜榜单聚合平台

基于 Django + Vue 3 + Vite 的前后端分离热搜榜单聚合系统，支持微博、百度、36氪、抖音等多个平台的热搜数据展示。

## 📋 目录

- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [本地开发](#本地开发)
  - [原生部署方式](#原生部署方式)
  - [容器化部署方式](#容器化部署方式)
- [生产环境部署](#生产环境部署)
- [API 文档](#api-文档)
- [开发指南](#开发指南)
- [故障排查](#故障排查)

## 🛠️ 技术栈

### 后端
- **框架**: Django 5.2.11 + Django REST Framework 3.16.1
- **Web 服务器**: Gunicorn 25.0.1
- **数据库**: MySQL 8.0 (生产环境使用阿里云 RDS)
- **缓存**: Django Cache Framework
- **依赖管理**: pip + requirements.txt

### 前端
- **框架**: Vue 3.4 (Composition API)
- **构建工具**: Vite 7.3.1
- **HTTP 客户端**: Axios 1.6.0
- **开发服务器**: Vite Dev Server

### 部署
- **开发环境**: Docker Compose (可选) / 原生部署
- **生产环境**: 原生部署 + Nginx + Systemd
- **反向代理**: Nginx
- **服务器**: 阿里云 ECS (Ubuntu 22.04 LTS)

---

## 📁 项目结构

```
HotNews/
├── backend/                    # Django 后端
│   ├── HotNews/                # Django 项目配置
│   │   ├── __init__.py         # PyMySQL 初始化
│   │   ├── settings.py         # 项目配置（数据库、CORS、静态文件）
│   │   ├── urls.py             # 主路由配置
│   │   ├── wsgi.py             # WSGI 入口
│   │   └── asgi.py             # ASGI 入口
│   ├── news/                   # 新闻应用
│   │   ├── models.py           # NewsArticle 数据模型
│   │   ├── views.py            # API 视图（get_sources, get_ranking_data）
│   │   ├── urls.py             # 应用路由
│   │   ├── admin.py            # Django Admin 配置
│   │   └── migrations/         # 数据库迁移文件
│   ├── manage.py               # Django 管理脚本
│   ├── requirements.txt        # Python 依赖列表
│   └── Dockerfile              # 后端 Docker 镜像（容器化部署用）
│
├── frontend/                   # Vue 3 前端
│   ├── src/
│   │   ├── App.vue             # 主组件（榜单展示逻辑）
│   │   ├── main.js             # Vue 应用入口
│   │   └── style.css           # 全局样式
│   ├── public/                 # 静态资源目录
│   ├── index.html              # HTML 模板
│   ├── package.json            # Node.js 依赖
│   ├── vite.config.js          # Vite 配置（代理、构建）
│   └── Dockerfile.dev          # 前端开发镜像（容器化用）│
├── .env                        # 环境变量（不提交，生产环境敏感信息）
├── .env.example                # 环境变量模板
├── .gitignore                  # Git 忽略规则
├── docker-compose.yml          # Docker 开发环境配置
├── deploy.sh                   # 生产环境部署脚本
└── README.md                   # 项目文档
```

### 关键文件说明

| 文件 | 作用 | 说明 |
|------|------|------|
| `backend/HotNews/settings.py` | Django 配置 | 数据库连接、CORS、静态文件、缓存配置 |
| `backend/news/models.py` | 数据模型 | `NewsArticle` 模型，包含索引优化 |
| `backend/news/views.py` | API 视图 | 榜单数据查询逻辑，含缓存优化 |
| `frontend/src/App.vue` | 前端主组件 | 榜单展示、数据刷新、响应式布局 |
| `frontend/vite.config.js` | Vite 配置 | API 代理、构建优化 |
| `.env` | 环境变量 | 数据库密码、密钥等敏感信息 |
| `deploy.sh` | 部署脚本 | 自动化生产环境部署流程 |

---

## 💻 本地开发

本地开发支持两种方式：**原生部署**（推荐）和 **Docker 容器化部署**。

### 方式一：原生部署（推荐）

#### 1. 环境准备

**必备软件**：
- Python 3.13+ ([下载](https://www.python.org/downloads/))
- Node.js 24+ ([下载](https://nodejs.org/))
- Git ([下载](https://git-scm.com/))
- MySQL 8.0（可选，用于生产环境测试）

**验证安装**：
```bash
python --version   # 应输出 Python 3.13.x
node --version     # 应输出 v24.x.x
npm --version      # 应输出 11.x.x
git --version      # 应输出 git version 2.x.x
```

#### 2. 克隆项目

```bash
# 克隆仓库
git clone https://github.com/ZH1995/HotNews.git
cd HotNews
```

#### 3. 配置环境变量

```bash
# 复制模板
cp .env.example .env

# 编辑配置
# Windows:
notepad .env

# Linux/Mac:
vim .env
```

**本地开发推荐配置** (`.env`):
```env
# Django Settings
SECRET_KEY='your-dev-secret-key-here'
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:8090

# Database - 本地开发使用 SQLite（无需 MySQL）
# Django 会自动创建 backend/db.sqlite3

# 如果要使用 MySQL（可选）
MYSQL_DATABASE=hot_list
MYSQL_USER=root
MYSQL_PASSWORD=your-mysql-password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_CHARSET=utf8mb4

# 前端配置
VITE_API_URL=http://localhost:8090
```

#### 4. 后端配置

**4.1 创建虚拟环境**

```bash
cd backend

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# Linux/Mac:
source .venv/bin/activate

# 验证虚拟环境（命令行前应有 (.venv) 标识）
which python  # Linux/Mac
where python  # Windows
```

**4.2 安装依赖**

```bash
# 升级 pip
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt

# 验证安装
pip list | grep Django  # Linux/Mac
pip list | findstr Django  # Windows
```

**4.3 配置数据库**

```bash
# 创建数据库迁移文件
python manage.py makemigrations

# 执行迁移（创建数据库表）
python manage.py migrate

# 创建超级用户（用于访问 Django Admin）
python manage.py createsuperuser
# 根据提示输入：
# - 用户名（如：admin）
# - 邮箱（可留空）
# - 密码（需输入两次确认）
```

**4.4 启动开发服务器**

```bash
# 启动服务器（默认端口 8000）
python manage.py runserver

# 或指定端口（推荐）
python manage.py runserver 0.0.0.0:8090

# 看到以下输出表示成功：
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CONTROL-C.
```

**验证后端服务**：
- API 测试: http://localhost:8000/api/sources/
- Django Admin: http://localhost:8000/admin/
  - 使用刚创建的超级用户登录

#### 5. 前端配置

**打开新的终端窗口**（保持后端服务运行）：

```bash
cd frontend

# 安装依赖
npm install

# 如果遇到网络问题，可使用国内镜像
npm install --registry=https://registry.npmmirror.com

# 启动开发服务器
npm run dev

# 看到以下输出表示成功：
# VITE v7.3.1  ready in 500 ms
# ➜  Local:   http://localhost:5173/
# ➜  Network: use --host to expose
```

**访问应用**：
- 前端: http://localhost:5173/
- 看到榜单数据表示前后端通信成功

#### 6. 开发调试技巧

**后端调试**：

```bash
# 进入 Django Shell（Python 交互式环境）
python manage.py shell

# 测试数据库查询
>>> from news.models import NewsArticle
>>> NewsArticle.objects.count()  # 查看数据总数
>>> NewsArticle.objects.filter(source=1).count()  # 查看微博数据

# 查看 SQL 日志
# 在 settings.py 中添加：
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

**前端调试**：

1. **浏览器开发者工具**（F12）:
   - **Network 标签**: 查看 API 请求和响应
   - **Console 标签**: 查看 `console.log` 输出和错误
   - **Vue DevTools**: 安装浏览器扩展 ([Chrome](https://chrome.google.com/webstore/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd) / [Firefox](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/))

2. **Vite 配置调试** ([frontend/vite.config.js](frontend/vite.config.js)):
   ```javascript
   server: {
     proxy: {
       '/api': {
         configure: (proxy, options) => {
           proxy.on('proxyReq', (proxyReq, req, res) => {
             console.log('代理请求:', req.method, req.url);
           });
           proxy.on('proxyRes', (proxyRes, req, res) => {
             console.log('代理响应:', proxyRes.statusCode);
           });
         }
       }
     }
   }
   ```

#### 7. 常用开发命令

**后端命令**：

```bash
cd backend
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# === 数据库操作 ===
python manage.py makemigrations          # 创建迁移文件
python manage.py migrate                 # 执行迁移
python manage.py showmigrations          # 查看迁移状态
python manage.py sqlmigrate news 0001    # 查看迁移 SQL

# === 管理员操作 ===
python manage.py createsuperuser         # 创建超级用户
python manage.py changepassword admin    # 修改密码

# === 静态文件 ===
python manage.py collectstatic           # 收集静态文件

# === 测试 ===
python manage.py test                    # 运行所有测试
python manage.py test news               # 运行指定应用测试

# === 数据导入/导出 ===
python manage.py dumpdata news > backup.json   # 导出数据
python manage.py loaddata backup.json          # 导入数据
```

**前端命令**：

```bash
cd frontend

# === 开发 ===
npm run dev                  # 启动开发服务器
npm run dev -- --host        # 暴露到局域网
npm run dev -- --port 3000   # 指定端口

# === 构建 ===
npm run build                # 生产构建
npm run preview              # 预览生产构建

# === 依赖管理 ===
npm install axios            # 安装新依赖
npm update                   # 更新所有依赖
npm outdated                 # 查看过期依赖

# === 代码质量（如配置） ===
npm run lint                 # ESLint 检查
npm run format               # Prettier 格式化
```

#### 8. 常见问题排查

**问题 1：端口被占用**

```bash
# 症状：
Error: listen EADDRINUSE: address already in use :::8000

# Windows 解决：
netstat -ano | findstr :8000     # 查找占用进程
taskkill /PID <进程ID> /F         # 结束进程

# Linux/Mac 解决：
lsof -ti:8000 | xargs kill -9
```

**问题 2：后端 500 错误**

```bash
# 检查 Django 日志
# 终端输出会显示详细错误栈

# 检查数据库连接
python manage.py dbshell

# 重新执行迁移
python manage.py migrate --run-syncdb
```

**问题 3：前端 API 请求 404**

```bash
# 1. 确认后端正在运行
curl http://localhost:8000/api/sources/

# 2. 检查 Vite 代理配置
# frontend/vite.config.js 中的 proxy 配置

# 3. 检查后端路由
# backend/HotNews/urls.py 和 backend/news/urls.py
```

**问题 4：CORS 错误**

```bash
# 症状：
Access to XMLHttpRequest at 'http://localhost:8000/api/...' 
from origin 'http://localhost:5173' has been blocked by CORS policy

# 解决：检查 .env 中的 CORS_ALLOWED_ORIGINS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:8090
```

**问题 5：数据库迁移冲突**

```bash
# 删除所有迁移文件
rm backend/news/migrations/0*.py

# 重新创建
python manage.py makemigrations
python manage.py migrate
```

---

### 方式二：Docker 容器化部署（可选）

**优点**：
- 环境一致性，无需安装 Python/Node
- 快速切换不同项目
- 隔离依赖

**缺点**：
- 国内 Docker Hub 连接不稳定
- 资源占用较高
- 调试相对复杂

#### 1. 环境准备

```bash
# 安装 Docker Desktop
# Windows/Mac: https://www.docker.com/products/docker-desktop
# Linux: https://docs.docker.com/engine/install/ubuntu/

# 验证安装
docker --version
docker-compose --version
```

#### 2. 配置国内镜像（可选）

编辑 Docker 配置文件：
- Windows/Mac: Docker Desktop → Settings → Docker Engine
- Linux: `/etc/docker/daemon.json`

```json
{
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://registry.docker-cn.com"
  ]
}
```

#### 3. 启动容器

```bash
# 配置环境变量
cp .env.example .env

# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 查看服务状态
docker-compose ps
```

#### 4. 初始化数据库

```bash
# 执行迁移
docker-compose exec backend python manage.py migrate

# 创建超级用户
docker-compose exec backend python manage.py createsuperuser
```

#### 5. 访问应用

- 前端: http://localhost:5190
- 后端: http://localhost:8090/api/
- Admin: http://localhost:8090/admin/

#### 6. 容器管理命令

```bash
# 查看日志
docker-compose logs -f backend   # 后端日志
docker-compose logs -f frontend  # 前端日志

# 进入容器
docker-compose exec backend bash
docker-compose exec frontend sh

# 重启服务
docker-compose restart backend
docker-compose restart frontend

# 停止服务
docker-compose stop

# 停止并删除
docker-compose down

# 重新构建
docker-compose up -d --build
```

---

## 🚀 生产环境部署

生产环境采用 **原生部署** 方式（非容器化），避免国内 Docker Hub 连接问题。

### 架构图

```
互联网
  ↓
Nginx (80/443)
  ↓
├─→ 前端静态文件 (/var/www/hotnews)
└─→ 后端 Gunicorn (127.0.0.1:8090)
       ↓
    阿里云 RDS MySQL
```

### 部署步骤

#### 1. 服务器准备

**推荐配置**：
- CPU: 2 核
- 内存: 4GB
- 系统: Ubuntu 22.04 LTS
- 带宽: 1Mbps+

**初始化服务器**：

```bash
# SSH 连接服务器
ssh root@your-server-ip

# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装基础工具
sudo apt install -y git curl wget vim ufw

# 配置防火墙
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable         # 启用防火墙
```

#### 2. 安装软件依赖

**安装 Python 3.12**：

```bash
# 添加 deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# 安装 Python 3.12
sudo apt install -y python3.12 python3.12-venv python3.12-dev

# 验证安装
python3.12 --version
```

**安装 Node.js 20**：

```bash
# 使用 NodeSource 仓库
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# 验证安装
node --version
npm --version
```

**安装系统依赖**：

```bash
# MySQL 客户端库（连接 RDS 必需）
sudo apt install -y build-essential libmysqlclient-dev pkg-config

# Nginx 反向代理
sudo apt install -y nginx

# 验证 Nginx
sudo systemctl status nginx
```

#### 3. 克隆项目

```bash
# 创建项目目录
sudo mkdir -p /opt/HotNews
sudo chown -R $USER:$USER /opt/HotNews

# 克隆代码
cd /opt
git clone https://github.com/your-username/HotNews.git
cd HotNews
```

#### 4. 配置环境变量

```bash
# 复制模板
cp .env.example .env

# 编辑配置
vim .env
```

**生产环境配置** (`.env`):

```env
# Django Settings
SECRET_KEY=your-random-secret-key-here-change-in-production
DEBUG=False
ALLOWED_HOSTS=your-domain.com,localhost
CORS_ALLOWED_ORIGINS=https://your-domain.com,http://localhost:5173

# Database (阿里云 RDS)
MYSQL_DATABASE=hot_list
MYSQL_USER=root
MYSQL_PASSWORD=your-mysql-password
MYSQL_HOST=rm-xxxxxxxx.mysql.rds.aliyuncs.com
MYSQL_PORT=3306
MYSQL_CHARSET=utf8mb4
```

**生成随机 SECRET_KEY**：

```bash
python3.12 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 5. 部署后端

**5.1 创建虚拟环境**

```bash
cd /opt/HotNews/backend

# 创建虚拟环境
python3.12 -m venv .venv

# 激活虚拟环境
source .venv/bin/activate

# 升级 pip
pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt
```

**5.2 初始化数据库**

```bash
# 执行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 收集静态文件
python manage.py collectstatic --noinput
```

**5.3 创建 Systemd 服务**

创建服务文件：

```bash
sudo vim /etc/systemd/system/hotnews-backend.service
```

**配置内容**：

```ini
[Unit]
Description=HotNews Django Backend
After=network.target

[Service]
Type=notify
User=ubuntu
Group=ubuntu
WorkingDirectory=/opt/HotNews/backend
Environment="PATH=/opt/HotNews/backend/.venv/bin"
EnvironmentFile=/opt/HotNews/.env

ExecStart=/opt/HotNews/backend/.venv/bin/gunicorn \
    --bind 127.0.0.1:8090 \
    --workers 4 \
    --worker-class sync \
    --timeout 60 \
    --access-logfile /var/log/hotnews/gunicorn-access.log \
    --error-logfile /var/log/hotnews/gunicorn-error.log \
    --log-level info \
    HotNews.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**启动服务**：

```bash
# 创建日志目录
sudo mkdir -p /var/log/hotnews
sudo chown -R ubuntu:ubuntu /var/log/hotnews

# 重载 systemd
sudo systemctl daemon-reload

# 启动并设置开机自启
sudo systemctl start hotnews-backend
sudo systemctl enable hotnews-backend

# 检查状态
sudo systemctl status hotnews-backend

# 查看日志
sudo journalctl -u hotnews-backend -f
tail -f /var/log/hotnews/gunicorn-error.log
```

#### 6. 部署前端

**6.1 构建生产版本**

```bash
cd /opt/HotNews/frontend

# 安装依赖
npm install

# 生产构建
npm run build

# 验证构建产物
ls -lh dist/
```

**6.2 部署静态文件**

```bash
# 创建 Web 根目录
sudo mkdir -p /var/www/hotnews

# 复制构建文件
sudo cp -r dist/* /var/www/hotnews/

# 设置权限
sudo chown -R www-data:www-data /var/www/hotnews
sudo chmod -R 755 /var/www/hotnews

# 验证
ls -lh /var/www/hotnews/
```

#### 7. 配置 Nginx

**7.1 创建 Nginx 配置**

```bash
sudo vim /etc/nginx/sites-available/hotnews.zhenbucuo.tech
```

**完整配置**：

```nginx
# HTTP 重定向到 HTTPS
server {
    listen 80;
    server_name hotnews.zhenbucuo.tech www.hotnews.zhenbucuo.tech;
    return 301 https://$server_name$request_uri;
}

# HTTPS 主配置
server {
    listen 443 ssl http2;
    server_name hotnews.zhenbucuo.tech www.hotnews.zhenbucuo.tech;

    # SSL 证书
    ssl_certificate /etc/ssl/certs/zhenbucuo.tech.pem;
    ssl_certificate_key /etc/ssl/certs/zhenbucuo.tech.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # 前端静态文件
    root /var/www/hotnews;
    index index.html;

    # gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript 
               application/x-javascript application/xml+rss 
               application/javascript application/json;

    # 后端 API 代理
    location /api/ {
        proxy_pass http://127.0.0.1:8090;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $server_name;
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        proxy_no_cache 1;
        proxy_cache_bypass 1;
    }

    # Django admin
    location /admin/ {
        proxy_pass http://127.0.0.1:8090;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Django 静态文件
    location /static/ {
        alias /opt/HotNews/backend/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # 前端静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # SPA 路由支持
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 禁止访问隐藏文件
    location ~ /\. {
        deny all;
    }

    # 日志
    access_log /var/log/nginx/hotnews_access.log;
    error_log /var/log/nginx/hotnews_error.log;
}
```

**7.2 启用配置**

```bash
# 测试配置
sudo nginx -t

# 删除旧配置（如果存在）
sudo rm -f /etc/nginx/sites-enabled/hotnews.zhenbucuo.tech

# 创建软链接
sudo ln -s /etc/nginx/sites-available/hotnews.zhenbucuo.tech \
           /etc/nginx/sites-enabled/

# 重启 Nginx
sudo systemctl restart nginx

# 检查状态
sudo systemctl status nginx
```

#### 8. 配置 SSL 证书（可选）

**使用 Let's Encrypt 免费证书**：

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取证书
sudo certbot --nginx -d hotnews.zhenbucuo.tech -d www.hotnews.zhenbucuo.tech

# 测试自动续期
sudo certbot renew --dry-run

# 设置自动续期（已自动配置）
sudo systemctl status certbot.timer
```

**或使用已有证书**：

```bash
# 上传证书到服务器
sudo mkdir -p /etc/ssl/certs
sudo cp zhenbucuo.tech.pem /etc/ssl/certs/
sudo cp zhenbucuo.tech.key /etc/ssl/certs/

# 设置权限
sudo chmod 644 /etc/ssl/certs/zhenbucuo.tech.pem
sudo chmod 600 /etc/ssl/certs/zhenbucuo.tech.key
```

#### 9. 部署脚本

使用 [deploy.sh](deploy.sh) 脚本实现一键部署：

```bash
# 添加执行权限
chmod +x deploy.sh

# 执行部署
./deploy.sh
```

**脚本功能**：
1. 拉取最新代码
2. 更新后端依赖
3. 执行数据库迁移
4. 收集静态文件
5. 构建前端
6. 部署前端静态文件
7. 重启后端服务
8. 重启 Nginx

#### 10. 验证部署

```bash
# 检查后端服务
sudo systemctl status hotnews-backend
curl http://127.0.0.1:8090/api/sources/

# 检查 Nginx
sudo systemctl status nginx
curl -I https://hotnews.zhenbucuo.tech

# 查看日志
sudo journalctl -u hotnews-backend -n 50
tail -f /var/log/nginx/hotnews_access.log
```

---

## 📖 API 文档

### 基础信息

- **Base URL**: `/api`
- **协议**: HTTP/HTTPS
- **响应格式**: JSON
- **字符编码**: UTF-8

### 接口列表

#### 1. 获取数据源列表

**请求**：
```http
GET /api/sources/
```

**查询参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `show_school_sources` | string | 否 | 设置为 `1` 显示学校榜单 |

**响应示例**：
```json
{
  "sources": [
    {
      "id": 1,
      "title": "微博",
      "logo": "/images/weibo_logo.png",
      "limit": 50
    },
    {
      "id": 3,
      "title": "百度",
      "logo": "/images/baidu_logo.png",
      "limit": 50
    }
  ]
}
```

#### 2. 获取指定榜单数据

**请求**：
```http
GET /api/ranking/<source_id>/
```

**路径参数**：
| 参数 | 类型 | 说明 |
|------|------|------|
| `source_id` | integer | 数据源 ID (如 1=微博, 3=百度) |

**响应示例**：
```json
{
  "id": 1,
  "title": "微博",
  "logo": "/images/weibo_logo.png",
  "articles": [
    {
      "id": 12345,
      "title": "热搜标题",
      "url": "https://weibo.com/...",
      "hot_rank": 1
    },
    {
      "id": 12346,
      "title": "第二条热搜",
      "url": "https://weibo.com/...",
      "hot_rank": 2
    }
  ]
}
```

**错误响应**：
```json
{
  "error": "Source not found"
}
```

### 数据源 ID 对照表

| ID | 平台 | Logo |
|----|------|------|
| 1 | 微博 | weibo_logo.png |
| 3 | 百度 | baidu_logo.png |
| 4 | 36氪 | kr36_logo.png |
| 5 | 抖音 | douyin_logo.png |
| 6 | 华尔街见闻 | wallstreetcn_logo.png |
| 7 | 澎湃新闻 | thepaper_logo.png |

---

## 🔧 开发指南

### 添加新数据源

#### 1. 修改后端配置

编辑 [backend/news/views.py](backend/news/views.py)：

```python
SOURCE_CONFIG = {
    # ...existing code...
    8: {  # 新数据源 ID
        'title': '知乎',
        'logo': '/images/zhihu_logo.png',
        'limit': 50
    },
}
```

#### 2. 添加 Logo

将 Logo 文件放到 [frontend/public/images/](frontend/public/images/) 目录。

#### 3. 实现爬虫

详见：[ScrapyHub](https://github.com/ZH1995/ScrapyHub)

### 数据库迁移流程

#### 1. 修改模型

编辑 [backend/news/models.py](backend/news/models.py)：

```python
class NewsArticle(models.Model):
    # ...existing fields...
    view_count = models.IntegerField(default=0)  # 新增字段
```

#### 2. 生成迁移文件

```bash
python manage.py makemigrations

# 输出：
# Migrations for 'news':
#   news/migrations/0003_newsarticle_view_count.py
#     - Add field view_count to newsarticle
```

#### 3. 查看 SQL（可选）

```bash
python manage.py sqlmigrate news 0003
```

#### 4. 执行迁移

```bash
# 本地测试
python manage.py migrate

# 生产环境（在服务器上）
source /opt/HotNews/backend/.venv/bin/activate
cd /opt/HotNews/backend
python manage.py migrate
sudo systemctl restart hotnews-backend
```

### 前端组件开发

#### 添加新功能

编辑 [frontend/src/App.vue](frontend/src/App.vue)：

```vue
<template>
  <div class="container">
    <!-- 新增筛选功能 -->
    <div class="filter-bar">
      <button @click="filterBySource(1)">仅显示微博</button>
      <button @click="showAll()">显示全部</button>
    </div>

    <div class="rankings-container">
      <!-- ...existing code... -->
    </div>
  </div>
</template>

<script setup>
// ...existing code...

const filteredSources = ref([])

const filterBySource = (sourceId) => {
  filteredSources.value = sources.value.filter(s => s.id === sourceId)
}

const showAll = () => {
  filteredSources.value = sources.value
}
</script>
```

### 性能优化

#### 后端优化

**1. 数据库查询优化**：

```python
# views.py
articles = NewsArticle.objects.filter(
    source=source_id,
    batch_timestamp=latest_batch
).only('id', 'title', 'url', 'hot_rank')  # 仅查询需要的字段
```

**2. 缓存优化**：

```python
from django.core.cache import cache

# 缓存榜单数据 60 秒
cache_key = f'ranking_{source_id}'
data = cache.get(cache_key)
if not data:
    data = fetch_ranking_data(source_id)
    cache.set(cache_key, data, timeout=60)
```

**3. 批量插入优化**：

```python
# 使用 bulk_create 代替逐条插入
NewsArticle.objects.bulk_create([
    NewsArticle(title='...', url='...') for item in data
], batch_size=500)  # 每批 500 条
```

#### 前端优化

**1. 懒加载**：

```vue
<script setup>
import { ref, onMounted } from 'vue'

const visibleSources = ref([])

const loadMoreSources = () => {
  // 加载更多数据源
}

onMounted(() => {
  window.addEventListener('scroll', loadMoreSources)
})
</script>
```

**2. 虚拟滚动**（大数据量）：

```bash
npm install vue-virtual-scroller
```

---

## 🐛 故障排查

### 后端问题

#### 1. 服务无法启动

**症状**：
```bash
sudo systemctl status hotnews-backend
● hotnews-backend.service - HotNews Django Backend
   Loaded: loaded (/etc/systemd/system/hotnews-backend.service; enabled)
   Active: failed (Result: exit-code)
```

**排查步骤**：

```bash
# 查看详细日志
sudo journalctl -u hotnews-backend -n 100 --no-pager

# 手动启动测试
cd /opt/HotNews/backend
source .venv/bin/activate
gunicorn --bind 127.0.0.1:8090 HotNews.wsgi:application

# 常见错误：
# - ModuleNotFoundError: 虚拟环境依赖未安装
# - OperationalError: 数据库连接失败
# - PermissionError: 日志目录权限问题
```

**解决方法**：

```bash
# 重新安装依赖
source .venv/bin/activate
pip install -r requirements.txt

# 修复日志权限
sudo chown -R ubuntu:ubuntu /var/log/hotnews

# 测试数据库连接
python manage.py dbshell
```

#### 2. 数据库连接失败

**症状**：
```
django.db.utils.OperationalError: (2003, "Can't connect to MySQL server")
```

**排查步骤**：

```bash
# 1. 检查 RDS 白名单
# 阿里云控制台 → RDS → 数据安全性 → 白名单设置
# 添加 ECS 内网 IP 或公网 IP

# 2. 测试网络连通性
telnet rm-xxxxxxxx.mysql.rds.aliyuncs.com 3306

# 3. 验证凭据
mysql -h rm-xxxxxxxx.mysql.rds.aliyuncs.com -u xxx -p hot_list
```

#### 3. 静态文件 404

**症状**：
```
GET /static/admin/css/base.css => 404
```

**解决方法**：

```bash
# 收集静态文件
cd /opt/HotNews/backend
source .venv/bin/activate
python manage.py collectstatic --noinput

# 检查 Nginx 配置
sudo nginx -t
sudo systemctl restart nginx
```

### 前端问题

#### 1. 白屏或页面无法加载

**排查步骤**：

```bash
# 检查构建产物
ls -lh /var/www/hotnews/
# 应包含 index.html, assets/ 等文件

# 查看 Nginx 错误日志
sudo tail -f /var/log/nginx/hotnews_error.log

# 查看浏览器控制台
# F12 → Console 标签，查看 JavaScript 错误
```

**解决方法**：

```bash
# 重新构建
cd /opt/HotNews/frontend
npm install
npm run build
sudo rm -rf /var/www/hotnews/*
sudo cp -r dist/* /var/www/hotnews/
sudo systemctl restart nginx
```

#### 2. API 请求失败

**症状**：
```
GET https://hotnews.zhenbucuo.tech/api/sources/ => 502
```

**排查步骤**：

```bash
# 1. 检查后端服务
sudo systemctl status hotnews-backend
curl http://127.0.0.1:8090/api/sources/

# 2. 检查 Nginx 代理
sudo nginx -t
cat /etc/nginx/sites-enabled/hotnews.zhenbucuo.tech | grep "proxy_pass"

# 3. 查看 Nginx 日志
sudo tail -f /var/log/nginx/hotnews_error.log
```

### Nginx 问题

#### 配置测试失败

**症状**：
```bash
sudo nginx -t
nginx: configuration file /etc/nginx/nginx.conf test failed
```

**解决方法**：

```bash
# 查看详细错误
sudo nginx -t

# 常见错误：
# - 证书文件不存在
# - 配置文件语法错误（缺少分号）
# - 重复的 server_name

# 恢复备份配置
sudo cp /etc/nginx/sites-available/default.bak \
       /etc/nginx/sites-enabled/default
```

---

## 📊 监控与维护

### 日志管理

```bash
# 后端日志
sudo journalctl -u hotnews-backend -f          # 实时日志
sudo journalctl -u hotnews-backend -n 100       # 最近 100 行
tail -f /var/log/hotnews/gunicorn-access.log   # 访问日志
tail -f /var/log/hotnews/gunicorn-error.log    # 错误日志

# Nginx 日志
tail -f /var/log/nginx/hotnews_access.log       # 访问日志
tail -f /var/log/nginx/hotnews_error.log        # 错误日志

# 日志清理
sudo find /var/log -name "*.log" -mtime +30 -delete  # 删除 30 天前日志
```

### 性能监控

```bash
# 系统资源
htop                    # 实时资源监控
df -h                   # 磁盘使用
free -m                 # 内存使用
iostat                  # IO 统计

# 进程监控
ps aux | grep gunicorn  # 查看 Gunicorn 进程
ss -tlnp | grep :8090   # 查看端口占用
```

### 数据库维护

```bash
# 备份数据库
python manage.py dumpdata news > backup_$(date +%Y%m%d).json

# 恢复数据库
python manage.py loaddata backup_20260215.json

# 清理旧数据（保留最近 7 天）
python manage.py shell
>>> from news.models import NewsArticle
>>> from datetime import timedelta
>>> from django.utils import timezone
>>> old_date = timezone.now() - timedelta(days=7)
>>> NewsArticle.objects.filter(batch_timestamp__lt=old_date).delete()
```

### 更新部署

```bash
# 拉取最新代码
cd /opt/HotNews
git pull origin main

# 执行部署脚本
./deploy.sh

# 或手动执行
cd backend
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

cd ../frontend
npm install
npm run build
sudo cp -r dist/* /var/www/hotnews/

sudo systemctl restart hotnews-backend
sudo systemctl restart nginx
```

---

## 📝 常见问题 FAQ

### Q1: 如何切换数据库（SQLite → MySQL）？

**A**: 修改 `.env` 文件，然后重新执行迁移：

```bash
# 1. 修改 .env（删除 USE_SQLITE 行，配置 MySQL）
MYSQL_DATABASE=hot_list
MYSQL_HOST=localhost

# 2. 删除旧数据库
rm backend/db.sqlite3

# 3. 重新迁移
python manage.py migrate
```

### Q2: 如何添加新的管理员账号？

**A**:

```bash
cd /opt/HotNews/backend
source .venv/bin/activate
python manage.py createsuperuser
```

### Q3: 如何配置多个域名？

**A**: 修改 Nginx 配置的 `server_name`：

```nginx
server {
    listen 443 ssl http2;
    server_name hotnews.example.com another-domain.com;
    # ...
}
```

### Q4: 如何查看 API 响应时间？

**A**: 查看 Nginx 访问日志或使用 `curl` 测试：

```bash
curl -w "\nTime: %{time_total}s\n" https://hotnews.zhenbucuo.tech/api/sources/
```

### Q5: 如何备份整个项目？

**A**:

```bash
# 备份代码
cd /opt
tar -czf HotNews_backup_$(date +%Y%m%d).tar.gz HotNews/

# 备份数据库
python manage.py dumpdata > db_backup.json

# 备份 Nginx 配置
sudo cp -r /etc/nginx/sites-enabled /opt/nginx_backup
```

---

## 📞 技术支持

- **项目地址**: https://github.com/ZH1995/HotNews
- **问题反馈**: GitHub Issues
- **文档更新**: 2026-02-16

## 📄 License

MIT License - 详见 [LICENSE](LICENSE) 文件

---

**祝开发顺利！🎉**
