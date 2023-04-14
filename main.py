from kivy.config import Config
Config.set('kivy','log_dir','/storage/emulated/0/.kivy/logs')
from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.card import MDCard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.icon_definitions import md_icons
from kivy.utils import get_color_from_hex
from datetime import date,datetime
from kivy.uix.scrollview import ScrollView
from kivymd.uix.datatables import MDDataTable,CellHeader
from kivy.metrics import dp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRaisedButton
import threading
import asyncio

#from firebase_admin import credentials,auth,db
from kivy.core.window import Window
from kivy.properties import NumericProperty,ObjectProperty,StringProperty
import pickle
import os
from kivymd.uix.label import MDLabel
from kivy.app import App
from kivymd.toast import toast
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.utils import rgba
import smtplib
#import requests
import json
import re
import sys
#----------Error--------
# for python >=10 --->[from collections.abc import MutableMapping ] for python <=3.9 ------>[from collections import MutableMapping]
import pyrebase
print(dir(pyrebase))


# outside of the class id getting
#home_screen = HomeScreen()
#toolbar_widget = home_screen.ids.toolbar

'''
here the outside of the id accessing
class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.my_button.text = "Click me"

class MyWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.my_box.add_widget(Button(id="my_button"))

my_window = MyWindow()
my_button = my_window.ids.my_box.ids.my_button
'''
Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
Window.softinput_mode = "below_target"

#auth='kyhXIS9w7Zu1j80j7SgG1ElflTWis0KLGr4YkMd4'

class HomeScreen(Screen):
    from_date=StringProperty()
    to_date=StringProperty()

    


    def fromdate_save(self, instance, value, date_range):
        '''
        :type instance: <kivymd.uix.picker.MDDatePicker object>;

        :param value: selected date;
        :type value: <class 'datetime.date'>;

        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''
        
        self.from_date=value.strftime("%d-%m-%Y")
        


    def on_cancel(self, instance, value):
        pass
        '''Events called when the "CANCEL" dialog box button is clicked.'''
    def show_from_date(self):
        toast('Please Wait...')
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.fromdate_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def todate_save(self, instance, value, date_range):
        '''
        :type instance: <kivymd.uix.picker.MDDatePicker object>;

        :param value: selected date;
        :type value: <class 'datetime.date'>;

        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''
        self.to_date=value.strftime("%d-%m-%Y")

    def on_cancel(self, instance, value):
        pass
        '''Events called when the "CANCEL" dialog box button is clicked.'''
    def show_to_date(self):
        toast('Please Wait...')
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.todate_save, on_cancel=self.on_cancel)
        date_dialog.open()


class Content(BoxLayout):
    pass

class Screen2(Screen):
    pass

class Welcome_Screen(Screen):
    pass

class Login_Screen(Screen):
    pass

class Sign_Up(Screen):
    pass

class First_Screen(Screen):
    pass

class Tab(MDFloatLayout, MDTabsBase):
    pass


class WindowManager(ScreenManager):
    pass

class ContentNavDrawer(BoxLayout):
    pass

#buy_amount  id for buy tab label
#sell_amount  id for sell tab label
#buy_value id for home tab
#sell_value id for home tab
#profit_value id for home tab
#loss_value id for home tab

class TestApp(MDApp):
    dialog = None
    dialog2 = None
    buy_amount = StringProperty()
    sell_amount = StringProperty()
    set_buyamount=StringProperty()
    set_sellamount=StringProperty()
    profit=StringProperty()
    loss=StringProperty()

     #Define some data to store
    price_dict = {"buy_amount":0,"sell_amount":0}



    def build(self): 
        self.kv=Builder.load_file("kvfile.kv")       
        return  self.kv
   
    def on_start(self):
        login_file=os.path.isfile('./account.json')
        if login_file is True:
            with open('account.json','r+') as file:
                data=json.load(file)
            for key in data:
                json_user=data[key]

            self.root.get_screen('home').ids.nav_name.text=str(json_user['Name'])
            self.root.get_screen('home').ids.nav_email.text=str(key)
            self.check_func(0.1)
            self.root.current='home'           
            
                
        else:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE]) 
            self.root.current='first'

        
        

        
        

#---------------------------table1--------------------------------------------------
    def show_confirmation_dialog(self):          # for tabel 1
        if not self.dialog:
            self.dialog = MDDialog(
                title="Add Product:",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color,on_release=lambda x:self.dialog.dismiss(force=True)
                    ),
                    MDRaisedButton(
                        text="ADD", on_release=self.submit_dialog
                    ),
                ],
            )
        self.dialog.open()
        self.dialog.content_cls.ids.item.text=' '
        self.dialog.content_cls.ids.price.text=' '

    def submit_dialog(self, instance):
        current=datetime.now()
        current_date = str(datetime.today().strftime("%d-%m-%Y %H:%M:%S"))
        
        dateformat=current.strftime("%d/%m/%Y %H:%M:%S")
        item_value = self.dialog.content_cls.ids.item.text
        price_value = self.dialog.content_cls.ids.price.text

        # Create a thread to run the save_file function
        save_thread = threading.Thread(target=self.add_data,args=(dateformat,item_value,price_value))
        save_thread.start()

        filesave_thread = threading.Thread(target=self.buyfile,args=(dateformat,item_value,price_value))
        filesave_thread.start()

        # Use asyncio to run the send_file_to_server function asynchronously
        asyncio.set_event_loop(asyncio.new_event_loop()) # Create a new event loop
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_send_data(dateformat,item_value,price_value,current_date))
        loop.close()
        #self.total_buy(price=price_value)
        self.dialog.dismiss(force=True)
        print("All tasks completed")


    def add_data(self,dateformat,item_value,price_value):
        
        row_datas=(item_value, dateformat, price_value)  
        print(row_datas)    
        datalayout1=self.root.get_screen('home').ids.table1_row
        Clock.schedule_once(lambda dt:datalayout1.add_widget(MDLabel(text=str(price_value), halign='center'),len(datalayout1.children)),0)
        Clock.schedule_once(lambda dt:datalayout1.add_widget(MDLabel(text=str(dateformat), halign='center'),len(datalayout1.children)),0)
        Clock.schedule_once(lambda dt:datalayout1.add_widget(MDLabel(text=str(item_value), halign='center'),len(datalayout1.children)),0)
        #Clock.schedule_once(lambda dt: self.root.get_screen('home').ids.table1_row._trigger_layout())
    def buyfile(self,dateformat,item_value,price_value):
       
        print(price_value)
        buy_file=os.path.isfile('total_buy.txt')
        if buy_file is True:
            data=None
            with open('total_buy.txt', 'r') as f:
               data = f.read()
            print('file data',data)
            totalbuy=int(price_value)+int(data)
            with open('total_buy.txt','w') as file:
                file.write(str(totalbuy))
            self.root.get_screen('home').ids.label1.text=f"Today's Buy: {totalbuy}"
        else:
            with open('total_buy.txt','w') as file1:
                file1.write(str(price_value))
            self.root.get_screen('home').ids.label1.text=f"Today's Buy: {price_value}"




 




    async def run_send_data(self, dateformat,item_value,price_value,current_date):
        # Call the send_data function and wait for it to complete
        await self.send_data(dateformat,item_value,price_value,current_date)


    async def send_data(self,dateformat,item_value,price_value,current_date):
        # Function to send the file to a server asynchronously
        only_date= str(datetime.today().strftime("%d-%m-%Y"))
        # Initialize Firebase with a service account
        client_email=(str(self.root.get_screen('home').ids.nav_email.text)).replace('.','-')
        
        self.initialize_func()
        
        # Define the JSON data to be saved
        data = {
            "Item": item_value,
            "Date&Time": dateformat,
            "Price": price_value,
            "Date" : only_date
        }

        # Get a reference to the Firebase Realtime Database root
        ref = self.firebase.database()
        ref.child('Buy').child(client_email).child(current_date).set(data)


        # Set the JSON data at the root reference
        
       
        
        await asyncio.sleep(1) # Simulate a network delay
        print("File sent to server")



# -------------------- tabel 2 function -------------------------

    def show_confirmation_dialog2(self):          # for tabel 2
        if not self.dialog2:
            self.dialog2= MDDialog(
                title="Add Product:",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color,on_release=lambda x:self.dialog2.dismiss(force=True)         
                    ),
                    MDRaisedButton(
                        text="ADD", on_release=self.submit_dialog2
                    ),
                ],
            )
        self.dialog2.open()
        self.dialog2.content_cls.ids.item.text=' '
        self.dialog2.content_cls.ids.price.text=' '

    def submit_dialog2(self, instance):
        current=datetime.now()
        current_date = str(datetime.today().strftime("%d-%m-%Y %H:%M:%S"))
        
        dateformat=current.strftime("%d/%m/%Y %H:%M:%S")
        item_value = self.dialog2.content_cls.ids.item.text
        price_value = self.dialog2.content_cls.ids.price.text

        # Create a thread to run the save_file function
        save_thread = threading.Thread(target=self.add_data2,args=(dateformat,item_value,price_value))
        save_thread.start()
        file_save_thread = threading.Thread(target=self.sellfile,args=(dateformat,item_value,price_value))
        file_save_thread.start()
        # Use asyncio to run the send_file_to_server function asynchronously
        asyncio.set_event_loop(asyncio.new_event_loop()) # Create a new event loop
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_send_data2(dateformat,item_value,price_value,current_date))
        loop.close()
        #self.total_sell(price=price_value)
        self.dialog2.dismiss(force=True)
        print("All tasks completed")

    def add_data2(self,dateformat,item_value,price_value):
        
        rowdata=(item_value, dateformat, price_value)  
            
        datalayout2=self.root.get_screen('home').ids.table2_row
        Clock.schedule_once(lambda dt:datalayout2.add_widget(MDLabel(text=str(price_value), halign='center'),len(datalayout2.children)),0)
        Clock.schedule_once(lambda dt:datalayout2.add_widget(MDLabel(text=str(dateformat), halign='center'),len(datalayout2.children)),0)
        Clock.schedule_once(lambda dt:datalayout2.add_widget(MDLabel(text=str(item_value), halign='center'),len(datalayout2.children)),0)
    
    def sellfile(self,dateformat,item_value,price_value):
        sell_file=os.path.isfile('total_sell.txt')
        if sell_file is True:
            data=None
            with open('total_sell.txt', 'r') as f:
               data = f.read()
            totalsell=int(price_value)+int(data)
            with open('total_sell.txt','w') as file:
                file.write(str(totalsell))
            self.root.get_screen('home').ids.label2.text=f"Today's Sell: {totalsell}"    
        else:
            with open('total_sell.txt','w') as file1:
                file1.write(str(price_value))
            self.root.get_screen('home').ids.label1.text=f"Today's Buy: {price_value}"

    async def run_send_data2(self, dateformat,item_value,price_value,current_date):
        # Call the send_data function and wait for it to complete
        await self.send_data2(dateformat,item_value,price_value,current_date)


    async def send_data2(self,dateformat,item_value,price_value,current_date):
        # Function to send the file to a server asynchronously
        only_date= str(datetime.today().strftime("%d-%m-%Y"))
        # Initialize Firebase with a service account
        #if not firebase_admin._apps:
            #cred=credentials.Certificate('serviceAccountKey.json')
            #firebase_admin.initialize_app(cred, {'databaseURL': "https://user-data-39d9f-default-rtdb.firebaseio.com/"})
        client_email2=(str(self.root.get_screen('home').ids.nav_email.text)).replace('.','-')

        self.initialize_func()
        # Define the JSON data to be saved
        data = {
            "Item": item_value,
            "Date&Time": dateformat,
            "Price": price_value,
            "Date" : only_date


        }

        # Get a reference to the Firebase Realtime Database root
        ref = self.firebase.database().child('Sell').child(client_email2)


        # Set the JSON data at the root reference
        users_ref = ref.child(current_date)
        users_ref.set(data)
        
        await asyncio.sleep(1) # Simulate a network delay

        print("File sent to server")
        
    

#--------------------- table1 retrive function ----------------------------------------

    async def retrivefunc(self):
        #if not firebase_admin._apps:
            #cred=credentials.Certificate('serviceAccountKey.json')
            #firebase_admin.initialize_app(cred, {'databaseURL': "https://user-data-39d9f-default-rtdb.firebaseio.com/"})
        client_email=(str(self.root.get_screen('home').ids.nav_email.text)).replace('.','-')
        self.initialize_func()
        # Get a database reference to our posts
        ref = self.firebase.database().child('Buy').child(client_email)
        # Read the data at the posts reference (this is a blocking operation)
        obj_data=(ref.get())
        data=obj_data.val()
        
        #print(data.val())
        #print(data.key())
        if data:
            print(data)
        else:
            print("No data found in Sell node.")
        date_now = str(datetime.today().strftime("%d-%m-%Y"))
        
        datalayout1=self.root.get_screen('home').ids.table1_row
        datalayout1.clear_widgets()
        # self.table1.row_data.append(('','No data found',''))
        total=0
        if (data != None):
            if ((len(data)) != 0):          
                for key in data:                   
                    if date_now in key:                         
                        value2=data[key]['Date&Time']
                        value1=data[key]['Item']
                        value3=data[key]['Price']
                        #print(value1,value2,value3)
                        data_row=(value1, value2, value3)
                                                                         
                        print(data_row)
                        total+=int(value3)                                              
                        
                        datalayout1.add_widget(MDLabel(text=str(value1), halign='center'))
                        datalayout1.add_widget(MDLabel(text=str(value2), halign='center'))
                        datalayout1.add_widget(MDLabel(text=str(value3), halign='center'))
        print(total)
        self.root.get_screen('home').ids.label1.text=f"Today's Buy: {total}"
        sell_file=os.path.isfile('total_buy.txt')
        if sell_file is True:
            data=None
            with open('total_buy.txt', 'r') as f:
               data = f.read()
                                        
            with open('total_buy.txt','w') as file:
                file.write(str(total))
            print("tab change ",total)
            

        else:
            with open('total_buy.txt','w') as file1:
                file1.write(str(total))
    	

            
            
            
            	   

    #def clear_table(self):
#        self.table1.row_data.clear()

    async def run_get_data(self):
        # Call the send_data function and wait for it to complete
        await self.retrivefunc()

#---------------------------------------------- table2 retrive function ----------------------------------------------------    
    async def retrivefunc2(self):
        #if not firebase_admin._apps:
            #cred=credentials.Certificate('serviceAccountKey.json')
            #firebase_admin.initialize_app(cred, {'databaseURL': "https://user-data-39d9f-default-rtdb.firebaseio.com/"})
        client_email2=(str(self.root.get_screen('home').ids.nav_email.text)).replace('.','-')
        self.initialize_func()
        # Get a database reference to our posts
        ref = self.firebase.database().child('Sell').child(client_email2)#.child(client_email2)  #db.reference('/Sell/')
        # Read the data at the posts reference (this is a blocking operation)
        
        # Read the data at the posts reference
        obj_data=(ref.get())
        data=obj_data.val()
        
        #print(data.val())
        #print(data.key())
        if data:
            pass#print(data)
        else:
            print("No data found in Sell node.")


        date_now = str(datetime.today().strftime("%d-%m-%Y"))
        
        datalayout2=self.root.get_screen('home').ids.table2_row
        datalayout2.clear_widgets()
        #self.table2.row_data.append(('','No data found','')) 
        total=0
        if (data != None):
            if ((len(data)) != 0):          
                for key in data:                   
                    if date_now in key:                         
                        value2=data[key]['Date&Time']
                        value1=data[key]['Item']
                        value3=data[key]['Price']
                        #print(value1,value2,value3)
                        data_row=(value1, value2, value3)
                        total+=int(value3)                                              
                        print(data_row)
                        datalayout2.add_widget(MDLabel(text=str(value1), halign='center'))
                        datalayout2.add_widget(MDLabel(text=str(value2), halign='center'))
                        datalayout2.add_widget(MDLabel(text=str(value3), halign='center'))
        print(total)
        self.root.get_screen('home').ids.label2.text=f"Today's Sell: {total}"
        sell_file=os.path.isfile('total_sell.txt')
        if sell_file is True:
            #data=None
            #with open('total_sell.txt', 'r') as f:
               #data = f.read()
            
                               
            with open('total_sell.txt','w') as file:
                file.write(str(total))

        else:
            with open('total_sell.txt','w') as file1:
                file1.write(str(total))
        
                          		        		           		   
                		
        
        
    async def run_get_data2(self):
        # Call the send_data function and wait for it to complete
        await self.retrivefunc2() 


#----------home screen data update--------------------------------------
        


    def check_func(self,t):
        buy_file=os.path.isfile('total_buy.txt')
        sell_file=os.path.isfile('total_sell.txt')
        if buy_file is True:
            data=None
            with open('total_buy.txt', 'r') as f:
               data = f.read()
            self.root.get_screen('home').ids.buy_value.text=str(data)
        else:
            print('file not found')
            self.root.get_screen('home').ids.buy_value.text="0"

        if sell_file is True:
            data2=None
            with open('total_sell.txt', 'r') as file:
               data2 = file.read()
            print(data2)
            self.root.get_screen('home').ids.sell_value.text=str(data2)
        else:
            print('file not found')
            self.root.get_screen('home').ids.sell_value.text="0"



         #checking profit & loss
        #buy_value=(self.root.get_screen('home').ids.buy_value.text)
        #sell_value=(self.root.get_screen('home').ids.sell_value.text)
        #print("buy:",(buy_value))
        # Extract only digits from the strings
        #buy_value = re.sub(r'\D', '', buy_value1)
        #sell_value = re.sub(r'\D', '', sell_value2)



        sellvalue=self.root.get_screen('home').ids.sell_value.text
        buyvalue=self.root.get_screen('home').ids.buy_value.text
        value = int(sellvalue) - int(buyvalue)
        
        
        if value < 0:
            #self.root.get_screen('home').ids.profit_value.text=''
            self.root.get_screen('home').ids.profit_value.text='0'
            #self.root.get_screen('home').ids.sell_value.text=''
            self.root.get_screen('home').ids.loss_value.text=str(value)

        elif value==0:
            #self.root.get_screen('home').ids.profit_value.text=''
            self.root.get_screen('home').ids.profit_value.text='0'
            #self.root.get_screen('home').ids.sell_value.text=''
            self.root.get_screen('home').ids.loss_value.text='0'

        else:
            #self.root.get_screen('home').ids.profit_value.text=''
            self.root.get_screen('home').ids.profit_value.text=str(value)
            #self.root.get_screen('home').ids.sell_value.text=''
            self.root.get_screen('home').ids.loss_value.text='0'
            
            
    def download_data(self,time):
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_get_data())
        loop.close()
        
        print("All tasks completed")
    def download_data2(self,time):
        asyncio.set_event_loop(asyncio.new_event_loop()) # Create a new event loop
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_get_data2())
        loop.close()
        #self.total_sell()
        print("All tasks completed")
        
        
        
        

        





#--------------------- on tab switch -----------------------------------------------------
    
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
  
        if (instance_tab.title == "BUY"):
            
            #save_thread = threading.Thread(target=self.clear_table)
#            save_thread.start()

            
            
            Clock.schedule_once(self.download_data,0.1)           
            

        elif (instance_tab.title == "SELL"):
            # Create a thread to run the save_file function
            #save_thread = threading.Thread(target=self.clear_table2)
#            save_thread.start()

            # Use asyncio to run the send_file_to_server function asynchronously
            Clock.schedule_once(self.download_data2,0.1) 
            
        else:
            Clock.schedule_once(self.check_func,0.1)
            

#---------------check records function------------------------------------------

    def check_record(self):
        form_date=(self.root.get_screen('home').ids.fromdate.text)  
        to_date=(self.root.get_screen('home').ids.todate.text)
        # convert date strings to Unix timestamps
        print(form_date)
        #form_timestamp = str(form_date.strftime("%d-%m-%Y"))
        #to_timestamp =str(to_date.strftime("%d-%m-%Y"))
        datalayout=self.root.get_screen('home').ids.data_layout
        switch_id1=self.root.get_screen('home').ids.switch1
        switch_id2=self.root.get_screen('home').ids.switch2
        user_mail=(str(self.root.get_screen('home').ids.nav_email.text)).replace(".", "-")
        if switch_id2.active==True:
            #if not firebase_admin._apps:
                #cred=credentials.Certificate('serviceAccountKey.json')
                #firebase_admin.initialize_app(cred, {'databaseURL': "https://user-data-39d9f-default-rtdb.firebaseio.com/"})
            self.initialize_func()
            ref = self.firebase.database().child('Sell').child(user_mail)#db.reference('/Sell/')
            # Read the data at the posts reference (this is a blocking operation)
            obj_data=ref.order_by_child('Date').start_at(form_date).end_at(to_date).get()
            data=obj_data.val()
            print(data)
            print(obj_data)
            datalayout.clear_widgets()
            for key, value in data.items():      
                datalayout.add_widget(MDLabel(text=str(value["Item"]), halign='center'))
                datalayout.add_widget(MDLabel(text=str(value["Date&Time"]), halign='center'))
                datalayout.add_widget(MDLabel(text=str(value["Price"]), halign='center'))

        else:
            #if not firebase_admin._apps:
                #cred=credentials.Certificate('serviceAccountKey.json')
                #firebase_admin.initialize_app(cred, {'databaseURL': "https://user-data-39d9f-default-rtdb.firebaseio.com/"})
            self.initialize_func()
            ref = self.firebase.database().child('Buy').child(user_mail)  #db.reference('/Buy/')
            # Read the data at the posts reference (this is a blocking operation)
            obj_ref=ref.order_by_child('Date').start_at(form_date).end_at(to_date).get()
            data=obj_ref.val()
            datalayout.clear_widgets()
            for key, value in data.items():
                datalayout.add_widget(MDLabel(text=str(value["Item"]), halign='center'))
                datalayout.add_widget(MDLabel(text=str(value["Date&Time"]), halign='center'))
                datalayout.add_widget(MDLabel(text=str(value["Price"]), halign='center'))

        
    def back_func(self):
        if self.root.current=="about":
            self.root.current="home"
        else:
            self.root.current="about"

        






        
        
        #self.table2.row_data.append(('','No data found','')) 
        #if (data != None):
            #if ((len(data)) != 0):
                #for key in data:
                    #if date_now in key:
                        #value2=data[key]['Date&Time']
                        #value1=data[key]['Item']
                        #value3=data[key]['Price']
                        #print(value1,value2,value3)
                        
                        #data_row=(value1, value2, value3)                                                  
                        #self.table2.row_data.append(data_row)
        

    def current_slide(self,index):
        for i in range(3):
            if index ==i:
                self.root.get_screen('first').ids[f'slide{index}'].color=rgba(253,140,95,255)
            else:
                self.root.get_screen('first').ids[f'slide{i}'].color=rgba(235,237,240,255)
    def next(self):
        self.root.get_screen('first').ids.carousel.load_next(mode="next")

    def signup_func(self):                         
        name=self.root.get_screen('sign_up').ids.reg_name.text
        email=self.root.get_screen('sign_up').ids.reg_email.text
        password=self.root.get_screen('sign_up').ids.reg_password.text
        # Only allow valid Gmail addresses
        if ( re.match(r'^[a-zA-Z0-9._%+-]+@gmail\.com$', email)) != None:
            if len(password) >=6:

                self.initialize_func()
                try:
                    pyrebase_auth=self.firebase.auth()
                    user_info=pyrebase_auth.create_user_with_email_and_password(email, password)
                    # Set the user's display name
                    pyrebase_auth.update_profile(user_info['idToken'],display_name=name,)
                    send_email=pyrebase_auth.send_email_verification(user_info['idToken'])
                    toast("Sending Email Verification Link")
                    self.root.get_screen('sign_up').ids.reg_name.text=''
                    self.root.get_screen('sign_up').ids.reg_email.text=''
                    self.root.get_screen('sign_up').ids.reg_password.text=''
                    self.root.current='login'    
                except Exception as er:
                    self.root.get_screen('sign_up').ids.reg_name.text=''
                    self.root.get_screen('sign_up').ids.reg_email.text=''
                    self.root.get_screen('sign_up').ids.reg_password.text=''
                    toast("Email already exist! Please login...") 
                    print(er)
            else:
                toast("Please enter password more than 6 charecters") 
        else:
            toast('Please enter only Google Mail Id') 


        
        
    def login_func(self):
        user_email=self.root.get_screen('login').ids.user_email.text
        user_password=self.root.get_screen('login').ids.user_password.text
        # Only allow valid Gmail addresses
        if ( re.match(r'^[a-zA-Z0-9._%+-]+@gmail\.com$', user_email)) != None:
            
            if len(user_password) >=6:
      
                self.initialize_func()
                             

                self.auth_email=None
                try:
                    pyrebase_auth=self.firebase.auth()
                    user = pyrebase_auth.sign_in_with_email_and_password(user_email, user_password)

                	# Get information about the current user
                    user_details = pyrebase_auth.get_account_info(user["idToken"])
                    print(user_details)
                    # Check if the user's email is verified
                    email_verified = user_details["users"][0]["emailVerified"]

                    
                   
                    if email_verified:
                        print("Email verification complete!")
                        #toast("Email verification complete!")
                        self.auth_email=user
                        # Access the display name field of the user data
                        display_name = user_details["users"][0]["displayName"]
                        self.root.get_screen('home').ids.nav_name.text=str(display_name)
                        self.root.get_screen('home').ids.nav_email.text=str(user_email)
                        with open('account.json','w+') as user_file:            
                            user_file.write('{"'+str(user_email)+'"'+':{"Name":'+'"'+display_name+'"'+',"Password":'+'"'+user_password+'"'+'}}')                           
                        
                        self.root.current='home'
                    else:
                        toast('Please varify your Email!...')
                    
                except Exception as er:
                    self.root.get_screen('login').ids.user_email.text=''
                    self.root.get_screen('login').ids.user_password.text=''
                    toast('Please Enter Valid Email Address...')
                    print(er)
            else:
                toast("Please enter password more than 6 charecters")
        else:
            toast('Please enter only Google Mail Id')	
        
    def initialize_func(self):
        config={'apiKey': "AIzaSyD831yLZwF8d_Hw9qktC3AG7eHlto7zI8M",
  	  'authDomain': "user-data-39d9f.firebaseapp.com",
        'databaseURL': "https://user-data-39d9f-default-rtdb.firebaseio.com",
        'projectId': "user-data-39d9f",
        'storageBucket': "user-data-39d9f.appspot.com",
        'messagingSenderId': "864339125441",
        'appId': "1:864339125441:web:d4210e06cd6ed59323e040",
        'measurementId': "G-PL70R27DMX",
        "serviceAccount": "serviceAccountKey.json"}
        self.firebase = pyrebase.initialize_app(config)
        
    
    



 
if __name__ == '__main__':
    LabelBase.register(name='semi_poppins',
                       fn_regular='Poppins-SemiBold.ttf')

    LabelBase.register(name='mid_poppins',
                       fn_regular='Poppins-Medium.ttf')
    TestApp().run()



 