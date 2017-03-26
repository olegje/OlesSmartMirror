# Name_of_file.py
# Requierments.....

from tkinter import *
import locale
import time
import threading
from contextlib import contextmanager
import os, platform
import xml.etree.ElementTree as ET
from urllib import request
from PIL import Image
# import more stuff

# set variables
ole_ip = "192.168.11.103" # Static ip adress on phone
ina_ip = "192.168.11.107"
yr_url = "http://www.yr.no/sted/Norge/Troms/M%C3%A5lselv/Andselv/varsel.xml" # Location spesified url to xml file

#create classes whit all methods
LOCALE_LOCK = threading.Lock() # What is this?


ui_locale = ""
time_format = 24
date_format = "%b %d %Y" 



@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

class Clock(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, bg='black')
        #Frame.config(self, highlightthickness=1)
        # initialize time label
        self.time1 = ''
        self.timeLbl = Label(self, font=('Helvetica', 48), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Helvetica', 18), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E)
        # initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Helvetica', 18), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self):
        with setlocale(ui_locale):
            if time_format == 12:
                time2 = time.strftime('%I:%M %p') #hour in 12h format
            else:
                time2 = time.strftime('%H:%M') #hour in 24h format

            day_of_week2 = time.strftime('%A')
            date2 = time.strftime(date_format)
            # if time string has changed, update it
            if time2 != self.time1:
                self.time1 = time2
                self.timeLbl.config(text=time2)
            if day_of_week2 != self.day_of_week1:
                self.day_of_week1 = day_of_week2
                self.dayOWLbl.config(text=day_of_week2)
            if date2 != self.date1:
                self.date1 = date2
                self.dateLbl.config(text=date2)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            # could use >200 ms, but display gets jerky
            self.timeLbl.after(200, self.tick)

class Home_status(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, bg='black')
        Frame.config(self, highlightthickness=1)
        self.ole_label = Label(self, font=('Helvetica', 20), fg="white", bg="black")
        self.ole_label.pack(side=TOP, anchor=E)
        self.ina_label = Label(self, font=('Helvetica', 20), fg="white", bg="black")
        self.ina_label.pack(side=TOP, anchor=E)
        self.ole_home_status = False
        self.ina_home_status = False
        self.ole_home_str = ""
        self.ina_home_str = ""
        self.refresh()
    def ping(self,host):
    
          #Returns True if host responds to a ping request, works on windows and linux

        if  platform.system().lower()=="windows":
            return os.system("ping -n 1" + " " + host) == 0
        
        else:
            return os.system("sudo ping -c 1 " + str(host)) == 0   
          
    def refresh(self,*args, **kwargs):

        self.ole_home_status = self.ping(ole_ip)
        self.ina_home_status = self.ping(ina_ip)
        
        if self.ole_home_status == True:
            self.ole_home_str = "Ole er hjemme"
        else:
            self.ole_home_str = "Ole er ute"    
        if self.ina_home_status == True:
            self.ina_home_str = "Ina er hjemme"
        else:
            self.ina_home_str = "Ina er ute" 

        self.ole_label.config(text=self.ole_home_str)
        self.ina_label.config(text=self.ina_home_str)
        if self.ole_home_status == True and self.ina_home_status == True:
            #self.ole_label.after(1000, self.refresh)
            self.ina_label.after(180000, self.refresh)
        else:
            #self.ole_label.after(3000, self.refresh)
            self.ina_label.after(3000, self.refresh)


class Wheather_data(Frame):
    def __init__(self, *args, period):
        # all variables here

        self.wind_dir_photo_path = r"C:\Users\Jonny\OneDrive\Documents\Programmer\Oles Smart Mirror\sym\wind_dir\white_arrow.png" #for use on mirror
        #self.wind_dir_photo_path = r"\\NSA325\Nettverkshardisk\Jonny\Programmer\Oles Smart Mirror\sym\wind_dir\white_arrow.png"
        # setup of all the frames
        Frame.__init__(self, background='black')
        #Frame.config(self, highlightthickness=1)
        self.period_frame = Frame(self, bg="black")
        self.period_frame.pack()
        self.label_frame = Frame(self, bg="black")
        self.label_frame.pack(side="right")
        self.icon_frame = Frame(self, bg="black")
        self.icon_frame.pack(side="bottom")
        #Frame.config(self.icon_frame, highlightthickness=1)
        #Frame.config(self.label_frame, highlightthickness=1)
        #Frame.config(self.period_frame, highlightthickness=1)

        #create GUI objets here
        self.period_label = Label(self.period_frame, font=('Helvetica', 20), fg="white", background="black")
        self.period_label.pack()
        self.temp_label = Label(self.label_frame, font=('Helvetica', 20), fg="white", background="black")
        self.temp_label.pack(side=TOP, anchor=E)
        self.precipitation_label = Label(self.label_frame, font=('Helvetica', 20), fg="white", background="black")
        self.precipitation_label.pack(side=TOP, anchor=E)
        self.icon_label = Label(self.icon_frame, bg="black")
        self.icon_label.pack(side=TOP, anchor=W)
        self.wind_dir_label = Label(self.icon_frame, bg="black")
        self.wind_dir_label.pack(side=TOP, anchor=W)
        self.wind_label = Label(self.label_frame, font=('Helvetica', 20), fg="white", background="black")
        self.wind_label.pack(side=TOP, anchor=E)
        self.windmps_label = Label(self.label_frame, font=('Helvetica', 20), fg="white", background="black")
        self.windmps_label.pack(side=TOP, anchor=E)
        self.pressure_label = Label(self.label_frame, font=('Helvetica', 20), fg="white", background="black")
        self.pressure_label.pack(side=TOP, anchor=E)
        

        self.get_wheather_data(period)


    def get_wheather_data(self, period):
        try:
            response = request.urlopen(yr_url)
            contense = response.read()
            self.root = ET.fromstring(contense) #replaces the first object from the XML data
            self.forecast1 = self.get_forecast_data(self.get_period(period)) #Creates a dictonery with the forecast data from the period that is passed in
            #Configure GUI objects
            self.temp_label.config(text=self.forecast1.get("temperature"))
            self.precipitation_label.config(text=self.forecast1.get("precipitation"))
            self.period_label.config(text=self.forecast1.get("from_to_str"))
            self.wind_label.config(text=self.forecast1.get("wind_speed_name"))
            self.windmps_label.config(text=self.forecast1.get("wind_speedmps"))
            self.pressure_label.config(text=self.forecast1.get("pressure"))
            #Symbol icon config
            self.symbol_path = r"C:\Users\Jonny\OneDrive\Documents\Programmer\Oles Smart Mirror\sym\b100\%s.png" %(self.forecast1.get("symbolnumber")) #for use on mirror
            #self.symbol_path = r"\\NSA325\Nettverkshardisk\Jonny\Programmer\Oles Smart Mirror\sym\b100\%s.png" %(self.forecast1.get("symbolnumber"))
            while True:
                try:
                    photo = PhotoImage(file=self.symbol_path)
                    break
                except:
                    self.symbol_path = r"C:\Users\Jonny\OneDrive\Documents\Programmer\Oles Smart Mirror\sym\b100\%sm.png" %(self.forecast1.get("symbolnumber")) #for use on mirror
                    #self.symbol_path = r"\\NSA325\Nettverkshardisk\Jonny\Programmer\Oles Smart Mirror\sym\b100\%sm.png" %(self.forecast1.get("symbolnumber"))
                    photo = PhotoImage(file=self.symbol_path)

            self.icon_label.config(image=photo)
            self.icon_label.image = photo
            #wind direction icon config
            src_image = Image.open(self.wind_dir_photo_path)
            angle = 360 - (int(float(self.forecast1.get("wind_direction"))))
            size = 100, 100
            rotated_image = src_image.rotate(angle, expand=2).resize(size)
            rotated_image.save(r"C:\Users\Jonny\OneDrive\Documents\Programmer\Oles Smart Mirror\sym\wind_dir\current.png") #for use on mirror
            self.wind_dir_path = r"C:\Users\Jonny\OneDrive\Documents\Programmer\Oles Smart Mirror\sym\wind_dir\current.png" #for use on mirror
            #rotated_image.save(r"\\NSA325\Nettverkshardisk\Jonny\Programmer\Oles Smart Mirror\sym\wind_dir\current.png")
            #self.wind_dir_path = r"\\NSA325\Nettverkshardisk\Jonny\Programmer\Oles Smart Mirror\sym\wind_dir\current.png"
            photo2 = PhotoImage(file=self.wind_dir_path) #må få denne til å bruke "rotated_image" istedefor
            #photo2 = PhotoImage(rotated_image)
            self.wind_dir_label.config(image=photo2)
            self.wind_dir_label.image = photo2

            self.period_frame.after(60000, self.get_wheather_data, period)
        except:
            self.period_label.config(text="cannot get weather")
            self.period_frame.after(10000, self.get_wheather_data, period)

    def get_period(self, period):
        forecast = self.root.find("forecast")
        tabular = forecast.find("tabular")
        all_periods = tabular.findall("time")
        current_period = all_periods[period]
        return current_period
    def get_forecast_data(self, period):
        tfrom = period.attrib.get("from")
        tto = period.attrib.get("to")
        from_to_str = tfrom[11:16]+" - "+tto[11:16]
        symbolnumber0 = period.find("symbol").get("numberEx")
        symbolnumber = symbolnumber0.zfill(2)
        precipitation = period.find("precipitation").get("value")+"mm"
        wind_direction = period.find("windDirection").get("deg")
        wind_speed = period.find("windSpeed").get("name")
        wind_speedmps = period.find("windSpeed").get("mps")+"Mps"
        degree_sign = u'\N{DEGREE CELSIUS}'
        temperature = period.find("temperature").get("value")+ degree_sign+"  "
        pressure = period.find("pressure").get("value")
        forecast_data = {"from_to_str": from_to_str, "symbolnumber": symbolnumber, "precipitation": precipitation, "wind_direction": wind_direction,
         "wind_speed_name" : wind_speed, "wind_speedmps": wind_speedmps, "temperature": temperature, "pressure": pressure}
        return forecast_data
class FullscreenWindow:

    def __init__(self): #This sets up the main window and the main frame
        self.tk = Tk()
        self.tk.configure(bg="black")
        self.Frame = Frame(self.tk, background="black")
        self.Frame.pack(fill=BOTH, expand=NO)
        self.tk.attributes("-fullscreen", True)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        #put all the widgets inn here example:
        self.clock = Clock(self.Frame)
        self.clock.pack(side=LEFT, anchor=NW, padx=100, pady=100)
        #self.home_status = Home_status(self.Frame)  #slows down program as of now
        #self.home_status.pack(side=BOTTOM, anchor=SW)
        self.wheather_data1 = Wheather_data(self.Frame, period=0) #Creates a object from the Wheather data and passes in the frame mainwindow
        self.wheather_data1.pack(side=TOP, anchor=NE, padx=100, pady=100)
        self.wheather_data2 = Wheather_data(self.Frame, period=1)
        self.wheather_data2.pack(side=TOP, anchor=NE, padx=100, pady=0)


    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"



if __name__ == "__main__":
    w = FullscreenWindow()
    w.tk.mainloop()







