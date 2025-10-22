Web Scraper Universal 
    
Extrae datos de cualquier sitio web de forma automatizada, inteligente y robusta.
Un web scraper avanzado construido con Python, Selenium y BeautifulSoup que automatiza la extracción de datos de sitios web modernos, incluso aquellos con contenido dinámico JavaScript. Diseñado para ser robusto, flexible y fácil de usar.
-	 Características
•	Compatible con JavaScript: Maneja sitios web modernos con contenido dinámico
•	 Anti-detección avanzada: Evita bloqueos simulando comportamiento humano
•	 Extracción inteligente: Múltiples estrategias de búsqueda automática
•	 Exportación a Excel/CSV: Datos organizados listos para análisis
•	Sistema de diagnóstico: Capturas y logs para debugging
•	 Altamente configurable: Adapta fácilmente a cualquier sitio web
•	 Multi-plataforma: Windows, macOS y Linux

 Tabla de Contenidos
•	Instalación
•	Uso Rápido
•	Configuración
•	Ejemplos
•	Casos de Uso
•	Características Avanzadas
•	Solución de Problemas
•	Contribuir
•	Licencia

 Instalación
-	Requisitos Previos
•	Python 3.8 o superior
•	Microsoft Edge (u otro navegador compatible con Selenium)
•	Conexión a Internet
Instalación de Dependencias
# Clonar el repositorio
# Instalar dependencias
pip install -r requirements.txt
requirements.txt
selenium>=4.0.0
beautifulsoup4>=4.11.0
Instalación de WebDriver
pip install webdriver-manager

 Uso Rápido
Ejemplo Básico
# 1. Configurar parámetros al inicio del script
url = "https://www.ebay.com/sch/i.html?_nkw=laptop"


Ejemplos
Ejemplo 1: Scrapear eBay
url = "https://www.ebay.com/sch/i.html?_nkw=laptop&_ipg=60" selectores_items = ["li.s-item"] nombre_archivo = "laptops_ebay"

Ejemplo 2: Bienes Raíces
url = "https://sitio-inmobiliario.com/venta/casas"
selectores_items = [    ".property-card",    "div.listing-item"]
nombre_archivo = "propiedades"

 Casos de Uso
Industria	Aplicación	Datos Extraídos
E-commerce	Monitoreo de precios	Productos, precios, disponibilidad
Marketing	Análisis de competencia	Ofertas, descripciones, imágenes
Inmobiliaria	Catálogo de propiedades	Precios, ubicaciones, características
RRHH	Ofertas laborales	Puestos, salarios, requisitos
Investigación	Recopilación de datos	Artículos, opiniones, estadísticas
Finanzas	Cotizaciones	Precios, históricos, noticias

-  Características Avanzadas
1. Sistema Anti-Detección
# Elimina propiedades que delatan automatización
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """
})
2. Scroll Inteligente
# Scroll gradual aleatorio que imita humanos
scroll_amount = random.randint(300, 600)
driver.execute_script(f"window.scrollTo(0, {current_position});")
time.sleep(random.uniform(1.5, tiempo_scroll))
3. Múltiples Estrategias de Extracción
El programa prueba automáticamente:
•	 Selector CSS directo
•	 Búsqueda por atributos parciales
•	 Búsqueda dentro de contenedores
•	 Fallback por etiquetas HTML
4. Sistema de Diagnóstico
Genera automáticamente:
•	 captura_inicial.png - Estado antes del scraping
•	 captura_final.png - Estado después del scraping
•	 page_full.html - HTML completo para análisis manual

 Solución de Problemas
Problema: "No se encontraron elementos"
Solución:
1.	Abre page_full.html en un navegador
2.	Inspecciona un producto (F12 → Inspeccionar elemento)
3.	Copia la clase CSS correcta
4.	Actualiza selectores_items en el código

Problema: "CAPTCHA detectado"
Soluciones:
•	Aumenta tiempo_espera_inicial a 30 segundos
•	Resuelve el CAPTCHA manualmente cuando se pause
•	Usa proxies rotativos (configuración avanzada)
•	Considera usar la API oficial del sitio
-	 Estructura de Datos Exportados
Ejemplo:
Excel/CSV Output
Columna	Descripción	Ejemplo
Producto	Título o nombre del item	"Laptop HP 15.6" Intel Core i5"
Precio	Precio del producto	"$599.99"
Enlace	URL completa del producto	"https://ejemplo.com/producto/123"

