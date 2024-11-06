import streamlit as st
import pandas as pd
from supabase import create_client, Client
import altair as alt

#Configurar el Supabase
url = "https://pbsjxezvcmdlwusveukd.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBic2p4ZXp2Y21kbHd1c3ZldWtkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY1MzYxMjgsImV4cCI6MjA0MjExMjEyOH0.LPj5kYWsWQ-wfLry8FBTpXiJxUUVI5qNCTL2CBKMxYY"
supabase: Client = create_client(url, key)

#Cargar datos de Supabase
def cargar_datos_supabase():
    response = supabase.table("ventas_cafe").select("*").execute()
    if response.status_code == 200:
        return pd.DataFrame(response.data)
    else:
        st.error("Error al cargar datos desde Supabase")
        return pd.DataFrame()

#Datos
df = cargar_datos_supabase()

#Interfaz de Streamlit
st.title("Dasboard de Ventas de Café")
st.subheader("Análisis de ventas de café")

#Filtro por fecha
fecha_seleccionada = st.date_input("Selecciona una fecha", value = pd.to_datetime("2024-11-01"))
df_filtrado = df[df['fecha'] == fecha_seleccionada]

#Mostrar los datos filtrados
st.write("Datos de ventas para la fecha seleccionada:", df_filtrado)