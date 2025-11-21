# CarImport API

## Descripción

CarImport es una API RESTful desarrollada con FastAPI para analizar y calcular el costo estimado de importación de vehículos. Utiliza datos reales de APIs externas para obtener tasas de cambio, información de países y datos de vehículos. La API permite comparar precios de importación versus precios locales en Colombia (COP).

## Características

- Conversión de divisas en tiempo real (usando ER-API).
- Cálculo de costos de importación incluyendo aranceles, IVA y otros gastos.
- Comparación entre precios importados y locales.
- Información detallada de vehículos y países de origen.
- Respuestas en formato JSON.

## Instalación

### Prerrequisitos

- Python 3.8 o superior.
- Pip para instalar dependencias.

### Pasos de Instalación

1. Clona el repositorio:
   ```
   git clone <url-del-repositorio>
   cd apiRestful
   ```

2. Crea un entorno virtual (opcional pero recomendado):
   ```
   python -m venv venv
   venv\Scripts\activate  # En Windows
   ```

3. Instala las dependencias:
   ```
   pip install fastapi uvicorn requests
   ```

4. Ejecuta la aplicación:
   ```
   uvicorn main:app --reload
   ```

La API estará disponible en `http://127.0.0.1:8000`.

## Uso

Una vez ejecutada, puedes acceder a la documentación interactiva de FastAPI en `http://127.0.0.1:8000/docs` para probar los endpoints directamente.

### Ejemplos de Uso

- **Obtener tasa de cambio**: `GET /divisas?moneda_base=USD&moneda_objetivo=COP`
- **Calcular importación**: `GET /importacion?precio_origen=10000&moneda=USD&pais_origen=japan`
- **Comparar precios**: `GET /comparacion?precio_origen=10000&precio_local_cop=50000000&moneda=USD&pais_origen=japan`
- **Información de vehículo**: `GET /vehiculo?marca=Toyota&modelo=Corolla&pais_origen=japan&precio_origen=10000&moneda=USD`

## Endpoints Detallados

### 1. GET /

**Descripción**: Endpoint de inicio que proporciona información básica sobre la API.

**Respuesta**:
```json
{
  "nombre_api": "CarImport",
  "descripción": "API para analizar el costo de importación de un vehículo utilizando APIs externas.",
  "endpoints": ["/divisas", "/importacion", "/comparacion", "/vehiculo"]
}
```

### 2. GET /divisas

**Descripción**: Obtiene la tasa de cambio entre dos monedas.

**Parámetros**:
- `moneda_base` (str, opcional, default: "USD"): Moneda base.
- `moneda_objetivo` (str, opcional, default: "COP"): Moneda objetivo.

**Respuesta**:
```json
{
  "moneda_base": "USD",
  "moneda_objetivo": "COP",
  "tasa_cambio": 4000.0,
  "api_valida": true
}
```

### 3. GET /importacion

**Descripción**: Calcula el costo estimado de importación de un vehículo.

**Parámetros**:
- `precio_origen` (float, requerido): Precio del vehículo en la moneda de origen.
- `moneda` (str, opcional, default: "USD"): Moneda del precio de origen.
- `pais_origen` (str, opcional, default: "japan"): País de origen.

**Respuesta**:
```json
{
  "pais_origen": "japan",
  "precio_origen": 10000.0,
  "moneda_origen": "USD",
  "tasa_cambio": 4000.0,
  "precio_en_COP": 40000000.0,
  "precio_final_estimado_COP": 73600000.0,
  "api_tasa_ok": true
}
```

### 4. GET /comparacion

**Descripción**: Compara el precio de importación estimado con un precio local en COP.

**Parámetros**:
- `precio_origen` (float, requerido): Precio del vehículo en la moneda de origen.
- `precio_local_cop` (float, requerido): Precio local en COP.
- `moneda` (str, opcional, default: "USD"): Moneda del precio de origen.
- `pais_origen` (str, opcional, default: "japan"): País de origen.

**Respuesta**:
```json
{
  "precio_local_COP": 50000000.0,
  "precio_importado_estimado_COP": 73600000.0,
  "diferencia_COP": -23600000.0,
  "más_barato": "local",
  "api_tasa_ok": true
}
```

### 5. GET /vehiculo

**Descripción**: Proporciona información del vehículo, país de origen y análisis de importación.

**Parámetros**:
- `marca` (str, requerido): Marca del vehículo.
- `modelo` (str, requerido): Modelo del vehículo.
- `pais_origen` (str, requerido): País de origen.
- `precio_origen` (float, requerido): Precio del vehículo en la moneda de origen.
- `moneda` (str, opcional, default: "USD"): Moneda del precio de origen.

**Respuesta**:
```json
{
  "marca": "Toyota",
  "modelo_buscado": "Corolla",
  "modelo_encontrado_en_api": true,
  "sugerencias": ["Corolla", "Camry", "RAV4", "Prius", "Highlander"],
  "pais_origen": {
    "nombre": "Japan",
    "capital": "Tokyo",
    "region": "Asia",
    "moneda": "JPY"
  },
  "analisis_importacion": {
    "pais_origen": "japan",
    "precio_origen": 10000.0,
    "moneda_origen": "USD",
    "tasa_cambio": 4000.0,
    "precio_en_COP": 40000000.0,
    "precio_final_estimado_COP": 73600000.0,
    "api_tasa_ok": true
  }
}
```

## Dependencias

- `fastapi`: Framework para construir APIs.
- `uvicorn`: Servidor ASGI para ejecutar FastAPI.
- `requests`: Para hacer peticiones HTTP a APIs externas.

## APIs Externas Utilizadas

- **ER-API** (https://open.er-api.com/): Para tasas de cambio.
- **REST Countries** (https://restcountries.com/): Para información de países.
- **NHTSA API** (https://vpic.nhtsa.dot.gov/): Para datos de vehículos.

## Contribución

Si deseas contribuir, por favor crea un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT.
