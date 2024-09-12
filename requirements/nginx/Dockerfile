FROM debian

RUN apt update && apt install nginx  -y

EXPOSE 8443

CMD ["nginx", "-g", "daemon off;"]