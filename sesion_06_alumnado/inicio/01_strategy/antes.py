from decimal import Decimal


def total(base: Decimal, campana: str) -> Decimal:
    if campana == "normal":
        return base
    if campana == "promocion":
        return base * Decimal("0.90")
    raise ValueError("Campaña desconocida")

if __name__ == "__main__":
    print(f'{total(Decimal("200.00"), "promocion"):.2f}')
