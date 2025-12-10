import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# ==============================================================================
# --- 0. Función Sigmoide ---
# ==============================================================================
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# ==============================================================================
# --- 1. Cargar y Aplanar el JSON Original (Limpieza total) ---
# ==============================================================================
print("Cargando y aplanando el JSON original...")
file_path = 'telecom_churn_semi_structured.json' 

try:
    df_json = pd.read_json(file_path)
    df = pd.json_normalize(df_json.to_dict('records'), sep='_')
    
    if 'additional_features_churn' in df.columns:
        df = df.rename(columns={'additional_features_churn': 'churn'})
    
    print(f"Datos cargados. Total de {len(df)} clientes.")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo {file_path}")
    exit()

# ==============================================================================
# --- 2. MODIFICAR LOS DATOS (Lógica V8: Precio Libre) ---
# ==============================================================================
print("Modificando los datos base...")

# 2a. Modificar Scores por Localización (Causa 1: Cobertura)
# Añadimos el clip AQUÍ porque una nota no puede ser menor que 1 ni mayor que 5
print("Aplicando penalización de cobertura (Rural/Suburban)...")
def modify_network_score(row):
    score = row['customer_support_network_quality_score']
    if row['personal_info_location'] == 'Rural': return score - 0.8 
    elif row['personal_info_location'] == 'Suburban': return score - 0.3
    return score


df['customer_support_network_quality_score'] = df.apply(modify_network_score, axis=1).clip(lower=1.0, upper=5.0)

# 2b. Inyectar el "Falso Culpable" (Edad -> Precio)
print("Inyectando el 'falso culpable' (precios naturales más altos para mayores)...")

# Normalizamos la edad
age_min = df['personal_info_age'].min()
age_max = df['personal_info_age'].max()
df['age_normalized_01'] = (df['personal_info_age'] - age_min) / (age_max - age_min)

# Calculamos el bonus (hasta +25$)
MAX_PRICE_BONUS_FOR_AGE = 25.0 
df['age_price_bonus'] = df['age_normalized_01'] * MAX_PRICE_BONUS_FOR_AGE

# Aplicamos el bonus al precio
df['subscription_monthly_charges'] += df['age_price_bonus']

print("Precios modificados sin límite superior artificial.")

# ==============================================================================
# --- 3. Preparar los Datos para el Modelo de Riesgo ---
# ==============================================================================
print("Normalizando las variables...")
scaler = StandardScaler()

df['price_scaled'] = scaler.fit_transform(df[['subscription_monthly_charges']]) 
df['tenure_scaled'] = scaler.fit_transform(df[['subscription_tenure_months']])
df['age_scaled'] = scaler.fit_transform(df[['personal_info_age']])
df['network_score_scaled'] = scaler.fit_transform(df[['customer_support_network_quality_score']]) 

# ==============================================================================
# --- 4. Calcular el "Score de Riesgo" ---
# ==============================================================================
print("Calculando el score de riesgo...")

PESO_PRECIO = 1.8        
PESO_PERMANENCIA = 1.2
PESO_NETWORK = -2.5      
PESO_EDAD = 0.1
PESO_GENERO = 0.05

df['risk_score_final'] = (
    (df['price_scaled'] * PESO_PRECIO) +           # Driver Real
    (df['tenure_scaled'] * PESO_PERMANENCIA) +     # Driver Real
    (df['network_score_scaled'] * PESO_NETWORK) +  # Driver Real
    (df['age_scaled'] * PESO_EDAD) +               # Falso Culpable
    (np.where(df['personal_info_gender'] == 'Female', PESO_GENERO, -PESO_GENERO))
)

# ==============================================================================
# --- 5. Convertir y Simular ---
# ==============================================================================
print("Simulando churn...")
df['churn_prob'] = sigmoid(df['risk_score_final'])
df['random_roll'] = np.random.rand(len(df))
df['churn'] = (df['churn_prob'] > df['random_roll']).astype(int)

# ==============================================================================
# --- 6. Guardar ---
# ==============================================================================
print("Guardando archivo V8...")
df_final = df.drop(columns=[
    'age_normalized_01', 'age_price_bonus', 
    'price_scaled', 'tenure_scaled', 'age_scaled', 'network_score_scaled', 
    'risk_score_final', 'churn_prob', 'random_roll'
])

output_file = 'telecom_churn_MODIFICADO.csv'
df_final.to_csv(output_file, index=False)

print(f"\n¡Listo! Se ha guardado el dataset en: {output_file}")


# ==============================================================================
# --- 7. Verificación final ---
# ==============================================================================
print("\n--- Verificación Final ---")
print(f"Precio Máximo Real: {df_final['subscription_monthly_charges'].max():.2f} (Debe ser > 150)")
print(f"Score Red Mínimo: {df_final['customer_support_network_quality_score'].min():.2f} (Debe ser >= 1.0)")
print("\nChurn por Localización:")
print(df.groupby('personal_info_location')['churn'].mean())
print("\n--- Análisis completado! ---")