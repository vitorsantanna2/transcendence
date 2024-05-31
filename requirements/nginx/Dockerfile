# Use the debian
FROM debian

RUN apt update && apt install nginx  -y

# Expose ports 80 and 443
EXPOSE 443

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]