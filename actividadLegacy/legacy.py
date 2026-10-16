from typing import TypedDict


class LineaLegacy(TypedDict):
    concepto: str
    uds: int
    precio: float

class FacturaLegacy:
    def procesar(self, cliente: str, cif: str, lineas: list[LineaLegacy],
                 tipo_iva: str, email: str | None) -> float:
        # 1. Validación mezclada con la operación completa.
        if not cif.startswith(('A', 'B')) or len(cif) != 9:
            raise ValueError(f'CIF no válido para el taller: {cif}')
        if not lineas:
            raise ValueError('Factura sin líneas comerciales')

        # 2. Cálculo acoplado a las opciones disponibles.
        subtotal = sum(linea['uds'] * linea['precio'] for linea in lineas)
        if tipo_iva == 'GENERAL':
            total = subtotal * 1.21
        elif tipo_iva == 'REDUCIDO':
            total = subtotal * 1.10
        else:
            raise ValueError(f'IVA desconocido: {tipo_iva}')
        total = round(total, 2)

        # 3. Persistencia simulada, elegida dentro del método.
        print(f'[SQL INSERT SIMULADO] {cliente} ({cif}): {total:.2f} EUR')

        # 4. Comunicación simulada, elegida dentro del método.
        if email:
            print(f'[SMTP SIMULADO] Factura para {email}')
        return total

if __name__ == '__main__':
    lineas: list[LineaLegacy] = [
        {'concepto': 'Licencia ERP', 'uds': 1, 'precio': 1500.0},
        {'concepto': 'Soporte', 'uds': 2, 'precio': 250.0},
    ]
    print(FacturaLegacy().procesar(
        'Comercial Aula SL', 'B12345678', lineas, 'GENERAL', 'aula@example.com'))
