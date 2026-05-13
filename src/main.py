import flet as ft
import requests
import threading
import time

PROJECT_URL = "https://bplssskenjelcjwbyinv.supabase.co"
TABLE_NAME = "messages"
REST_URL = f"{PROJECT_URL}/rest/v1/{TABLE_NAME}"

KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJwbHNzc2tlbmplbGNqd2J5aW52Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzg2MDM5ODYsImV4cCI6MjA5NDE3OTk4Nn0.F2NM0t7b3fgSuYdO20eoecFUeWnpkh13fOCyMY6IGe8"

HEADERS = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def main(page: ft.Page):
    page.title = "Xach Cloud Chat"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 700
    page.padding = 10
    
    chat = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, auto_scroll=True)
    user_name = ft.TextField(label="Твое имя", width=200, value="Дима")
    new_message = ft.TextField(hint_text="Введите сообщение...", expand=True)
    status_text = ft.Text("", size=12)

    def load_messages():
        try:
            res = requests.get(REST_URL, headers=HEADERS, params={"select": "*", "order": "created_at.asc", "limit": "50"}, timeout=10)
            if res.status_code == 200:
                data = res.json()
                chat.controls.clear()
                for m in data:
                    chat.controls.append(ft.Text(f"{m['name']}: {m['content']}", size=14))
                page.update()
        except:
            status_text.value = "Нет соединения"
            page.update()

    def send_click(e):
        msg = new_message.value.strip()
        name = user_name.value.strip()
        if not msg:
            return
        try:
            requests.post(REST_URL, headers=HEADERS, json={"name": name, "content": msg}, timeout=10)
            new_message.value = ""
            load_messages()
            page.update()
        except:
            status_text.value = "Ошибка"
            page.update()

    page.add(
        ft.Row([ft.Text("💬 Xach Chat", size=20)]),
        ft.Row([user_name]),
        ft.Container(content=chat, expand=True),
        ft.Row([new_message, ft.ElevatedButton("Send", on_click=send_click)]),
        status_text,
    )
    load_messages()
    
    def update_loop():
        while True:
            time.sleep(2)
            load_messages()
    threading.Thread(target=update_loop, daemon=True).start()

ft.app(target=main)
