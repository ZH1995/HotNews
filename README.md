# HotNews（热点新闻聚合网站）

基于 Django + Vue 3 + Vite 的前后端分离热搜榜单聚合系统。

## 技术栈

- **后端**: Django 5.2 + Django REST Framework
- **前端**: Vue 3 + Vite
- **数据库**: MySQL (阿里云 RDS) / SQLite (本地开发)
- **部署**: Docker + Docker Compose + Nginx
- **服务器**: 阿里云 ECS (Ubuntu 22.04)

## 项目结构

```
HotNews/
├── .env                  # 环境变量配置
├── .env.example          # 环境变量模板
├── backend/              # Django 后端
│   ├── HotNews/          # Django 项目配置
│   ├── news/             # 新闻应用
│   ├── manage.py         # Django 管理脚本
│   ├── requirements.txt  # Python 依赖
│   └── Dockerfile        # 后端 Docker 镜像
├── frontend/             # Vue 3 + Vite 前端
│   ├── src/              # 源代码
│   ├── public/           # 静态资源
│   ├── package.json      # Node 依赖
│   ├── vite.config.js    # Vite 配置
│   └── Dockerfile        # 前端 Docker 镜像
├── docker-compose.yml    # 开发环境配置
├── docker-compose.prod.yml # 生产环境配置
└── deploy.sh             # 部署脚本
```

## 本地开发（不使用 Docker）

### 1. 环境准备

**必备工具**：
- Python 3.12+
- Node.js 20+
- Git

**可选工具**：
- MySQL 8.0（或使用 SQLite）

### 2. 克隆项目

```bash
git clone <your-repo-url>
cd HotNews
```

### 3. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
# Windows: notepad .env
# Linux/Mac: nano .env
```

**本地开发推荐配置**（使用 SQLite）：

```env
# Django Settings
SECRET_KEY=dev-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# 本地开发使用 SQLite
USE_SQLITE=True

# Database (阿里云 RDS - 生产环境使用)
MYSQL_DATABASE=hot_list
MYSQL_USER=dev
MYSQL_PASSWORD=your-password
MYSQL_HOST=your-rds-host.mysql.rds.aliyuncs.com
MYSQL_PORT=3306
```

### 4. 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户（用于访问 admin）
python manage.py createsuperuser

# 启动开发服务器
python manage.py runserver
```

**后端服务地址**：
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

### 5. 前端设置

**打开新的终端窗口**：

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

**前端服务地址**：
- 应用: http://localhost:5173/

### 6. 本地开发常用命令

#### 后端命令

```bash
cd backend

# 激活虚拟环境（每次打开新终端需要）
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 启动开发服务器
python manage.py runserver

# 启动并指定端口
python manage.py runserver 0.0.0.0:8000

# 数据库操作
python manage.py makemigrations      # 创建迁移文件
python manage.py migrate             # 执行迁移
python manage.py showmigrations      # 查看迁移状态

# 创建管理员账号
python manage.py createsuperuser

# 进入 Django Shell（调试用）
python manage.py shell

# 运行测试
python manage.py test

# 收集静态文件
python manage.py collectstatic

# 抓取热搜数据（需先实现爬虫）
python manage.py fetch_hot_news
python manage.py fetch_hot_news --source 1  # 抓取指定源

# 数据库查询示例
python manage.py shell
>>> from news.models import NewsArticle
>>> NewsArticle.objects.count()
>>> NewsArticle.objects.filter(source=1).count()
```

#### 前端命令

```bash
cd frontend

# 开发服务器
npm run dev

# 生产构建
npm run build

# 预览生产构建
npm run preview

# 安装新依赖
npm install package-name

# 更新依赖
npm update

# 代码格式化（如果配置了）
npm run format

# 代码检查（如果配置了）
npm run lint
```

### 7. 调试技巧

#### 后端调试

**查看 SQL 查询**：

在 `settings.py` 中添加：

```python
if DEBUG:
    LOGGING = {
        'version': 1,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },
    }
```

**使用 Django Debug Toolbar**：

```bash
pip install django-debug-toolbar
```

**测试 API**：

```bash
# 使用 curl
curl http://localhost:8000/api/sources/

# 使用 httpie（更友好）
http http://localhost:8000/api/sources/

# 或直接在浏览器打开
```

#### 前端调试

**浏览器开发者工具**：
- F12 打开开发者工具
- Network 标签：查看 API 请求
- Console 标签：查看日志和错误
- Vue DevTools：安装 Vue.js devtools 扩展

**Vite 配置调试**：

在 `vite.config.js` 中添加：

```javascript
server: {
  proxy: {
    '/api': {
      configure: (proxy, options) => {
        proxy.on('proxyReq', (proxyReq, req, res) => {
          console.log('代理请求:', req.method, req.url)
        })
      }
    }
  }
}
```

### 8. 常见问题

#### 问题 1：端口被占用

**症状**：`Address already in use`

**解决**：

```bash
# Windows - 查找占用 8000 端口的进程
netstat -ano | findstr :8000
# 结束进程（替换 PID）
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

#### 问题 2：数据库连接失败

**症状**：`Can't connect to MySQL server`

**解决**：

```env
# .env 文件中设置
USE_SQLITE=True
```

#### 问题 3：前端请求 404

**检查**：
1. 后端是否运行在 8000 端口
2. vite.config.js 中 proxy 配置是否正确
3. 后端路由是否正确（查看 urls.py）

```bash
# 测试后端 API
curl http://localhost:8000/api/sources/
```

#### 问题 4：CORS 错误

**症状**：`Access-Control-Allow-Origin`

**解决**：检查 `.env` 中的 CORS 配置：

```env
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

#### 问题 5：静态文件 404

```bash
# 收集静态文件
python manage.py collectstatic --noinput
```

## Docker 容器化开发

### 1. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，Docker 环境无需修改太多
```

### 2. 启动开发环境

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 仅启动后端
docker-compose up -d backend

# 仅启动前端
docker-compose up -d frontend
```

### 3. 访问应用

- 前端: http://localhost:5173
- 后端 API: http://localhost:8000/api
- 后端管理: http://localhost:8000/admin

### 4. Docker 常用命令

```bash
# 查看容器状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 进入容器
docker-compose exec backend bash
docker-compose exec frontend sh

# 重启服务
docker-compose restart backend
docker-compose restart frontend

# 停止服务
docker-compose stop

# 停止并删除容器
docker-compose down

# 重新构建并启动
docker-compose up -d --build

# 执行数据库迁移
docker-compose exec backend python manage.py migrate

# 创建超级用户
docker-compose exec backend python manage.py createsuperuser

# 查看容器资源使用
docker stats
```

## 生产环境部署 (阿里云 ECS)

### 1. 服务器准备

```bash
# 安装 Docker
curl -fsSL https://get.docker.com | bash -s docker
sudo systemctl start docker
sudo systemctl enable docker

# 安装 Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 安装 Git
sudo apt update
sudo apt install git -y
```

### 2. 克隆项目

```bash
cd /opt
sudo git clone <your-repo-url> HotNews
cd HotNews
```

### 3. 配置环境

```bash
# 复制并编辑环境变量
sudo cp .env.example .env
sudo nano .env

# 配置以下必填项:
# - SECRET_KEY (生成随机密钥)
# - DEBUG=False
# - ALLOWED_HOSTS (你的域名或IP)
# - USE_SQLITE=False
# - MYSQL_* (RDS 连接信息)
```

### 4. 执行部署

```bash
# 添加执行权限
sudo chmod +x deploy.sh

# 执行部署
sudo ./deploy.sh
```

### 5. 配置防火墙

```bash
# 开放 80 端口
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp  # 如果使用 HTTPS
```

### 6. 配置域名 (可选)

在阿里云控制台配置域名解析，将域名指向 ECS 公网 IP。

## 生产环境常用命令

```bash
# 查看容器状态
docker-compose -f docker-compose.prod.yml ps

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend

# 进入后端容器
docker-compose -f docker-compose.prod.yml exec backend bash

# 执行数据库迁移
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

# 创建超级用户
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser

# 收集静态文件
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput

# 重启服务
docker-compose -f docker-compose.prod.yml restart

# 更新代码并重新部署
git pull origin main
docker-compose -f docker-compose.prod.yml up -d --build

# 查看容器资源使用情况
docker stats

# 清理未使用的镜像和容器
docker system prune -a

# 查看磁盘使用
df -h

# 备份数据库（如果使用 SQLite）
docker-compose -f docker-compose.prod.yml exec backend python manage.py dumpdata > backup.json

# 恢复数据库
docker-compose -f docker-compose.prod.yml exec backend python manage.py loaddata backup.json
```

## API 文档

### 获取数据源列表

```http
GET /api/sources/
```

**响应示例**：

```json
{
  "sources": [
    {
      "id": 1,
      "title": "微博",
      "logo": "/images/weibo_logo.png",
      "limit": 50
    }
  ]
}
```

### 获取指定榜单数据

```http
GET /api/ranking/<source_id>/
```

**响应示例**：

```json
{
  "id": 1,
  "title": "微博",
  "logo": "/images/weibo_logo.png",
  "articles": [
    {
      "id": 123,
      "title": "热搜标题",
      "url": "https://...",
      "hot_rank": 1
    }
  ]
}
```

## 开发工作流

### 1. 功能开发流程

```bash
# 1. 创建功能分支
git checkout -b feature/new-feature

# 2. 启动开发服务器
cd backend && python manage.py runserver  # 终端 1
cd frontend && npm run dev                # 终端 2

# 3. 开发并测试

# 4. 提交代码
git add .
git commit -m "feat: 添加新功能"
git push origin feature/new-feature

# 5. 创建 Pull Request 并合并
```

### 2. 数据库变更流程

```bash
# 1. 修改 models.py

# 2. 创建迁移文件
python manage.py makemigrations

# 3. 查看 SQL 语句（可选）
python manage.py sqlmigrate news 0001

# 4. 执行迁移
python manage.py migrate

# 5. 提交迁移文件
git add backend/news/migrations/
git commit -m "feat: 添加新表字段"
```

### 3. 添加新的爬虫数据源

```bash
# 1. 在 views.py 中添加数据源配置

# 2. 创建爬虫脚本
# backend/news/management/commands/fetch_SOURCE_NAME.py

# 3. 测试爬虫
python manage.py fetch_hot_news --source SOURCE_ID

# 4. 配置定时任务（crontab 或 APScheduler）
```

## 监控与维护

### 健康检查

```bash
# 检查服务状态
curl http://localhost:8000/api/sources/
curl http://localhost:5173/

# 检查容器健康
docker-compose ps
docker inspect --format='{{.State.Health.Status}}' container_name
```

### 日志管理

```bash
# 查看实时日志
docker-compose logs -f --tail=100 backend

# 清理日志（docker-compose.yml 中配置日志轮转）
docker-compose logs --no-log-prefix backend > backend.log
```

### 性能监控

```bash
# 容器资源使用
docker stats

# 系统资源
htop
df -h
free -m
```

## 故障排查

### 1. 容器无法启动

**检查**：
- `.env` 配置是否正确
- 端口是否被占用
- Docker 是否正常运行

```bash
docker-compose ps
docker-compose logs backend
```

### 2. 数据库连接失败

**检查**：
- RDS 白名单是否配置
- 数据库凭据是否正确
- 网络是否可达

```bash
# 测试数据库连接
docker-compose exec backend python test_mysql.py
```

### 3. 前端无法访问后端

**检查**：
- CORS 配置
- Vite 代理配置
- 后端路由配置

```bash
# 查看网络请求
curl -I http://localhost:8000/api/sources/
```

### 4. 502 Bad Gateway

**可能原因**：
- 后端服务未启动
- Nginx 配置错误
- 容器网络问题

```bash
docker-compose ps
docker-compose logs nginx
docker network ls
```

## 技术支持

- 项目文档：查看代码注释
- Issue 提交：GitHub Issues
- 联系方式：查看项目主页

## License

MIT

---
