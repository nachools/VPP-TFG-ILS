import VARIABLES
import numpy as np
import math

# CALCULO DE AREAS 
#Mainsail
TrapArea1 = 0.25 * VARIABLES.P * (VARIABLES.E + VARIABLES.MGL) * 0.5
TrapArea2 = 0.25 * VARIABLES.P * (VARIABLES.MGL + VARIABLES.MGM) * 0.5
TrapArea3 = 0.25 * VARIABLES.P * (VARIABLES.MGM + VARIABLES.MGU) * 0.5
TrapArea4 = 0.125 * VARIABLES.P * (VARIABLES.MGU + VARIABLES.MGT) * 0.5
TrapArea5 = 0.125 * VARIABLES.P * (VARIABLES.MGT + VARIABLES.HB) * 0.5
MainSailArea = TrapArea1 + TrapArea2 + TrapArea3 + TrapArea4 + TrapArea5
#HeadSail
HeadSailArea = (((VARIABLES.I)**2 + (VARIABLES.J)**(2))**(0.5)) * (VARIABLES.LP/2)
#TotalSail
SailArea = MainSailArea + HeadSailArea

# ALTURA CENTRO DE GRAVEDAD
# Para el Solver
def calcular_Zsail ():
    Zsail = (((VARIABLES.I/3) * HeadSailArea) + ((VARIABLES.BAS + (VARIABLES.P/3))*MainSailArea))/SailArea
    return Zsail

# DEPOWERING
def ZCEdepowered(flat):
    ZCEdepowered = calcular_Zsail() * (1 - (0.203 * (1 - flat)) - (0.415 * (1 - flat)*(1-(VARIABLES.I/(VARIABLES.BAS + VARIABLES.P)))))
    return ZCEdepowered

# TRIANGULO DE VIENTO
def TWSce(flat, escora):
    TWSce = VARIABLES.TWS * (((ZCEdepowered(flat) + VARIABLES.FBAV) * np.cos(escora * np.pi/180))/10)**(0.03)
    return TWSce
def AWAce(velocidad, flat,  escora):
    AWAce = (180/np.pi)*math.atan2(
    (math.cos(math.radians(escora)) * TWSce(flat, escora) * math.sin(math.radians(VARIABLES.TWA))), 
    ((TWSce(flat, escora) * math.cos(math.radians(VARIABLES.TWA))) + velocidad)
)
    return AWAce
def AWSce(velocidad, flat, escora):
    AWSce = math.sqrt(
    (TWSce(flat, escora) * math.cos(math.radians(VARIABLES.TWA)) + velocidad) ** 2 + 
    (math.cos(math.radians(escora)) * TWSce(flat, escora) * math.sin(math.radians(VARIABLES.TWA))) ** 2
)
    return AWSce

