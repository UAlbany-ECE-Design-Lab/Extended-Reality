import sys, csv
import socket
import numpy as np
import PySpice
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1',5001))

server.listen()


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
#************************************************
############################################################################

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