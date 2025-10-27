FROM nginx:alpine

# Copiar configuración personalizada
COPY nginx.conf /etc/nginx/nginx.conf

# Exponer puerto 8080
EXPOSE 8080

# Comando por defecto
CMD ["nginx", "-g", "daemon off;"]


