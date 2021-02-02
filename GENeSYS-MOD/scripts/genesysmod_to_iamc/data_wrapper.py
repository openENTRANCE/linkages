import pandas as pd
import genesysmod_to_iamc.pyam_aggregator as pa

from genesysmod_to_iamc._statics import *


class DataWrapper(object):

    def __init__(self, input_file, output_gdx):
        self._output_gdx = output_gdx

        self.usage_values = pd.DataFrame()
        self.production_values = pd.DataFrame()
        self.emission_values = pd.DataFrame()
        self.capacity_values = pd.DataFrame()
        self.cost_values = pd.DataFrame()
        self.trade_capacity_values = pd.DataFrame()

        self.transformed_data = {}
        self.map_timeslices = {}
        self.demand_series = {}
        self.output_series = {}

        self.reinit_output_columns()
        self.init_time_slices()

        self.input_file = input_file
        self.hourly_data_excel = None

        self.idataframe = None

    def reinit_output_columns(self):
        _raw_production_values: pd.DataFrame = self._output_gdx[DEF_PRODUCTION_SHEET]
        _raw_production_values.columns = DEF_PRODUCTION_COLUMNS

        # Filter to corresponding type
        _usage_values: pd.DataFrame = _raw_production_values[_raw_production_values['type'] == 'Use']
        _production_values: pd.DataFrame = _raw_production_values[_raw_production_values['type'] == 'Production']

        # Filter output units
        self.usage_values: pd.DataFrame = _usage_values[_usage_values['unit'] == 'PJ']
        self.production_values: pd.DataFrame = _production_values[_production_values['unit'] == 'PJ']

        _raw_emission_values: pd.DataFrame = self._output_gdx[DEF_EMISSION_SHEET]
        _raw_emission_values.columns = DEF_EMISSION_COLUMNS
        self.emission_values = _raw_emission_values

        _raw_capacity_values: pd.DataFrame = self._output_gdx[DEF_CAPACITY_SHEET]
        _raw_capacity_values.columns = DEF_CAPACITY_COLUMNS
        self.capacity_values = _raw_capacity_values

        _raw_capacity_values: pd.DataFrame = self._output_gdx[DEF_CAPACITY_SHEET]
        _raw_capacity_values.columns = DEF_CAPACITY_COLUMNS
        self.capacity_values = _raw_capacity_values

        _raw_cost_values: pd.DataFrame = self._output_gdx[DEF_EXOGENOUS_COST_SHEET]
        _raw_cost_values.columns = DEF_EXOGENOUS_COST_COLUMNS
        self.cost_values = _raw_cost_values

        _raw_trade_capacity_values: pd.DataFrame = self._output_gdx[DEF_TRADE_CAPACITY_SHEET]
        _raw_trade_capacity_values.columns = DEF_TRADE_CAPACITY_COLUMNS
        self.trade_capacity_values = _raw_trade_capacity_values

    def init_time_slices(self):
        timeslices = self.production_values['subannual'].unique()
        map_timeslices = {}
        counter = 0
        for entry in timeslices:
            counter += 1
            map_timeslices[entry] = 'Reduced|t' + str(counter)

        self.map_timeslices = map_timeslices

    def write_all_transformed_csv(self):
        for file in self.transformed_data:
            filename = file + ".csv"
            self.transformed_data[file].to_csv(DEF_OUTPUT_PATH / filename, sep=';')

    def generate_idataframe(self, filter_only_yearly_values=False):
        self.idataframe = pa.generate_idataframe(self, filter_only_yearly_values)

    def generate_idataframe_renewable_series(self):
        self.idataframe = pa.generate_idataframe_renewable_series(self)

