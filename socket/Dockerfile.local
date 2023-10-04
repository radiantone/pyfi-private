FROM node:16

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY server.ts server.ts

EXPOSE 3003

CMD [ "npx","ts-node","server.ts" ]


