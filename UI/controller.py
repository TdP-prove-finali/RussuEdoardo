import flet as ft
class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handleAnalizzaProvincia(self, e):
        provincia = self._view._province.value
        self._view.lv1.controls.clear()
        if not provincia:
            #controllo se è stata inserita la provincia
            #in caso contrario lancio errore
            self._view.lv1.controls.append(
                ft.Text(
                    "❌ Errore : seleziona una provincia prima di procedere.",
                    color="red",
                    weight="bold",
                    text_align=ft.TextAlign.CENTER,
                    size=16,
                )
            )
            self._view.update_page()
            return
        grafo = self._model.buildGraph(provincia)
        ordinati = self._model.getOrdinati()
        self._view.lv1.controls.append(
            ft.Text(
                f"Grafo correttamente creato:"
                        f"{len(grafo.nodes)} nodi e "
                        f"{len(grafo.edges)} archi" ,
                        weight = "bold"
            )
        )
        for o in ordinati:
            self._view.lv1.controls.append(
                ft.Row([
                    ft.Text(f"{o.nome}",color = "blue", weight = "bold"),
                    ft.Text(f"({o.codiceP})" , color = "blue"),
                    ft.Text(f"→ {o.punteggio}" ,color = "black", weight = "bold")
                ]))
        self._view._partenza.options.clear()
        self._view._partenza.options = [ft.dropdown.Option(
            text=nodo.nome,
            key = nodo.codice
        ) for nodo in grafo.nodes]
        self._view._partenza.disabled = False
        self._view._NGiorni.disabled = False
        self._view._NTappe.disabled = False
        self._view._btnCalcolaPercorso.disabled = False
        self._view.update_page()

    def fullProvince(self):
        province = self._model._province
        self._view._province.options = [ft.dropdown.Option(p) for p in province]
        self._view.update_page()

    def handleCalcolaPercorso(self, e):
        grafo = self._model._grafo
        partenza = self._view._partenza.value
        giorni = self._view._NGiorni.value
        tappe = self._view._NTappe.value

        self._view.lv2.controls.clear()

        if not partenza or not giorni or not tappe:
            self._view.lv2.controls.append(
                ft.Text(
                    "⚠️ Errore: inserisci tutti i vincoli (partenza, giorni e tappe)"
                        "prima di calcolare il percorso.",
                    color="red",
                    weight="bold",
                    text_align=ft.TextAlign.CENTER,
                    size=16,
                )
            )
            self._view.update_page()
            return
        percorso, punteggio = self._model.trovaPercorso(
            int(partenza),
            int(giorni),
            int(tappe)
        )
        self._view.lv2.controls.clear()
        if not percorso:
            self._view.lv2.controls.append(
                ft.Text(
                    "❌ Nessun percorso trovato.\nProva a diminuire le tappe o aumentare i giorni.",
                    color="red",
                    weight="bold",
                    text_align=ft.TextAlign.CENTER,
                    size=16,
                )
            )
            self._view.update_page()
            return
        for i, comune in enumerate(percorso):
            self._view.lv2.controls.append(
                ft.Row([
                    ft.Text(f"{i + 1}. ", weight="bold", color="black"),
                    ft.Text(comune.nome, color="blue", weight="bold"),
                    ft.Text(" → ", weight="bold", color="black"),
                    ft.Text(f"punteggio: {comune.punteggio:.2f}", weight="bold", color="black"),
                ])
            )
            if i < len(percorso) - 1:
                prossimo = percorso[i + 1]
                distanza = float(grafo[comune][prossimo].get("weight", 0.0))
                tempo_percorrenza = distanza / self._model.getVelocitaMedia(distanza)
                self._view.lv2.controls.append(
                    ft.Row([
                        ft.Text(comune.nome, color="blue"),
                        ft.Text(" → ", weight="bold"),
                        ft.Text(prossimo.nome, color="blue"),
                        ft.Text(f": {distanza:.2f} km"),
                        ft.Text(f" → ", weight = "bold"),
                        ft.Text(f"{tempo_percorrenza:.2f} h")
                    ])
                )
        self._view.lv2.controls.append(
            ft.Text(f"\nPunteggio ottenuto: {punteggio:.2f}", weight="bold", color="black")
        )
        tempo_totale = self._model.calcolaTempo(percorso)
        self._view.lv2.controls.append(
            ft.Text(f"Tempo utilizzato: {tempo_totale:.2f} h", weight="bold", color="black")
        )
        self._view.update_page()