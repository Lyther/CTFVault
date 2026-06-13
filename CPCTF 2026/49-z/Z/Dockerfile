FROM node:24.15.0-bookworm-slim

RUN npm install -g pnpm

WORKDIR /app

COPY . .

RUN pnpm install
RUN pnpm --filter client build
RUN mkdir -p server/public && cp -r client/dist/* server/public/

WORKDIR /app/server

EXPOSE 3000

CMD ["pnpm", "start"]
