FROM mcr.microsoft.com/playwright:v1.59.1-noble

WORKDIR /app
ENV NODE_ENV=production

COPY package*.json ./
RUN npm ci --omit=dev && npx playwright install chromium --with-deps

COPY index.js ./

USER pwuser
EXPOSE 8081

CMD ["node", "--run", "start"]
