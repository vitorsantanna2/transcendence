# Use the official Nginx base image
FROM nginx

# Copy the SSL certificate and key to the container
COPY ../../local/ssl/fullchain.pem /etc/nginx/ssl/fullchain.pem
COPY ../../local/ssl/privkey.pem /etc/nginx/ssl/privkey.pem

# Copy the Nginx configuration file to the container
COPY conf/nginx.conf /etc/nginx/nginx.conf

# Expose ports 80 and 443
EXPOSE 443

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]