FROM node:18-alpine

WORKDIR /app

# package.json ve package-lock.json varsa kopyala
COPY package*.json ./

RUN npm install

# Tüm dosyaları kopyala
COPY . .

# Varsayalım ana dosyan index.js
CMD ["node", "index.js"]

