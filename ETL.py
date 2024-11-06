import pandas as pd
import time
from supabase import create_client, Client

#Configuración de conexión a Supabase
url = "https://pbsjxezvcmdlwusveukd.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBic2p4ZXp2Y21kbHd1c3ZldWtkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjY1MzYxMjgsImV4cCI6MjA0MjExMjEyOH0.LPj5kYWsWQ-wfLry8FBTpXiJxUUVI5qNCTL2CBKMxYY"
supabase: Client = create_client(url, key)

#Ruta del archivo CSV en el disco D:\
csv_path = r"D:\ventas_cafe.csv"

#Función para cargar datos a Supabase
def cargar_datos():
    try:
        #Leer el CSV
        df = pd.read_csv(csv_path)
        data = df.to_dict(orient="records")

        #Inserta cada registro a supabase
        for row in data:
            response = supabase.table("ventas_cafe").insert(row).execute()
            if response.data:
                print("Dato insertado", row)
            else:
                print("Error al insertar: ", response)
        print("Datos cargados exitosamente.")
    except Exception as e:
        print("Ocurrió un error al cargar los datos:", e)

#Ejecuta el proceso cada 5 min
if __name__ == "__main__":
    while True:
        cargar_datos()
        print("Esperando 5 min para la próxima carga")
        time.sleep(300)