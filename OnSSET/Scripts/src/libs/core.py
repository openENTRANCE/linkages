from .constants import CSV_COLUMNS, CSV_FLD_ELECPOPCALIB, CSV_FLD_MINIMUMOVERALL, CSV_FLD_NEWCONNECTIONS, CSV_FLD_POP
from .constants import XLSX_FLD_MODEL, XLSX_FLD_REGION, XLSX_FLD_SCENARIO, XLSX_FLD_UNIT, XLSX_FLD_VARIABLE, XLSX_FIELDS
from glob import iglob
import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

_variables: tuple[str, ...] = (
    'Population', 'Population|Connected', 'Network|Electricity|Expansion Cost', 'Capacity|Added')
_units: tuple[str | None, ...] = (None, None, 'us$', 'kW')
_tags: tuple[str, ...] = ('Grid', 'Hybrid', 'Hydro', 'PV', 'Wind')
_w_columns: tuple[str, ...] = ('Grid', 'MG_PV_Hybrid', 'MG_Hydro', 'SA_PV', 'MG_Wind_Hybrid')


def get_statistics_v1(df: pd.DataFrame, years: list[int]) -> list[pd.Series]:
    """

    :param df:
    :param years:
    :return:
    """
    _data: list[tuple[str, int, float]] = list()

    for _year in years:  # type: int
        _key: str = f'{CSV_FLD_NEWCONNECTIONS}{_year}'
        _data.append(('Population|Connected', _year, df[_key].sum()))
        _w_key: str = f'MinimumOverall{_year}'
        _w = df[_w_key].eq(f'Grid{_year}')
        _data.append(('Population|Connected|Grid', _year, df[_w][_key].sum()))
        _w = df[_w_key].eq(f'MG_PV_Hybrid{_year}')
        _data.append(('Population|Connected|Hybrid', _year, df[_w][_key].sum()))
        _w = df[_w_key].eq(f'MG_Hydro{_year}')
        _data.append(('Population|Connected|Hydro', _year, df[_w][_key].sum()))
        _w = df[_w_key].eq(f'SA_PV{_year}')
        _data.append(('Population|Connected|PV', _year, df[_w][_key].sum()))
        _w = df[_w_key].eq(f'MG_Wind_Hybrid{_year}')
        _data.append(('Population|Connected|Wind', _year, df[_w][_key].sum()))

        _key: str = f'InvestmentCost{_year}'
        _data.append(('Network|Electricity|Expansion Cost', _year, df[_key].sum()))
        _w_key: str = f'MinimumOverall{_year}'
        _w = df[_w_key].eq(f'Grid{_year}')
        _data.append(('Network|Electricity|Expansion Cost|Grid', _year, df[_w][_key].sum()))
        _w = df[_w_key].eq(f'MG_PV_Hybrid{_year}')
        _data.append(('Network|Electricity|Expansion Cost|Hybrid', _year, df[_w][_key].sum()))
        _w = df[_w_key].eq(f'MG_Hydro{_year}')
        _data.append(('Network|Electricity|Expansion Cost|Hydro', _year, df[_w][_key].sum()))
        _w = df[_w_key].eq(f'SA_PV{_year}')
        _data.append(('Network|Electricity|Expansion Cost|PV', _year, df[_w][_key].sum()))
        _w = df[_w_key].eq(f'MG_Wind_Hybrid{_year}')
        _data.append(('Network|Electricity|Expansion Cost|Wind', _year, df[_w][_key].sum()))

        _key: str = f'NewCapacity{_year}'
        _data.append(('Capacity|Added', _year, df[_key].sum()))
        _w_key: str = f'MinimumOverall{_year}'
        _w = df[_w_key].eq(f'Grid{_year}')
        _data.append(('Capacity|Added|Grid', _year, df[_w][_key].sum()))
        _w = df[_w_key].eq(f'MG_PV_Hybrid{_year}')
        _data.append(('Capacity|Added|Hybrid', _year, df[_w][_key].sum()))
        _w = df[_w_key].eq(f'MG_Hydro{_year}')
        _data.append(('Capacity|Added|Hydro', _year, df[_w][_key].sum()))
        _w = df[_w_key].eq(f'SA_PV{_year}')
        _data.append(('Capacity|Added|PV', _year, df[_w][_key].sum()))
        _w = df[_w_key].eq(f'MG_Wind_Hybrid{_year}')
        _data.append(('Capacity|Added|Wind', _year, df[_w][_key].sum()))

    _data_new: list[pd.Series] = list()
    for _year in years:
        _data_new.append(
            pd.Series(data=dict(map(lambda item: (item[0], item[2]), filter(lambda item: item[1] == _year, _data))),
                      name=str(_year)))
    return _data_new


def get_statistics_v2(df: pd.DataFrame, years: list[int]) -> list[pd.Series]:
    """

    :param df:
    :param years:
    :return:
    """
    _data_new: list[pd.Series] = list()
    _pop_base: float | None = None
    _pop_connected_var: str = _variables[1]

    for idx_1, _year in enumerate(years):  # type: int, int
        _columns_years: list[str] = list(f'{_c}{_year}' for _c in CSV_COLUMNS)
        _s: pd.Series = df[_columns_years].sum()
        _s.index = list(_variables)
        _s.name = str(_year)

        if idx_1 == 0:
            _pop_base = df[f'{CSV_FLD_POP}{_year}'].sum()
            _column_name: str = CSV_FLD_ELECPOPCALIB
            _s[_pop_connected_var] = df[_column_name].sum()
        else:
            _column_name: str = f'{CSV_FLD_NEWCONNECTIONS}{_year}'
            _s[_pop_connected_var] = _pop_base + df[_column_name].sum()

        _w_key: str = f'{CSV_FLD_MINIMUMOVERALL}{_year}'

        for idx_2, _w_c in enumerate(_w_columns):
            _w = df[_w_key].eq(f'{_w_c}{_year}')
            _s1: pd.Series = df[_w][_columns_years[1:]].sum()
            _s1.index = list(f'{_v}|{_tags[idx_2]}' for _v in _variables[1:])
            _s1.name = str(_year)
            _s = pd.concat([_s, _s1])

        _data_new.append(_s.copy())

    return _data_new


def check_dataframe(df: pd.DataFrame, years: list[int]) -> bool:
    """

    :param df:
    :return:
    """
    from itertools import product
    if isinstance(df, pd.DataFrame) is True and df.empty is False:
        _df_columns: set[str] = set(df.columns.to_list())
        _columns_used: set[str] = set(f'{a}{b}' for a, b in product(CSV_COLUMNS + (CSV_FLD_MINIMUMOVERALL,), years, repeat=1))
        _columns_used.add(CSV_FLD_ELECPOPCALIB)
        _diff = _columns_used - _df_columns
        if len(_diff) == 0:
            return True
        logger.error(_diff)
    return False


def get_statistics(df: pd.DataFrame, years: list[int], scenario: str, version: int = 2) -> pd.DataFrame:
    """
    
    :param df: 
    :param years: 
    :param scenario: 
    :return: 
    """
    if check_dataframe(df=df, years=years) is False:
        raise Exception('df variable is not a valid Pandas Dataframe!')

    FLD_ORDER: str = 'order'
    (_country,) = tuple(set(df['Country']))

    #
    fnc = get_statistics_v2 if version == 2 else get_statistics_v1
    serie_list: list[pd.Series] = fnc(df=df, years=years)
    for idx, s in enumerate(serie_list):  # type: int, pd.Series
        serie_list[idx] = s.astype('int64')
    #
    df_new: pd.DataFrame = pd.concat(serie_list, axis='columns')
    df_new.index.name = XLSX_FLD_VARIABLE
    df_new = df_new.sort_index().reset_index()

    df_new[XLSX_FLD_MODEL] = 'OnSSET 1.0'
    df_new[XLSX_FLD_SCENARIO] = scenario
    df_new[XLSX_FLD_REGION] = _country
    df_new[XLSX_FLD_UNIT] = None
    df_new[FLD_ORDER] = -1

    for idx, _v in enumerate(_variables):
        _u = _units[idx]
        _w = df_new[XLSX_FLD_VARIABLE].str.startswith(_v)
        if _u is not None:
            df_new.loc[_w, XLSX_FLD_UNIT] = _u
        df_new.loc[_w, FLD_ORDER] = idx

    df_new = df_new.sort_values(by=[FLD_ORDER, XLSX_FLD_VARIABLE])
    __columns: list[str] = XLSX_FIELDS + list(str(_year) for _year in years)
    df_new = df_new[__columns]

    return df_new


def merge_csv_filenames(input_folder: str, delimiter: str, sheet_name: str = 'data', delete_csv: bool = True) -> int:
    """

    :param input_folder:
    :return:
    """
    res: int = 0

    _pattern: str = os.path.join(input_folder, '*_sum.csv')
    logger.debug(f'regex pattern: {_pattern}')

    filenames: list[str] = sorted(iglob(_pattern))
    pd_list: list[pd.DataFrame] = list()

    for filename in filenames:
        if os.path.exists(filename) is True:
            pd_list.append(pd.read_csv(filename, sep=delimiter))
            if delete_csv is True:
                os.remove(filename)
                logger.debug(f'file {filename} removed from local filesystem.')

    df: pd.DataFrame = pd.concat(pd_list, ignore_index=True)

    xlxs_filename: str = os.path.join(input_folder, 'result.xlsx')
    df.to_excel(xlxs_filename, sheet_name=sheet_name, index=False)

    return res
