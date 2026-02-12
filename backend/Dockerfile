FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 非 root 用户运行
RUN useradd -m -u 1000 appuser

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY --chown=appuser:appuser . .

# 收集静态文件
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

# 改用非 root 用户
USER appuser

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/sources/ || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "HotNews.wsgi:application"]
