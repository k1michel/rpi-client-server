from typing import Optional
from pydantic import BaseModel
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
km_contactor= {
    "desactivacion": bool(False)
}
recibir_contactor=dict(
    estado_contactor = False
)

#####################
# CREACION API
#####################
proyecto_client = FastAPI()

class Datos(BaseModel):
    estado_contactor: bool
#####################
#  API
#####################
@proyecto_client.post("/estado")
def recibir_estado(contactor_activo: Datos):
    global recibir_contactor
    recibir_contactor = dict(
        estado_contactor = contactor_activo.estado_contactor
    )
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
    
    while True:
        if recibir_contactor["estado_contactor"] == True:
            led_contactor.on()
            if (pulsador_1.is_pressed or pulsador_2.is_pressed or pulsador_3.is_pressed):
                km_contactor["desactivacion"] = True
                print("Contactor Desactivado")

        else:
            led_conexion.on()
            led_contactor.off()
            km_contactor["desactivacion"] = False
        print("\n" + "-"*30)
        print("Recibido estado contactor => ", recibir_contactor)
        print("Desactivacion km_contactor => ", km_contactor)
        print("Pulsador 1 => ", pulsador_1.is_pressed,"\nPulsador 2 => ", pulsador_2.is_pressed, "\nPulsador 3 => ",pulsador_3.is_pressed)
        print("-"*30 + "\n")
        sleep(1)

if __name__ == "__main__":
    chequeo = Thread(target=programa, daemon=True)
    chequeo.start()
    uvicorn.run(proyecto_client, host="0.0.0.0", port=8080)

