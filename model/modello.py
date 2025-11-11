import copy
import time

import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._provincia = None
        self._grafo = nx.Graph()
        self._idMap = {}
        self._province = DAO.getProvince()
        self._tempoSosta = 2 #h
        self._oreGiornaliere = 8 #h
        self._percorsoOttimo = []
        self._punteggioMax = 0
        self._tempoMin = 10000

    def buildGraph(self, provincia):
        self._grafo.clear()
        self._provincia = provincia
        self._nodes = DAO.getAllComuni(provincia)
        self.calcolaPunteggio(self._nodes)
        self._grafo.add_nodes_from(self._nodes)
        for n in self._nodes:
            self._idMap[int(n.codice)] = n
        self._edges = DAO.getAllEdges(provincia)
        for edge in self._edges:
            self._grafo.add_edge(
                self._idMap[int(edge.codice1)],
                self._idMap[int(edge.codice2)],
                weight=edge.distanza
            )
        return self._grafo

    def calcolaPunteggio(self, comuni):
        self._minElettori = min(c.elettori for c in comuni)
        self._maxElettori = max(c.elettori for c in comuni)
        self._minAffluenza = min(c.affluenza for c in comuni)
        self._maxAffluenza = max(c.affluenza for c in comuni)

        for comune in comuni:
            self._normaElettori = ((comune.elettori - self._minElettori) /
                                    (self._maxElettori - self._minElettori))
            self._normaAffluenza = 1 - ((comune.affluenza - self._minAffluenza) /
                                         (self._maxAffluenza - self._minAffluenza))
            # Ho cambiato le proporzioni da 60-40 a 70-30 per rendere
            # il punteggio più affine alla realtà
            media = (0.7 * self._normaElettori) + (0.3 * self._normaAffluenza)
            comune.punteggio = round(media * 10, 2)
        return

    def trovaPercorso(self, partenza, giorniMax, nTappe):
        self._percorsoOttimo = []
        self._punteggioMax = 0
        nodo = self._idMap[int(partenza)]
        parziale = [nodo]
        giorniUtilizzati = 1
        oreUtilizzate = self._tempoSosta
        self.ricorsione(parziale, giorniUtilizzati, oreUtilizzate, giorniMax, nTappe)
        return self._percorsoOttimo, self._punteggioMax

    def ricorsione(self, parziale, giorniUtilizzati, oreUtilizzate, giorniMax, tappe):
        if len(parziale) == tappe:
            if self.calcolaPeso(parziale) > self._punteggioMax:
                self._punteggioMax = self.calcolaPeso(parziale)
                self._percorsoOttimo = copy.deepcopy(parziale)
                self._tempoMin = self.calcolaTempo(parziale)
            if self.calcolaPeso(parziale) == self._punteggioMax and self.calcolaTempo(parziale) < self._tempoMin:
                self._punteggioMax = self.calcolaPeso(parziale)
                self._percorsoOttimo = copy.deepcopy(parziale)
                self._tempoMin = self.calcolaTempo(parziale)
            return
        ultimo = parziale[-1]
        for nodo in self._grafo.nodes:
            if nodo in parziale:
                continue
            distanza = float(self._grafo[ultimo][nodo].get("weight",0.0))
            tempoViaggio = distanza / (self.getVelocitaMedia(distanza))
            tot = tempoViaggio + self._tempoSosta
            if oreUtilizzate + tot <= self._oreGiornaliere:  # stesso giorno
                parziale.append(nodo)
                self.ricorsione(parziale, giorniUtilizzati, oreUtilizzate + tot, giorniMax, tappe)
                parziale.pop()
            else:
                if giorniUtilizzati + 1 <= giorniMax and tot <= self._oreGiornaliere: # cambio giorno
                    parziale.append(nodo)
                    self.ricorsione(parziale, giorniUtilizzati + 1, tot, giorniMax, tappe)
                    parziale.pop()
        return

    def calcolaPeso(self, parziale):
        punteggioTot = 0
        for nodo in parziale:
            punteggioTot += nodo.punteggio
        return punteggioTot

    def calcolaTempo(self, parziale):
        tempoTot = 0
        for i in range(1, len(parziale)):
            u = parziale[i - 1]
            v = parziale[i]
            if self._grafo.has_edge(u, v):
                distanza = float(self._grafo[u][v].get("weight", 0.0))
                vel = self.getVelocitaMedia(distanza)
                tempoTot += distanza / vel + self._tempoSosta
        tempoTot += self._tempoSosta
        return tempoTot

    def getOrdinati(self):
        ordinati = sorted(self._grafo.nodes, key=lambda x: x.punteggio, reverse=True)
        return ordinati

    def getVelocitaMedia(self,distanza):
        # calcolo la velocità media in base alla distanza tra i comuni
        if distanza < 5:
            velocita = 40
        elif distanza < 20:
            velocita = 60
        elif distanza < 80:
            velocita = 80
        else:
            velocita = 100
        return velocita