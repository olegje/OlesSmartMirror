import Mirrorbuttons as MB

print("start")
buttonControll = MB.ButtonControll()
try:
    buttonControll.loop()
except KeyboardInterrupt:
    buttonControll.destroy()
