from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDFloatingActionButtonSpeedDial
from kivymd.uix.label import MDLabel
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

class LockScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        
        # الواجهة: صورة "الضاحك" (bg_lock.jpg)
        self.bg = Image(
            source="bg_lock.jpg", 
            allow_stretch=True, 
            keep_ratio=False
        )
        
        self.password = TextInput(
            password=True, 
            size_hint=(.8, .07), 
            pos_hint={"center_x": .5, "center_y": .45},
            background_color=(0,0,0,0.7), 
            foreground_color=(0,1,0,1), 
            hint_text="ENTER KEY", 
            halign="center", 
            multiline=False
        )
        
        btn = MDRaisedButton(
            text="[ LOGIN ]", 
            pos_hint={"center_x": .5, "center_y": .32},
            md_bg_color=(0, 0.5, 0.8, 1), 
            on_release=self.check
        )
        
        layout.add_widget(self.bg)
        layout.add_widget(self.password)
        layout.add_widget(btn)
        self.add_widget(layout)

    def check(self, *args):
        if self.password.text == "20057":
            self.manager.current = "main"

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root_layout = FloatLayout()
        
        # الخلفية الداخلية: الصورة "السوداء" (bg_main.jpg)
        self.bg_main = Image(
            source="bg_main.jpg",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )
        
        main_box = BoxLayout(orientation='vertical')
        
        # منطقة عرض الرسائل
        self.msgs_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=20)
        self.msgs_layout.bind(minimum_height=self.msgs_layout.setter('height'))
        scroll = ScrollView(size_hint_y=0.9)
        scroll.add_widget(self.msgs_layout)
        
        # شريط الإدخال مع أيقونة الإرسال
        in_bar = BoxLayout(size_hint_y=0.1, padding=10, spacing=5)
        self.ti = TextInput(
            hint_text="System command...", 
            background_color=(0.1, 0.1, 0.1, 0.8), 
            foreground_color=(0, 1, 0, 1), 
            multiline=False, 
            size_hint_x=0.85
        )
        btn_send = MDIconButton(
            icon="send", 
            icon_color=(0, 0.8, 1, 1),
            on_release=self.send_message
        )
        in_bar.add_widget(self.ti)
        in_bar.add_widget(btn_send)
        
        # زر الـ (+) الرمادي
        self.plus_btn = MDFloatingActionButtonSpeedDial()
        self.plus_btn.data = {'Camera': 'camera', 'Gallery': 'image', 'Files': 'file-document'}
        self.plus_btn.root_button_anim = True
        self.plus_btn.bg_color_root_button = (0.8, 0.8, 0.8, 1)
        
        main_box.add_widget(scroll)
        main_box.add_widget(in_bar)
        
        self.root_layout.add_widget(self.bg_main)
        self.root_layout.add_widget(main_box)
        self.root_layout.add_widget(self.plus_btn)
        self.add_widget(self.root_layout)

    def send_message(self, *args):
        if self.ti.text:
            new_msg = MDLabel(
                text=f"Mustafa: {self.ti.text}", 
                theme_text_color="Custom", 
                text_color=(0, 0.8, 1, 1), 
                size_hint_y=None, 
                height=40, 
                halign="right"
            )
            self.msgs_layout.add_widget(new_msg)
            self.ti.text = ""

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        sm = MDScreenManager()
        sm.add_widget(LockScreen(name="lock"))
        sm.add_widget(MainScreen(name="main"))
        return sm

if __name__ == "__main__":
    MainApp().run()
