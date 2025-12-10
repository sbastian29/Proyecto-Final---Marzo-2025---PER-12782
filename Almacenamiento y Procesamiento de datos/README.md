# 📄 README: Proyecto TFM - Procesamiento de Datos en Tiempo Real y Análisis de Churn

## 🚀 Visión General

Este repositorio contiene el código y la infraestructura necesarios para un proyecto de Trabajo de Fin de Máster (TFM) centrado en el **procesamiento de datos semi-estructurados en tiempo real** (utilizando Apache Kafka y Apache Spark Streaming) y el **análisis del churn** (abandono de clientes) en el sector de las telecomunicaciones.

La infraestructura se orquesta mediante **Docker Compose** para asegurar un entorno de desarrollo reproducible y coherente.

## 🏗️ Estructura del Proyecto

El directorio raíz (`TFM`) organiza el proyecto en los siguientes componentes clave:

| Directorio/Archivo | Descripción |
|-------------------|-------------|
| `database/` | Contiene los scripts de inicialización de la base de datos PostgreSQL. Incluye la creación de la base de datos, las tablas, los índices (para optimizar el rendimiento de las consultas y la velocidad de búsqueda) y una vista predefinida para facilitar la consulta rápida de datos completos de un cliente. |
| `scripts/` | Almacena los principales scripts de Python para la lógica de negocio del proyecto. Estos scripts son montados como volúmenes en los contenedores de Spark y Spark Notebook. |
| `scripts/Kafka/` | Contiene la lógica para la ingestión y el manejo de datos con Apache Kafka. Hay un único script principal aquí para el rol de **Productor** que simula el envío de datos de churn. |
| `scripts/spark/` | Contiene la lógica para el procesamiento de streaming de datos con Apache Spark. Hay un único script principal aquí que actúa como **Consumidor** de Kafka y realiza el procesamiento. |
| `Health/` | Carpeta dedicada a los scripts o archivos para realizar chequeos de salud (Health Checks) de los servicios en los contenedores de Docker, asegurando que cada componente esté operativo. |
| `Attachments/` | Carpeta para archivos de entrada semi-estructurados, como `telecom_churn_semi_structured.json`, que se utilizarán para la simulación de datos o pruebas. |
| `.vscode/` | Configuración específica del editor VS Code (opcional). |
| `.env`/`.gitignore` | Archivos de configuración de entorno y de exclusión de archivos para el control de versiones. |
| `venv/` | Entorno virtual de Python para gestionar las dependencias locales. |
| `requirements.txt` | Lista de dependencias de Python del proyecto. |
| `docker-compose.yml` | Archivo de configuración que define y orquesta todos los servicios de la infraestructura Docker. |

## ⚙️ Infraestructura con Docker Compose

La infraestructura del proyecto se levanta con `docker-compose.yml`, que define los siguientes servicios clave:

| Servicio | Imagen Base | Puerto | Descripción |
|----------|-------------|--------|-------------|
| `postgres-tfm` | `postgres:15` | 5433:5432 | Base de datos PostgreSQL para persistir los resultados del análisis de churn. Se inicializa con los scripts de la carpeta `database/`. |
| `pgadmin-tfm` | `dpage/pgadmin4` | 8080:80 | Interfaz web PgAdmin para gestionar la base de datos PostgreSQL. |
| `zookeeper` | `confluentinc/cp-zookeeper` | 2181:2181 | Coordinador necesario para que Kafka funcione. |
| `kafka` | `confluentinc/cp-kafka` | 9092:9092 | Broker de mensajes Apache Kafka para la ingesta de datos en streaming. |
| `spark` | `apache/spark:3.5.0` | 7077, 8081:8080 | Master de Apache Spark para el procesamiento de datos en tiempo real (Spark Streaming). |
| `spark-notebook` | `jupyter/pyspark-notebook` | 8888:8888 | Entorno Jupyter Notebook preconfigurado con PySpark, ideal para desarrollo, prototipado y análisis exploratorio de datos. |

## 💻 Puesta en Marcha del Proyecto

Para levantar la infraestructura completa, asegúrate de tener **Docker** y **Docker Compose** instalados.

### 1. Inicialización

Ejecuta el siguiente comando desde la raíz del proyecto para construir y levantar todos los servicios definidos:

```bash
docker-compose up -d
```

### 2. Ejecución de Tareas

Una vez que los contenedores estén operativos:

- **Productor Kafka**: El script principal dentro de `scripts/Kafka/` debe ejecutarse para simular la generación y el envío de los eventos de churn al topic de Kafka.

- **Procesador Spark**: El script principal dentro de `scripts/spark/` debe ejecutarse para consumir los datos de Kafka, aplicar la lógica de procesamiento y analítica, y persistir los resultados en PostgreSQL.

### 3. Acceso a Interfaces

Puedes acceder a las siguientes interfaces web:

- **PgAdmin**: http://localhost:8080 (Consulta las credenciales en `docker-compose.yml`).
- **Spark Notebook (Jupyter)**: http://localhost:8888 (Utiliza el token definido en `docker-compose.yml`).

## 📌 Dependencias y Configuración

- El archivo `requirements.txt` detalla las librerías de Python necesarias para la ejecución local o dentro de los contenedores (p.ej., `pyspark`, `kafka-python`, `psycopg2`).
- Los contenedores de Spark y Spark Notebook tienen montado el directorio `scripts/` para poder acceder y ejecutar los scripts de procesamiento.