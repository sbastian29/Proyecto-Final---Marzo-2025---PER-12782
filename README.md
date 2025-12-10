# 📊 Proyecto TFM: Almacenamiento y Procesamiento de Datos en Tiempo Real


## 🚀 **Almacenamiento y Procesamiento**

Este proyecto implementa una infraestructura para el **análisis de churn en telecomunicaciones** utilizando:

- **Apache Kafka** para ingesta de datos en streaming
- **Apache Spark** para procesamiento distribuido
- **PostgreSQL** para almacenamiento de resultados
- **Docker** para gestión de contenedores

La arquitectura incluye servicios como PostgreSQL, Kafka, Spark y Jupyter Notebook para desarrollo.

---

## 📊 **Análisis de Datasets**

### **Dataset Original**
- `telecom_churn_semi_structured.json` - Datos originales en formato JSON
- `EDA Original.Rmd` - Análisis exploratorio en R
- `EDA Original_Telecom Churn.pdf` - Reporte de análisis

### **Dataset Modificado con Anomalías**
- `telecom_churn_MODIFICADO.csv` - Dataset con anomalías artificiales
- `crear_anomalia.py` - Script para generar anomalías
- `EDA telecom_churn_MODIFICADO.Rmd` - Análisis del dataset modificado
- `EDA_Telecom Churn_modificado.pdf` - Reporte del análisis

---

## 📈 **Visualización de Datos**

### **Paneles en Power BI**
- Dashboard de análisis de churn
- Visualización de métricas y KPIs
- Reportes de tendencias y patrones


---

## 🤖 **Modelos de Machine Learning (BigML)**

### **Modelos Implementados**
- **Árbol de Decisión** - Evaluaciones y visualizaciones
- **Random Forest** - Modelo ensemble con análisis de importancia
- **Árbol Potenciado (Boosted Tree)** - Modelo avanzado con múltiples evaluaciones

Los modelos están enfocados en la predicción de churn y detección de anomalías.

---

## 🚀 **Flujo de Procesamiento**

1. **Ingesta**: Datos JSON semi-estructurados
2. **Streaming**: Procesamiento en tiempo real con Kafka y Spark
3. **Almacenamiento**: Resultados en PostgreSQL
4. **Análisis**: EDA en R sobre datasets original y modificado
5. **Modelado**: Machine Learning con BigML
6. **Visualización**: Dashboards en Power BI (con datos exportados)

---

## 🎯 **Objetivo del Proyecto**

Desarrollar un sistema para el análisis de churn en telecomunicaciones que combine:
- Procesamiento en tiempo real
- Almacenamiento escalable
- Análisis predictivo
- Visualización de resultados

