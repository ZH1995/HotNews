#!/bin/bash

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}开始部署 HotNews (原生部署)...${NC}"

cd /opt/HotNews

# 1. 拉取最新代码
echo -e "${YELLOW}[1/6] 拉取最新代码...${NC}"
git pull origin main

# 2. 后端部署
echo -e "${YELLOW}[2/6] 更新后端...${NC}"
cd backend
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
#python manage.py migrate
python manage.py collectstatic --noinput
deactivate

# 3. 前端构建
echo -e "${YELLOW}[3/6] 构建前端...${NC}"
cd /opt/HotNews/frontend
npm install
npm run build

# 4. 部署前端静态文件
echo -e "${YELLOW}[4/6] 部署前端...${NC}"
sudo rm -rf /var/www/hotnews/*
sudo cp -r dist/* /var/www/hotnews/
sudo chown -R www-data:www-data /var/www/hotnews
sudo chmod -R 755 /var/www/hotnews

# 5. 重启后端服务
echo -e "${YELLOW}[5/6] 重启后端服务...${NC}"
sudo systemctl restart hotnews-backend
sleep 3

# 6. 重启 Nginx
echo -e "${YELLOW}[6/6] 重启 Nginx...${NC}"
sudo nginx -t
sudo systemctl restart nginx

# 检查服务状态
echo -e "${GREEN}检查服务状态...${NC}"
sudo systemctl status hotnews-backend --no-pager
sudo systemctl status nginx --no-pager

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}部署完成!${NC}"
echo -e "${GREEN}访问地址: https://hotnews.zhenbucuo.tech${NC}"
echo -e "${GREEN}========================================${NC}"