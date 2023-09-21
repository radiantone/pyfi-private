FROM node:16

WORKDIR /usr/src/app

COPY socket/package*.json ./

RUN npm install

COPY socket/server.ts server.ts

EXPOSE 3003

CMD [ "npx","ts-node","server.ts" ]


