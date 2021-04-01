from typing import Optional
from fastapi import FastAPI
import uvicorn
from gpiozero import Button, LED
from threading import Thread
from time import sleep
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
recibir_contactor = None

km_contactor= {
    'desactivavion': bool(False)
}
#####################
# CREACION API
#####################
proyecto_client = FastAPI()

#####################
#  API
#####################
@proyecto_client.post("/estado")
def recibir_estado(contactor_activo):
    global recibir_contactor
    recibir_contactor = contactor_activo
    return recibir_contactor
@proyecto_client.get("/desactivacion")
def enviar_desactivacion():
    global km_contactor
    return km_contactor

###################
# PROGRAMA 2PLANO
###################
def programa():
    global km_contactor
    global recibir_contactor
    while True:
        if recibir_contactor.estado_contactor == True:
            led_contactor.on()
            print("Contactor activado")
            if (pulsador_1.is_pressed or pulsador_2.is_pressed or pulsador_3.is_presseed):
                km_contactor.desactivacion=True
                print("Contactor Desactivado")

        else:
            led_conexion.on()
            led_contactor.off()
            km_contactor.desactivacion = False
        print("Recibido contactor", recibir_contactor)
        print("km contactor", km_contactor)
        print("Pulsador", pulsador_1.is_pressed)
        sleep(3)

if __name__ == "__main__":
    chequeo = Thread(target=programa, daemon=True)
    chequeo.start()
    uvicorn.run(proyecto_client, host="0.0.0.0", port=8080)

