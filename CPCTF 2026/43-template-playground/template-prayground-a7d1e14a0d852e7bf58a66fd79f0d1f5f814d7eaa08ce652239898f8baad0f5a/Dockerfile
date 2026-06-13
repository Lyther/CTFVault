FROM node:25-alpine

WORKDIR /app
COPY app/package*.json ./
RUN npm install --omit=dev
COPY app/ ./

COPY flag.txt /flag.txt

EXPOSE 3000
CMD ["node", "server.js"]
