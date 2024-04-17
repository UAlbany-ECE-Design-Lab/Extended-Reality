import sys, csv
import socket
import numpy as np
import PySpice
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

import matplotlib.pyplot as plt
from PySpice.Probe.Plot import plot

from scipy.optimize import curve_fit

figure, (ax1, ax2) = plt.subplots(2, figsize=(20, 10))

########################################################################################################

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1',5001))

server.listen()
"""
###########################################################################################
## RC Circuit Example Preset Circuits
#########################################################################################
print('RC Circuit')
circuitRC = Circuit('RC')
simulatorRC = circuitRC.simulator(temperature = 27, nominal_temperature = 27)

sourceRC = circuitRC.PulseVoltageSource('input', 'in', circuitRC.gnd,
                initial_value=0@u_V, pulsed_value=10@u_V,
                pulse_width=10@u_ms, period=20@u_ms)

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

"""
# Example of node voltage and current
####################################################################################

# Voltage
#************************************************
def format_output(analysis):
    sim_res_dict = {}
    for node in analysis.nodes.values():
        data_label = "%s" % str(node)
        sim_res_dict[data_label] = np.array(node)
    return sim_res_dict

circuit = Circuit('Voltage Divider')

circuit.V('1', '1', '0', 5@u_V)
circuit.R('1', '1', '2', .1@u_kOhm)
circuit.R('2', '2', '0', 1@u_kOhm)


simulator = circuit.simulator(temprature = 27, nominal_temprature = 27)

analysis = simulator.operating_point()
print(circuit)

print(format_output(analysis))
#************************************************
"""
# Current
#************************************************ 
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
"""
list = []

while True:
    client,address = server.accept()

    print('Connected')

    val = client.recv(1024).decode('utf-8')

    if not val:
        # if data is not received break
        break

    if val == 'quit':
        client.close()
        sys.exit()
    else:
        ############################################################################################
        #Presets
        """if val == 'VoltageDivider':

            client.send(b'Compute: VoltageDivider')
            circuit = Circuit('Voltage Divider')
            circuit.V('1', '1', '0', 5@u_V)
            circuit.R('1', '1', '2', .1@u_kOhm)
            circuit.R('2', '2', '0', 1@u_kOhm)
            simulator = circuit.simulator(temprature = 27, nominal_temprature = 27)
            analysis = simulator.operating_point()
            print(circuit)
            print(format_output(analysis))

        elif val == 'RCCircuit':

            client.send(b'Compute: RCCircuit')
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

        elif val == 'RLCircuit':
            client.send(b'Compute: RLCircuit')

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
            plt.show()"""

        if val[0] == 'V':
            print('Voltage')
            print(val)
            list.append(val)

        elif val[0] == 'R':
            print('Resistor')
            print(val)
            list.append(val)
            
        elif val[0] == 'C':
            print('Capacitor')
            print(val)
            list.append(val)
    
        elif val == 'Del':
            if len(list) == 0:
                pass
            else:
                list.pop(len(list)-1)
        elif val == 'compute':
            print('compute')
            if len(list):
                voltageCount = 0
                resistorCount = 0

                circuitTest = Circuit('Test')
                
                simulatorTest = circuitTest.simulator(temprature = 27, nominal_temprature = 27)

                for component in list:
                    componentList = component.split()
                    print(componentList)
                    if component[0] == 'V':
                        circuitTest.V(str(component[1]), str(componentList[1]), str(componentList[2]), float(componentList[3])@u_V)
                    elif component[0] == 'R':
                        circuitTest.R(str(component[1]), str(componentList[1]), str(componentList[2]), float(componentList[3])@u_kOhm)

                analysisTest = simulatorTest.operating_point()
                print(circuitTest)
                print(format_output(analysisTest))
                nodesOutput = format_output(analysisTest)

                computeString = 'Compute:\n'
                inv_nodesOutput = {}
                for key in reversed(nodesOutput):
                    inv_nodesOutput[key] = nodesOutput[key]

                for amps in inv_nodesOutput:
                    computeString += 'Node {}: {:5.4f} V\n'.format(amps[0], float(nodesOutput[amps][0]))

                print(computeString)
                client.send(computeString.encode())

            else:
                client.send(b'Compute: No components')
         
        else:
            print('Not a valid component')

        if val != 'compute':
            if len(list):
                client.send(', '.join(component for component in list).encode())
            else:
                client.send(b'Server Ouput')
    client.close()