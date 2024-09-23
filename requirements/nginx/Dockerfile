FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

COPY requirements/nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]