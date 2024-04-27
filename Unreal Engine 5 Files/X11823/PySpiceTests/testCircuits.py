import sys, csv
import socket
import numpy as np
import PySpice
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

import matplotlib.pyplot as plt
from PySpice.Probe.Plot import plot

from scipy.optimize import curve_fit

import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1',5001))

server.listen()

#########################################################################################
## RC Circuit Example
#########################################################################################
print('RC Circuit')
circuitRC = Circuit('RC')
simulatorRC = circuitRC.simulator(temperature = 27, nominal_temperature = 27)

source = circuitRC.PulseVoltageSource('input', 'in', circuitRC.gnd,
                initial_value=0@u_V, pulsed_value=10@u_V,
                pulse_width=10@u_ms, period=20@u_ms)

circuitRC.R(1, 'in', 'out', 1@u_kΩ)
element = circuitRC.C
value = 1@u_uF
element(1, 'out', circuitRC.gnd, value)
tau = circuitRC['R1'].resistance * circuitRC['C1'].capacitance

step_time = 10@u_us
analysis = simulatorRC.transient(step_time=step_time, end_time=source.period*3)

def out_voltage(t, tau):
    return float(source.pulsed_value) * (1 -  np.exp(-t / tau))

i_max = int(5 * tau / float(step_time))
popt, pcov = curve_fit(out_voltage, analysis.out.abscissa[:i_max], analysis.out[:i_max])
tau_measured = popt[0]

print('tau {0} = {1}'.format('capacitor', tau.canonise().str_space()))
print('tau measured {0} = {1:.1f} ms'.format('capacitor', tau_measured * 1000))

ax = ax1
title = "Capacitor: voltage is constant"

ax.set_title(title)
ax.grid()
current_scale = 1000
ax.plot(analysis['in'])
ax.plot(analysis['out'])
ax.plot(((analysis['in'] - analysis.out)/circuitRC['R1'].resistance) * current_scale)
ax.axvline(x=float(tau), color='red')
ax.set_ylim(-11, 11)
ax.set_xlabel('t [s]')
ax.set_ylabel('[V]')
ax.legend(('Vin [V]', 'Vout [V]', 'I'), loc=(.8,.8))

plt.tight_layout()
plt.show()
####################################################

## RL Circuit Example
#########################################################################################
print('RL Circuit')
circuitRL = Circuit('RL')

source = circuitRL.PulseVoltageSource('input', 'in', circuitRL.gnd,
                initial_value=0@u_V, pulsed_value=10@u_V,
                pulse_width=10@u_ms, period=20@u_ms)

circuitRL.R(1, 'in', 'out', 1@u_kΩ)
element = circuitRL.L
value = 1@u_H
element(1, 'out', circuitRL.gnd, value)
tau = circuitRL['L1'].inductance / circuitRL['R1'].resistance

simulatorRL = circuitRL.simulator(temperature = 27, nominal_temperature = 27)
step_time = 10@u_us
analysis = simulatorRL.transient(step_time=step_time, end_time=source.period*3)

def out_voltage(t, tau):
    return float(source.pulsed_value) * np.exp(-t / tau)

i_max = int(5 * tau / float(step_time))
popt, pcov = curve_fit(out_voltage, analysis.out.abscissa[:i_max], analysis.out[:i_max])
tau_measured = popt[0]

print('tau {0} = {1}'.format('capacitor', tau.canonise().str_space()))
print('tau measured {0} = {1:.1f} ms'.format('capacitor', tau_measured * 1000))

ax = ax2
title = "Inductor: current is constant"

ax.set_title(title)
ax.grid()
current_scale = 1000
ax.plot(analysis['in'])
ax.plot(analysis['out'])
ax.plot(((analysis['in'] - analysis.out)/circuitRL['R1'].resistance) * current_scale)
ax.axvline(x=float(tau), color='red')
ax.set_ylim(-11, 11)
ax.set_xlabel('t [s]')
ax.set_ylabel('[V]')
ax.legend(('Vin [V]', 'Vout [V]', 'I'), loc=(.8,.8))

plt.tight_layout()
plt.show()
####################################################


circuitRC.R(1, 'in', 'out', 1@u_kΩ)
circuitRC.C(1, 'out', circuitRC.gnd, 1@u_uF)

tau = circuitRC['R1'].resistance * circuitRC['C1'].capacitance

step_time = 10@u_us
analysis = simulatorRC.transient(step_time=step_time, end_time=sourceRC.period*3)

def out_voltage(t, tau):
    return float(sourceRC.pulsed_value) * (1 -  np.exp(-t / tau))

i_max = int(5 * tau / float(step_time))
popt, pcov = curve_fit(out_voltage, analysis.out.abscissa[:i_max], analysis.out[:i_max])
tau_measured = popt[0]

print('tau {0} = {1}'.format('capacitor', tau.canonise().str_space()))
print('tau measured {0} = {1:.1f} ms'.format('capacitor', tau_measured * 1000))

ax = ax1
title = "Capacitor: voltage is constant"

ax.set_title(title)
ax.grid()
current_scale = 1000
ax.plot(analysis['in'])
ax.plot(analysis['out'])
ax.plot(((analysis['in'] - analysis.out)/circuitRC['R1'].resistance) * current_scale)
ax.axvline(x=float(tau), color='red')
ax.set_ylim(-11, 11)
ax.set_xlabel('t [s]')
ax.set_ylabel('[V]')
ax.legend(('Vin [V]', 'Vout [V]', 'I'), loc=(.8,.8))

plt.tight_layout()
plt.show()
#########################################################################################
## RL Circuit Example
#########################################################################################
print('RL Circuit')
circuitRL = Circuit('RL')

source = circuitRL.PulseVoltageSource('input', 'in', circuitRL.gnd,
                initial_value=0@u_V, pulsed_value=10@u_V,
                pulse_width=10@u_ms, period=20@u_ms)

circuitRL.R(1, 'in', 'out', 1@u_kΩ)
element = circuitRL.L
value = 1@u_H
element(1, 'out', circuitRL.gnd, value)
tau = circuitRL['L1'].inductance / circuitRL['R1'].resistance

simulatorRL = circuitRL.simulator(temperature = 27, nominal_temperature = 27)
step_time = 10@u_us
analysis = simulatorRL.transient(step_time=step_time, end_time=source.period*3)

def out_voltage(t, tau):
    return float(source.pulsed_value) * np.exp(-t / tau)

i_max = int(5 * tau / float(step_time))
popt, pcov = curve_fit(out_voltage, analysis.out.abscissa[:i_max], analysis.out[:i_max])
tau_measured = popt[0]

print('tau {0} = {1}'.format('capacitor', tau.canonise().str_space()))
print('tau measured {0} = {1:.1f} ms'.format('capacitor', tau_measured * 1000))

ax = ax2
title = "Inductor: current is constant"

ax.set_title(title)
ax.grid()
current_scale = 1000
ax.plot(analysis['in'])
ax.plot(analysis['out'])
ax.plot(((analysis['in'] - analysis.out)/circuitRL['R1'].resistance) * current_scale)
ax.axvline(x=float(tau), color='red')
ax.set_ylim(-11, 11)
ax.set_xlabel('t [s]')
ax.set_ylabel('[V]')
ax.legend(('Vin [V]', 'Vout [V]', 'I'), loc=(.8,.8))

plt.tight_layout()
plt.show()

####################################################
# Example of node current
####################################################
circuitCurrent = Circuit('Current Divider')

circuitCurrent.I('1', '1', '0', 4.545@u_mA)
circuitCurrent.R('1', '1', '2', .1@u_kOhm)
circuitCurrent.R('2', '2', '0', 1@u_kOhm)

resistorList = [circuitCurrent.R1, circuitCurrent.R2]

for resistance in resistorList:
    resistance.minus.add_current_probe(circuitCurrent) # to get positive value

simulatorCurrent = circuitCurrent.simulator(temperature = 27, nominal_temperature = 27)
analysisCurrent = simulatorCurrent.operating_point()


for node in analysisCurrent.branches.values():
    print('Node {}: {:5.4f} mA'.format(str(node), float(node)*10000))