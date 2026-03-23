FROM node:20-alpine AS builder

WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

COPY . .
# Point API calls at the nginx reverse proxy in production
ENV VITE_API_URL=""
RUN npm run build

FROM nginx:1.27-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
# SPA fallback — serve index.html for all routes
RUN echo 'server { listen 80; root /usr/share/nginx/html; location / { try_files $uri $uri/ /index.html; } }' \
    > /etc/nginx/conf.d/default.conf
EXPOSE 80
