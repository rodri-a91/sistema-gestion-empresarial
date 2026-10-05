"""Ejercicio (30-45 min): cierre de inventario.

Completa las partes TODO. Un movimiento desconocido o que dejaría
existencias negativas se informa y se omite; se sigue con el siguiente.
No necesitas lanzar ni capturar excepciones."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Movimiento:
    sku: str
    variacion: int


class Articulo:
    def __init__(self, sku: str, precio: float, existencias: int) -> None:
        self.sku = sku
        self.precio = precio
        self._existencias = existencias

    @property
    def existencias(self) -> int:
        return self._existencias
    
    @property
    def valor_en_almacen(self) -> float:
        return self.precio * self.existencias

    def aplicar_variacion(self, variacion: int) -> bool:
        resultado: int = self._existencias + variacion
        
        if resultado < 0:
            return False
        else:
            self._existencias = resultado
            return True

    def __repr__(self) -> str:
        return f"Artículo con código {self.sku} y {self._existencias} existencias"
        


def procesar_movimientos(
    inventario: dict[str, Articulo], movimientos: list[Movimiento]
) -> list[str]:
    incidencias: list[str] = []
    for m in movimientos:
        if m.sku not in inventario:
            incidencias.append(f"El artículo {m.sku} no existe")
        elif not inventario[m.sku].aplicar_variacion(m.variacion):
            incidencias.append(f"No hay existencias de {m.sku}")
        
    return incidencias


def skus_bajo_minimo(inventario: dict[str, Articulo], minimo: int) -> list[str]:
    return [sku for sku, articulo in inventario.items() if articulo.existencias <= minimo]


def valor_por_sku(inventario: dict[str, Articulo]) -> dict[str, float]:
    return {sku: inventario[sku].valor_en_almacen for sku in inventario}


inventario = {
    "A-10": Articulo("A-10", 12.50, 8),
    "B-20": Articulo("B-20", 4.00, 3),
    "C-30": Articulo("C-30", 9.50, 6),
}

movimientos = [
    Movimiento("A-10", -4),
    Movimiento("B-20", +5),
    Movimiento("C-30", -7),
    Movimiento("X-99", +2),
    Movimiento("A-10", +1),
]

print(procesar_movimientos(inventario, movimientos))
for sku, articulo in inventario.items():
    print(f"{sku}: {articulo.existencias}")
print(skus_bajo_minimo(inventario,5))
print(valor_por_sku(inventario))

