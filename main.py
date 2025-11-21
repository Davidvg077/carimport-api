from fastapi import FastAPI, HTTPException
import requests
from fastapi.responses import JSONResponse

app = FastAPI(
    title="CarImport",
    description="API para analizar importación de vehículos utilizando datos reales.",
    version="1.0.0"
)

# 1. Endpoint de inicio

@app.get("/")
def read_root():
    return {
        "nombre_api": "CarImport",
        "descripción": "API para analizar el costo de importación de un vehículo utilizando APIs externas.",
        "endpoints": ["/divisas", "/importacion", "/comparacion", "/vehiculo"]
    }

# 2. Convertir divisas

@app.get("/divisas", summary="Obtener tasa de cambio")
def obtener_divisas(moneda_base: str = "USD", moneda_objetivo: str = "COP"):
    try:
        url = f"https://open.er-api.com/v6/latest/{moneda_base}"
        response = requests.get(url, timeout=5)
        data = response.json()

        if "rates" not in data or moneda_objetivo not in data["rates"]:
            raise HTTPException(status_code=500, detail="No se pudo obtener la tasa real.")

        tasa = data["rates"][moneda_objetivo]

        return {"moneda_base": moneda_base, "moneda_objetivo": moneda_objetivo, "tasa_cambio": tasa, "api_valida": True}

    except Exception:
        return {"moneda_base": moneda_base, "moneda_objetivo": moneda_objetivo, "tasa_cambio": 4000, "api_valida": False}


# 3. Calcular importación

@app.get("/importacion", summary="Calcular importación estimada")
def calcular_importacion(precio_origen: float, moneda: str = "USD", pais_origen: str = "japan"):
    divisa = obtener_divisas(moneda_base=moneda, moneda_objetivo="COP")
    tasa = divisa["tasa_cambio"]

    precio_en_cop = precio_origen * tasa
    arancel = 0.15
    iva = 0.19
    otros = 0.05

    precio_final = precio_en_cop * (1 + arancel + iva + otros)

    return {
        "pais_origen": pais_origen,
        "precio_origen": precio_origen,
        "moneda_origen": moneda,
        "tasa_cambio": tasa,
        "precio_en_COP": round(precio_en_cop, 2),
        "precio_final_estimado_COP": round(precio_final, 2),
        "api_tasa_ok": divisa["api_valida"]
    }


# 4. Comparación de importación vs local

@app.get("/comparacion", summary="Comparar con precio local")
def comparar_importacion_vs_local(precio_origen: float, precio_local_cop: float, moneda: str = "USD", pais_origen: str = "japan"):
    importacion = calcular_importacion(precio_origen, moneda, pais_origen)
    diferencia = precio_local_cop - importacion["precio_final_estimado_COP"]

    return {
        "precio_local_COP": precio_local_cop,
        "precio_importado_estimado_COP": importacion["precio_final_estimado_COP"],
        "diferencia_COP": diferencia,
        "más_barato": "local" if diferencia < 0 else "importado",
        "api_tasa_ok": importacion["api_tasa_ok"]
    }

# 5. Información del vehículo + país

@app.get("/vehiculo", summary="Información de vehículo y país")
def obtener_info_vehiculo(marca: str, modelo: str, pais_origen: str, precio_origen: float, moneda: str = "USD"):
    # Datos del país
    try:
        pais_url = f"https://restcountries.com/v3.1/name/{pais_origen.capitalize()}"
        pais_resp = requests.get(pais_url, timeout=5).json()
        pais_data = {
            "nombre": pais_resp[0]["name"]["common"],
            "capital": pais_resp[0]["capital"][0],
            "region": pais_resp[0]["region"],
            "moneda": list(pais_resp[0]["currencies"].keys())[0]
        }
    except:
        pais_data = {"error": "API de países no respondió"}

    # Verificar modelo con API de vehículos
    try:
        veh_url = f"https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{marca}?format=json"
        veh_resp = requests.get(veh_url, timeout=5).json()
        modelos = [v["Model_Name"] for v in veh_resp["Results"]]
        encontrado = modelo in modelos
    except:
        modelos = []
        encontrado = False

    # Importación
    importacion = calcular_importacion(precio_origen, moneda, pais_origen)

    return {
        "marca": marca,
        "modelo_buscado": modelo,
        "modelo_encontrado_en_api": encontrado,
        "sugerencias": modelos[:5],
        "pais_origen": pais_data,
        "analisis_importacion": importacion
    }
