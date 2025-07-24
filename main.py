
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty
from kivymd.app import MDApp
from tinydb import TinyDB, Query
import requests
import uuid, os

KV = """
#:import MDRectangleFlatButton kivymd.uix.button.MDRectangleFlatButton

ScreenManager:
    LoginScreen:
    TerminalScreen:

<LoginScreen@Screen>:
    name: "login"
    MDBoxLayout:
        orientation: "vertical"
        spacing: "20dp"
        padding: "24dp"
        MDLabel:
            text: "TERMINAL"
            halign: "center"
            font_style: "H4"
        MDTextField:
            id: username
            hint_text: "Kullanıcı adı"
        MDRectangleFlatButton:
            text: "Giriş / Kayıt"
            pos_hint: {"center_x": .5}
            on_release: app.login(username.text)

<TerminalScreen@Screen>:
    name: "terminal"
    MDBoxLayout:
        orientation: "vertical"
        MDLabel:
            id: output
            text: "Terminal'e hoş geldin. /help yaz."
            halign: "left"
            valign: "top"
            size_hint_y: 0.9
            text_size: self.width, None
        MDTextField:
            id: cmd
            hint_text: "Komut gir (/help)"
            on_text_validate: app.run_cmd(self.text); self.text=""
"""

class TerminalApp(MDApp):
    is_premium = BooleanProperty(False)
    user = StringProperty("")

    def build(self):
        self.title = "Terminal"
        self.db = TinyDB("users.json")
        return Builder.load_string(KV)

    def login(self, username):
        if not username:
            return
        self.user = username
        users = self.db.table("users")
        q = Query()
        user = users.get(q.username == username)
        if not user:
            users.insert({"username": username, "premium": False, "uuid": str(uuid.uuid4())})
            self.is_premium = False
        else:
            self.is_premium = user.get("premium", False)
        self.root.current = "terminal"
        self._print(f"Giriş yapıldı: {username} | Premium: {self.is_premium}")

    def run_cmd(self, text):
        text = text.strip()
        if not text:
            return
        if text == "/help":
            self._print("""Komutlar:
/help
/info
/run <python_kodu>
/botcreate (premium)
/sitebuild (premium)
/advancedcode (premium)
""")
        elif text == "/info":
            self._print(f"Kullanıcı: {self.user} | Premium: {self.is_premium}")
        elif text.startswith("/run "):
            code = text[5:]
            try:
                out = str(eval(code, {}, {}))
            except Exception as e:
                out = f"Hata: {e}"
            self._print(out)
        elif text.startswith("/botcreate") or text.startswith("/sitebuild") or text.startswith("/advancedcode"):
            if not self.is_premium:
                self._print("Bu komut premium. WhatsApp üzerinden 29,99 USD ödeyerek aktif edebilirsin: 05357984380")
            else:
                self._print("Premium komut çalıştı (placeholder).")
        else:
            self._print("Bilinmeyen komut. /help yaz.")

    def _print(self, s):
        out = self.root.get_screen("terminal").ids.output
        out.text += "\n" + s

if __name__ == "__main__":
    TerminalApp().run()
