# import required packages
import os
import shutil
import pandas as pd
import urbs
# import python scripts
import compare_results
import write_IAMC_format
import write_globalvalues_to_pandas
import Elec_profile_to_ext_IAMC

# change terminal display
pd.set_option('display.max_columns', None)  
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)

# set up directory file
input_files = 'Technical_economic_input_data.xlsx' # xlsx file recommended
input_dir = 'Input'
input_path = os.path.join(input_dir, input_files)

# set output folder name individually
result_name = 'Case_study_3'
result_dir = urbs.prepare_result_directory(result_name)  # name + time stamp

# copy input file to result directory
try:
    shutil.copytree(input_path, os.path.join(result_dir, input_dir))
except NotADirectoryError:
    shutil.copyfile(input_path, os.path.join(result_dir, input_files))
# copy run file to result directory
shutil.copy(__file__, result_dir)

# choose Solver (cplex, glpk, gurobi, ...)
# solver needs to be installed to environment previously
solver = 'gurobi'


# simulation timesteps
(offset, length) = (-1, 8760)  # time step selection
timesteps = range(offset, length)

dt = 1  # length of each time step (unit: hours)

# detailed reporting commodity/sites
report_tuples = [
    (9999, 'LMAB1', 'Elec'),
    (9999, 'LMAB2', 'Elec'),
    (9999, 'LMAB3', 'Elec'),
    (9999, 'LMAB4', 'Elec'),
    (9999, 'LMAB5', 'Elec'),
    (9999, 'LMAB6', 'Elec'),
    (9999, 'LMAB7', 'Elec'),
    (9999, 'LMAB8', 'Elec'),
    (9999, 'LMAB9', 'Elec'),
    (9999, 'LMAB10', 'Elec')
    ]

# optional: define names for sites in report_tuples
report_sites_name = {('SFH1', 'SFH2', 'SFH3', 'LMAB4','LMAB5', 'LMAB6', 'LMAB7', 'LMAB8','LMAB9', 'LMAB10','Node'): 'All'}

# plotting commodities/sites
plot_tuples = [
    (9999, 'LMAB1', 'Elec'),
    # (2030, 'LMAB2', 'Elec'),
    # (2030, 'LMAB3', 'Elec'),
    # (2030, 'LMAB4', 'Elec'),
    # (2030, 'LMAB5', 'Elec'),
    # (2030, 'LMAB6', 'Elec'),
    # (2030, 'LMAB7', 'Elec'),
    # (2030, 'LMAB8', 'Elec'),
    # (2030, 'LMAB9', 'Elec'),
    # (2030, 'LMAB10', 'Elec'),
    # (2030, 'Node', 'Elec')
    ]

# optional: define names for sites in plot_tuples
plot_sites_name = {('LMAB1', 'LMAB2', 'LMAB3', 'LMAB4','LMAB5', 'LMAB6', 'LMAB7', 'LMAB8','LMAB9', 'LMAB10','Node'): 'All'}

# plotting timesteps
plot_periods = {
    'all': timesteps[1:]
}

# add or change plot colors
my_colors = {
    'LMAB1': (176, 202, 199),
    'LMAB2': (255, 87, 34),
    'LMAB3': (240, 154, 233),
    'LMAB4': (75, 93, 103)
}
for country, color in my_colors.items():
    urbs.COLORS[country] = color


# A) run pareto front optimization of local deficit/excess

# select scenarios and objective function to be run
# scenarios = [
#     [urbs.scenario_baseline, 'local'],
#     [urbs.scenario_baseline90, 'local'],
#     [urbs.scenario_baseline1, 'local'],
#     [urbs.scenario_baseline2, 'local'],
#     [urbs.scenario_baseline3, 'local'],
#     [urbs.scenario_baseline4, 'local']
#             ]

# multi criteria optimization: set max(local self-consumption) or min(supply and feed-in from public grid) as objective
# function, set further criteria dimension with upper bound of total costs while optimizing local self-consumption
# start Pareto front algorithm with inf. upper bound and set upper bound after each iteration step accordingly
# upper_bound = 9999999999
#
# for scenario, objective in scenarios:
#
#     # tba: stop criteria if 'upper_bound' < Cost minimal solution (A)
#     # then calculate solution with (A) and stop algorithm
#
#     print('Running scenario:', scenario.__name__[9:])
#     print('Selected objective function:', objective)
#     prob = urbs.run_scenario(input_path, solver, timesteps, scenario,
#                              result_dir, dt, objective,
#                              plot_tuples=plot_tuples,
#                              plot_sites_name=plot_sites_name,
#                              plot_periods=plot_periods,
#                              report_tuples=report_tuples,
#                              report_sites_name=report_sites_name,
#                              upperbound=upper_bound)
#     # set 'upper_bound' variable accordingly related to current iteration step
#     # 'upper_bound' is used in the scenario parameters
#     upper_bound = 0
#     for index in prob.costs:
#         upper_bound += prob.costs[index].value


# # comparison figure
# compare_results.generate_comparison_figure()
# # figure of output curves using pyam package
# write_IAMC_format.write_to_iamc_format()
# # generate Pareto front figure
# write_globalvalues_to_pandas.write_globvar_to_paretofront()

# B) run only maximum points of pareto front (three dimensions)
scenarios = [
    [urbs.scenario_SocietalxCommitmentxIBERIANxCityEC, 'cost'],
    [urbs.scenario_SocietalxCommitmentxIBERIANxCityEC, 'local'],
    [urbs.scenario_SocietalxCommitmentxIBERIANxTownEC, 'cost'],
    [urbs.scenario_SocietalxCommitmentxIBERIANxTownEC, 'local'],
    [urbs.scenario_SocietalxCommitmentxIBERIANxMixedEC, 'cost'],
    [urbs.scenario_SocietalxCommitmentxIBERIANxMixedEC, 'local'],
    [urbs.scenario_SocietalxCommitmentxIBERIANxRuralEC, 'cost'],
    [urbs.scenario_SocietalxCommitmentxIBERIANxRuralEC, 'local']
]


for scenario, objective in scenarios:

    # tba: stop criteria if 'upper_bound' < Cost minimal solution (A)
    # then calculate solution with (A) and stop algorithm

    print('Running scenario:', scenario.__name__[9:])
    print('Selected objective function:', objective)
    prob = urbs.run_scenario(input_path, solver, timesteps, scenario,
                             result_dir, dt, objective,
                             plot_tuples=plot_tuples,
                             plot_sites_name=plot_sites_name,
                             plot_periods=plot_periods,
                             report_tuples=report_tuples,
                             report_sites_name=report_sites_name,
                             )

    # set 'upper_bound' variable accordingly related to current iteration step
    # 'upper_bound' is used in the scenario parameters


# comparison figure
compare_results.generate_comparison_figure()
# figure of output curves using pyam package
write_IAMC_format.write_to_iamc_format()
# generate Pareto front figure
write_globalvalues_to_pandas.write_globvar_to_paretofront()
Elec_profile_to_ext_IAMC.write_to_iamc_format()