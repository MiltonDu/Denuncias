from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

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
url = "https://www.datosabiertos.gob.pe/dataset/codigos-equivalentes-de-ubigeo-del-peru"

driver.get(url)

try:
    # Esperar un poco para que la página cargue
    time.sleep(5)  # Ajusta el tiempo según sea necesario

    # Encuentra el enlace de descarga y haz clic en él
    download_button = driver.find_element(By.XPATH, "//a[contains(@href, 'https://cloud.minsa.gob.pe/s/GkfcJD8xKHJeCqn/download')]")
    download_button.click()

    # Esperar a que la descarga se complete
    file_name = "TB_UBIGEOS.csv"  # Usamos el nombre real sin codificación
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
        # Ahora simplemente guardamos el archivo descargado
        print(f"El archivo CSV se ha descargado correctamente en: {file_path}")

except Exception as e:
    print(f"Ocurrió un error: {e}")

finally:
    # Cerrar el navegador
    driver.quit()
