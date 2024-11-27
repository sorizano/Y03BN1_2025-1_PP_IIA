#1. Importar las librerias
import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from supabase import create_client, Client

#2. Configurar Supabase
SUPABASE_URL = "https://pbsjxezvcmdlwusveukd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBic2p4ZXp2Y21kbHd1c3ZldWtkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY1MzYxMjgsImV4cCI6MjA0MjExMjEyOH0.LPj5kYWsWQ-wfLry8FBTpXiJxUUVI5qNCTL2CBKMxYY"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


#3. Función para cargar datos desde supabase
@st.cache_data
def fetch_data():
    respose = supabase.table("users_data").select("*").execute()
    data = pd.DataFrame(respose.data)
    return data
#3.1 
def save_prediction_to_supabase(edad, salario, estado_civil, prediction):
    data = {
        "edad": edad,
        "salario": salario,
        "estado_civil": estado_civil,
        "comprado": prediction
    }
    respose = supabase.table("users_data").insert(data).execute()
    return respose

#4. Interfaz Streamlit
st.title("Modelo Random Forest")

#5. Cargando y mostrando datos
data = fetch_data()
if data.empty:
    st.warning("No hay datos en la base de datos. por favor, inserta datos primero.")
else:
    st.write("Datos cargados desde Supabase:")
    st.dataframe(data)


#6. Preprocesamiento de datos
X = data[['edad', 'salario']]
X = pd.get_dummies(X)
y = data['comprado']

#7. División de datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#8. Entrenar el modelo
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

#9. Evaluación del modelo
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
st.write(f"Precisión del modelo: {accuracy:.2f}")

# 10. predicción personalizada
edad = st.number_input("Edad", min_value=18, max_value=100, value=30)
salario = st.number_input("Salario", min_value=0, max_value=200000, value=50000)
estado_civil = st.selectbox("Estado civil", options=["soltero", "casado", "divorciado"])

input_data = pd.DataFrame({
    "edad": [edad],
    "salario": [salario]
})

# Asegúrate de que la predicción sea un booleano
prediction = bool(model.predict(input_data)[0])

st.write("¿Comprará el producto?", "Sí" if prediction else "No")

# 11. Botón para guardar predicción
if st.button("Guardar predicción"):
    result = save_prediction_to_supabase(edad, salario, estado_civil, prediction)

    # Si la respuesta tiene un atributo error
    if hasattr(result, "error") and result.error is None:
        st.success("¡Predicción guardada exitosamente!")
    else:
        st.error(f"Hubo un error al guardar la predicción: {getattr(result.error, 'message', 'Error desconocido')}")


