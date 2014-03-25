from src.CLI_Director                              import CLI_director



def malware_propagation_mode(malware_node_list):
    '''Launching Malware propagation mode.

    Args:
        malware_node_list: Infection map of hosts in network graph.
    '''
    # prepare malware director
    #malware_director = Malware_propagation_director()
    #
    #init_population_number = malware_director.get_infected_nodes_number()
    ##logger_MalwareProp.info("Try\t\t\tSuccess\t\t\tCurrent\t\t\tTotal")
    ##logger_MalwareProp.info("0\t\t\t" + "0\t\t\t" + str(init_population_number) +
    ##                        '\t\t\t' + str(len(malware_node_list)))
    #malware_director.set_init_population(init_population_number)
    #malware_director.propagation_loop(MALWARE_PROP_STEP_NUMBER)
    #malware_director.show_node_list()
    #print("initial population number = " + str(init_population_number))
    #print("total population number = ")
    #
    #malware_director.stop_malware_center()
    pass


def cli_mode(hosts, nodes, cluster_info):
    '''Launching CLI node.

    Args:

    '''
    cli_director = CLI_director(hosts, nodes, cluster_info)
    cli_director.cmdloop()