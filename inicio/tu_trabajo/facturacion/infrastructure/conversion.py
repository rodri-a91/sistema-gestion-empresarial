import math

from facturacion.domain.entidades import Factura, LineaFactura


def _exigir_texto(datos: dict, campo: str) -> str:
    if campo not in datos:
        raise ValueError(f"Falta el campo '{campo}'")
    valor = datos[campo]
    if not isinstance(valor, str):
        raise ValueError(f"El campo '{campo}' debe ser texto")
    return valor


def _exigir_unidades(valor: object) -> int:
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise ValueError("'unidades' debe ser un número entero")
    return valor


def _exigir_precio(valor: object) -> float:
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError("'precio' debe ser un número")
    try:
        precio = float(valor)
    except OverflowError:
        raise ValueError("'precio' no es representable") from None
    if not math.isfinite(precio):
        raise ValueError("'precio' debe ser finito")
    return precio


def _convertir_linea(datos: object) -> LineaFactura:
    if not isinstance(datos, dict):
        raise ValueError('Cada línea debe ser un objeto')
    for campo in ('unidades', 'precio'):
        if campo not in datos:
            raise ValueError(f"Falta el campo '{campo}' en una línea")
    return LineaFactura(
        _exigir_texto(datos, 'concepto'),
        _exigir_unidades(datos['unidades']),
        _exigir_precio(datos['precio']),
    )


def convertir_factura(datos: dict) -> Factura:
    if not isinstance(datos, dict):
        raise ValueError('Se esperaba un objeto con la factura')
    numero = _exigir_texto(datos, 'numero')
    cliente = _exigir_texto(datos, 'cliente')
    cif = _exigir_texto(datos, 'cif')
    lineas = datos.get('lineas')
    if not isinstance(lineas, list):
        raise ValueError("'lineas' debe ser una lista")
    return Factura(numero, cliente, cif,
                   tuple(_convertir_linea(linea) for linea in lineas))
