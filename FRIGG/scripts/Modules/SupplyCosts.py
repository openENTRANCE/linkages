
import numpy as np
import warnings


class SupplyCosts:
    """Computes derivative from hourly variable costs and capacities.

    Builds up a piece-wise function that maps quantities in hour to costs of marginal generator.
    """

    def __init__(self, var_costs, capacities):
        """Constructs object from variable costs and capacities.

        Args
        var_costs : list/np.array
            two-dimensional list/array with units in first dimension and time steps in 2nd dimension
        capacities : list/np.array
            two-dimensional list/array with units in first dimension and time steps in 2nd dimension
        """

        # set timeset
        T = range(len(var_costs[0]))
        # get sorting indices for each time step
        index = [np.argsort([unit_costs[t] for unit_costs in var_costs]) for t in T]
        # sort costs
        self.sorted_costs = [[var_costs[i][t] for i in index[t]] for t in T]
        # sort capacities
        self.sorted_capacities = [[capacities[i][t] for i in index[t]] for t in T]
        # get cumulative capacities to build up function
        self.sorted_cumulative_capacities = [np.cumsum(self.sorted_capacities[t]).tolist() for t in T]

    def get_cumulative(self, y, t):
        """Takes demand y and time step t as an input and returns total costs of production (i.e. integral of marginal costs).
        """

        # generator capacities in t, sorted by costs
        capacities = self.sorted_capacities[t]
        # corresponding sorted costs in t
        costs = self.sorted_costs[t]
        # resulting costs
        cumulative_costs = 0
        # demand that is not 'priced' yet
        unpriced_demand = y
        # iterate over capacities/costs (have same ordering)
        i = 0
        # while unpriced demand remaining
        while unpriced_demand > 0.0:
            try:
                # capacity of next-cheapest generator
                cap = capacities[i]
                # demand that can be priced in iteration:
                priceable_demand = np.min([cap, unpriced_demand])
                # increase costs
                cumulative_costs += priceable_demand * costs[i]
                # updated unpriced demand
                unpriced_demand -= priceable_demand
                # update index
                i += 1
            # demand too high to be supplied
            except IndexError:
                warnings.warn('Trying to get cumulative costs for too high a demand. Setting marginal costs to 10e10')
                # demand that can be priced in iteration:
                priceable_demand = unpriced_demand
                # increase costs
                cumulative_costs += priceable_demand * 10e10
                # updated unpriced demand
                unpriced_demand -= priceable_demand

        return cumulative_costs
