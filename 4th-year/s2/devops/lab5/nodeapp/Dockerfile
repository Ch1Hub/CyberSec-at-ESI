FROM node:20-alpine

WORKDIR /app

COPY package.json ./
COPY server.js ./

ENV NODE_ENV=production
ENV PORT=3000
ENV APP_VERSION=v1

EXPOSE 3000

CMD ["npm", "start"]

