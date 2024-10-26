# build environment
FROM node:18-alpine as build
WORKDIR /app
COPY package.json package.json
# RUN yarn
# RUN npx browserslist@latest --update-db
RUN yarn install
COPY . .
# RUN yarn start
Run yarn build

# production environment
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY --from=build /app/nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]