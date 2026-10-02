ventas = [
    {"id": "PED-01", "total": 1250.0},
    {"id": "PED-02", "total": 80.0},
    {"id": "PED-03", "total": 3500.0},
    {"id": "PED-04", "total": 100.0},
    {"id": "PED-05", "total": 220.0},
]


def pedidos_relevantes(datos, umbral):
    return [p["id"] for p in datos if p["total"] > umbral]


def indexar_por_id(datos):
    return {v["id"]: v["total"] for v in datos}


print(pedidos_relevantes(ventas, 200))
print(indexar_por_id(ventas))
