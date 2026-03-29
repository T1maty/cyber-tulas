FROM node:20-alpine

WORKDIR /app

COPY package*.json ./


RUN npm install


COPY . .

EXPOSE 8080


CMD ["npx", "http-server", "-p", "3000", "-c-1"]