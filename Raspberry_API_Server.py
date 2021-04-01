import requests
import json
from gpiozero import Button,LED
from time import sleep

####################
#   GPIO RASPBERRY
####################
pulsador_1 = Button(23)

led_contactor = LED(5)
led_contactor.off()
km_contactor = LED(6)
km_contactor.off()

####################
# VARIABLES GLOBALES
####################
contactor_activo= {
    'estado_contactor': bool(False)
}
recibir_desactivacion = {
    'desactivacion': False
}
####################
# PROGRAMA BUCLE
####################
while True:
    if pulsador_1.is_pressed==True and contactor_activo['estado_contactor']==False:
        contactor_activo['estado_contactor']= True
    if contactor_activo['estado_contactor']==True:
        km_contactor.on()
        led_contactor.on()
        sleep(1)
        led_contactor.off()
        sleep(1)
        recibir_desactivacion = requests.get("http://192.168.43.221:8080/desactivacion",verify=False).json() #IP cliente
        if recibir_desactivacion['desactivacion']==True:
            contactor_activo['estado_contactor']= False

    else:
        km_contactor.off()
        led_contactor.on()
    requests.post("http://192.168.43.221:8080/estado", data=json.dumps(contactor_activo))  # IP cliente
    print("Contactor",contactor_activo)
    print("Pusador", pulsador_1.is_pressed)
    print("Mensaje Recibido", recibir_desactivacion)
    sleep(3)



