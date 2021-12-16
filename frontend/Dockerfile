FROM node:current-alpine
WORKDIR /usr/src/app

COPY package*.json .
COPY svelte.config.js .
COPY tsconfig.json .

RUN npm install
