from gpiozero import Button,LED
boton = Button(23)
led = LED(5)

while True
    if boton.is_pressed==True:
        led.on()
        print("Pulsador ACTIVO")
    else:
        led.off() 
        print("Pulsador INACTIVO")