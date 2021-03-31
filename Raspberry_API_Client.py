from typing import Optional
from fastapi import FastAPI
import uvicorn
from gpiozero import Button, LED
from threading import Thread

####################
#   GPIO RASPBERRY
####################
pulsador_1 = Button(23)
pulsador_2 = Button(24)
pulsador_3 = Button(25)

led_conexion = LED(5)
led_contactor = LED(6)



#####################
#  VARIABLES GLOBALES
#####################
estado_contactor = None

km_contactor_off= False

#####################
# CREACION API
#####################
proyecto_client = FastAPI()

#####################
#  API
#####################
@proyecto_client.get("/estado")
def recibir_estado(contactor_activo):
    global estado_contactor
    estado_contactor = contactor_activo
    return estado_contactor
@proyecto_client.post("/desactivacion")
def enviar_desactivacion():
    global km_contactor_off
    return km_contactor_off

###################
# PROGRAMA 2PLANO
###################
def programa():
    global km_contactor_off
    global estado_contactor
    while True:
        if estado_contactor == True:
            led_contactor.on()
            print("Contactor activado")
            if (pulsador_1.is_pressed or pulsador_2.is_pressed or pulsador_3.is_presseed):
                km_contactor_off=True
                print("Contactor Desactivado")

        else:
            led_conexion.on()
            led_contactor.off()
            km_contactor_off = False


if __name__ == "__main__":
    chequeo = Thread(target=programa, daemon=True)
    chequeo.start()
    uvicorn.run(proyecto_client, host="0.0.0.0", port=8080)

