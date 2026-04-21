from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDIconButton, MDRaisedButton, MDFloatingActionButtonSpeedDial
from kivymd.uix.label import MDLabel
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage

class LockScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        # صورة الدخول (جين وو)
        self.bg = AsyncImage(
            source="https://w0.peakpx.com/wallpaper/404/695/HD-wallpaper-sung-jin-woo-eye-glowing-blue-anime-solo-leveling.jpg", 
            allow_stretch=True, keep_ratio=False
        )
        # حقل الباسورد مشفر (نقاط)
        self.password = TextInput(
            password=True, size_hint=(.8, .07), pos_hint={"center_x": .5, "center_y": .45},
            background_color=(0,0,0,0.7), foreground_color=(0,.8,1,1), 
            hint_text="ACCESS CODE", halign="center", multiline=False
        )
        btn = MDRaisedButton(
            text="[ ARISES ]", pos_hint={"center_x": .5, "center_y": .32},
            md_bg_color=(0, 0.5, 0.8, 1), on_release=self.check
        )
        layout.add_widget(self.bg); layout.add_widget(self.password); layout.add_widget(btn)
        self.add_widget(layout)

    def check(self, *args):
        if self.password.text == "20057": self.manager.current = "main"

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root_layout = FloatLayout()
        
        main_box = BoxLayout(orientation='vertical')
        
        # صورة الغلاف العلوية
        self.top_img = AsyncImage(
            source="https://w0.peakpx.com/wallpaper/326/289/HD-wallpaper-sung-jin-woo-solo-leveling-anime-aesthetic-shadows.jpg",
            size_hint_y=0.35, allow_stretch=True, keep_ratio=False
        )
        
        # منطقة عرض الرسائل
        self.msgs_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=20)
        self.msgs_layout.bind(minimum_height=self.msgs_layout.setter('height'))
        scroll = ScrollView(size_hint_y=0.55); scroll.add_widget(self.msgs_layout)
        
        # شريط الإدخال مع أيقونة الإرسال (مثل الصورة المطلوبة)
        in_bar_layout = BoxLayout(size_hint_y=0.1, padding=10, spacing=5)
        
        self.ti = TextInput(
            hint_text="Type a message...", 
            background_color=(0.1, 0.1, 0.1, 1), 
            foreground_color=(0, 1, 0, 1), # أخضر هكر
            multiline=False, size_hint_x=0.85
        )
        
        # زر الإرسال - أيقونة الطائرة الورقية
        btn_send = MDIconButton(
            icon="send", 
            icon_color=(0, 0.8, 1, 1),
            pos_hint={"center_y": 0.5},
            on_release=self.send_message
        )
        
        in_bar_layout.add_widget(self.ti)
        in_bar_layout.add_widget(btn_send)
        
        # زر الـ (+) الجانبي
        self.plus_btn = MDFloatingActionButtonSpeedDial()
        self.plus_btn.data = {'Camera': 'camera', 'Gallery': 'image', 'Files': 'file-document'}
        self.plus_btn.root_button_anim = True
        self.plus_btn.bg_color_root_button = (0.8, 0.8, 0.8, 1)
        
        main_box.add_widget(self.top_img); main_box.add_widget(scroll); main_box.add_widget(in_bar_layout)
        self.root_layout.add_widget(main_box)
        self.root_layout.add_widget(self.plus_btn)
        self.add_widget(self.root_layout)

    def send_message(self, *args):
        if self.ti.text:
            new_msg = MDLabel(
                text=f"Mustafa: {self.ti.text}", 
                theme_text_color="Custom", 
                text_color=(0, 0.8, 1, 1), 
                size_hint_y=None, height=40, halign="right"
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

MainApp().run()
