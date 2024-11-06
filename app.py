import streamlit as st
import pandas as pd
from supabase import create_client, Client
import altair as alt

# Configurar el Supabase
url = "https://pbsjxezvcmdlwusveukd.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBic2p4ZXp2Y21kbHd1c3ZldWtkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY1MzYxMjgsImV4cCI6MjA0MjExMjEyOH0.LPj5kYWsWQ-wfLry8FBTpXiJxUUVI5qNCTL2CBKMxYY"
supabase: Client = create_client(url, key)

# Cargar datos de Supabase
def cargar_datos_supabase():
    response = supabase.table("ventas_cafe").select("*").execute()
    
    # Depurar: imprimir la respuesta
    st.write("Respuesta de Supabase:", response)
    
    # Verificar si la respuesta contiene errores o está vacía
    if hasattr(response, 'error') and response.error:
        st.error(f"Error al cargar datos desde Supabase: {response.error}")
        return pd.DataFrame()
    elif not response.data:
        st.warning("No se encontraron datos en la tabla 'ventas_cafe'.")
        return pd.DataFrame()
    else:
        return pd.DataFrame(response.data)

# Datos
df = cargar_datos_supabase()

# Interfaz de Streamlit
st.title("Dashboard de Ventas de Café")
st.subheader("Análisis de Ventas de Café")

# Filtro por fecha
fecha_seleccionada = st.date_input("Selecciona una fecha", value=pd.to_datetime("2024-11-01"))
df_filtrado = df[df['fecha'] == fecha_seleccionada]

# Mostrar datos filtrados
st.write("Datos de ventas para la fecha seleccionada:", df_filtrado)

# Gráfico de barras: Ventas por Producto
grafico_barras = alt.Chart(df_filtrado).mark_bar().encode(
    x='producto:N',
    y='cantidad:Q',
    color='producto:N'
).properties(
    title='Cantidad Vendida por Producto'
)
st.altair_chart(grafico_barras, use_container_width=True)

# Gráfico de líneas: Total de Ventas en el Tiempo
grafico_lineas = alt.Chart(df).mark_line().encode(
    x='fecha:T',
    y='precio_total:Q',
    color='producto:N'
).properties(
    title='Total de Ventas en el Tiempo por Producto'
)
st.altair_chart(grafico_lineas, use_container_width=True)
