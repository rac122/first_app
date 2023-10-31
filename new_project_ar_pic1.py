from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton,MDFloatingActionButton
from kivymd.uix.chip import MDChip
from kivy.clock import Clock
from socket import *
import socket
import os
import time
from kivymd.toast import toast
from datetime import datetime
from datetime import date
from threading import Thread
from kivymd.uix.datatables import MDDataTable
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.pickers import MDTimePicker
from kivymd.uix.screen import MDScreen
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFloatingActionButtonSpeedDial
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image

from kivy.properties import NumericProperty, ListProperty, StringProperty, ObjectProperty
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem,OneLineIconListItem,ThreeLineIconListItem,IconLeftWidget,IconRightWidget,ThreeLineAvatarIconListItem,OneLineAvatarIconListItem
from kivymd.uix.list import ImageLeftWidget,MDList
from kivymd.uix.card import  MDCard
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.boxlayout import BoxLayout
from kivymd.icon_definitions import md_icons
from kivymd.uix.button import MDIconButton
import json

instance_contol = None   # control en cour
list_label_time =[]    # liste de label qui contien conteure  des aumpoules qui marche en temps
list_led=[]            # list des aupoules des controle (in = s1, ..... ) 
etat_led=[]            # list etat the led in micro
list_led_page=[]
#  declaration   variable  socket :
ip = '192.168.3.177'
addresse= (ip,8888)
#clien_socket = socket(AF_INET,SOCK_DGRAM)


class ItemConfirm(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False
class Content(BoxLayout):

    pass
class Content1(BoxLayout):
    
    def __init__(self, **kwargs):
        super(Content1, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = "30dp"
        self.size_hint_y = None
        self.height = "240dp"

        # import data json :::::
        with open('conection.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.text_fields = []
        for key in  data['sorti1']:
            if data['sorti1'][key]==instance_contol:
                container = self.ids.container_led_watt 
                
                #print(instance_contol)

                
                text_field = MDTextField(
                    id=key,
                    hint_text=key,
                    # mode= "rectangle",
                    helper_text="Entrez la valeur en watts de la lampe",
                    helper_text_mode="on_focus",
                    icon_right= "lightbulb-on",
                    icon_right_color= (1,0,0,1),
                    #pos_hint={'center_x': 0.5, 'center_y': 0.5},
                    size_hint_x=None,
                    width=300,
                    color_mode ="custom",
                    current_hint_text_color= (1.0,0,1)

                )
                
                self.text_fields.append(text_field)
                container .add_widget(text_field)
        # print(self.ids.container_led_watt.s1.text)

class ContentNavigationDrawer(MDScrollView):#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty() 
    facture = ObjectProperty() 
class Facturelist(Screen):
    pass
class ContentNavigationDrawer(MDBoxLayout):#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    pass
class MenuScreen(Screen):#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::MenuScreen::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    def show_data(self):
        self.parent.transition.direction = 'right'
        self.parent.current = 'profile'
        self.parent.get_screen('profile').start_page1()
###########################################################################################################################################
# 
# 
#                                                                 class ProfileScreen
# 
# 
##########################################################################################################################################           
class ProfileScreen(Screen):#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::ProfileScreen::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    textinputtext = StringProperty()
    dialog = None
    control_text_in = None
    
    
        #self.textinputtext = 'palim'
    def start_page1(self):
        self.rooms()
    def rooms(self) :
        with open('conection.json', 'r') as json_file:
                data = json.load(json_file)
            
        
        
        j=0 
        test_room_active=0
        list_room_active =[]
        list_index_room_active=[]
        list_index_room_disactive=[]
        list_room_disactive=[]
        # ///////////////////////////////////TEST DES ROOMS ACTIVER ET DESACTIVER ///////////////////////////////////
        for key in  data["control"].keys() :
            if (""  in data["control"][key] ):    
                test_room_active += 1
                list_room_active.append(key)
                list_index_room_active.append(j)   
            else: 
                list_index_room_disactive.append(j)
                list_room_disactive.append(key) 
            j += 1 
            #                                 IF ROOM ACTIVE =   {} or disactive = {}
        if (test_room_active>0 ) :
            #print(list_room_active)         
            #
            # print(list_index_room_active)
            self.show_rooms()
            self.empty_rooms()
        else:
            self.empty_rooms()
        #print(list_room_disactive)
        # print(list_index_room_disactive) 
               
         
        j +=1  
        newData = json.dumps(data, indent=4)      
        with open('conection.json', 'w') as file: 
             # write
            file.write(newData)
                                          
    def BackToStart2(self) :
        pass
    # add rooms active in list item 
    def show_rooms(self):   #::::::::::::::::::::::::::::criee de controls loooooop :::::::::::::::::::
        self.ids.container.clear_widgets()
        
        with open('conection.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        for item in data['control']:
            if (data['control'][item] != "" ):            
            
                item = ThreeLineAvatarIconListItem(IconLeftWidget(
                    
                    icon="./icons/plus.png",
                    icon_size= "35dp",
                    on_press=lambda x: self.add_rooms()
                                    ),     
                                            IconRightWidget(
                    id =  item,                           
                    icon="./icons/supprimer.png",
                    icon_size= "35dp",
                    
                    on_press=lambda x: self.suprime_rooms(x)
                                    ),

                    text="list+str(k)",
                                                                                
                   secondary_text =data['control'][item],
                   tertiary_text = "[size=16][color=#982176]Des contrôlers:[/size]",
                   id=data['control'][item],theme_text_color="Custom",
                   text_color=(1,0,1,1),
                   secondary_theme_text_color="Custom",
                   secondary_text_color=(1,0,1,1),
                   
                   on_press=lambda x: self.get_page2(x))
                
                # item.add_widget(icon2)
                # item.add_widget(icon1)
                self.ids.container.add_widget(item)  
    def set_button_properties(self, button_index, text, position):
        if 0 <= button_index < len(self.buttons):
            self.buttons[button_index].text = text
            self.remove_widget(self.buttons[button_index])
            # self.insert_widget(position, self.buttons[button_index])
            # if empty creat button for edit new rooms
    def empty_rooms(self):
        data = {
            
            "large": {"md_bg_color": "#f8d7e3", "text_color": "#311021"},
        }
        for type_button in data.keys():
            self.ids.container.add_widget(
                MDFloatingActionButton(
                    icon="pencil",
                    type=type_button,
                    pos_hint={"center_x": .5, "center_y": .5},
                    theme_icon_color="Custom",
                    md_bg_color=data[type_button]["md_bg_color"],
                    icon_color=data[type_button]["text_color"],
                    on_press=lambda x: self.add_rooms()
                )
            ) 
    def add_rooms(self):
        with open('conection.json', 'r', encoding='utf-8') as file:
            data = json.load(file) 
        if not self.dialog:
            self.dialog = MDDialog(
                title="Address:",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        on_release=self.dismiss_dialog
                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        on_release=self.get_input_values
                    ),
                ],
            )
        self.dialog.open() 
    def dismiss_dialog(self, instance):
        self.dialog.dismiss()    
    def get_input_values(self, instance):
        content_cls = self.dialog.content_cls
        self.control_text_in = content_cls.ids.control_text_in.text.upper()
        
        if (self.control_text_in==""):
            content_cls.ids.control_text_in.line_color_normal= (1,0,0,1)
            content_cls.ids.control_text_in.helper_text= 'Insere text '
        else:
            with open('conection.json', 'r', encoding='utf-8') as file:
               data = json.load(file)
            desired_item = None 
            list1 = []  
            for item in data['control']:
                if (data['control'][item] == self.control_text_in ):
                    desired_item = item
                    content_cls.ids.control_text_in.line_color_normal= (1,0,0,1)
                    content_cls.ids.control_text_in.helper_text= 'deja existe'
                    #self.add_rooms()
                    # print(item) 
                    
                elif (data['control'][item] == '') :
                   list1.append(item)
                #    print("list1")
            if desired_item is None:
                data['control'][list1[0]]= self.control_text_in.upper()
                #new_item = {'s'+str(len(data['control'])+1): self.control_text_in}
                #data.append(new_item) 
                with open('conection.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                    self.dialog.dismiss()
        self.start_page1()
                  
        # print("City:", self.control_text_in)
    def suprime_rooms(self,conrtrol):
        with open('conection.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        for key in data['sorti1'] :
            if (data['sorti1'][key]==data['control'][str(conrtrol.id)]):
                data['sorti1'][key]="rename"  

        data['control'][str(conrtrol.id)]=""

        with open('conection.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        # print(conrtrol.id) 
        self.start_page1() 
    def get_page2(self,x):
        
        self.parent.transition.direction = 'right'
        self.parent.current = 'upload'
        self.parent.get_screen('upload').start_page2(x.id)  


###########################################################################################################################################
# 
# 
#                                                                 UploadScreen
# 
# 
##########################################################################################################################################                                                  
class UploadScreen(Screen):#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    txt = StringProperty()
    dialog = None
    control_instan=None
    
    def start_page2(self,x):
        global instance_contol
        self.control_instan = x
        self.txt= x
        instance_contol=x
        with open('conection.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        # self.info_portd()  
        # 
        self.led_conrole()  
    

    def show_confirmation_dialog(self, x):
        with open('conection.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
         
            self.dialog = MDDialog(
                title="Phone ringtone",
                type="confirmation",
                items=[
                    ItemConfirm( IconRightWidget(
                                                icon="./icons/led_on.png",
                                                icon_size= "50dp"
                                            ) ,text=key  ) for key in data['sorti1'] if data['sorti1'][key] == x
                    
                ],
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        
                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        
                        on_release=self.get_selected_item
                    ),
                ],
            )
        self.dialog.open()

    def get_selected_item(self, *args):    
        with open('conection.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        selected_item = None
        for item in self.dialog.items:
            if item.ids.check.active:
                selected_item = item.text
                break

        if selected_item:
            print("Selected item:", selected_item)
            if (data['sorti1'][selected_item]=="rename"): # ajouter led ::::
                data['sorti1'][selected_item]= self.control_instan
                #self.led_conrole()                                   # refreche des led controle
            elif (data['sorti1'][selected_item]==self.control_instan ): # suprimer led :::
                data['sorti1'][selected_item]= "rename" 
                #self.led_conrole()                                   # refreche des led controle
            with open('conection.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            self.led_conrole()                                       # refreche des led controle
        else:
            print("No item selected")
        
        self.dialog.dismiss() 
    #:::::::::::::::::::::::::::::::::add led watt ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    # 
    #
    def add_led_watt(self):
        
        with open('conection.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
          
        
            
        # if not self.dialog:
            self.dialog = MDDialog(
                title="Address:",
                type="custom",
                content_cls=Content1(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        on_release=self.dismiss_dialog1
                    ),
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        on_release=self.get_textfield_values1
                    ),
                ],
            )
        self.dialog.open() 
    def dismiss_dialog1(self, instance):
        self.dialog.dismiss()  
    def get_textfield_values1(self, instance):
        with open('conection.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        i=0    
        for key in data['sorti1']  : 
            if data['sorti1'][key]==instance_contol:
               data['watt1'][key]=self.dialog.content_cls.text_fields[i].text
               i +=1 
                
        # first_name = self.dialog.content_cls.text_field[0].id
       # last_name = self.dialog.content_cls.text_fields[1].text
        # print(len(self.dialog.content_cls.text_fields))

        #print(f"First Name: {first_name}")
        #print(f"Last Name: {last_name}")
        # print(f"Email: {first_name}")
                
        with open('conection.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)    
    #
    # 
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!update led control and controle :::::::::::::::::::::::::::
    # 
    # 
    def led_conrole(self): # des aumpoules selectionne pour controler 

        global list_label_time,list_led
        list_label_time=[]  # vider list label time
        list_led=[]         # vider list led chip time
        with open('conection.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        self.ids.container1.clear_widgets()
        self.ids.topupdate.title=instance_contol
                                             #FOR LED STATUS ON OFF INCRIMMENT 1 for index list list_led_page
        i=False
        
        for key in data['sorti1']:
    
            if data['sorti1'][key]==instance_contol:
                b=0 
                

                if len(etat_led) == 0:
                    icon='./icons/led_off.png'
                    print('vide') 
                else:
                    for key2 in etat_led:
                    
                        if key+" = 1"==key2:
                            icon='./icons/led_on.png'
                        elif key+" = 0"==key2:    
                            icon='./icons/led_off.png' 
                    # 
                    
                                                 #incremment 1  
                
                box= MDBoxLayout(orientation= 'vertical',spacing= 10,adaptive_height= True)  
                box_horizontal= MDBoxLayout(orientation= 'horizontal',spacing= 10,adaptive_height= True) 
                screencard = Screen()  
                item = OneLineListItem(text=key ,id=key)
                SLED1 = MDIconButton (icon ="./icons/temperature.png",
                        id = str(key),      
                        icon_size= "50dp")
                SLED2 = MDIconButton (icon ="./icons/chronometre.png",
                        id = str(key),      
                        icon_size= "50dp")
                SLED3 = MDIconButton (icon ="./icons/prise3.png",
                        id = str(key),      
                        icon_size= "50dp")
                chip =MDIconButton(text='rac',
                    icon= icon,#list_led_page[b],#'./icons/led_on.png',
                    icon_size= "80dp",
                    id = str(key),
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                      #icon_right_color=colore1,
                      on_release = lambda x: self.commande_led_interepteur(x)
                    )
                label_time = MDLabel(text="time",
                        id = str(key),             
                        pos_hint={"center_x": 0.5, "center_y": 0.5},
                        halign="center"
                          
                    )
                labelloup1 = MDIconButton(text=" S",icon ="./icons/chronometre.png",
                        id = str(key),      
                        icon_size= "30dp" ,                                       
                        # pos_hint={"center_x": 0.5, "center_y": 0.1},
                                                                #halign="center",
                                                                #allow_selection= True,
                        on_release=lambda x: self.show_time_picker(x)
                                                                
                    ) 
                #chip.
                #screencard.add_widget(chip)
                if i ==False :
                    
                    
                    # sc.add_widget(SLED2)
                    box_horizontal.add_widget(SLED1)
                    box_horizontal.add_widget(SLED2)
                    box_horizontal.add_widget(SLED3)
                    box_horizontal.md_bg_color = [231/255, 203/255,203/255, .5] 
                    
                box.add_widget(box_horizontal)
                box.add_widget(chip)
                box.add_widget(label_time)
                box.add_widget(labelloup1)
                #screencard.add_widget(labelloup)
                #screencard.add_widget(labelloup1)
                                                        
                #box.add_widget(screencard)
                box.add_widget(item)
                #grid.add_widget(box)
                print(b)

                self.ids.container1.add_widget(box)
                list_label_time.append(label_time) # ajouler list wedget label time in list
                list_led.append(chip)              # ajouler list wedget led chip  in list
                i = True
            
    def commande_led_interepteur(self,x):
        with open('conection.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        bin1=[]
        bit=0
        t=len(etat_led)-1
        for key in etat_led:
             
            if x.id in key:
                

                if key == x.id+" = 1":
                    bit=0
                    bin1.append(0)
                    t -=1
                if key == x.id+" = 0":
                    bit=1
                    bin1.append(1)
                    t -=1
                    
            else:
                if "s"+str(t)+" = 1"  in key:
                    bit=1
                    bin1.append(1)
                    t -=1
                    
                if "s"+str(t)+" = 0" in key:
                    bit=0
                    bin1.append(0)
                    t -=1
                    
                    
            
        print(bin1)
        # convert list (self.bin )to bin 
        # 
        
        binary_string = ''.join(map(str, bin1))  # تحويل القائمة إلى سلسلة نصية
        decimal_number = int(binary_string, 2)  # تحويل السلسلة إلى عدد عشري
        binary_representation = bin(decimal_number)  # تحويل العدد العشري إلى رقم ثنائي
        print("الرقم الثنائي الممثل للقائمة هو:", binary_representation) 


        binary_number = int(binary_representation, 2)  # تحويل النص إلى رقم ثنائي
        print("الرقم الثنائي هو:", bin(binary_number))  # طباعة الرقم الثنائي
        print("الرقم العشري هو:", binary_number)  # طباعة الرقم العشري  
        data['portd']= binary_number  

        with open('conection.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)       
        self.led_conrole()


# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(ProfileScreen(name='profile'))
sm.add_widget(UploadScreen(name='upload'))
sm.add_widget(Facturelist(name='factur'))
###########################################################################################################################################
# 
# 
#                                                                 MAIN CLASSE
# 
# 
##########################################################################################################################################

class DemoApp(MDApp):
    
    def build(self):
        self.screen = Builder.load_file('screen_ar_pic1.kv')
    #    ProfileScreen.start_page1(self)
        self.start_thread()
        #self.background_task_reception()
        self.info_portd()
        
        return self.screen 
        
    def background_task_reception(self):
     
        
        try:
                HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
                PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
                s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((HOST, PORT))
                s.listen()
                conn, addr = s.accept()
                
                print(f"Connected by {addr}")
                while DemoApp.get_running_app():
                    data = conn.recv(1024)
                    if not data:
                        print('no data')
                        break
                    conn.sendall(data)
         
            
                
        except KeyboardInterrupt:
            # تم الضغط على Ctrl+C لإيقاف البرنامج
            print("Ctrl+C pressed. Exiting...")
        finally:
            # أغلق المأخذ عند الانتهاء من الحلقة
            # clien_socket.close()
            pass
    def background_task_send(self):
        #i=0 
        global etat_led,list_led_page
        test_if=etat_led
        try :
            
            while DemoApp.get_running_app(): 
                # 
                if etat_led != test_if:
                    UploadScreen.led_conrole() 
                else:
                    etat_led=test_if
                etat_led=self.info_portd() # list {s0 = 1 ,,,}
                if len(list_led) > 0 :
                    
                         
                    list_led_page=[]
                    for list in range(len(list_led)):
                        print(list_led[list].id)      #list des led page[s1,,,,,]
                        #list_label_time[0].text='rac'+str(i) 
                        # 
                        
                       
                
                else:
                    list_led_page=[]
                
                #print(etat_led)   
                                 
                time.sleep(1) 
        except Exception as e :
            print('send data error : ' +str(e))      
        finally:
            # أغلق المأخذ عند الانتهاء من الحلقة
            # clien_socket.close()
            pass
    
    def start_thread(self):
        try:
            thread = Thread(target=self.background_task_send)
            thread.start()
            #thread1 = Thread(target=self.background_task_reception)
            #thread1.start()
            
        except Exception as e :
            print("tread is error : "+ str(e))


    def info_portd(self) : #convert dec to binary and return value of out led name :
        list_etat_led=[]
        j=8                                        # info protD  RETURN
        with open('conection.json', 'r', encoding='utf-8') as file: #convert dec to bin
            data = json.load(file)
        decimal_number = int(data["portd"])


        # تحويل العدد الصحيح إلى النظام الثنائي وطباعته
        binary_number = bin(decimal_number)[2:] # decrimment 2 val in bin 
        binary_number_8_bytes = binary_number.zfill(8) 
        
        for i in binary_number_8_bytes:
             
            #increased_char = chr(j + ord('a')) 
            #print( "s"+str(j)+" = " + str(i)) 
            j-= 1
            list_etat_led.append("s"+str(j)+" = " + str(i))
        return list_etat_led    
        # self.led_conrole()   




    
    
    
if __name__ == '__main__':
    DemoApp().run()        