FROM nginx:alpine

WORKDIR /usr/share/nginx/html

# Copy the frontend files
COPY index.html .

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
