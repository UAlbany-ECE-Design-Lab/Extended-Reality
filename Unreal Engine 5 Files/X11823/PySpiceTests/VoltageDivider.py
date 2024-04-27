


# Example of a Voltage Divider
# Voltage
#************************************************
def format_output(analysis):
    sim_res_dict = {}
    for node in analysis.nodes.values():
        data_label = "%s" % str(node)
        sim_res_dict[data_label] = np.array(node)
    return sim_res_dict

#####################################################################

circuit = Circuit('Voltage Divider')

circuit.V('1', '1', '0', 5@u_V)
circuit.R('1', '1', '2', .1@u_kOhm)
circuit.R('2', '2', '0', 1@u_kOhm)


simulator = circuit.simulator(temprature = 27, nominal_temprature = 27)

analysis = simulator.operating_point()
print(circuit)

print(format_output(analysis))