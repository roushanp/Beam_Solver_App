import os
from kivy.factory import Factory as F
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList
from kivy.uix.scrollview import ScrollView
from kivymd.uix.textfield import MDTextField, MDTextFieldRect
from sympy import symbols
from sympy.plotting import plot
from sympy.physics.continuum_mechanics import Beam
from kivy.clock import Clock
from helpers import *

Window.size = (350, 650)  # adjusting window size equivalent to mobile phone


class StartScreen(Screen):
    pass


class ContentNavigationDrawer(BoxLayout):
    pass


class DrawerList(ThemableBehavior, MDList):
    pass


class Menuscreen(Screen):
    container = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Menuscreen, self).__init__(**kwargs)
        Clock.schedule_once(self.setup_scrollview, 1)

    def setup_scrollview(self, dt):
        self.container.bind(minimum_height=self.container.setter('height'))

    def add_shear_graph(self):
        if os.path.exists('./shear.png'):
            self.container.add_widget(F.MyTile(source='shear.png'))
        return self

    def add_bending_graph(self):
        if os.path.exists('./bending.png'):
            self.container.add_widget(F.MyTile(source='bending.png'))
        return self

    def add_slope_graph(self):
        if os.path.exists('./slope.png'):
            self.container.add_widget(F.MyTile(source='slope.png'))
        return self

    def add_deflection_graph(self):
        if os.path.exists('./deflection.png'):
            self.container.add_widget(F.MyTile(source='deflection.png'))
        return self

    def add_loading_graph(self):
        if os.path.exists('./loading.png'):
            self.container.add_widget(F.MyTile(source='loading.png'))
        return self

    def remove_graphs(self):
        self.container.clear_widgets()
        return self


class Toggle_btn(MDGridLayout):
    def __init__(self, **kwargs):
        super(Toggle_btn, self).__init__(**kwargs)
        self.cols = 2

        self.tb1 = ToggleButton(text='DOWN', group='dir', state='down')
        self.add_widget(self.tb1)

        self.tb2 = ToggleButton(text='UP', group='dir')
        self.add_widget(self.tb2)

    def get_state(self):
        return [self.tb1.state, self.tb2.state]

# -------------Toggle button and moment codes-----------------------------------

class Toggle_btn_moment(MDGridLayout):
    def __init__(self, **kwargs):
        super(Toggle_btn_moment, self).__init__(**kwargs)
        self.cols = 2

        self.tb1 = ToggleButton(text='CLOCK', group='dir', state='down')
        self.add_widget(self.tb1)

        self.tb2 = ToggleButton(text='ANTI-CLOCK', group='dir')
        self.add_widget(self.tb2)

    def get_state(self):
        return [self.tb1.state, self.tb2.state]

# -----------------Beam app codes--------------------------------------------------

class BeamApp(MDApp):
    in_class = ObjectProperty(None)
    container = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.E = '20'
        self.I = '40'
        self.Len = '20'
        self.reaction_vars = []
        self.BEAM = Beam(self.Len, self.E, self.I)

        # ---------------------support&load button----------------
        self.sup = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, None))
        self.sup.bind(minimum_height=self.sup.setter('height'))
        self.sup_scroll = ScrollView()
        self.sup_scroll.add_widget(self.sup)

        self.load = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, None))
        self.load.bind(minimum_height=self.load.setter('height'))
        self.load_scroll = ScrollView()
        self.load_scroll.add_widget(self.load)

        # --------------------Plots-----------------------------
        self.d = None
        self.shear_plot_cnt = 0
        self.slope_plot_cnt = 0
        self.bending_plot_cnt = 0
        self.deflection_plot_cnt = 0
        self.loading_plot_cnt = 0

        if os.path.exists('./shear.png'):
            os.remove('./shear.png')

        if os.path.exists('./bending.png'):
            os.remove('./bending.png')

        if os.path.exists('./slope.png'):
            os.remove('./slope.png')

        if os.path.exists('./deflection.png'):
            os.remove('./deflection.png')

        if os.path.exists('./loading.png'):
            os.remove('./loading.png')

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.screen = Builder.load_string(screen_helper)
        return self.screen

    def check_print(self):
        value = self.root.in_class.text
        self.dialog = MDDialog(title='Welcome',
                               text="Hi " + value + "! To solve beam give all the required values in navigation bar of menu",
                               size_hint=(0.8, 1),
                               buttons=[MDFlatButton(text='More', on_release=self.menu_page)]
                               )
        self.dialog.open()

    def sign_con(self):
        self.dialog = MDDialog(
            title="considering upward direction and Anticlockwise sense to be positive",
            size_hint=(0.8, 1),
            buttons=[MDFlatButton(text='close', on_release=self.close_dialog)]
        )
        self.dialog.open()

    def menu_page(self, obj):
        self.screen.current = 'menu'
        self.dialog.dismiss()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def popup_default_value(self):
        layout1 = MDGridLayout(cols=2)
        layout1.add_widget(
            MDLabel(text='E = ', theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                    font_style="H4"))

        self.E_text = MDTextFieldRect(text=self.E, multiline=False)
        layout1.add_widget(self.E_text)

        layout1.add_widget(
            MDLabel(text='I = ', theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                    font_style="H4"))

        self.I_text = MDTextFieldRect(text=self.I, multiline=False)
        layout1.add_widget(self.I_text)

        layout1.add_widget(
            MDLabel(text='LENGTH (m) = ', theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                    font_style="H6"))

        self.len_text = MDTextFieldRect(text=self.Len, multiline=False)
        layout1.add_widget(self.len_text)

        btn = MDRectangleFlatButton(text='SAVE')
        layout1.add_widget(btn)
        btn.bind(on_press=self.set_E_I_Len)

        btn2 = MDRectangleFlatButton(text='CLOSE')
        layout1.add_widget(btn2)
        btn2.bind(on_press=self.popup_dismiss)

        self.popup = Popup(title='SET E, I  AND LENGTH FOR BEAM', content=layout1, size_hint=(.6, .6),
                           pos_hint={'center_x': .5, 'center_y': .5}, auto_dismiss=False)
        self.popup.open()

    def set_E_I_Len(self, instance):
        self.E = self.E_text.text
        self.I = self.I_text.text
        self.Len = self.len_text.text

        self.BEAM = Beam(self.Len, self.E, self.I)

        self.popup.dismiss()

    def popup_fix(self):
        layout = MDGridLayout(cols=2)

        layout.add_widget(
            MDLabel(text='X (m) = ', theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                    font_style="H6"))

        self.fix_text = MDTextFieldRect(multiline=False)
        layout.add_widget(self.fix_text)

        btn = MDRectangleFlatButton(text='SAVE')
        layout.add_widget(btn)
        btn.bind(on_press=self.add_fix)

        btn2 = MDRectangleFlatButton(text='CLOSE')
        layout.add_widget(btn2)
        btn2.bind(on_press=self.popup_dismiss)

        self.popup = Popup(title='FIXED SUPPPORT ', content=layout, size_hint=(.8, .4),
                           pos_hint={'center_x': .5, 'center_y': .5}, auto_dismiss=False)
        self.popup.open()

    def add_fix(self, instance):
        if self.fix_text.text:
            if int(self.fix_text.text) >= 0 and int(self.fix_text.text) <= int(self.Len):

                self.reaction_vars.append(symbols('R_{}'.format(self.fix_text.text)))
                self.reaction_vars.append(symbols('M_{}'.format(self.fix_text.text)))
                self.BEAM.apply_support(self.fix_text.text, 'fixed')
                self.BEAM.bc_deflection.append((self.fix_text.text, 0))
                self.BEAM.bc_slope.append((self.fix_text.text, 0))

                self.sup.add_widget(MDLabel(text=f"Fixed support at {self.fix_text.text} m", size_hint_y=None,
                                            theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                                            font_style="H6"))

                self.popup.dismiss()

            else:
                layout = BoxLayout(orientation='vertical')
                layout.add_widget(MDLabel(text="ENTER POSITION ON THE BEAM", theme_text_color="Custom",
                                          text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1), font_style="H6"))
                btn = MDRectangleFlatButton(text='CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press=self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title="INVALID POSTION", content=layout, size_hint=(.4, .4),
                                            pos_hint={'center_x': .5, 'center_y': .5})
                self.popup_in_popup.open()

        else:
            layout = BoxLayout(orientation='vertical')
            layout.add_widget(MDLabel(text="YOU HAVEN'T ENTERED POSITION", theme_text_color="Custom",
                                      text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1), font_style="H6"))
            btn = MDRectangleFlatButton(text='CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press=self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title="NOTHING TO SAVE", content=layout, size_hint=(.4, .4),
                                        pos_hint={'center_x': .5, 'center_y': .5})
            self.popup_in_popup.open()

    def popup_roller(self):

        layout = MDGridLayout(cols=2)

        layout.add_widget(
            MDLabel(text='X (m) = ', theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                    font_style="H6"))

        self.roller_text = MDTextFieldRect(multiline=False)
        layout.add_widget(self.roller_text)

        btn = MDRectangleFlatButton(text='SAVE')
        layout.add_widget(btn)
        btn.bind(on_press=self.add_roller)

        btn2 = MDRectangleFlatButton(text='CLOSE')
        layout.add_widget(btn2)
        btn2.bind(on_press=self.popup_dismiss)

        self.popup = Popup(title='ROLLER SUPPORT ', content=layout, size_hint=(.8, .4),
                           pos_hint={'center_x': .5, 'center_y': .5}, auto_dismiss=False)
        self.popup.open()

    def add_roller(self, instance):

        if self.roller_text.text:

            if int(self.roller_text.text) >= 0 and int(self.roller_text.text) <= int(self.Len):

                self.reaction_vars.append(symbols('R_{}'.format(self.roller_text.text)))
                self.BEAM.apply_support(self.roller_text.text, 'roller')
                self.BEAM.bc_deflection.append((self.roller_text.text, 0))

                self.sup.add_widget(MDLabel(text=f"Roller support at {self.roller_text.text} m", size_hint_y=None,
                                            theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                                            font_style="H6"))

                self.popup.dismiss()

            else:
                layout = BoxLayout(orientation='vertical')
                layout.add_widget(MDLabel(text="ENTER POSITION ON THE BEAM", theme_text_color="Custom",
                                          text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1), font_style="H6"))
                btn = MDRectangleFlatButton(text='CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press=self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title="INVALID POSTION", content=layout, size_hint=(.4, .4),
                                            pos_hint={'center_x': .5, 'center_y': .5})
                self.popup_in_popup.open()

        else:
            layout = BoxLayout(orientation='vertical')
            layout.add_widget(MDLabel(text="YOU HAVEN'T ENTERED POSITION", theme_text_color="Custom",
                                      text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1), font_style="H6"))
            btn = MDRectangleFlatButton(text='CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press=self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title="NOTHING TO SAVE", content=layout, size_hint=(.4, .4),
                                        pos_hint={'center_x': .5, 'center_y': .5})
            self.popup_in_popup.open()

    def popup_pin(self):

        layout = MDGridLayout(cols=2)

        layout.add_widget(
            MDLabel(text='X (m) = ', theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                    font_style="H6"))

        self.pin_text = MDTextFieldRect(multiline=False)
        layout.add_widget(self.pin_text)

        btn = MDRectangleFlatButton(text='SAVE')
        layout.add_widget(btn)
        btn.bind(on_press=self.add_pin)

        btn2 = MDRectangleFlatButton(text='CLOSE')
        layout.add_widget(btn2)
        btn2.bind(on_press=self.popup_dismiss)

        self.popup = Popup(title='PIN SUPPORT ', content=layout, size_hint=(.8, .4),
                           pos_hint={'center_x': .5, 'center_y': .5}, auto_dismiss=False)
        self.popup.open()

    def add_pin(self, instance):

        if self.pin_text.text:

            if int(self.pin_text.text) >= 0 and int(self.pin_text.text) <= int(self.Len):

                self.reaction_vars.append(symbols('R_{}'.format(self.pin_text.text)))
                self.BEAM.apply_support(self.pin_text.text, 'pin')
                self.BEAM.bc_deflection.append((self.pin_text.text, 0))

                self.sup.add_widget(
                    MDLabel(text=f"Pin support at {self.pin_text.text} m", size_hint_y=None, theme_text_color="Custom",
                            text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                            font_style="H6"))

                self.popup.dismiss()

            else:
                layout = BoxLayout(orientation='vertical')
                layout.add_widget(MDLabel(text="ENTER POSITION ON THE BEAM", theme_text_color="Custom",
                                          text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1), font_style="H6"))
                btn = MDRectangleFlatButton(text='CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press=self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title="INVALID POSTION", content=layout, size_hint=(.4, .4),
                                            pos_hint={'center_x': .5, 'center_y': .5})
                self.popup_in_popup.open()

        else:
            layout = BoxLayout(orientation='vertical')
            layout.add_widget(MDLabel(text="YOU HAVEN'T ENTERED POSITION", theme_text_color="Custom",
                                      text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1), font_style="H6"))
            btn = MDRectangleFlatButton(text='CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press=self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title="NOTHING TO SAVE", content=layout, size_hint=(.4, .4),
                                        pos_hint={'center_x': .5, 'center_y': .5})
            self.popup_in_popup.open()

    def popup_vertical(self):

        layout = BoxLayout(orientation='vertical')

        layout1 = MDGridLayout(cols=2)

        layout1.add_widget(
            MDLabel(text='X (m) = ', theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                    font_style="H6"))

        self.vertical_load_pos_text = MDTextFieldRect(multiline=False)
        layout1.add_widget(self.vertical_load_pos_text)
        layout.add_widget(layout1)

        layout2 = MDGridLayout(cols=2)

        layout2.add_widget(
            MDLabel(text='LOAD (kN) = ', theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                    font_style="H6"))

        self.vertical_load_mag_text = MDTextFieldRect(multiline=False)
        layout2.add_widget(self.vertical_load_mag_text)

        layout.add_widget(layout2)

        self.load_dir = Toggle_btn()
        layout.add_widget(self.load_dir)

        layout3 = MDGridLayout(cols=2)

        btn = MDRectangleFlatButton(text='SAVE')
        layout3.add_widget(btn)
        btn.bind(on_press=self.add_vertical_load)

        btn2 = MDRectangleFlatButton(text='CLOSE')
        layout3.add_widget(btn2)
        btn2.bind(on_press=self.popup_dismiss)

        layout.add_widget(layout3)

        self.popup = Popup(title='POINT LOAD ', content=layout, size_hint=(.8, .6),
                           pos_hint={'center_x': .5, 'center_y': .5}, auto_dismiss=False)

        self.popup.open()

    def add_vertical_load(self, instance):
        if self.vertical_load_mag_text.text != '' and self.vertical_load_pos_text.text != '':

            if int(self.vertical_load_pos_text.text) >= 0 and int(self.vertical_load_pos_text.text) <= int(self.Len):

                states = self.load_dir.get_state()
                print(states)
                if (states[0] == 'normal' and states[1] == 'down') or (states[0] == 'down' and states[1] == 'normal'):

                    if states[0] == 'normal' and states[1] == 'down':

                        self.BEAM.apply_load(self.vertical_load_mag_text.text, self.vertical_load_pos_text.text, -1)

                        self.load.add_widget(MDLabel(
                            text=f"Upward Point load of\n{self.vertical_load_mag_text.text} kN at {self.vertical_load_pos_text.text} m",
                            size_hint_y=None))

                        self.popup.dismiss()
                    else:
                        self.BEAM.apply_load('-' + self.vertical_load_mag_text.text, self.vertical_load_pos_text.text,
                                             -1)

                        self.load.add_widget(MDLabel(
                            text=f"Downward Point load of\n{self.vertical_load_mag_text.text} kN at {self.vertical_load_pos_text.text} m",
                            size_hint_y=None, theme_text_color="Custom",
                            text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                            font_style="H6"))

                        self.popup.dismiss()

                else:
                    layout = BoxLayout(orientation='vertical')
                    layout.add_widget(MDLabel(text="YOU MUST CHOOSE ONE DIRECTION", theme_text_color="Custom",
                                              text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1), font_style="H6"))
                    btn = MDRectangleFlatButton(text='CLOSE')
                    layout.add_widget(btn)
                    btn.bind(on_press=self.popup_in_popup_dismiss)
                    self.popup_in_popup = Popup(title="IN WHICH DIR. DO I APPLY LOAD ?", content=layout,
                                                size_hint=(.4, .4), pos_hint={'center_x': .5, 'center_y': .5})
                    self.popup_in_popup.open()

            else:
                layout = BoxLayout(orientation='vertical')
                layout.add_widget(MDLabel(text="ENTER POSITION ON THE BEAM", theme_text_color="Custom",
                                          text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1), font_style="H6"))
                btn = MDRectangleFlatButton(text='CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press=self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title="INVALID POSTION", content=layout, size_hint=(.4, .4),
                                            pos_hint={'center_x': .5, 'center_y': .5})
                self.popup_in_popup.open()

        else:
            layout = BoxLayout(orientation='vertical')
            layout.add_widget(MDLabel(text="ENTER BOTH LOAD MAG. AND POS.", theme_text_color="Custom",
                                      text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1), font_style="H6"))
            btn = MDRectangleFlatButton(text='CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press=self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title="INSUFFICIENT INFO !", content=layout, size_hint=(.7, .4),
                                        pos_hint={'center_x': .5, 'center_y': .5})
            self.popup_in_popup.open()

    def popup_moment(self):
        layout = BoxLayout(orientation='vertical')

        layout1 = MDGridLayout(cols=2)

        layout1.add_widget(
            MDLabel(text='X (m) = ', theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                    font_style="H6"))

        self.moment_pos_text = MDTextFieldRect(multiline=False)
        layout1.add_widget(self.moment_pos_text)
        layout.add_widget(layout1)

        layout3 = MDGridLayout(cols=2)
        layout3.add_widget(
            MDLabel(text='MOMENT (kN*m)= ', theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                    font_style="H6"))

        self.moment_mag_text = MDTextFieldRect(multiline=False)
        layout3.add_widget(self.moment_mag_text)

        layout.add_widget(layout3)

        self.moment_dir = Toggle_btn_moment()
        layout.add_widget(self.moment_dir)

        layout2 = MDGridLayout(cols=2)

        btn = MDRectangleFlatButton(text='SAVE')
        layout2.add_widget(btn)
        btn.bind(on_press=self.add_moment)

        btn2 = MDRectangleFlatButton(text='CLOSE')
        layout2.add_widget(btn2)
        btn2.bind(on_press=self.popup_dismiss)

        layout.add_widget(layout2)

        self.popup = Popup(title='MOMENT MAG. ', content=layout, size_hint=(.8, .6),
                           pos_hint={'center_x': .5, 'center_y': .5}, auto_dismiss=False)
        self.popup.open()

    def add_moment(self, instance):

        if self.moment_pos_text.text != '' and self.moment_mag_text.text != '':
            if int(self.moment_pos_text.text) >= 0 and int(self.moment_pos_text.text) <= int(self.Len):

                states = self.moment_dir.get_state()
                print(states)
                if (states[0] == 'normal' and states[1] == 'down') or (states[0] == 'down' and states[1] == 'normal'):

                    if states[0] == 'normal' and states[1] == 'down':

                        self.BEAM.apply_load(self.moment_mag_text.text, self.moment_pos_text.text, -2)

                        self.load.add_widget(MDLabel(
                            text=f"Anticlockwise moment of\n{self.moment_mag_text.text} kN-m at {self.moment_pos_text.text} m",
                            size_hint_y=None, theme_text_color="Custom",
                            text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                            font_style="H6"))

                        self.popup.dismiss()
                    else:
                        self.BEAM.apply_load('-' + self.moment_mag_text.text, self.moment_pos_text.text, -2)

                        self.load.add_widget(MDLabel(
                            text=f"Clockwise moment of\n{self.moment_mag_text.text} kN-m at {self.moment_pos_text.text} m",
                            size_hint_y=None, theme_text_color="Custom",
                            text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                            font_style="H6"))

                        self.popup.dismiss()


                else:
                    layout = BoxLayout(orientation='vertical')
                    layout.add_widget(MDLabel(text="YOU MUST CHOOSE ONE DIRECTION", theme_text_color="Custom",
                                              text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1), font_style="H6"))
                    btn = MDRectangleFlatButton(text='CLOSE')
                    layout.add_widget(btn)
                    btn.bind(on_press=self.popup_in_popup_dismiss)
                    self.popup_in_popup = Popup(title="IN WHICH DIR. DO I APPLY MOMENT ?", content=layout,
                                                size_hint=(.4, .4), pos_hint={'center_x': .5, 'center_y': .5})
                    self.popup_in_popup.open()

            else:
                layout = BoxLayout(orientation='vertical')
                layout.add_widget(MDLabel(text="ENTER POSITION ON THE BEAM", theme_text_color="Custom",
                                          text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1), font_style="H6"))
                btn = MDRectangleFlatButton(text='CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press=self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title="INVALID POSTION", content=layout, size_hint=(.4, .4),
                                            pos_hint={'center_x': .5, 'center_y': .5})
                self.popup_in_popup.open()

        else:
            layout = BoxLayout(orientation='vertical')
            layout.add_widget(MDLabel(text="ENTER BOTH MOMENT MAG. AND POS.", theme_text_color="Custom",
                                      text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1), font_style="H6"))
            btn = MDRectangleFlatButton(text='CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press=self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title="INSUFFICIENT INFO !", content=layout, size_hint=(.7, .4),
                                        pos_hint={'center_x': .5, 'center_y': .5})
            self.popup_in_popup.open()

    def popup_linear(self):

        self.ramp_order = 0

        layout = BoxLayout(orientation='vertical')

        layout1 = MDGridLayout(cols=2)

        layout1.add_widget(
            MDLabel(text='X1 (m) = ', theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                    font_style="H6"))

        self.starting_pos_text = MDTextFieldRect(multiline=False)
        layout1.add_widget(self.starting_pos_text)
        layout.add_widget(layout1)

        layout3 = MDGridLayout(cols=2)
        layout3.add_widget(
            MDLabel(text='X2 (m) = ', theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                    font_style="H6"))

        self.ending_pos_text = MDTextFieldRect(multiline=False)
        layout3.add_widget(self.ending_pos_text)
        layout.add_widget(layout3)

        layout4 = MDGridLayout(cols=2)
        layout4.add_widget(
            MDLabel(text='LOAD (kN) = ', theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                    font_style="H6"))

        self.load_per_m_text = MDTextFieldRect(multiline=False)
        layout4.add_widget(self.load_per_m_text)
        layout.add_widget(layout4)

        self.load_dir_linear = Toggle_btn()
        layout.add_widget(self.load_dir_linear)

        layout2 = MDGridLayout(cols=2)

        btn = MDRectangleFlatButton(text='SAVE')
        layout2.add_widget(btn)
        btn.bind(on_press=self.add_linear_load)

        btn2 = MDRectangleFlatButton(text='CLOSE')
        layout2.add_widget(btn2)
        btn2.bind(on_press=self.popup_dismiss)

        layout.add_widget(layout2)

        self.popup = Popup(title='CONSTANT PRESSURE', content=layout, size_hint=(.8, .7),
                           pos_hint={'center_x': .5, 'center_y': .5}, auto_dismiss=False)

        self.popup.open()

    def add_linear_load(self, instance):

        if self.starting_pos_text.text != '' and self.ending_pos_text.text != '' and self.load_per_m_text.text != '':

            if int(self.starting_pos_text.text) >= 0 and int(self.starting_pos_text.text) <= int(self.Len) and int(
                    self.ending_pos_text.text) >= 0 and int(self.ending_pos_text.text) <= int(self.Len):

                if int(self.starting_pos_text.text) != int(self.ending_pos_text.text):

                    states = self.load_dir_linear.get_state()
                    print(states)
                    if (states[0] == 'normal' and states[1] == 'down') or (
                            states[0] == 'down' and states[1] == 'normal'):

                        if self.ramp_order == 0:
                            dload_type = "constant pressure"
                            unit = "kN/m"
                        elif self.ramp_order == 1:
                            dload_type = "linear ramp"
                            unit = "kN/m/m"
                        elif self.ramp_order == 2:
                            dload_type = "prabolic ramp"
                            unit = "kN/m/m/m"

                        if states[0] == 'normal' and states[1] == 'down':

                            self.BEAM.apply_load(self.load_per_m_text.text, self.starting_pos_text.text,
                                                 self.ramp_order, int(self.ending_pos_text.text))

                            self.load.add_widget(MDLabel(
                                text=f"Upward {dload_type} of\n{self.load_per_m_text.text} {unit} from {self.starting_pos_text.text} m to {self.ending_pos_text.text} m",
                                size_hint_y=None, theme_text_color="Custom",
                                text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                                font_style="H6"))

                            self.popup.dismiss()
                        else:
                            self.BEAM.apply_load('-' + self.load_per_m_text.text, self.starting_pos_text.text,
                                                 self.ramp_order, int(self.ending_pos_text.text))

                            self.load.add_widget(MDLabel(
                                text=f"Downward {dload_type} of\n{self.load_per_m_text.text} {unit} from {self.starting_pos_text.text} m to {self.ending_pos_text.text} m",
                                size_hint_y=None, theme_text_color="Custom",
                                text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                                font_style="H6"))

                            self.popup.dismiss()


                    else:
                        layout = BoxLayout(orientation='vertical')
                        layout.add_widget(MDLabel(text="YOU MUST CHOOSE ONE DIRECTION", theme_text_color="Custom",
                                                  text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1), font_style="H6"))
                        btn = MDRectangleFlatButton(text='CLOSE')
                        layout.add_widget(btn)
                        btn.bind(on_press=self.popup_in_popup_dismiss)
                        self.popup_in_popup = Popup(title="IN WHICH DIR. DO I APPLY THE LOAD ?", content=layout,
                                                    size_hint=(.4, .4), pos_hint={'center_x': .5, 'center_y': .5})
                        self.popup_in_popup.open()

                else:

                    layout = BoxLayout(orientation='vertical')
                    layout.add_widget(MDLabel(text="STARTING AND ENDING POSITIONS\nCAN'T BE SAME !"))
                    btn = MDRectangleFlatButton(text='CLOSE')
                    layout.add_widget(btn)
                    btn.bind(on_press=self.popup_in_popup_dismiss)
                    self.popup_in_popup = Popup(title="INVALID ENTRY !", content=layout, size_hint=(.4, .4),
                                                pos_hint={'center_x': .5, 'center_y': .5})
                    self.popup_in_popup.open()

            else:
                layout = BoxLayout(orientation='vertical')
                layout.add_widget(MDLabel(text="ENTER POSITION ON THE BEAM", theme_text_color="Custom",
                                          text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1), font_style="H6"))
                btn = MDRectangleFlatButton(text='CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press=self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title="INVALID POSTION", content=layout, size_hint=(.4, .4),
                                            pos_hint={'center_x': .5, 'center_y': .5})
                self.popup_in_popup.open()

        else:
            layout = BoxLayout(orientation='vertical')
            layout.add_widget(MDLabel(text="ENTER ALL START, END AND LOAD", theme_text_color="Custom",
                                      text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1), font_style="H6"))
            btn = MDRectangleFlatButton(text='CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press=self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title="INSUFFICIENT INFO !", content=layout, size_hint=(.7, .4),
                                        pos_hint={'center_x': .5, 'center_y': .5})
            self.popup_in_popup.open()

    def popup_linear_ramp(self):

        self.ramp_order = 1

        layout = BoxLayout(orientation='vertical')

        layout1 = MDGridLayout(cols=2)

        layout1.add_widget(
            MDLabel(text='X1 (m) = ', theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                    font_style="H6"))

        self.starting_pos_text = MDTextFieldRect(multiline=False)
        layout1.add_widget(self.starting_pos_text)
        layout.add_widget(layout1)

        layout3 = MDGridLayout(cols=2)
        layout3.add_widget(
            MDLabel(text='X2 (m) = ', theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                    font_style="H6"))

        self.ending_pos_text = MDTextFieldRect(multiline=False)
        layout3.add_widget(self.ending_pos_text)
        layout.add_widget(layout3)

        layout4 = MDGridLayout(cols=2)
        layout4.add_widget(
            MDLabel(text='LOAD (kN/m/m) = ', theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                    font_style="H6"))

        self.load_per_m_text = MDTextFieldRect(multiline=False)
        layout4.add_widget(self.load_per_m_text)
        layout.add_widget(layout4)

        self.load_dir_linear = Toggle_btn()
        layout.add_widget(self.load_dir_linear)

        layout2 = MDGridLayout(cols=2)

        btn = MDRectangleFlatButton(text='SAVE')
        layout2.add_widget(btn)
        btn.bind(on_press=self.add_linear_load)

        btn2 = MDRectangleFlatButton(text='CLOSE')
        layout2.add_widget(btn2)
        btn2.bind(on_press=self.popup_dismiss)

        layout.add_widget(layout2)

        self.popup = Popup(title='LINEAR RAMP LOAD ', content=layout, size_hint=(.8, .7),
                           pos_hint={'center_x': .5, 'center_y': .5}, auto_dismiss=False)

        self.popup.open()

    def popup_parabolic_ramp(self):

        self.ramp_order = 2

        layout = BoxLayout(orientation='vertical')

        layout1 = MDGridLayout(cols=2)

        layout1.add_widget(
            MDLabel(text='X1 (m) = ', theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                    font_style="H6"))

        self.starting_pos_text = MDTextFieldRect(multiline=False)
        layout1.add_widget(self.starting_pos_text)
        layout.add_widget(layout1)

        layout3 = MDGridLayout(cols=2)
        layout3.add_widget(
            MDLabel(text='X2 (m) = ', theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                    font_style="H6"))

        self.ending_pos_text = MDTextFieldRect(multiline=False)
        layout3.add_widget(self.ending_pos_text)
        layout.add_widget(layout3)

        layout4 = MDGridLayout(cols=2)
        layout4.add_widget(MDLabel(text='LOAD (kN/m/m/m) = ', theme_text_color="Custom",
                                   text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1), font_style="H6"))

        self.load_per_m_text = MDTextFieldRect(multiline=False)
        layout4.add_widget(self.load_per_m_text)
        layout.add_widget(layout4)

        self.load_dir_linear = Toggle_btn()
        layout.add_widget(self.load_dir_linear)

        layout2 = MDGridLayout(cols=2)

        btn = MDRectangleFlatButton(text='SAVE')
        layout2.add_widget(btn)
        btn.bind(on_press=self.add_linear_load)

        btn2 = MDRectangleFlatButton(text='CLOSE')
        layout2.add_widget(btn2)
        btn2.bind(on_press=self.popup_dismiss)

        layout.add_widget(layout2)

        self.popup = Popup(title='PARABOLIC RAMP LOAD ', content=layout, size_hint=(.8, .7),
                           pos_hint={'center_x': .5, 'center_y': .5}, auto_dismiss=False)

        self.popup.open()

    def popup_loading(self):

        if self.loading_plot_cnt > 0:
            layout = BoxLayout(orientation='vertical')
            layout.add_widget(MDLabel(text="MAY NEED TO SCROLL DOWN", theme_text_color="Custom",
                                      text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                                      font_style="H6"))
            btn = MDRectangleFlatButton(text='CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press=self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title="ALREADY PLOTTED !!", content=layout, size_hint=(.8, .4),
                                        pos_hint={'center_x': .5, 'center_y': .5})
            self.popup_in_popup.open()
            return

        if self.d:
            self.loading_plot_cnt += 1
            x = symbols('x')
            graph = plot(self.BEAM.load, (x, 0, self.Len), show=False, title='Distributed Load Diagram',
                         xlabel='length (m)', ylabel='Load', xlim=(float(0), float(self.Len)))
            graph.save('./loading.png')
            Menuscreen.add_loading_graph(self.screen)
        else:

            try:
                self.BEAM.solve_for_reaction_loads(*self.reaction_vars)

            except:
                layout = BoxLayout(orientation='vertical')
                layout.add_widget(MDLabel(text="INSUFFICIENT DATA GIVEN!!", theme_text_color="Custom",
                                          text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                                          font_style="H6"))
                btn = MDRectangleFlatButton(text='CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press=self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title="BEAM UNSTABLE!", content=layout, size_hint=(.7, .4),
                                            pos_hint={'center_x': .5, 'center_y': .5})
                self.popup_in_popup.open()
            else:
                self.loading_plot_cnt += 1
                self.d = self.BEAM.reaction_loads
                x = symbols('x')
                graph = plot(self.BEAM.load, (x, 0, self.Len), show=False, title='Distributed Load Diagram',
                             xlabel='length (m)', ylabel='Load', xlim=(float(0), float(self.Len)))
                graph.save('./loading.png')
                Menuscreen.add_loading_graph(self.screen)

    def popup_reaction(self):

        if self.d:
            layout = BoxLayout(orientation='vertical')
            layout_react = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, None))
            layout_react.bind(minimum_height=layout_react.setter('height'))
            layout_react_scroll = ScrollView(size_hint=(1, .8))
            layout_react_scroll.add_widget(layout_react)
            for i, j in self.d.items():
                alphabet, distance = str(i).split('_')
                if alphabet == 'R':
                    text1 = 'Reaction Force at x = {} m is {} kN'.format(distance, round(float(eval(str(j))), 2))
                elif alphabet == 'M':
                    text1 = 'Reaction Moment at x = {} m is {} kN*m'.format(distance, round(float(eval(str(j))), 2))

                layout_react.add_widget(MDLabel(text=text1, size_hint_y=None, theme_text_color="Custom",
                                                text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                                                font_style="H6"))
            layout.add_widget(layout_react_scroll)
            btn = MDRectangleFlatButton(text='CLOSE', size_hint=(1, .2))
            layout.add_widget(btn)
            btn.bind(on_press=self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title="SUPPPORT REACTIONS", content=layout, size_hint=(.8, .8),
                                        pos_hint={'center_x': .5, 'center_y': .5})
            self.popup_in_popup.open()

        else:
            try:
                self.BEAM.solve_for_reaction_loads(*self.reaction_vars)
            except:
                layout = BoxLayout(orientation='vertical')
                layout.add_widget(MDLabel(text="INSUFFICIENT DATA GIVEN!!", theme_text_color="Custom",
                                          text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                                          font_style="H6"))
                btn = MDRectangleFlatButton(text='CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press=self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title="BEAM UNSTABLE!", content=layout, size_hint=(.7, .4),
                                            pos_hint={'center_x': .5, 'center_y': .5}, )
                self.popup_in_popup.open()
            else:
                layout = BoxLayout(orientation='vertical')
                layout_react = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, None))
                layout_react.bind(minimum_height=layout_react.setter('height'))
                layout_react_scroll = ScrollView(size_hint=(1, .8))
                layout_react_scroll.add_widget(layout_react)
                self.d = self.BEAM.reaction_loads
                for i, j in self.d.items():
                    alphabet, distance = str(i).split('_')
                    if alphabet == 'R':
                        text1 = 'Reaction Force at x = {} m is {} kN'.format(distance, round(float(eval(str(j))), 2))

                    elif alphabet == 'M':
                        text1 = 'Reaction Moment at x = {} m is {} kN*m'.format(distance, round(float(eval(str(j))), 2))

                    layout_react.add_widget(MDLabel(text=text1, size_hint_y=None, theme_text_color="Custom",
                                                    text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                                                    font_style="H6"))
                layout.add_widget(layout_react_scroll)
                btn = MDRectangleFlatButton(text='CLOSE', size_hint=(1, .2))
                layout.add_widget(btn)
                btn.bind(on_press=self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title="SUPPPORT REACTIONS", content=layout, size_hint=(.8, .8),
                                            pos_hint={'center_x': .5, 'center_y': .5})
                self.popup_in_popup.open()

    def popup_shear(self):

        if self.shear_plot_cnt > 0:
            layout = BoxLayout(orientation='vertical')
            layout.add_widget(MDLabel(text="ALREADY PLOTTED", theme_text_color="Custom",
                                      text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                                      font_style="H6"))
            btn = MDRectangleFlatButton(text='CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press=self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title="See in main screen", content=layout, size_hint=(.8, .4),
                                        pos_hint={'center_x': .5, 'center_y': .5})
            self.popup_in_popup.open()
            return

        if self.d:
            self.shear_plot_cnt += 1
            x = symbols('x')
            graph = plot(self.BEAM.shear_force(), (x, 0, self.Len), show=False, title="Shear Force Diagram")
            graph.xlabel = 'length (m)'
            graph.ylabel = 'Shear Force (N)'
            graph.xlim = (float(0), float(self.Len))
            graph.save('./shear.png')
            Menuscreen.add_shear_graph(self.screen)
        else:

            try:
                self.BEAM.solve_for_reaction_loads(*self.reaction_vars)

            except:
                layout = BoxLayout(orientation='vertical')
                layout.add_widget(MDLabel(text="INSUFFICIENT DATA GIVEN!!", theme_text_color="Custom",
                                          text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                                          font_style="H6"))
                btn = MDRectangleFlatButton(text='CLOSE')

                layout.add_widget(btn)
                btn.bind(on_press=self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title="BEAM UNSTABLE!", content=layout, size_hint=(.7, .4),
                                            pos_hint={'center_x': .5, 'center_y': .5})
                self.popup_in_popup.open()
            else:
                self.shear_plot_cnt += 1
                self.d = self.BEAM.reaction_loads
                x = symbols('x')
                graph = plot(self.BEAM.shear_force(), (x, 0, self.Len), show=False, title='Shear Force Diagram')
                graph.xlabel = 'length (m)'
                graph.ylabel = 'Shear Force (N)'
                graph.xlim = (float(0), float(self.Len))
                graph.save('./shear.png')
                Menuscreen.add_shear_graph(self.screen)

    def popup_bending(self):

        if self.bending_plot_cnt > 0:
            layout = BoxLayout(orientation='vertical')
            layout.add_widget(MDLabel(text="MAY NEED TO SCROLL DOWN", theme_text_color="Custom",
                                      text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                                      font_style="H6"))
            btn = MDRectangleFlatButton(text='CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press=self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title="ALREADY PLOTTED !!", content=layout, size_hint=(.8, .4),
                                        pos_hint={'center_x': .5, 'center_y': .5})
            self.popup_in_popup.open()
            return

        if self.d:
            self.bending_plot_cnt += 1
            x = symbols('x')
            graph = plot(self.BEAM.bending_moment(), (x, 0, self.Len), show=False, title='Bending Moment Diagram',
                         xlabel='length (m)', ylabel='Bending Moment (N m)', xlim=(float(0), float(self.Len)))
            graph.save('./bending.png')
            Menuscreen.add_bending_graph(self.screen)
        else:

            try:
                self.BEAM.solve_for_reaction_loads(*self.reaction_vars)

            except:
                layout = BoxLayout(orientation='vertical')
                layout.add_widget(MDLabel(text="INSUFFICIENT DATA GIVEN!!", theme_text_color="Custom",
                                          text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                                          font_style="H6"))
                btn = MDRectangleFlatButton(text='CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press=self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title="BEAM UNSTABLE!", content=layout, size_hint=(.7, .4),
                                            pos_hint={'center_x': .5, 'center_y': .5})
                self.popup_in_popup.open()
            else:
                self.bending_plot_cnt += 1
                self.d = self.BEAM.reaction_loads
                x = symbols('x')
                graph = plot(self.BEAM.bending_moment(), (x, 0, self.Len), show=False, title='Bending Moment Diagram',
                             xlabel='length (m)', ylabel='Bending Moment (N m)', xlim=(float(0), float(self.Len)))
                graph.save('./bending.png')
                Menuscreen.add_bending_graph(self.screen)

    def popup_slope(self):

        if self.slope_plot_cnt > 0:
            layout = BoxLayout(orientation='vertical')
            layout.add_widget(MDLabel(text="MAY NEED TO SCROLL DOWN", theme_text_color="Custom",
                                      text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                                      font_style="H6"))
            btn = MDRectangleFlatButton(text='CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press=self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title="ALREADY PLOTTED !!", content=layout, size_hint=(.8, .4),
                                        pos_hint={'center_x': .5, 'center_y': .5})
            self.popup_in_popup.open()
            return

        if self.d:
            self.slope_plot_cnt += 1
            x = symbols('x')
            graph = plot(self.BEAM.slope(), (x, 0, self.Len), show=False, title='Slope Diagram', xlabel='length (m)',
                         ylabel='Slope', xlim=(float(0), float(self.Len)))
            graph.save('./slope.png')
            Menuscreen.add_slope_graph(self.screen)
        else:

            try:
                self.BEAM.solve_for_reaction_loads(*self.reaction_vars)

            except:
                layout = BoxLayout(orientation='vertical')
                layout.add_widget(MDLabel(text="INSUFFICIENT DATA GIVEN!!", theme_text_color="Custom",
                                          text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                                          font_style="H6"))
                btn = MDRectangleFlatButton(text='CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press=self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title="BEAM UNSTABLE!", content=layout, size_hint=(.7, .4),
                                            pos_hint={'center_x': .5, 'center_y': .5})
                self.popup_in_popup.open()
            else:
                self.slope_plot_cnt += 1
                self.d = self.BEAM.reaction_loads
                x = symbols('x')
                graph = plot(self.BEAM.slope(), (x, 0, self.Len), show=False, title='Slope Diagram',
                             xlabel='length (m)', ylabel='Slope', xlim=(float(0), float(self.Len)))
                graph.save('./slope.png')
                Menuscreen.add_slope_graph(self.screen)

    def popup_deflection(self):

        if self.deflection_plot_cnt > 0:
            layout = BoxLayout(orientation='vertical')
            layout.add_widget(MDLabel(text="MAY NEED TO SCROLL DOWN", theme_text_color="Custom",
                                      text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                                      font_style="H6"))
            btn = MDRectangleFlatButton(text='CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press=self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title="ALREADY PLOTTED !!", content=layout, size_hint=(.8, .4),
                                        pos_hint={'center_x': .5, 'center_y': .5})
            self.popup_in_popup.open()
            return

        if self.d:
            self.deflection_plot_cnt += 1
            x = symbols('x')
            graph = plot(self.BEAM.deflection(), (x, 0, self.Len), show=False, title='Deflection Diagram',
                         xlabel='length (m)', ylabel='Deflection (m)', xlim=(float(0), float(self.Len)))
            graph.save('./deflection.png')
            Menuscreen.add_deflection_graph(self.screen)
        else:

            try:
                self.BEAM.solve_for_reaction_loads(*self.reaction_vars)

            except:
                layout = BoxLayout(orientation='vertical')
                layout.add_widget(MDLabel(text="INSUFFICIENT DATA GIVEN!!", theme_text_color="Custom",
                                          text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                                          font_style="H6"))
                btn = MDRectangleFlatButton(text='CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press=self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title="BEAM UNSTABLE!", content=layout, size_hint=(.7, .4),
                                            pos_hint={'center_x': .5, 'center_y': .5})
                self.popup_in_popup.open()
            else:
                self.deflection_plot_cnt += 1
                self.d = self.BEAM.reaction_loads
                x = symbols('x')
                graph = plot(self.BEAM.deflection(), (x, 0, self.Len), show=False, title='Deflection Diagram',
                             xlabel='length (m)', ylabel='Deflection (m)', xlim=(float(0), float(self.Len)))
                graph.save('./deflection.png')
                Menuscreen.add_deflection_graph(self.screen)

    def popup_sup_and_load(self):

        self.mlayout = BoxLayout(orientation='vertical')
        self.head = MDGridLayout(cols=2, size_hint=(1, .1))
        self.head.add_widget(
            MDLabel(text="SUPPORTS", theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                    font_style="H6"))
        self.head.add_widget(
            MDLabel(text="LOADS", theme_text_color="Custom", text_color=(0, 184.0 / 255.0, 230.0 / 255.0, 1),
                    font_style="H6"))
        self.mlayout.add_widget(self.head)
        self.layout = MDGridLayout(cols=2, size_hint=(1, .8))
        self.layout.add_widget(self.sup_scroll)
        self.layout.add_widget(self.load_scroll)
        self.mlayout.add_widget(self.layout)
        btn = MDRectangleFlatButton(text='CLOSE', size_hint=(1, .1))
        self.mlayout.add_widget(btn)
        btn.bind(on_press=self.dismiss_pop_sup_and_load)
        self.popup_sl = Popup(title="SUPPORTS AND LOADS", content=self.mlayout, size_hint=(.98, .98),
                              pos_hint={'center_x': .5, 'center_y': .5})
        self.popup_sl.open()

        pass

    def dismiss_pop_sup_and_load(self, instance):
        self.layout.remove_widget(self.sup_scroll)
        self.layout.remove_widget(self.load_scroll)
        self.popup_sl.dismiss()

    def popup_newbeam(self):
        del self.BEAM
        self.E = "20"
        self.I = "40"
        self.Len = '10'
        self.reaction_vars = []
        self.d = None
        self.shear_plot_cnt = 0
        self.slope_plot_cnt = 0
        self.bending_plot_cnt = 0
        self.deflection_plot_cnt = 0
        self.loading_plot_cnt = 0

        Menuscreen.remove_graphs(self.screen)

        self.BEAM = Beam(self.Len, self.E, self.I)

        if os.path.exists('./shear.png'):
            os.remove('./shear.png')

        if os.path.exists('./bending.png'):
            os.remove('./bending.png')

        if os.path.exists('./slope.png'):
            os.remove('./slope.png')

        if os.path.exists('./deflection.png'):
            os.remove('./deflection.png')

        if os.path.exists('./loading.png'):
            os.remove('./loading.png')

    def popup_dismiss(self, instance):
        self.popup.dismiss()

    def popup_in_popup_dismiss(self, instance):
        self.popup_in_popup.dismiss()


BeamApp().run()
