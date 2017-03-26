# Name_of_file.py
# Requierments.....

import tkinter as tk
from tkinter import *
import locale
import time
import threading
from contextlib import contextmanager
import os, platform
import xml.etree.ElementTree as ET
from urllib import request
from PIL import Image
import queue
import subprocess
import glob
# import more stuff

# set variables / setup
ole_ip = "192.168.11.102" # Static ip adress on phone
ina_ip = "192.168.11.116"
q1 = queue.Queue() # queue to pass variabels between threads
q2 = queue.Queue()
yr_url = "http://www.yr.no/sted/Norge/Troms/M%C3%A5lselv/Andselv/varsel.xml" # Location spesified url to xml file
sun_rise = "m" # "m" if sun never rise "d" if sun rises
ui_locale = ""
time_format = 24
date_format = "%b %d %Y"

#create classes whit all methods
LOCALE_LOCK = threading.Lock() # What is this?


@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

class Clock(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="black")

        #Frame.config(self, highlightthickness=1)
        # initialize time label
        self.time1 = ''
        self.timeLbl = tk.Label(self, font=('Helvetica', 48), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = tk.Label(self, text=self.day_of_week1, font=('Helvetica', 18), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E)
        # initialize date label
        self.date1 = ''
        self.dateLbl = tk.Label(self, text=self.date1, font=('Helvetica', 18), fg="white", bg="black")
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
            self.timeLbl.after(1000, self.tick)

class Home_status(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="black")
        self.ole_label = tk.Label(self, font=('Helvetica', 20), fg="white", bg="black")
        self.ole_label.pack(side=TOP, anchor=E)
        self.ina_label = tk.Label(self, font=('Helvetica', 20), fg="white", bg="black")
        self.ina_label.pack(side=TOP, anchor=E)
        self.ole_home_str = ""
        self.ina_home_str = ""
        self.ole_home_status = False
        self.ina_home_status = False
        self.refresh_GUI()

    def refresh_GUI(self):

        try:
            # get new data if available
            self.ole_home_status = q1.get_nowait()
            q1.task_done()
            self.ina_home_status = q2.get_nowait()
            q2.task_done()
        except:
            pass

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
        self.ina_label.after(2000, self.refresh_GUI)


class Wheather_data(tk.Frame):
    def __init__(self, parent, period):
        tk.Frame.__init__(self, parent, bg="black")

        self.wind_dir_photo_path = "//sym/wind_dir/white_arrow.png" #for use on mirror
        # setup of all the frames
        
        self.period_frame = tk.Frame(self, bg="black")
        self.period_frame.pack()
        self.label_frame = tk.Frame(self, bg="black")
        self.label_frame.pack(side="right")
        self.icon_frame = tk.Frame(self, bg="black")
        self.icon_frame.pack(side="bottom")
        #Frame.config(self.icon_frame, highlightthickness=1)
        #Frame.config(self.label_frame, highlightthickness=1)
        #Frame.config(self.period_frame, highlightthickness=1)

        #create GUI objets here
        self.period_label = tk.Label(self.period_frame, font=('Helvetica', 20), fg="white", background="black")
        self.period_label.pack()
        self.temp_label = tk.Label(self.label_frame, font=('Helvetica', 20), fg="white", background="black")
        self.temp_label.pack(side=TOP, anchor=E)
        self.precipitation_label = tk.Label(self.label_frame, font=('Helvetica', 20), fg="white", background="black")
        self.precipitation_label.pack(side=TOP, anchor=E)
        self.icon_label = tk.Label(self.icon_frame, bg="black")
        self.icon_label.pack(side=TOP, anchor=W)
        self.wind_dir_label = tk.Label(self.icon_frame, bg="black")
        self.wind_dir_label.pack(side=TOP, anchor=W)
        self.wind_label = tk.Label(self.label_frame, font=('Helvetica', 20), fg="white", background="black")
        self.wind_label.pack(side=TOP, anchor=E)
        self.windmps_label = tk.Label(self.label_frame, font=('Helvetica', 20), fg="white", background="black")
        self.windmps_label.pack(side=TOP, anchor=E)
        self.pressure_label = tk.Label(self.label_frame, font=('Helvetica', 20), fg="white", background="black")
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
            self.symbol_path = "/sym/b100/%s.png" %(self.forecast1.get("symbolnumber"))
            while True:
                try:
                    photo = PhotoImage(file=self.symbol_path)
                    break
                except:
                    self.symbol_path = "/sym/b100/%sm.png" %(self.forecast1.get("symbolnumber"))
                    photo = PhotoImage(file=self.symbol_path)

            self.icon_label.config(image=photo)
            self.icon_label.image = photo
            #wind direction icon config
            src_image = Image.open(self.wind_dir_photo_path)
            angle = 360 - (int(float(self.forecast1.get("wind_direction"))))
            size = 100, 100
            rotated_image = src_image.rotate(angle, expand=2).resize(size)
            rotated_image.save("/sym/wind_dir/current.png")
            self.wind_dir_path = "/sym/wind_dir/current.png"
            photo2 = PhotoImage(file=self.wind_dir_path) #må få denne til å bruke "rotated_image" istedefor
            #photo2 = PhotoImage(rotated_image)
            self.wind_dir_label.config(image=photo2)
            self.wind_dir_label.image = photo2

            self.period_frame.after(60000, self.get_wheather_data, period)
        except NameError:
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
        raw_pressure = period.find("pressure").get("value")
        pressure = round(float(raw_pressure))
        forecast_data = {"from_to_str": from_to_str, "symbolnumber": symbolnumber, "precipitation": precipitation, "wind_direction": wind_direction,
         "wind_speed_name" : wind_speed, "wind_speedmps": wind_speedmps, "temperature": temperature, "pressure": pressure}
        return forecast_data

class Pinger(threading.Thread):

    def __init__(self, *args, **kwargs):

        threading.Thread.__init__(self, *args, **kwargs)
        self.daemon = True
    def ping(self, host):

        # Returns True if host responds to a ping request, works on windows and linux

        if platform.system().lower() == "windows":
            try:
                response_str = subprocess.check_output(
                    ['ping', '-n', '3', host],
                    stderr=subprocess.STDOUT,  # get all output
                    universal_newlines=True)  # return string not bytes
            except subprocess.CalledProcessError:
                response_str = "None"
            if "unreachable" in response_str:
                host_status = False
            elif "100% loss" in response_str:
                host_status = False
            else:
                host_status = True
            return host_status

        else:
            return os.system("sudo ping -c 2 " + str(host)) == 0

    def refresh(self):

        ole_home_status = self.ping(ole_ip)
        ina_home_status = self.ping(ina_ip)
        q1.put(ole_home_status)
        q2.put(ina_home_status)


        if ole_home_status == True and ina_home_status == True:
            time.sleep(180)
            self.refresh()
        else:
            time.sleep(3)
            self.refresh()
    def run(self):

         self.refresh()
class Tempratures(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg="black")

        self.label1 = Label(self, text="Rom: 22.3* C", font=('Helvetica', 20), fg="white", bg="black")
        self.label1.pack(side=TOP)
        self.label2 = Label(self, text="CPU: 45.8* C", font=('Helvetica', 20), fg="white", bg="black")
        self.label2.pack(side=TOP)
        self.label3 = Label(self, text="Load: 30%", font=('Helvetica', 12), fg="white", bg="black")
        self.label3.pack(side=TOP)

        #os.system('modprobe w1-gpio')
        #os.system('modprobe w1-therm')
        #base_dir = '/sys/bus/w1/devices/'
        #device_folder = glob.glob(base_dir + '28*')[0]
        #device_file = device_folder + '/w1_slave'

    def read_temp_raw():
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp():
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

#while True:
	#print(read_temp())	
	#time.sleep(1)     
class Widget(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.label1 = Label(self, text="test text")
        self.label1.pack()
class Master_GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        self.attributes("-fullscreen", True)
        self.state = False
        self.bind("<Return>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}


        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self) # creation of frame
            self.frames[F] = frame # puts frame in dictionary
            frame.grid(row=0, column=0, sticky="nsew")
            frame.config(bg="black")
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont] # local variable
        frame.tkraise() # raises frame from self.frames
    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes("-fullscreen", False)
        return "break"


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #Frames inside main frame
        self.right_frame = Frame(self, bg="black")
        self.right_frame.pack(side="right", fill=BOTH, expand=NO,  padx=100, pady=100)
        tk.Frame.config(self.right_frame, highlightthickness=1)
        self.left_frame = Frame(self, bg="black")
        self.left_frame.pack(side="left", fill=BOTH, expand=NO, padx=100, pady=100)
        tk.Frame.config(self.left_frame, highlightthickness=1)




        self.clock = Clock(self.left_frame)
        self.clock.pack(side=TOP, anchor=N, padx=0, pady=0)
        self.home_status = Home_status(self.left_frame)
        self.home_status.pack(side=BOTTOM, anchor=W)
        self.wheather_data1 = Wheather_data(self.right_frame, period=0) #Creates a object from the Wheather data and passes in the frame mainwindow
        self.wheather_data1.pack(side=TOP, anchor=N, padx=0, pady=0)
        self.padding_label = tk.Label(self.right_frame, bg="black")
        self.padding_label.pack(side=TOP, pady=30)
        self.wheather_data2 = Wheather_data(self.right_frame, period=1)
        self.wheather_data2.pack(side=TOP, anchor=N, padx=0, pady=0)
        self.tempratures = Tempratures(self.right_frame)
        self.tempratures.pack(side=BOTTOM, anchor=E)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button3 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button3.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!")
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!")
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()

if __name__ == "__main__":
    app = Master_GUI()
    t1 = Pinger(name="ping_thread")
    t1.start()
    app.mainloop()

