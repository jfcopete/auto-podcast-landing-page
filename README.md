# AI Podcast Generator Landing Page

Una landing page moderna para un generador de podcasts con IA, con sistema de contador oculto y base de datos SQLite.

## 🚀 Quick Start

### ⚠️ Importante: No abrir index.html directamente
Si abres `index.html` directamente en el navegador, verás errores de CORS. **Usa Docker** para funcionalidad completa.

### Pasos rápidos:
```bash
# 1. Clonar y entrar al directorio
git clone <repository-url>
cd auto-podcast-landing-page

# 2. Crear directorio de datos
mkdir -p data

# 3. Ejecutar con Docker
docker-compose up --build

# 4. Abrir en navegador
# http://localhost
```

## 🚀 Características

- **Landing page responsive** con diseño moderno
- **Sistema de contador oculto** que guarda emails verificados en SQLite
- **Sección de feedback** para nuevas ideas y comentarios
- **Docker setup** con persistencia de datos
- **API REST** para manejo de formularios
- **Muestras de audio** con indicadores de idioma

## 🎵 Muestras de Audio

El proyecto incluye 3 muestras de audio para demostrar las capacidades del generador de podcasts:

### Archivos de Audio Requeridos:

**Ubicación:** `assets/audios/`

1. **Vulnerabilidades en AI.wav**
   - Idioma: Español
   - Categoría: Tecnología
   - Duración: ~6 min
   - Descripción: Vulnerabilidades en sistemas de IA

2. **Technical Analysis for Stock Market Investment.wav**
   - Idioma: Inglés
   - Categoría: Finanzas
   - Duración: ~7 min
   - Descripción: Análisis técnico de inversiones en bolsa

3. **Dopamine Fasting_ Science, Habits, and Self-Control.wav**
   - Idioma: Español
   - Categoría: Salud
   - Duración: ~7 min
   - Descripción: Ciencia del ayuno de dopamina y productividad

### Estructura de Carpetas:
```
auto-podcast-landing-page/
├── assets/
│   └── audios/
│       ├── Vulnerabilidades en AI.wav
│       ├── Technical Analysis for Stock Market Investment.wav
│       └── Dopamine Fasting_ Science, Habits, and Self-Control.wav
├── index.html
├── style.css
├── script.js
└── ...
```

### Notas Importantes:
- **Formato**: Los archivos deben estar en formato `.wav`
- **Nombres**: Los nombres de archivo deben coincidir exactamente con los especificados
- **Tamaño**: Recomendado mantener archivos bajo 10MB para mejor rendimiento
- **Calidad**: Usar calidad de audio estándar (44.1kHz, 16-bit)

### 🔧 Solución de Problemas de Audio

Si el botón de audio no funciona:

1. **Verificar que el archivo existe:**
   ```bash
   ls -la assets/audios/
   ```

2. **Verificar permisos del archivo:**
   ```bash
   chmod 644 assets/audios/*.wav
   ```

3. **Verificar en el navegador:**
   - Abrir las herramientas de desarrollador (F12)
   - Ir a la pestaña "Console"
   - Buscar mensajes de error relacionados con audio

4. **Formatos alternativos soportados:**
   - `.wav` (principal)
   - `.mp3` (alternativo)
   - `.ogg` (alternativo)

5. **Crear archivo de prueba:**
   ```bash
   # Si no tienes el archivo, puedes crear uno de prueba
   ffmpeg -f lavfi -i "sine=frequency=1000:duration=10" "assets/audios/Dopamine Fasting_ Science, Habits, and Self-Control.wav"
   ```

6. **Convención de nombres de archivos:**
   - ✅ **Correcto**: `Dopamine Fasting_ Science, Habits, and Self-Control.wav`
   - ❌ **Incorrecto**: `dopamine-fasting.wav`
   - **Regla**: Mantener espacios, guiones bajos y mayúsculas como en el archivo original

## 🛠️ Instalación y Ejecución

### Prerrequisitos
- Docker
- Docker Compose

### Pasos para ejecutar

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd auto-podcast-landing-page
   ```

2. **Crear directorio de datos**
   ```bash
   mkdir -p data
   ```

3. **Ejecutar con Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Acceder a la aplicación**
   - Frontend: http://localhost
   - API Backend: http://localhost:5000
   - Health Check: http://localhost/health

## 📊 Base de Datos y Archivos CSV

### Estructura de tablas

**email_submissions**
- `id`: ID único
- `email`: Email del usuario
- `categories`: Categorías seleccionadas (separadas por comas)
- `timestamp`: Fecha y hora de registro
- `ip_address`: IP del usuario

**feedback**
- `id`: ID único
- `type`: Tipo de feedback ('idea' o 'feedback')
- `content`: Contenido del feedback
- `email`: Email opcional del usuario
- `ip_address`: IP del usuario
- `timestamp`: Fecha y hora de registro

**kano_surveys**
- `id`: ID único
- `email`: Email opcional del usuario
- `ip_address`: IP del usuario
- `timestamp`: Fecha y hora de registro
- **Personalización**: funcional, disfuncional
- **Duración**: funcional, disfuncional
- **Voz**: funcional, disfuncional
- **Fuentes**: funcional, disfuncional

### Archivos CSV generados

**emails.csv**
- Contiene todos los emails registrados
- Se actualiza automáticamente con cada nuevo registro
- Formato: id, email, categories, ip_address, timestamp

**feedback.csv**
- Contiene todo el feedback e ideas recibidas
- Se actualiza automáticamente con cada nuevo registro
- Formato: id, type, content, email, ip_address, timestamp

**kano_surveys.csv**
- Contiene todas las respuestas de la encuesta de Kano
- Se actualiza automáticamente con cada nueva encuesta
- Formato: id, email, ip_address, timestamp + respuestas de las 4 características

### Acceder a la base de datos

```bash
# Conectar a la base de datos
docker exec -it auto-podcast-landing-page_backend_1 sqlite3 /data/counter.db

# Ver todas las tablas
.tables

# Ver emails registrados
SELECT * FROM email_submissions;

# Ver feedback
SELECT * FROM feedback;

# Ver encuestas de Kano
SELECT * FROM kano_surveys;

# Contar total de emails
SELECT COUNT(*) FROM email_submissions;

# Contar total de encuestas Kano
SELECT COUNT(*) FROM kano_surveys;

# Salir
.quit
```

### Acceder a los archivos CSV

```bash
# Ver archivos CSV en el directorio de datos
docker exec -it auto-podcast-landing-page_backend_1 ls -la /data/

# Ver contenido de emails.csv
docker exec -it auto-podcast-landing-page_backend_1 cat /data/emails.csv

# Ver contenido de feedback.csv
docker exec -it auto-podcast-landing-page_backend_1 cat /data/feedback.csv

# Ver contenido de kano_surveys.csv
docker exec -it auto-podcast-landing-page_backend_1 cat /data/kano_surveys.csv

# Descargar archivos CSV al host
docker cp auto-podcast-landing-page_backend_1:/data/emails.csv ./emails.csv
docker cp auto-podcast-landing-page_backend_1:/data/feedback.csv ./feedback.csv
docker cp auto-podcast-landing-page_backend_1:/data/kano_surveys.csv ./kano_surveys.csv
```

## 🔧 API Endpoints

### POST /api/submit-email
Envía un email y categorías al sistema.

**Body:**
```json
{
  "email": "usuario@ejemplo.com",
  "categories": ["tech", "finanzas"]
}
```

### GET /api/counter
Obtiene el total de emails registrados.

**Response:**
```json
{
  "count": 42
}
```

### POST /api/feedback
Envía feedback o nuevas ideas.

**Body:**
```json
{
  "type": "idea",
  "content": "Me gustaría ver podcasts sobre...",
  "email": "usuario@ejemplo.com"
}
```

### POST /api/kano-survey
Envía respuestas de la encuesta de Kano.

**Body:**
```json
{
  "email": "usuario@ejemplo.com",
  "personalizacion_funcional": "me_encantaria",
  "personalizacion_disfuncional": "lo_odiaria",
  "duracion_funcional": "lo_espero",
  "duracion_disfuncional": "podria_vivir_con_ello",
  "voz_funcional": "me_encantaria",
  "voz_disfuncional": "lo_odiaria",
  "fuentes_funcional": "me_encantaria",
  "fuentes_disfuncional": "lo_odiaria"
}
```

### GET /api/export-data
Exporta todos los datos como JSON.

**Response:**
```json
{
  "success": true,
  "timestamp": "2024-01-01T10:00:00Z",
  "data": {
    "emails": {
      "count": 42,
      "records": [
        {
          "id": 1,
          "email": "usuario@ejemplo.com",
          "categories": ["marketing", "tech"],
          "podcast_request": "Podcast sobre IA",
          "ip_address": "192.168.1.1",
          "timestamp": "2024-01-01 10:00:00"
        }
      ]
    },
    "feedback": {
      "count": 15,
      "records": [...]
    },
    "kano_surveys": {
      "count": 8,
      "records": [...]
    }
  }
}
```

### GET /api/emails
Obtiene todas las suscripciones de email.

### GET /api/feedback
Obtiene todo el feedback.

### GET /api/kano-surveys
Obtiene todas las encuestas de Kano.

### GET /health
Health check del sistema.

## 📁 Estructura del Proyecto

```
auto-podcast-landing-page/
├── index.html          # Página principal
├── style.css           # Estilos CSS
├── script.js           # JavaScript del frontend
├── app.py              # Backend Flask
├── requirements.txt    # Dependencias Python
├── Dockerfile          # Configuración Docker
├── docker-compose.yml  # Orquestación Docker
├── nginx.conf          # Configuración Nginx
├── assets/             # Archivos multimedia
│   └── audios/         # Muestras de audio
└── data/               # Base de datos SQLite (creado automáticamente)
```

## 🔒 Seguridad

- **Validación de emails**: Verificación de formato básico
- **Prevención de duplicados**: No se permiten emails repetidos
- **Registro de IPs**: Para auditoría y análisis
- **CORS configurado**: Para desarrollo local

## 📱 Responsive Design

La aplicación está optimizada para:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

## 🚀 Despliegue

### Producción
1. Configurar variables de entorno
2. Usar HTTPS
3. Configurar dominio personalizado
4. Monitorear logs y métricas

### Desarrollo
```bash
# Modo desarrollo
docker-compose up --build

# Ver logs
docker-compose logs -f

# Reconstruir después de cambios
docker-compose down
docker-compose up --build
```

## 📈 Monitoreo

- **Health checks** automáticos cada 30 segundos
- **Logs** disponibles en Docker Compose
- **Base de datos** persistente en `./data/`

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abrir un Pull Request

## 🚀 Despliegue en Elastic Beanstalk

### Prerrequisitos

1. **AWS CLI configurado**
   ```bash
   aws configure
   ```

2. **EB CLI instalado**
   ```bash
   pip install awsebcli
   ```

3. **Docker instalado** (para construir la imagen)

### Pasos de Despliegue

1. **Inicializar aplicación EB**
   ```bash
   eb init auto-podcast-app --platform docker --region us-east-1
   ```

2. **Crear ambiente**
   ```bash
   eb create auto-podcast-env --instance-type t3.micro
   ```

3. **Desplegar aplicación**
   ```bash
   chmod +x deploy-eb.sh
   ./deploy-eb.sh
   ```

### ⚠️ Consideraciones Importantes

#### **Persistencia de Datos**
- **EB no persiste archivos locales** entre deployments
- **Los datos se pierden** cuando se reinicia la instancia
- **Solución**: Usar RDS (PostgreSQL/MySQL) o S3 para datos persistentes

#### **Limitaciones**
- **Sin volúmenes Docker**: No puedes usar `./data:/data`
- **Sin Docker Compose**: Solo un contenedor por instancia
- **Sin archivos locales**: Los CSV se pierden en reinicios

#### **Recomendaciones**
- **Desarrollo**: Usar EC2 con Docker Compose
- **Producción**: Usar EB + RDS para datos persistentes
- **Backup**: Configurar S3 para backups automáticos

### 🔧 Configuración Alternativa

Para **datos persistentes** en EB, considera:

1. **Base de datos externa** (RDS)
2. **Almacenamiento S3** para archivos
3. **DynamoDB** para datos estructurados

## 📊 Persistencia de Datos
