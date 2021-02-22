#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 08:24:26 2020

@author: joonahuh
Joonatan Huhtasalo
joonatan.huhtasalo@helsinki.fi
"""

import numpy as np
import matplotlib.pyplot as pl
from matplotlib import rc

rc('text', usetex=True)

inV0 = 11096
inDT = 0.5
#Teoreettinen lähtönopeus: 11 096 m/s

# Funktio, jonka sisään simulaation ja datan keruun
# toiminnallisuus on rakennettu
def lento(dt, v0):
    t = 0.0 # Alkuaika
    R = 384400000 #[m] Kuun ja maan keskietäisyys
    rMaa = 6371000 #[m] Maan säde
    rKuu = 1738200 #[m] Kuun säde
    x = 0 # Lähtöetäisyys
    dMaa = 100000 + rMaa #[m] Paikka fyysisesti maan keskipisteestä
    dKuu = R - dMaa # Fysikaalinen etäisyys kuuhun
    mMaa = 5.974 * pow(10,24) #Maan massa
    mKuu = 7.348 * pow(10,22) #Kuun massa
    G =  6.67408 * pow(10,-11) #Gravitaatiovakio
    v = v0 # Asetetaan alkunopeus
    
    # Datalistat
    tt = np.array([0.0])
    xt = np.array([0.0])
    
    
    vrtD = R - (rKuu + dMaa)# While loopin vertailu
    
    while x < vrtD and x >= 0 and t < 200000:
        # Tiedetään nopeus, voidaan siis päivittää paikka
        x = x + v * dt
        
        # Nyt voidaan päivittää etäisyys maahan
        #ja kuuhun fysikaalisessa mallissa
        dMaa = dMaa + v * dt
        dKuu = dKuu - v * dt
        
        # Päivitetään kiihtyvyys
        a = G*(mKuu/pow(dKuu,2)-mMaa/pow(dMaa,2))
                
        # Päivitetään nopeus
        v = v + a * dt
        
        t = t + dt
        
        # DATA PRINT #
        ################################
        #print('('+str(x)+','+str(t)+')', end=" ")
        ################################
        # DATA PRINT #
        
        # Lisätään datapisteet
        tt = np.append(tt, t)
        xt = np.append(xt, x)
    return tt, xt



# KUVAAJAT JA DATANKERUU #

# Suoritetaan laskennalliset mallit ja kerätään datapisteet
t1, x1 = lento(inDT, inV0)
t2, x2 = lento(inDT*8, inV0)
t3, x3 = lento(inDT*20, inV0)

# Muunnetaan ajan datasarja sekunneista tunneiksi
for i in range(len(t1)):
    t1[i] = t1[i] / (60**2)
for i in range(len(t2)):
    t2[i] = t2[i] / (60**2)
for i in range(len(t3)):
    t3[i] = t3[i] / (60**2)

# Luodaan kuvaaja
pl.figure(figsize=(7,4))
pl.plot(
        t3,
        x3,
        marker=',',
        color='red',
        label='$dt$ $'+str(inDT*20)+'$ s')
pl.plot(
        t2,
        x2,
        marker=',',
        color='blue',
        label='$dt$ $'+str(inDT*8)+'$ s')
pl.plot(t1,
        x1,
        marker=',',
        color='navy',
        label='$dt$ $'+str(inDT)+'$ s')
pl.grid(True)

pl.suptitle('Raketin laskennallinen matka maasta kuuhun\n Paikka ajan funktiona $t$,$x$-koordinaatistossa')
pl.title('$v_0='+ str(inV0) +'$ m/s', loc='right', fontsize=10)
pl.ylabel('Paikka $x$ [$10^8$ m]')
pl.xlabel('Aika $t$ [h]')
pl.legend()

# Muuttaa x-akselin apuviivojen tiheyttä
pl.xticks(np.arange(min(t1), max(t1)+1, 6.0))

pl.show
pl.savefig('figure.png', dpi=300)