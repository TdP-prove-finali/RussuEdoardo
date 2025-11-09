from dataclasses import dataclass

@dataclass
class Comune :
    codice :int
    nome : str
    provincia : str
    codiceP : str
    elettori :int
    affluenza : int
    affluenza_percentuale :float
    punteggio :int


    def __hash__(self):
        return hash(self.codice)
    def __eq__(self, other):
        return self.codice == other.codice
    def __str__(self):
        return f'{self.nome} -> {self.provincia} -> {self.punteggio}'

