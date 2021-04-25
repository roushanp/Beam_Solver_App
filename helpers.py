screen_helper = """

<MyTile@SmartTileWithStar>
    size_hint_y: None
    height: "240dp"
ScreenManager:
    container: container
    id: scrmgr
    in_class: text
    container: container
    StartScreen:
        id: start
        name: 'start'
        in_class: text
        MDTextField:
            id: text
            hint_text: "Enter username"
            font_size: "25sp"
            helper_text_mode: "on_focus"
            icon_left: 'key-variant'
            icon_right: "keyboard-tab"
            icon_right_color: app.theme_cls.primary_color
            pos_hint:{'center_x': 0.5, 'center_y': 0.5}
            size_hint_x:None
            width:300
        MDRectangleFlatButton:
            text: 'Click here'
            pos_hint: {'center_x':0.5,'center_y':0.4}
            on_press: app.check_print()
    Menuscreen:
        id:menu
        name: 'menu'
        container: container
        NavigationLayout:
            ScreenManager:
                Screen:
                    BoxLayout:
                        orientation: 'vertical'
                        MDToolbar:
                            title: "Beam solver app"
                            elevation: 10
                            left_action_items: [['menu', lambda x: nav_drawer.set_state()]]
                        
                        
                        ScrollView:
                            id: scroll
                            size_hint: None, None
                            size: Window.width, Window.height * .9
                            bar_width: 10
                            bar_color: 1, 0, 0, 1   # red
                            bar_inactive_color: 0, 0, 1, 1   # blue
                            effect_cls: "ScrollEffect"
                            scroll_type: ['bars']
                            
                            MDGridLayout:
                                id: container
                                size_hint_y: None
                                cols: 1
                                adaptive_height: True
                                padding: dp(4), dp(4)
                                spacing: dp(4)
                                
                        Widget:
            MDNavigationDrawer:
                id: nav_drawer
                
                ContentNavigationDrawer:
                    orientation: 'vertical'
                    padding: "8dp"
                    spacing: "8dp"
                    BoxLayout:
                        orientation: 'vertical'
                        Image:
                            id: avatar
                            size_hint: (.6,.6)
                            pos_hint:{'center_x': 0.5, 'center_y': 0.5}
                            source: "author-image.png"
                        MDLabel:
                            text: " Created by Roushan Prakash"
                            font_style: "Subtitle1"
                            size_hint_y: None
                            height: self.texture_size[1]
                        MDLabel:
                            text: "   roushanprakash123@gmail.com"
                            size_hint_y: None
                            font_style: "Caption"
                            height: self.texture_size[1]
                        
                    
                        ScrollView:
    
                            MDList:
                                    
                                OneLineAvatarIconListItem:
                                    text: "sign_conv"
                                    on_release: app.sign_con()
                                    
                                OneLineAvatarIconListItem:
                                    text: "set E, I, and L"
                                    on_release: app.popup_default_value()
                                    
                                OneLineAvatarIconListItem:
                                    text: "Fix"
                                    on_release: app.popup_fix()
                                    
                                OneLineAvatarIconListItem:
                                    text: "Roller"
                                    on_release: app.popup_roller()
                                        
                                OneLineAvatarIconListItem:
                                    text: "Pin"
                                    on_release: app.popup_pin()
                                    
                                OneLineAvatarIconListItem:
                                    text: "Point Load"
                                    on_release: app.popup_vertical()
                                    
                                OneLineAvatarIconListItem:
                                    text: "Moment"
                                    on_release: app.popup_moment()
                                    
                                OneLineAvatarIconListItem:
                                    text: "Distributed Load"
                                    on_release: app.popup_linear()
                                    
                                OneLineAvatarIconListItem:
                                    text: "Linear Ramp"
                                    on_release: app.popup_linear_ramp()
                                    
                                OneLineAvatarIconListItem:
                                    text: "Parabolic Ramp"
                                    on_release: app.popup_parabolic_ramp()
                                OneLineAvatarIconListItem:
                                    text: "Shear Graph"
                                    on_release: app.popup_shear()
                                OneLineAvatarIconListItem:
                                    text: "Bending Graph"
                                    on_release: app.popup_bending()
                                OneLineAvatarIconListItem:
                                    text: "Slope Graph"
                                    on_release: app.popup_slope()
                                OneLineAvatarIconListItem:
                                    text: "Deflection Graph"
                                    on_release: app.popup_deflection()
                                OneLineAvatarIconListItem:
                                    text: "Loading Graph"
                                    on_release: app.popup_loading()
                                OneLineAvatarIconListItem:
                                    text: "Reaction Loads"
                                    on_release: app.popup_reaction()
                                OneLineAvatarIconListItem:
                                    text: " Supports and Loads"
                                    on_release: app.popup_sup_and_load()
                                OneLineAvatarIconListItem:
                                    text: "New Beam"
                                    on_release: app.popup_newbeam()
                           
"""

