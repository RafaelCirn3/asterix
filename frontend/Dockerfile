FROM node:24.13

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

CMD ["npm", "start", "--", "--host", "0.0.0.0"]

