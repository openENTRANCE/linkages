
import numpy as np
import pandas as pd
import yaml
import builtins
import warnings
import pyam
pyam.iiasa.Connection('openentrance')


class DataReader:
    """Module with helper functions for reading data
    """

    @staticmethod
    def get_settings(file_name='Settings.yaml'):
        """Read settings from Settings_...yaml file

        Needs to be called at module level in order to have settings when making module imports

        Args:
            file_name (str): name of settings file, default is 'Settings.yaml'
        """

        # read in yaml settings as dict and make all dict entries global variable
        print('Reading settings...')
        with open(file_name) as file:
            conf = yaml.load(file, Loader = yaml.FullLoader)

        builtins.num_cores = conf['num_cores']
        conf['T'] = range(conf['t_start'], conf['t_end'])

        return conf

    @staticmethod
    def get_production_capacities(conf, source='offline', verbose=True):
        """Read production capacities, either offline (locally) or online (from scenario explorer)
        """

        # if offline source, read local data
        if source == 'offline':
            hourly_capacities = pd.read_csv('Input/ProductionCapacities.csv', index_col=0).iloc[conf['t_start']:conf['t_end'], :]
        # if online source, read data from openENTRANCE scenario explorer
        if source == 'online':
            openentrance_capacities = pyam.read_iiasa(
                'openentrance',
                model=conf['openEntrance']['capacities']['model'],
                variable=conf['openEntrance']['capacities']['variable'],
                region=conf['openEntrance']['capacities']['region'],
                scenario=conf['openEntrance']['capacities']['scenario'])
            openentrance_capacities = openentrance_capacities.filter(year=conf['openEntrance']['capacities']['year'])
            if verbose:
                print('Production capacities (openENTRANCE):')
                print(openentrance_capacities.timeseries())

            # try to match downloaded data to technologies specified in .yaml file. If that fails, use local data
            try:
                installed_capacities = {source: openentrance_capacities.filter(variable=conf['openEntrance']['capacities']['variable'] + source).timeseries()[int(conf['openEntrance']['capacities']['year'])][-1] for source in conf['openEntrance']['sources']}
            except (IndexError, ValueError, AttributeError):
                warnings.warn('Capacities data from scenario explorer does not fit sources supplied in Settings.yaml - using mock-up data.')
                installed_capacities = {source: 1 for source in conf['openEntrance']['sources']}
            # translate installed capacities to hourly capacities
            # for dispatchable sources, this is trivial; for non-dispatchable sources, use profiles supplied locally
            hourly_capacities = {source: np.repeat(installed_capacities[source], len(conf['T'])) if source in conf['openEntrance']['dispatchable_sources'] else pd.read_csv('input/' + source + '.csv', header=None).iloc[:, 0].values[conf['T']] * installed_capacities[source] for source in conf['openEntrance']['sources']}

        return hourly_capacities

    @staticmethod
    def get_production_costs(conf, source='offline', verbose=True):
        """Read production costs, either offline (locally) or online (from scenario explorer)
        """

        # if offline source, read local data
        if source == 'offline':
            hourly_costs = pd.read_csv('Input/ProductionCosts.csv', index_col=0).iloc[conf['t_start']:conf['t_end'], :]
        # if online source, read data from openENTRANCE scenario explorer
        if source == 'online':
            openentrance_costs = pyam.read_iiasa(
                'openentrance',
                model=conf['openEntrance']['costs']['model'],
                variable=conf['openEntrance']['costs']['variable'],
                region=conf['openEntrance']['costs']['region'],
                scenario=conf['openEntrance']['costs']['scenario'])
            openentrance_costs = openentrance_costs.filter(year=conf['openEntrance']['costs']['year'])
            if verbose:
                print('Production costs (openENTRANCE):')
                print(openentrance_costs.timeseries())

            # try to match downloaded data to technologies specified in .yaml file. If that fails, use local data
            try:
                static_costs = {source: openentrance_costs.filter(variable=conf['openEntrance']['costs']['variable'] + source).timeseries()[int(conf['openEntrance']['capacities']['year'])][-1] for source in conf['openEntrance']['sources']}
            except (IndexError, ValueError, AttributeError):
                warnings.warn('Cost data from scenario explorer does not fit sources supplied in Settings.yaml - using mock-up data.')
                static_costs = {source: 1 for source in conf['openEntrance']['sources']}
            # translate to hourly costs
            hourly_costs = {source: np.repeat(static_costs[source], len(conf['T'])) for source in conf['openEntrance']['sources']}

        return hourly_costs

    @staticmethod
    def get_initial_demand(conf, source='offline', verbose=True):
        """Read initial demand, either offline (locally) or online (from scenario explorer)
        """

        # if offline source, read local data
        if source == 'offline':
            initial_demand = pd.read_csv('Input/InitialDemand.csv', index_col=0).iloc[conf['t_start']:conf['t_end'], :]
        # if online source, read data from openENTRANCE scenario explorer
        if source == 'online':
            initial_demand = pyam.read_iiasa(
                'openentrance',
                model=conf['openEntrance']['initial_demand']['model'],
                variable=conf['openEntrance']['initial_demand']['variable'],
                region=conf['openEntrance']['initial_demand']['region'],
                scenario=conf['openEntrance']['initial_demand']['scenario'])
            initial_demand = initial_demand.filter(year=conf['openEntrance']['initial_demand']['year'])
            if verbose:
                print('Initial demand:')
                print(initial_demand.timeseries())

            # set yearly aggregate
            yearly_aggregate = initial_demand.as_pandas()['value'].sum()
            # create normalised hourly pattern from offline data
            hourly_basis = pd.read_csv('Input/InitialDemand.csv', index_col=0).iloc[conf['t_start']:conf['t_end'], :]
            hourly_basis_normalised = hourly_basis['2050'] / hourly_basis['2050'].max()
            # create non-normalised hourly demand
            initial_demand = yearly_aggregate * hourly_basis_normalised
            initial_demand = initial_demand.to_numpy()

        return initial_demand
