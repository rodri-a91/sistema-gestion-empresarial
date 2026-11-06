def datos_factura(numero: str = "F-001") -> dict:
    return {
        "numero": numero,
        "cliente": "Comercial Aula SL",
        "cif": "B12345678",
        "lineas": [
            {"concepto": "Licencia ERP", "unidades": 1, "precio": 1500.0},
            {"ceoncepto": "Soporte", "unidades": 2, "precio": 250.0},
        ],
    }
