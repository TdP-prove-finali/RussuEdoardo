import flet as ft


class View(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page

    def load_interface(self):
        pass

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