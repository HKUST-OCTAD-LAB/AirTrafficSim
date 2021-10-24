# Stage 1: Build react client
FROM node:lts-alpine

# Working directory be app
WORKDIR /usr/app

COPY package*.json ./

# Install dependencies
RUN yarn install

# copy local files to app folder
COPY . .

EXPOSE 3000

CMD ["yarn","start"]

# # => Run container
# FROM nginx:1.16.0

# COPY --from=build /cloudl-client/build /usr/share/nginx/html

# RUN rm /etc/nginx/conf.d/default.conf

# COPY nginx/nginx.conf /etc/nginx/conf.d

# EXPOSE 80

# # Start Nginx server
# CMD ["/bin/bash", "-c", "nginx -g \"daemon off;\""]