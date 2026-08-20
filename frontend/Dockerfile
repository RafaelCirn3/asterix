FROM node:24.13-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

RUN npm run build -- --configuration production \
    && mkdir -p /dist-output \
    && if [ -d /app/dist/frontend/browser ]; then cp -r /app/dist/frontend/browser/. /dist-output/; \
       else cp -r /app/dist/frontend/. /dist-output/; fi

FROM nginx:1.27-alpine AS runtime

COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=build /dist-output/ /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

