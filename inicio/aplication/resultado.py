from dataclasses import dataclass


@dataclass(frozen=True)
class ResultadoEmision:
    numero: str
    total: float
