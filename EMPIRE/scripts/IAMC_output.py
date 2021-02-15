from __future__ import division
from pyomo.environ import *

#EMPIRE Abstract Model here, omitted for brevity

if IAMC_PRINT:
    ####################
    ###STANDARD PRINT###
    ####################
    
    import pandas as pd
    
    Modelname = "EMPIRE"
    Scenario = "1.5degree"

    dict_countries = {"Austria": "Austria",
                      "Bosnia and Herzegovina": "BosniaH",
                      "Belgium": "Belgium", "Bulgaria": "Bulgaria",
                      "Switzerland": "Switzerland", 
                      "Czech Republic": "CzechR", "Germany": "Germany",
                      "Denmark": "Denmark", "Estonia": "Estonia", 
                      "Spain": "Spain", "Finland": "Finland",
                      "France": "France", "United Kingdom": "GreatBrit.",
                      "Greece": "Greece", "Croatia": "Croatia", 
                      "Hungary": "Hungary", "Ireland": "Ireland", 
                      "Italy": "Italy", "Lithuania": "Lithuania",
                      "Luxembourg": "Luxemb.", "Latvia": "Latvia",
                      "North Macedonia": "Macedonia", 
                      "The Netherlands": "Netherlands", "Norway": "Norway",
                      "Poland": "Poland", "Portugal": "Portugal",
                      "Romania": "Romania", "Serbia": "Serbia", 
                      "Sweden": "Sweden", "Slovenia": "Slovenia",
                      "Slovakia": "Slovakia", "Norway|Ostland": "NO1", 
                      "Norway|Sorland": "NO2", "Norway|Norgemidt": "NO3",
                      "Norway|Troms": "NO4", "Norway|Vestmidt": "NO5"}

    dict_countries_reversed = dict([reversed(i) for i in dict_countries.items()])

    dict_generators = {"Bio": "Biomass", "Bioexisting": "Biomass",
                       "Coalexisting": "Coal|w/o CCS",
                       "Coal": "Coal|w/o CCS", "CoalCCS": "Coal|w/ CCS",
                       "CoalCCSadv": "Coal|w/ CCS", 
                       "Lignite": "Lignite|w/o CCS",
                       "Liginiteexisting": "Lignite|w/o CCS", 
                       "LigniteCCSadv": "Lignite|w/ CCS", 
                       "Gasexisting": "Gas|CCGT|w/o CCS", 
                       "GasOCGT": "Gas|OCGT|w/o CCS", 
                       "GasCCGT": "Gas|CCGT|w/o CCS", 
                       "GasCCS": "Gas|CCGT|w/ CCS", 
                       "GasCCSadv": "Gas|CCGT|w/ CCS", 
                       "Oilexisting": "Oil", "Nuclear": "Nuclear", 
                       "Wave": "Ocean", "Geo": "Geothermal", 
                       "Hydroregulated": "Hydro|Reservoir", 
                       "Hydrorun-of-the-river": "Hydro|Run-of-River", 
                       "Windonshore": "Wind|Onshore", 
                       "Windoffshore": "Wind|Offshore", 
                       "Solar": "Solar|PV", "Waste": "Waste", 
                       "Bio10cofiring": "Coal|w/o CCS", 
                       "Bio10cofiringCCS": "Coal|w/ CCS", 
                       "LigniteCCSsup": "Lignite|w/ CCS"}
    
    #Make datetime from HoursOfSeason       
    seasonstart={"winter": '2020-01-01',
                 "spring": '2020-04-01',
                 "summer": '2020-07-01',
                 "fall": '2020-10-01',
                 "peak1": '2020-11-01',
                 "peak2": '2020-12-01'}
    
    seasonhours=[]

    for s in instance.Season:
        if s not in 'peak':
            t=pd.to_datetime(list(range(lengthRegSeason)), unit='h', origin=pd.Timestamp(seasonstart[s]))
            t=[str(i)[5:-3] for i in t]
            t=[str(i)+"+01:00" for i in t]
            seasonhours+=t
        else:
            t=pd.to_datetime(list(range(lengthPeakSeason)), unit='h', origin=pd.Timestamp(seasonstart[s]))
            t=[str(i)[5:-3] for i in t]
            t=[str(i)+"+01:00" for i in t]
            seasonhours+=t       
    
    #Scalefactors to make units
    Mtonperton = (1/1000000)

    GJperMWh = 3.6
    EJperMWh = 3.6*10**(-9)

    GWperMW = (1/1000)

    USD10perEUR10 = 1.33 #Source: https://www.statista.com/statistics/412794/euro-to-u-s-dollar-annual-average-exchange-rate/ 
    EUR10perEUR18 = 154/171 #Source: https://www.inflationtool.com/euro 
    USD10perEUR18 = USD10perEUR10*EUR10perEUR18 

    print("Writing standard output to .csv...")
    
    f = pd.DataFrame(columns=["model", "scenario", "region", "variable", "unit", "subannual"]+[value(2020+(i)*instance.LeapYearsInvestment) for i in instance.Period])

    def row_write(df, region, variable, unit, subannual, input_value, scenario=Scenario, modelname=Modelname):
        df2 = pd.DataFrame([[modelname, scenario, region, variable, unit, subannual]+input_value],
                           columns=["model", "scenario", "region", "variable", "unit", "subannual"]+[value(2020+(i)*instance.LeapYearsInvestment) for i in instance.Period])
        df = df.append(df2)
        return df

    f = row_write(f, "Europe", "Discount rate|Electricity", "%", "Year", [value(instance.discountrate*100)]*len(instance.Period)) #Discount rate
    f = row_write(f, "Europe", "Capacity|Electricity", "GW", "Year", [value(sum(instance.genInstalledCap[n,g,i]*GWperMW for (n,g) in instance.GeneratorsOfNode)) for i in instance.Period]) #Total European installed generator capacity 
    f = row_write(f, "Europe", "Investment|Energy Supply|Electricity", "billion US$2010/yr", "Year", [value((1/instance.LeapYearsInvestment)*USD10perEUR18* \
                sum(instance.genInvCost[g,i]*instance.genInvCap[n,g,i] for (n,g) in instance.GeneratorsOfNode) + \
                sum(instance.transmissionInvCost[n1,n2,i]*instance.transmisionInvCap[n1,n2,i] for (n1,n2) in instance.BidirectionalArc) + \
                sum((instance.storPWInvCost[b,i]*instance.storPWInvCap[n,b,i]+instance.storENInvCost[b,i]*instance.storENInvCap[n,b,i]) for (n,b) in instance.StoragesOfNode)) for i in instance.Period]) #Total European investment cost (gen+stor+trans)
    f = row_write(f, "Europe", "Investment|Energy Supply|Electricity|Electricity storage", "billion US$2010/yr", "Year", [value((1/instance.LeapYearsInvestment)*USD10perEUR18* \
                sum((instance.storPWInvCost[b,i]*instance.storPWInvCap[n,b,i]+instance.storENInvCost[b,i]*instance.storENInvCap[n,b,i]) for (n,b) in instance.StoragesOfNode)) for i in instance.Period]) #Total European storage investment cost
    f = row_write(f, "Europe", "Investment|Energy Supply|Electricity|Transmission and Distribution", "billion US$2010/yr", "Year", [value((1/instance.LeapYearsInvestment)*USD10perEUR18* \
                sum(instance.transmissionInvCost[n1,n2,i]*instance.transmisionInvCap[n1,n2,i] for (n1,n2) in instance.BidirectionalArc)) for i in instance.Period]) #Total European transmission investment cost
    for w in instance.Scenario:
        f = row_write(f, "Europe", "Emissions|CO2|Energy|Supply|Electricity", "Mt CO2/yr", "Year", [value(Mtonperton*sum(instance.seasScale[s]*instance.genCO2TypeFactor[g]*(GJperMWh/instance.genEfficiency[g,i])* \
                instance.genOperational[n,g,h,i,w] for (n,g) in instance.GeneratorsOfNode for (s,h) in instance.HoursOfSeason)) for i in instance.Period], Scenario+"|"+str(w)) #Total European emissions per scenario
        f = row_write(f, "Europe", "Secondary Energy|Electricity", "EJ/yr", "Year", \
                [value(sum(EJperMWh*instance.seasScale[s]*instance.genOperational[n,g,h,i,w] for (n,g) in instance.GeneratorsOfNode for (s,h) in instance.HoursOfSeason)) for i in instance.Period], Scenario+"|"+str(w)) #Total European generation per scenario
        for g in instance.Generator:
            f = row_write(f, "Europe", "Active Power|Electricity|"+dict_generators[str(g)], "MWh", "Year", \
                [value(sum(instance.seasScale[s]*instance.genOperational[n,g,h,i,w] for n in instance.Node if (n,g) in instance.GeneratorsOfNode for (s,h) in instance.HoursOfSeason)) for i in instance.Period], Scenario+"|"+str(w)) #Total generation per type and scenario
        for (s,h) in instance.HoursOfSeason:
            for n in instance.Node:
                f = row_write(f, dict_countries_reversed[str(n)], "Price|Secondary Energy|Electricity", "US$2010/GJ", seasonhours[h-1], \
                    [value(instance.dual[instance.FlowBalance[n,h,i,w]]/(GJperMWh*instance.discount_multiplier[i]*instance.operationalDiscountrate*instance.seasScale[s]*instance.sceProbab[w])) for i in instance.Period], Scenario+"|"+str(w)+str(s))
    for g in instance.Generator:
        f = row_write(f, "Europe", "Capacity|Electricity|"+dict_generators[str(g)], "GW", "Year", [value(sum(instance.genInstalledCap[n,g,i]*GWperMW for n in instance.Node if (n,g) in instance.GeneratorsOfNode)) for i in instance.Period]) #Total European installed generator capacity per type
        f = row_write(f, "Europe", "Capital Cost|Electricity|"+dict_generators[str(g)], "US$2010/kW", "Year", [value(instance.genCapitalCost[g,i]*USD10perEUR18) for i in instance.Period]) #Capital generator cost
        if instance.genMargCost[g,instance.Period[1]] != 0: 
            f = row_write(f, "Europe", "Variable Cost|Electricity|"+dict_generators[str(g)], "EUR/MWh", "Year", [value(instance.genMargCost[g,i]) for i in instance.Period])
        f = row_write(f, "Europe", "Investment|Energy Supply|Electricity|"+dict_generators[str(g)], "billion US$2010/yr", "Year", [value((1/instance.LeapYearsInvestment)*USD10perEUR18* \
                sum(instance.genInvCost[g,i]*instance.genInvCap[n,g,i] for n in instance.Node if (n,g) in instance.GeneratorsOfNode)) for i in instance.Period]) #Total generator investment cost per type
        if instance.genCO2TypeFactor[g] != 0:
            f = row_write(f, "Europe", "CO2 Emmissions|Electricity|"+dict_generators[str(g)], "tons/MWh", "Year", [value(instance.genCO2TypeFactor[g]*(GJperMWh/instance.genEfficiency[g,i])) for i in instance.Period]) #CO2 factor per generator type
    for (n,g) in instance.GeneratorsOfNode:
        f = row_write(f, dict_countries_reversed[str(n)], "Capacity|Electricity|"+dict_generators[str(g)], "GW", "Year", [value(instance.genInstalledCap[n,g,i]*GWperMW) for i in instance.Period]) #Installed generator capacity per country and type
    
    f = f.groupby(['model','scenario','region','variable','unit','subannual']).sum().reset_index() #NB! DOES NOT WORK FOR UNIT COSTS; SHOULD BE FIXED
    
    if not os.path.exists(result_file_path + "/" + 'IAMC'):
        os.makedirs(result_file_path + "/" + 'IAMC')
    f.to_csv(result_file_path + "/" + 'IAMC/empire_iamc.csv', index=None)