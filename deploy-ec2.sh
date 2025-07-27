#!/bin/bash

# Script de despliegue para EC2
# AI Podcast Generator Landing Page

echo "🚀 Iniciando despliegue en EC2..."

# Actualizar el sistema
echo "📦 Actualizando sistema..."
sudo yum update -y

# Instalar Docker
echo "🐳 Instalando Docker..."
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Instalar Docker Compose
echo "📦 Instalando Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Crear directorio de datos
echo "📁 Creando directorio de datos..."
mkdir -p data

# Dar permisos necesarios
echo "🔐 Configurando permisos..."
sudo chown -R ec2-user:ec2-user data

# Construir y ejecutar la aplicación
echo "🏗️ Construyendo aplicación..."
docker-compose up --build -d

# Verificar que los servicios estén corriendo
echo "🔍 Verificando servicios..."
sleep 10
docker-compose ps

# Mostrar información de acceso
echo ""
echo "✅ Despliegue completado!"
echo ""
echo "🌐 URLs de acceso:"
echo "   - Frontend: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo "   - API Backend: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):5000"
echo "   - Health Check: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)/health"
echo ""
echo "📊 Para ver los datos:"
echo "   - Emails: docker exec -it \$(docker-compose ps -q backend) cat /data/emails.csv"
echo "   - Feedback: docker exec -it \$(docker-compose ps -q backend) cat /data/feedback.csv"
echo ""
echo "📝 Comandos útiles:"
echo "   - Ver logs: docker-compose logs -f"
echo "   - Parar: docker-compose down"
echo "   - Reiniciar: docker-compose restart" 