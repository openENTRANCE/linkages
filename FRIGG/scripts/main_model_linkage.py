
""" Main script to run dynamic programming algorithm

Reads data and settings, runs optimisation and prints results to CSV
"""

import numpy as np
import pandas as pd
import pyam

from Modules.SupplyCosts import SupplyCosts
from Modules.DataReader import DataReader


def get_supply_costs(production_costs, production_capacities):

    supply_costs = SupplyCosts(
        var_costs=production_costs.to_numpy().transpose(),
        capacities=production_capacities.to_numpy().transpose())

    return supply_costs

def get_costs_from_demand(supply_costs, demand):

    T = range(len(demand))
    costs = [supply_costs.get_cumulative(y=demand[t], t=t) for t in T]

    return np.sum(costs)


def main():

    pyam.iiasa.Connection('openentrance')

    conf = DataReader.get_settings()
    production_capacities = DataReader.get_production_capacities(conf, source=conf['data_source']['capacities'])
    production_costs = DataReader.get_production_costs(conf, source=conf['data_source']['costs'])
    initial_demand = DataReader.get_initial_demand(conf, source=conf['data_source']['initial_demand'])

    supply_costs = get_supply_costs(
        production_costs=pd.DataFrame(production_costs),
        production_capacities=pd.DataFrame(production_capacities))

    ### Execute Frigg here
    # DataWriter.print_new_demand_to_csv(initial_demand=baseline, new_demand=flexible_demand, val_col_name='2050')


    print('Problem solved successfully!')


if __name__ == "__main__":
    main()
