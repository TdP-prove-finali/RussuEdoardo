from dataclasses import dataclass
@dataclass
class Arco:
    codice1:int
    comune1: str
    codice2:int
    comune2: str
    distanza_km :float