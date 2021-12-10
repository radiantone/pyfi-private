FROM node:16

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY server.js server.js

EXPOSE 3000

CMD [ "node", "server.js" ]


