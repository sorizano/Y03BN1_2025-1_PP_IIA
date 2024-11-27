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

#4. Interfaz Streamlit
st.title("Nodelo Random Forest")

#5. Cargando y mostrando datos
data = fetch_data()
if data.empty:
    st.warning("No hay datos en la base de datos. por favor, inserta datos primero.")
else:
    st.write("Datos cargados desde Supabase:")
    st.dataframe(data)
