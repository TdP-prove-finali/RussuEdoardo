import flet as ft


class View(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._controller = None
        self._title = None
        self._btnAnalizzaProvincia = None
        self._btnCalcolaPercorso = None
        self._province = None
        self.lv1 = None
        self.lv2 = None
        self._partenza = None
        self._NGiorni = None
        self._NTappe = None

    def load_interface(self):
        self._page.padding = ft.padding.only(top=10, left=12, right=12)
        self._title = ft.Text(
            "Ottimizzazione degli itinerari di campagna elettorale",
            color="blue",
            size=45,
            text_align=ft.TextAlign.CENTER,
        )
        self._btnAnalizzaProvincia = ft.ElevatedButton(
            text="Analizza provincia",
            on_click=(self._controller.handleAnalizzaProvincia),
            bgcolor="blue",
            color="white",
            width=200,
        )
        self._btnCalcolaPercorso = ft.ElevatedButton(
            text="Ottimizza itinerario",
            on_click=(self._controller.handleCalcolaPercorso),
            bgcolor="blue",
            color="white",
            width=200,
            disabled = True,
        )
        self._province = ft.Dropdown(
            label="Province",
            options=[],
            width=250,
            bgcolor="white",
            color="blue",
            border_color="blue",
        )
        self._partenza = ft.Dropdown(
            label="Comune di partenza",
            options=[],
            width=250,
            bgcolor="white",
            color="blue",
            border_color="blue",
            disabled=True,
        )
        self._NGiorni = ft.Dropdown(
            label="Giorni a disposizione",
            options=[],
            width=250,
            bgcolor="white",
            color="blue",
            border_color="blue",
            disabled=True,
        )
        self._NTappe = ft.Dropdown(
            label="Tappe da visitare",
            options=[],
            width=250,
            bgcolor="white",
            color="blue",
            border_color="blue",
            disabled=True,
        )
        self.lv1 = ft.ListView(expand=1,spacing=10,padding=10,auto_scroll=True)
        self.lv2 = ft.ListView(expand=1,spacing=10,padding=10,auto_scroll=True)
        lv_container1 = ft.Container(
            content=self.lv1,
            border_radius=10,
            padding=50,
            margin=ft.margin.all(20),
            expand=True,
            height=500,
            border=ft.border.all(1, color = "blue"),
        )
        lv_container2 = ft.Container(
            content=self.lv2,
            border_radius=10,
            padding=50,
            margin=ft.margin.all(20),
            expand=True,
            height=500,
            border=ft.border.all(1, color = "blue"),
        )
        self._page.controls.append(
            ft.Row([self._title], alignment=ft.MainAxisAlignment.CENTER)
        )
        self._page.controls.append(
            ft.Row(
                [self._province, self._partenza],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=16,
            )
        )
        self._page.controls.append(
            ft.Row(
                [self._NGiorni, self._NTappe],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=16,
            )
        )
        self._page.controls.append(
            ft.Row(
                [self._btnAnalizzaProvincia, self._btnCalcolaPercorso],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=16,
            )
        )
        self._page.controls.append(
            ft.Container(
                content=ft.Row(
                    controls=[lv_container1, lv_container2],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=16,
                    expand=True,
                )
            )
        )
        self._controller.fullProvince()
        self._NGiorni.options = [ft.dropdown.Option(str(i)) for i in range(1,11)]
        self._NTappe.options = [ft.dropdown.Option(str(i)) for i in range(1, 11)]
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def update_page(self):
        self._page.update()

