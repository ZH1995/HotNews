# HotNews

热点新闻网站

## 环境设置

1. 创建虚拟环境
```bash
python3 -m venv .venv
```

2. 激活虚拟环境
```bash
# 在macOS或Linux上
source .venv/bin/activate
# 在Windows上
.venv\Scripts\activate
```

3.安装依赖
```bash
pip install -r requirements.txt
```

## 启动服务器
```bash
python manage.py runserver 0.0.0.0:8000
```

**注意:**

- 0.0.0.0表示允许所有IP访问

- 如果使用云服务，请先在安全规则中开放相应端口