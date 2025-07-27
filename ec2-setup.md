# 🚀 Despliegue en Amazon EC2

## 📋 Prerrequisitos

- Cuenta de AWS
- Instancia EC2 (recomendado: t3.medium o superior)
- Acceso SSH a la instancia

## 🔧 Configuración de la Instancia EC2

### 1. Crear Instancia EC2

**Especificaciones recomendadas:**
- **Tipo**: t3.medium (2 vCPU, 4 GB RAM)
- **Sistema Operativo**: Amazon Linux 2
- **Almacenamiento**: 20 GB mínimo
- **Security Group**: Ver configuración abajo

### 2. Configurar Security Group

Crear un Security Group con las siguientes reglas:

| Tipo | Puerto | Origen | Descripción |
|------|--------|--------|-------------|
| SSH | 22 | Tu IP | Acceso SSH |
| HTTP | 80 | 0.0.0.0/0 | Frontend web |
| Custom TCP | 5000 | 0.0.0.0/0 | API Backend |

### 3. Conectar a la Instancia

```bash
# Conectar via SSH
ssh -i tu-key.pem ec2-user@tu-ip-publica

# O si usas AWS CLI
aws ec2 connect --instance-id i-1234567890abcdef0
```

## 🚀 Despliegue Automático

### Opción 1: Script Automático

```bash
# 1. Subir archivos a EC2
scp -i tu-key.pem -r ./* ec2-user@tu-ip-publica:~/auto-podcast-landing-page/

# 2. Conectar a EC2
ssh -i tu-key.pem ec2-user@tu-ip-publica

# 3. Navegar al directorio
cd auto-podcast-landing-page

# 4. Ejecutar script de despliegue
chmod +x deploy-ec2.sh
./deploy-ec2.sh
```

### Opción 2: Despliegue Manual

```bash
# 1. Actualizar sistema
sudo yum update -y

# 2. Instalar Docker
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# 3. Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 4. Crear directorio de datos
mkdir -p data
sudo chown -R ec2-user:ec2-user data

# 5. Desplegar aplicación
docker-compose up --build -d
```

## 🌐 Verificar Despliegue

### 1. Verificar Servicios

```bash
# Verificar que los contenedores estén corriendo
docker-compose ps

# Ver logs
docker-compose logs -f
```

### 2. Probar Endpoints

```bash
# Frontend
curl http://localhost

# API Health Check
curl http://localhost/health

# Contador
curl http://localhost/api/counter
```

### 3. Acceso Web

- **Frontend**: http://tu-ip-publica
- **API**: http://tu-ip-publica:5000
- **Health Check**: http://tu-ip-publica/health

## 📊 Gestión de Datos

### Ver Datos en Tiempo Real

```bash
# Ver emails registrados
docker exec -it $(docker-compose ps -q backend) cat /data/emails.csv

# Ver feedback
docker exec -it $(docker-compose ps -q backend) cat /data/feedback.csv

# Ver base de datos SQLite
docker exec -it $(docker-compose ps -q backend) sqlite3 /data/counter.db
```

### Descargar Datos

```bash
# Descargar CSV files
docker cp $(docker-compose ps -q backend):/data/emails.csv ./emails.csv
docker cp $(docker-compose ps -q backend):/data/feedback.csv ./feedback.csv

# Descargar base de datos
docker cp $(docker-compose ps -q backend):/data/counter.db ./counter.db
```

## 🔧 Mantenimiento

### Comandos Útiles

```bash
# Reiniciar servicios
docker-compose restart

# Parar servicios
docker-compose down

# Ver logs en tiempo real
docker-compose logs -f

# Actualizar aplicación
git pull
docker-compose up --build -d

# Backup de datos
tar -czf backup-$(date +%Y%m%d).tar.gz data/
```

### Monitoreo

```bash
# Ver uso de recursos
docker stats

# Ver espacio en disco
df -h

# Ver logs del sistema
sudo journalctl -u docker
```

## 🔒 Seguridad

### Recomendaciones

1. **Configurar HTTPS** con certificado SSL
2. **Limitar acceso SSH** a IPs específicas
3. **Configurar firewall** adicional
4. **Monitorear logs** regularmente
5. **Hacer backups** automáticos de datos

### Configurar HTTPS (Opcional)

```bash
# Instalar Certbot
sudo yum install -y certbot python3-certbot-nginx

# Obtener certificado SSL
sudo certbot --nginx -d tu-dominio.com

# Renovar automáticamente
sudo crontab -e
# Agregar: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 🆘 Troubleshooting

### Problemas Comunes

**Puerto 80 ocupado:**
```bash
sudo netstat -tulpn | grep :80
sudo systemctl stop httpd  # Si hay Apache corriendo
```

**Permisos de Docker:**
```bash
sudo usermod -a -G docker ec2-user
# Reconectar SSH
```

**Espacio en disco:**
```bash
docker system prune -a
df -h
```

**Logs de errores:**
```bash
docker-compose logs backend
docker-compose logs nginx
```

## 📞 Soporte

Si tienes problemas:

1. Verificar logs: `docker-compose logs -f`
2. Verificar servicios: `docker-compose ps`
3. Verificar conectividad: `curl http://localhost/health`
4. Revisar Security Group en AWS Console 