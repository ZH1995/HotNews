FROM node:24-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# 使用轻量级 HTTP 服务器
FROM node:24-alpine

WORKDIR /app

RUN npm install -g http-server

COPY --from=builder /app/dist /app/dist

EXPOSE 80

CMD ["http-server", "dist", "-p", "80", "--cors", "-c-1"]