import kivy
kivy.require('1.11.1')
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.event import EventDispatcher
from kivy.core.window import Window
from kivy.uix.checkbox import CheckBox
from socket import *
from kivy.clock import Clock
from threading import Thread
import threading
import time
import atexit  # استيراد وحدة atexit
import json

from kivy.properties import StringProperty
from datetime import datetime

repet=0
IpAddress=''
ex=''
NombreDeLed=0
but=0    
a=0
but2=0 
but3=0
Controle=''
ConroleAuto=''
data1=""
data2 =""
sorti2=""
sorti3=""
buttonplus=''
deferece=''
z=0
LED=' '
text2=''
with open('new_data.json', 'r') as json_file:
    data = json.load(json_file)
Chomber1 = data['Chomber1']
Chomber2 = data['Chomber2']
Cuisine = data['Cuisine']
Couloire = data['Couloire']
Salon = data['Salon']
Laumpe = data['Laumpe'] 
AddresseIp= data['AdresseIp']   
Port=data['Port']

with open('instance_data.json', 'r') as json_file:
    data = json.load(json_file)
Instance1 = data['Insance1']    
buttonText ='no modifier'
class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        self.menu_bar = BoxLayout(size_hint_y=None, height=100)
        self.text_input = TextInput(hint_text=' Name control')
        self.add_button = Button(text='Add New', on_press=self.on_add_button_press, disabled=True)
        self.remove_button = Button(text='Inc', on_press=self.show_remove_popup, disabled=False)
        self.connect_button = Button(text='Connect', on_press=self.show_settings_popup)
        
        self.menu_bar.add_widget(self.text_input)
        self.menu_bar.add_widget(self.add_button)
        self.menu_bar.add_widget(self.remove_button)
        self.menu_bar.add_widget(self.connect_button)
        
        
        
        self.add_widget(self.menu_bar)
        
        self.label = Label(text='Waiting for updates...',padding=10, size_hint_y=None, height=50, text_size=(None, None))
        
        self.menu_bar.add_widget(self.label)
        
        self.running = True  # متغير للتحكم في الـ loop
        self.start_thread()
        Clock.schedule_interval(self.update_label, 1)  # تحديث الواجهة كل ثانية
        
        self.text_input.bind(text=self.on_text_input_change)
        
        self.checkbox_group = []
        self.button_layout = GridLayout(cols=4, spacing=10, size_hint_y=None)
        self.scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height - 100))
        self.scrollview.add_widget(self.button_layout)
        self.add_widget(self.scrollview)
        
        
        
        self.settings_ip = ''
        self.settings_port = ''    
        # /////////////////////////
    def update_label(self, dt):
        updated_text = f'Updated: {time.ctime()}'
        self.label.text = updated_text
        self.label.text_size = self.label.size  # تعيين حجم النص الحالي
        self.label.set_right
    def start_thread(self):
        thread = Thread(target=self.background_task)
        thread.start()
    def background_task(self):
        while App.get_running_app(): # التأكد من تنفيذ الـ loop فقط إذا كان self.running = True
            print("Performing background task...")
            time.sleep(5)    
    def stop_thread(self):
        self.running = False  # قم بتعيين القيمة إلى False لإنهاء الـ loop
        if self.thread is not None:
            self.thread.join()  # انتظر حتى انتهاء الـ thread
    def background_task(self):
        # هنا يمكنك وضع الكود الخاص بالتواصل عبر الـ socket أو أية عمليات أخرى
        #addresse= (IpAddress,8888)
        
        while App.get_running_app():
            #print("Performing background task...")
            if(IpAddress!=''):
                global a
                a=5
                
                for button in self.button_layout.children:
                    #button_name = button.text
                    #print(button.text)
                    
                    global but3
                    but3=but3+1
                            
                self.add_button.text=str(but3)
            #print(str(but))
            #print(str(a-but))
            if(but3==a):
                self.add_button.disabled = True
            
            else: 
                       
                but3=0
                self.add_button.disabled = False
                 
            but3=0
            global LED  
            self.send_socket_data(LED)
            #for x in range(3):
                        
            if(IpAddress!=IpAddress):
                print('connecte to : '+IpAddress)
                ex=''
                
            else:
                if(IpAddress!=IpAddress):
                    print('not connect to : '+IpAddress)
                    
                    ex=''
            
            #_____________________________________mise ajour de button____________________#
            
            s1 = sorti3.split(" ")
            arrylomp=[Chomber1, Chomber2, Salon,Couloire,Cuisine]
            
            i=0        
            for s in s1:     
                for button in self.button_layout.children: 
                    if(button.text in s):
                         #print ("trouve")
                        for s in s1: 
                            if ( button.text+str(111) in s):
                                #button.text=button.text +' Alummer'
                                button.background_color=(1, 0, 0, 1)
                                for a in arrylomp:
                                    if (a==button.text):
                                        arrylomp[i]=1
                                    i=i+1    
                                 #print ("yess")
                            else:
                                if ( button.text+str(000) in s):
                                    #button.text=button.text +' At'
                                    button.background_color=(0, .5, 1, .6)
                                    for a in arrylomp:
                                        if (a==button.text):
                                            arrylomp[i]=0
                                        i=i+1 
            self.data_json()                 
                
            #time.sleep(0.01) 
            #_______________________________________Data Json Input and Output_________________________________#
    def data_json(self):
        global Chomber2,Chomber1,Couloire,Salon,Laumpe,Cuisine
        new_data = {
            "Chomber1": Chomber1,
            "Chomber2": Chomber2,
            "Cuisine": Cuisine,
            "Couloire": Couloire,
            "Salon": Salon,
            "Laumpe": Laumpe,
            "AdresseIp":"192.168.137.177",
            "Port":8888 ,
            
        }
    
        # كتابة البيانات إلى ملف JSON
        with open('new_data.json', 'w') as json_file:
            json.dump(new_data, json_file)
    
        # قراءة محتوى ملف JSON
        with open('new_data.json', 'r') as json_file:
            data = json.load(json_file)

        # الآن يمكنك الوصول إلى البيانات كما تفعل مع القواميس (dictionaries)
        #global Chomber2,Chomber1,Couloire,Salon,Laumpe,Cuisine
        Chomber1 = data['Chomber1']
        Chomber2 = data['Chomber2']
        Cuisine = data['Cuisine']
        Couloire = data['Couloire']
        Salon = data['Salon']
        Laumpe = data['Laumpe']
        AddresseIp= data['AdresseIp']   
        Port=data['Port']
        

       
        
    def cree_button_auto(self,instance):
        new_button = Button(text='self.text_input.text', on_press=self.show_button_screen,padding=10)
        self.button_layout.add_widget(new_button)
        self.remove_button.disabled = False               
              
    def send_data1(self, instance):
        self.send_socket_data("rac0")

    def send_data2(self, instance):
        self.send_socket_data("rac1")

    def send_data3(self, instance):
        self.send_socket_data("rac2")
    
    def send_socket_data(self, data):
        #addresse=IpAddress
        addresse= (IpAddress,8888)          
        clien_socket = socket(AF_INET,SOCK_DGRAM)
        clien_socket.settimeout(1)
      
        try:
            clien_socket.sendto(data.encode(),addresse)
            rec_data,addr = clien_socket.recvfrom(2028)
            #print(rec_data.decode())
            #global data1
            data1 = rec_data.decode()
            global data2
            global Controle
            
            if(data1 == data2):
                pass
            else:
                #________________________________test buton____________________#
                
                #________________________________end test _______________________#
                data2=data1
                Controle = data1.split(",")
                #print(Controle)
                switch1=True
                for sorti in Controle:
                    if(sorti!="end\r\nstart" and switch1==True):
                        global sorti2
                        sorti2 = sorti2 + sorti + " "
                        #print(sorti) 
                    else:
                        switch1=False 
                    if(sorti!="end\r\n" and switch1==False ) :
                            global sorti3
                            sorti3 = sorti3 + sorti + " "  
                print(sorti2 +"  sorti 2\n")   
                print(sorti3 +"  sorti 3\n")              
        except Exception as e:
            global ex
            if(ex!=e):
               #print(f"Error sending data: {e}") 
               ex=e   
        #//////////////////////////
     
    def on_text_input_change(self, instance, value):
        if value.strip():
            self.add_button.disabled = False
        else:
            self.add_button.disabled = True
                        #_________________________ creat button list ___________________#
    def on_add_button_press(self, instance):
        s1 = sorti2.split(" ")
        global buttonplus
        global ConroleAuto
        for s in s1:
            #print ("premiere i = "+i)
            if(len(self.button_layout.children)==0 ):
                
                ConroleAuto=s1[0]
                
                
                break
            else:
                if( s not in buttonplus):
                 ConroleAuto=s
                   
        if(ConroleAuto!='' and ConroleAuto!=' '):  
            new_button = Button(text=ConroleAuto, on_press=self.show_button_screen,padding=10)            
            self.button_layout.add_widget(new_button)
            self.remove_button.disabled = False
            
        buttonplus=''
        for button in self.button_layout.children:
            #print(button.text)
            buttonplus = buttonplus +" "+ button.text
        
        #print(buttonplus)
        ConroleAuto=''
        

                                  #_____ End to creeate button _____________#
                                  #_______changer button properties______________#
                                  
    def change_button_properties(self, index, **kwargs):
        if 0 <= index < len(self.button_layout.children):
            button = self.button_layout.children[index]
            for key, value in kwargs.items():
                setattr(button, key, value) 
                                  #_____________end change button properties _______________# 
                                                              
                                  #______show list the button to remove ___________________#
        
    def show_remove_popup(self, instance):
        # كود الـ Popup هنا
        if self.button_layout.children:
            popup_content = BoxLayout(orientation='vertical', padding=10)
            self.checkbox_group = []
            
            for button in self.button_layout.children:
                button_name = button.text
                button_checkbox = CheckBox(active=False)
                popup_content.add_widget(button_checkbox)
                popup_content.add_widget(Label(text=button_name))
                self.checkbox_group.append(button_checkbox)
                
            remove_button = Button(text=' Selection Delete', on_press=self.remove_selected_buttons)
            popup_content.add_widget(remove_button)
            
            self.popup = Popup(title=' choisi the controle to deleted', content=popup_content, size_hint=(None, None), size=(400, 400))
            self.popup.open()

            for checkbox in self.checkbox_group:
                checkbox.bind(active=self.update_remove_button_state)
        else:
            popup = Popup(title=' no any controle', content=Label(text=' List void'), size_hint=(None, None), size=(300, 150))
            popup.open()
                                  #____________________________end list button remove _______________________#
                                  
    def update_remove_button_state(self, instance, value):
        if any(checkbox.active for checkbox in self.checkbox_group):
            self.remove_button.disabled = False
        else:
            self.remove_button.disabled = True

    def remove_selected_buttons(self, instance):
        selected_buttons = [button for button, checkbox in zip(self.button_layout.children, self.checkbox_group) if checkbox.active]
        for button in selected_buttons:
            self.button_layout.remove_widget(button)
            #global but2
            #but2=but2+1
        self.popup.dismiss()
        #if(but2>0):
            #self.add_button.disabled = False
            #self.add_button.text=str(a-but2)
        #but2=0
        

    def show_button_screen(self, instance):
        global text2 
        text2=instance.text
        global Instance1
        new_data = {
            "Insance1": instance.text,

                        }
        # كتابة البيانات إلى ملف JSON
        with open('instance_data.json', 'w') as json_file:
            json.dump(new_data, json_file)
        with open('instance_data.json', 'r') as json_file:
            data = json.load(json_file)
        
        # الآن يمكنك الوصول إلى البيانات كما تفعل مع القواميس (dictionaries)
        Instance1 = data['Insance1']
        
        new_screen = ButtonScreen(text1=instance.text)
        App.get_running_app().root.current = 'button_screen'
        App.get_running_app().button_layout = self.button_layout
        App.get_running_app().checkbox_group = self.checkbox_group
        
        
        self.remove_button.disabled=False
    def show_settings_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        ip_input = TextInput(hint_text='IP Address', multiline=False)
        ip_input.text=AddresseIp
        port_input = TextInput(hint_text='Port Number', multiline=False)
        
        confirm_button = Button(text='Confirm', on_press=lambda x: self.save_settings(ip_input.text, port_input.text))
        content.add_widget(ip_input)
        content.add_widget(port_input)
        content.add_widget(confirm_button)

        self.settings_popup = Popup(title='Settings', content=content, size_hint=(None, None), size=(300, 200))
        self.settings_popup.open()

    def save_settings(self, ip, port):
        
        self.settings_ip = ip
        self.settings_port = port
        global IpAddress 
        
        IpAddress = self.settings_ip
        self.settings_popup.dismiss()
        #print(IpAddress)
class ButtonScreen(BoxLayout):
    
    def __init__(self, text1, **kwargs):
        super().__init__(**kwargs)
        #threading.Thread(target=self.refreche).start()
        self.orientation = 'vertical'
        #//////////////////////////////////////////////////////////////////////"""""""
        
        self.menu_bar = BoxLayout(size_hint_y=None, height=100)
        self.text_input = TextInput(hint_text=' Name control')
        self.add_button = Button(text='Add New', on_press=self.on_add_button_press, disabled=True)
        
        
        
        self.menu_bar.add_widget(self.text_input)
        self.menu_bar.add_widget(self.add_button)
        
        
        self.add_widget(self.menu_bar)
        
        self.button_layout = GridLayout(cols=4, spacing=10, size_hint_y=None)
        self.scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height - 100))
        self.scrollview.add_widget(self.button_layout)
        self.add_widget(self.scrollview)
        
   
        ######"""""""""""""""""""""""""""""""""""""""""""""""""""###"""""""""""""""""""""
        
        layout = BoxLayout(orientation='vertical')
        self.label=Label(text=f' no : {text1}')
        layout.add_widget(self.label)
        self.add_widget(layout)
        back_button = Button(text='back', on_press=self.on_back_button_press, size_hint_y=None, height=40)
        layout.add_widget(back_button)
        #Clock.schedule_interval(self.on_add_button_press, 1)  # تحديث الواجهة كل ثانية 
      
    def on_add_button_press(self, instance):
        global repet,deferece
        if (repet <= 5):
            new_button = Button(text=Instance1,padding=10)            
            self.button_layout.add_widget(new_button)    
            repet=repet+1
            deferece=Instance1
            
        if (deferece!=Instance1):
            repet=0    
            
    def test(self) :   
        buttonRef = Button(text=self.text1)
        self.add_widget(buttonRef)
        
       
        #___________________________________________Control  led send data ______________________#
    
     
        
            
     
         
      
                                                    #|_________________________________#|
                                          
    def on_back_button_press(self, instance):
        App.get_running_app().root.current = 'main'
        #for checkbox in App.get_running_app().checkbox_group:
            #checkbox.active = True
                                              
class MyApp(App,EventDispatcher):
    button_layout = None
    checkbox_group = None
    data_to_update = StringProperty("Initial Value")
    def on_back_button_press(self):
            App.get_running_app().root.current = 'main'  
    def update_secondary(self, dt):
        #self.button_layout.clear_widgets()
        self.button_screen.clear_widgets()
        orientation = 'vertical'
        #//////////////////////////////////////////////////////////////////////"""""""
        
        menu_bar = BoxLayout(size_hint_y=None, height=100)
        text_input = TextInput(hint_text=' Name control')
        add_button = Button(text='Add New', disabled=True)
        
        
        
        menu_bar.add_widget(text_input)
        menu_bar.add_widget(add_button)
        
        
        self.button_screen.add_widget(menu_bar)
        
        button_layout = GridLayout(cols=4, spacing=10, size_hint_y=None)
        scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height - 100))
        scrollview.add_widget(button_layout)
        self.button_screen.add_widget(scrollview)
        
   
        ######"""""""""""""""""""""""""""""""""""""""""""""""""""###"""""""""""""""""""""
        
        layout = BoxLayout(orientation='vertical')
        label=Label(text=f' no : {text2}')
        layout.add_widget(label)
        self.button_screen.add_widget(layout)
        back_button = Button(text='back')
        back_button.on_press=on_back_button_press
        back_button.size_hint_y=None
        back_button.height=40
        layout.add_widget(back_button)
        #Clock.schedule_interval(self.on_add_button_press, 1)  # تحديث الواجهة كل ثانية 
      
    def on_add_button_press(self, instance):
        global repet,deferece
        if (repet <= 5):
            new_button = Button(text=Instance1,padding=10)            
            self.button_layout.add_widget(new_button)    
            repet=repet+1
            deferece=Instance1
            
          
        
        
    def build(self):
        
        self.screen_manager = ScreenManager()
        self.main_screen = Screen(name='main')
        self.main_layout = MyBoxLayout()
        self.main_screen.add_widget(self.main_layout)
        
        self.button_screen = Screen(name='button_screen')
        self.button_layout = ButtonScreen(text1=text2)  # تمرير نص فارغ هنا
        self.button_screen.add_widget(self.button_layout)
        
        self.screen_manager.add_widget(self.main_screen)
        self.screen_manager.add_widget(self.button_screen)
        
        #_______________________________des botton ajouter pour test ___________________#
        Clock.schedule_interval(self.update_secondary, 0.8)  # تحديث كل ثانية
        return self.screen_manager
    def update_data(self, instance):
        self.data_to_update = "New Value"  # تحديث القيمة
        
        #______________________________APP__________________end ___________________________#
def on_back_button_press():
    App.get_running_app().root.current = 'main' 
    print('back')  
def on_stop(self):
        self.layout.stop_thread()    
def cleanup():
    #app.layout.stop_thread()
    pass

if __name__ == '__main__':
    app = MyApp()
    app.run()
    atexit.register(cleanup)  # تسجيل الدالة cleanup للتنفيذ عند إغلاق البرنامج
    
