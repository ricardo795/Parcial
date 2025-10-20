from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# ----------------- CONFIGURACIÓN -----------------
print(" Iniciando Web Scraper Universal...\n")

# PERSONALIZA AQUÍ TU BÚSQUEDA
url = "https://www.ebay.com/sch/i.html?_nkw=telefono&_sacat=0&_from=R40&_trksid=m570.l1313&_odkw=laptop&_ipg=60"
selectores_contenedor = ["ul.srp-results", ".results-container", "#results"]
selectores_items = ["li.s-item", ".s-item", "li[class*='s-item']", ".srp-results li"]
nombre_archivo = "productos_extraidos"

# Configurar opciones de Edge
edge_options = Options()
edge_options.add_argument('--no-sandbox')
edge_options.add_argument('--disable-dev-shm-usage')
edge_options.add_argument('--disable-blink-features=AutomationControlled')
edge_options.add_argument('--start-maximized')
edge_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0')
edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
edge_options.add_experimental_option('useAutomationExtension', False)

# Inicializar driver de Edge
driver = None
try:
    service = Service()
    driver = webdriver.Edge(service=service, options=edge_options)
    driver.set_page_load_timeout(30)
    print(f" Accediendo a: {url}\n")
    driver.get(url)
except Exception as e:
    print(f" Error al iniciar el navegador: {e}")
    if driver:
        driver.quit()
    exit()

# Espera inicial
print(" Esperando 8 segundos para que cargue completamente...")
time.sleep(8)

# Verificar carga
print(f" Título de la página: {driver.title}")
print(f"🔗 URL actual: {driver.current_url}\n")

# Tomar captura inicial
try:
    driver.save_screenshot("captura_inicial.png")
    print(" Captura 'captura_inicial.png' guardada\n")
except:
    pass

# Scroll suave para activar carga de elementos
print(" Realizando scroll en la página...")
for i in range(5):
    driver.execute_script(f"window.scrollTo(0, {(i+1)*500});")
    time.sleep(1)

# Esperar contenedor principal
print("🔍 Buscando contenedor de resultados...\n")
contenedor_encontrado = False
for selector_cont in selectores_contenedor:
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector_cont))
        )
        print(f" Contenedor encontrado: '{selector_cont}'\n")
        contenedor_encontrado = True
        break
    except:
        print(f"    No encontrado: '{selector_cont}'")

if not contenedor_encontrado:
    print(" No se encontró ningún contenedor específico\n")

# Esperar por items individuales
items_selenium = None
selector_usado = None

for selector in selectores_items:
    try:
        print(f"   Intentando: {selector}")
        items_selenium = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )
        if len(items_selenium) > 0:
            print(f"    Encontrados {len(items_selenium)} elementos con '{selector}'\n")
            selector_usado = selector
            break
    except:
        print(f"    Falló con '{selector}'")

if not items_selenium or len(items_selenium) == 0:
    print("\n No se encontraron items con Selenium. Intentando con BeautifulSoup...\n")

# Guardar HTML completo
html_content = driver.page_source
with open("page_full.html", "w", encoding="utf-8") as f:
    f.write(html_content)
print(" HTML completo guardado en 'page_full.html'\n")

# Tomar captura final
try:
    driver.save_screenshot("captura_final.png")
    print(" Captura 'captura_final.png' guardada\n")
except:
    pass

driver.quit()

# ----------------- ANÁLISIS CON BEAUTIFULSOUP -----------------
print(" Analizando contenido HTML...\n")
soup = BeautifulSoup(html_content, "html.parser")

productos, precios, links = [], [], []

# Estrategia 1: Buscar con selector específico
items = []
if selector_usado:
    items = soup.select(selector_usado)
    print(f" Estrategia 1 (selector usado): {len(items)} elementos")

# Estrategia 2: Buscar por clase parcial
if len(items) == 0:
    for selector in selectores_items:
        items = soup.select(selector)
        if len(items) > 0:
            print(f" Estrategia 2 ({selector}): {len(items)} elementos")
            break

# Estrategia 3: Buscar dentro de contenedores
if len(items) == 0:
    for selector_cont in selectores_contenedor:
        contenedor = soup.select_one(selector_cont)
        if contenedor:
            items = contenedor.find_all("li") or contenedor.find_all("div", class_=lambda x: x and "item" in x.lower() if x else False)
            if len(items) > 0:
                print(f" Estrategia 3 (dentro de {selector_cont}): {len(items)} elementos")
                break

print()

# Extraer información
for idx, item in enumerate(items):
    # Buscar título con múltiples variantes
    titulo = (item.find("div", class_=lambda x: x and "title" in x.lower() if x else False) or
              item.find("h3") or item.find("h2") or item.find("h4") or
              item.find("span", class_=lambda x: x and "title" in x.lower() if x else False) or
              item.find(class_=lambda x: x and "name" in x.lower() if x else False))
    
    # Buscar precio con múltiples variantes
    precio = (item.find("span", class_=lambda x: x and "price" in x.lower() if x else False) or
              item.find("div", class_=lambda x: x and "price" in x.lower() if x else False) or
              item.find(class_=lambda x: x and "cost" in x.lower() if x else False))
    
    # Buscar link
    link = (item.find("a", href=True) or
            item.find_parent("a", href=True))
    
    # Debug: mostrar primeros 3 items
    if idx < 3:
        print(f"--- Item {idx + 1} ---")
        print(f"Título encontrado: {titulo is not None}")
        print(f"Precio encontrado: {precio is not None}")
        print(f"Link encontrado: {link is not None}")
        if titulo:
            print(f"Texto título: {titulo.get_text(strip=True)[:60]}")
        if precio:
            print(f"Texto precio: {precio.get_text(strip=True)[:30]}")
        print()
    
    # Extraer datos
    if titulo:
        titulo_texto = titulo.get_text(strip=True)
        
        # Filtrar elementos vacíos o no deseados
        palabras_excluir = ["shop on", "related searches", "ver más", "more results"]
        if not any(excluir in titulo_texto.lower() for excluir in palabras_excluir) and len(titulo_texto) > 3:
            productos.append(titulo_texto)
            
            # Precio
            if precio:
                precios.append(precio.get_text(strip=True))
            else:
                precios.append("No disponible")
            
            # Link
            if link and link.get("href"):
                href = link["href"]
                # Convertir URLs relativas a absolutas
                if href.startswith("/"):
                    from urllib.parse import urljoin
                    href = urljoin(url, href)
                links.append(href)
            else:
                links.append("No disponible")

# ----------------- RESULTADOS -----------------
print("="*60)
if not productos:
    print("\n NO SE ENCONTRARON PRODUCTOS\n")
    print(" DIAGNÓSTICO:")
    print("   1. Revisa las capturas: 'captura_inicial.png' y 'captura_final.png'")
    print("   2. Abre 'page_full.html' en un navegador")
    print("   3. Busca manualmente la clase CSS de los elementos")
    print("   4. El sitio puede estar bloqueando el scraping\n")
    print(" SOLUCIONES:")
    print("   - Modifica los selectores_items al inicio del código")
    print("   - Agrega más tiempo de espera")
    print("   - Usa un proxy o VPN")
    print("   - Verifica si el sitio tiene API oficial")
else:
    print(f"\n {len(productos)} ELEMENTOS EXTRAÍDOS\n")
    
    df = pd.DataFrame({
        "Producto": productos,
        "Precio": precios,
        "Enlace": links
    })
    
    # Mostrar muestra
    print(" MUESTRA DE RESULTADOS:")
    print(df.head(5).to_string(index=False))
    print()
    
    # Guardar archivo
    ruta_excel = os.path.join(os.getcwd(), f"{nombre_archivo}.xlsx")
    
    try:
        df.to_excel(ruta_excel, index=False, engine='openpyxl')
        print(f" Archivo Excel guardado: {ruta_excel}")
    except Exception as e:
        print(f" Error con Excel: {e}")
        ruta_csv = os.path.join(os.getcwd(), f"{nombre_archivo}.csv")
        df.to_csv(ruta_csv, index=False, encoding='utf-8-sig')
        print(f" Archivo CSV guardado: {ruta_csv}")

print("\n" + "="*60)
print(" PROCESO FINALIZADO")
print("="*60)