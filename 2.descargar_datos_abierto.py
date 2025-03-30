from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
import pandas as pd  # Usamos pandas para manejar el archivo Excel

# Configuración de opciones para el navegador
download_dir = r"C:\Users\2018008505005\Documents\GitHub\WEBSCRAPING-CURSO\descargas"  # Cambia esto a tu ruta de descarga deseada

chrome_options = Options()
#chrome_options.add_argument("--headless")  # Ejecutar en modo headless (sin interfaz gráfica)
#chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--disable-dev-shm-usage")

# Configurar preferencias de descarga
prefs = {
    "download.default_directory": download_dir,  # Cambia la carpeta de descarga
    "download.prompt_for_download": False,  # No preguntar para descargar
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True  # Habilitar la navegación segura
}
chrome_options.add_experimental_option("prefs", prefs)

# Inicializar el navegador
serv = Service(executable_path=r'C:\driver\chromedriver.exe')  # Usar "r" para evitar el problema con las secuencias de escape
driver = webdriver.Chrome(service=serv, options=chrome_options)

# URL de la página donde se encuentra el archivo
url = "https://observatorio.mininter.gob.pe/proyectos/base-de-datos-hechos-delictivos-basados-en-denuncias-en-el-sidpol"

driver.get(url)

try:
    # Esperar un poco para que la página cargue
    time.sleep(5)  # Ajusta el tiempo según sea necesario

    # Encuentra el enlace de descarga y haz clic en él
    download_button = driver.find_element(By.XPATH, "//a[contains(@href, 'Base%20de%20datos%20SIDPOL%20a%20febrero%20del%202025.xlsx')]")
    download_button.click()

    # Esperar a que la descarga se complete
    file_name = "Base de datos SIDPOL a febrero del 2025.xlsx"  # Usamos el nombre real sin codificación
    file_path = os.path.join(download_dir, file_name)

    timeout = 60  # 1 minuto de espera máxima
    start_time = time.time()

    while True:
        if os.path.exists(file_path):  # Verifica si el archivo existe
            print(f"Archivo encontrado: {file_path}")
            break
        if time.time() - start_time > timeout:
            print("La descarga tardó demasiado.")
            break
        time.sleep(1)  # Esperar un segundo antes de volver a comprobar

    if not os.path.exists(file_path):
        print(f"No se encontró el archivo en la ruta: {file_path}")
    else:
        # Parte para separar las hojas del archivo Excel en CSV
        print("Iniciando procesamiento del archivo Excel...")

        # Ruta de salida para los archivos CSV
        csv_dir = r"C:\Users\2018008505005\Documents\GitHub\WEBSCRAPING-CURSO\csv_output"
        os.makedirs(csv_dir, exist_ok=True)  # Crear la carpeta si no existe

        # Leer el archivo Excel
        excel_data = pd.ExcelFile(file_path)

        # Obtener los nombres de todas las hojas
        sheet_names = excel_data.sheet_names

        # Separar cada hoja en un archivo CSV
        for sheet_name in sheet_names:
            # Leer la hoja
            df = excel_data.parse(sheet_name)

            # Crear el nombre del archivo CSV basado en el nombre de la hoja
            csv_file_path = os.path.join(csv_dir, f"{sheet_name}.csv")

            # Guardar la hoja como archivo CSV
            df.to_csv(csv_file_path, index=False)  # index=False para no incluir la columna de índice

            print(f"Se ha guardado la hoja '{sheet_name}' como CSV en: {csv_file_path}")

        print("Todas las hojas han sido convertidas a CSV.")

except Exception as e:
    print(f"Ocurrió un error: {e}")

finally:
    # Cerrar el navegador
    driver.quit()
