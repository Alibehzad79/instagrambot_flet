import flet as ft
import time

def main(page: ft.Page):
    def start(e=None):
        for i in range(100):
            page.add(ft.Text(i))
            page.update()
            time.sleep(1)
    def stop(e):
        start.terminate()
    page.add(ft.ElevatedButton(text="start", color="green", on_click=start))
    page.add(ft.ElevatedButton(text="stop", color="red", on_click=stop))

ft.app(target=main)