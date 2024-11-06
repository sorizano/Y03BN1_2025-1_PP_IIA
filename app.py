import streamlit as st
import pandas as pd
from supabase import create_client, Client
import altair as alt

#Configurar el Supabase
url = "https://pbsjxezvcmdlwusveukd.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBic2p4ZXp2Y21kbHd1c3ZldWtkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY1MzYxMjgsImV4cCI6MjA0MjExMjEyOH0.LPj5kYWsWQ-wfLry8FBTpXiJxUUVI5qNCTL2CBKMxYY"
supabase: Client = create_client(url, key)

# Cargar datos de Supabase
def cargar_datos_supabase():
    try:
        #Realizamos la consulta a supabase
        response = supabase.table("ventas_cafe").select("*").execute()

        # Verificar si no hay errore en la respuesta
        if response.data:
            return pd.DataFrame(response.data)
        else:
            st.error("No se encontraron datos en la tabla 'ventas_cafe'.")
    except Exception as e:
        st.error(f"No se encontraron datos desde supabase: {str(e)}")
        return pd.DataFrame()

# Datos
df = cargar_datos_supabase()

# Interfaz de Streamlit
if not df.empty:
    st.title("Dashboard de Ventas de Café")
    st.subheader("Análisis de Ventas de Café")

    # Filtro por fecha
    fecha_seleccionada = st.date_input("Selecciona una fecha", value=pd.to_datetime("2024-11-01"))
    df_filtrado = df[df['fecha'] == fecha_seleccionada]

    # Mostrar datos filtrados
    st.write("Datos de ventas para la fecha seleccionada:", df_filtrado)

    #gráfico de barras: ventas por producto
    grafico_barras = alt.Chart(df_filtrado).mark_bar().encode(
        x='producto:N',
        y='cantidad:Q',
        color='producto:N'
    ).properties(
        title='Cantidad vendida por Producto'
    )
    st.altair_chart(grafico_barras, use_container_width=True)

else:
    st.error("No se pudieron cargar los datos.")