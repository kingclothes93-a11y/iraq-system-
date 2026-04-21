from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.button import MDRaisedButton, MDFloatingActionButtonSpeedDial
from kivymd.uix.label import MDLabel
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.clock import Clock

class LockScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        # صورة جين وو برابط مباشر وعالي الجودة
        self.bg = AsyncImage(
            source="https://raw.githubusercontent.com/Kivy-Design/KivyMD-Assets/main/images/logo/kivymd-logo-black.png", 
            allow_stretch=True, keep_ratio=False, opacity=0.8
        )
        # ملاحظة للملك: جرب هذا الرابط، إذا اشتغل نغيره لصورة Solo Leveling فوراً
        
        self.password = TextInput(
            password=True, size_hint=(.7, .06), pos_hint={"center_x": .5, "center_y": .5},
            background_color=(0,0,0,0.8), foreground_color=(0,.8,1,1), hint_text="Password: 20057"
        )
        btn = MDRaisedButton(text="[ ARISES ]", pos_hint={"center_x": .5, "center_y": .35}, on_release=self.check)
        
        layout.add_widget(self.bg); layout.add_widget(self.password); layout.add_widget(btn)
        self.add_widget(layout)

    def check(self, *args):
        if self.password.text == "20057": self.manager.current = "main"

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root_layout = FloatLayout()
        
        main_box = BoxLayout(orientation='vertical')
        # الجزء العلوي (بدون Overlay معقد)
        self.top_img = AsyncImage(
            source="https://w0.peakpx.com/wallpaper/326/289/HD-wallpaper-sung-jin-woo-solo-leveling-anime-aesthetic-shadows.jpg",
            size_hint_y=0.4, allow_stretch=True, keep_ratio=False
        )
        
        # منطقة الرسائل
        self.msgs = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=15)
        self.msgs.bind(minimum_height=self.msgs.setter('height'))
        scroll = ScrollView(size_hint_y=0.5); scroll.add_widget(self.msgs)
        
        # زر الـ (+) Speed Dial اللي طلبته
        self.plus_btn = MDFloatingActionButtonSpeedDial()
        self.plus_btn.data = {
            'Camera': 'camera',
            'Gallery': 'image',
            'Files': 'file-document'
        }
        self.plus_btn.root_button_anim = True
        
        # شريط الإدخال
        in_bar = BoxLayout(size_hint_y=0.1, padding=10)
        self.ti = TextInput(hint_text="Enter Command...", background_color=(0.1, 0.1, 0.1, 1), foreground_color=(0, 0.8, 1, 1), multiline=False)
        in_bar.add_widget(self.ti)
        
        main_box.add_widget(self.top_img); main_box.add_widget(scroll); main_box.add_widget(in_bar)
        self.root_layout.add_widget(main_box)
        self.root_layout.add_widget(self.plus_btn)
        self.add_widget(self.root_layout)

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        sm = MDScreenManager()
        sm.add_widget(LockScreen(name="lock"))
        sm.add_widget(MainScreen(name="main"))
        return sm

MainApp().run()
