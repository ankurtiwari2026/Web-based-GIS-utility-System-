FROM node:20-alpine
WORKDIR /usr/src/app
COPY package.json package-lock.json* ./
RUN npm install --no-audit --no-fund
COPY src ./src
EXPOSE 8080
CMD ["npm", "run", "start"]

