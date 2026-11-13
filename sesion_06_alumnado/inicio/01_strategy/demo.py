from abc import ABC, abstractmethod
from decimal import Decimal


class Descuento(ABC):
    @abstractmethod
    def aplicar(self, base: Decimal) -> Decimal:
        pass


class SinDescuento(Descuento):
    def aplicar(self, base):
        return base


class DiezPorCiento(Descuento):
    def aplicar(self, base):
        return base * Decimal("0.90")


class PorVolumen(Descuento):
    def aplicar(self, base: Decimal):
        if base >= Decimal("500.00"):
            return base * Decimal("0.85")

        return base


class Pedido:
    def __init__(self, base: Decimal, descuento: Descuento):
        if base < 0:
            raise ValueError("Base negativa")
        self.base = base
        self.descuento = descuento

    def total(self) -> Decimal:
        return self.descuento.aplicar(self.base)


def main() -> None:
    pedido = Pedido(Decimal("200.00"), SinDescuento())
    print(f"Sin descuento: {pedido.total}")

    pedido.descuento = DiezPorCiento()
    print(f"Con descuento: {pedido.total}")


if __name__ == "__main__":
    main()
