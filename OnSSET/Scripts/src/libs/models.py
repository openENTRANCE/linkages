from collections import OrderedDict
from pydantic import BaseModel, Field
from typing import Any, Generator, Iterable
import logging
import re

logger = logging.getLogger(__name__)

_regex: re.Pattern = re.compile(
    r'^(?P<cc>\D\D)-(?P<v>2)-(?P<t>[01])_(?P<s>[01])_(?P<g>[01])_(?P<p>[01])_(?P<i>[01])_(?P<r>[01]).csv$')


class CsvColumn(BaseModel):
    year: int
    name: str

    @property
    def name_without_year(self) -> str:
        return self.name.replace(str(self.year), '')

    @classmethod
    def load(cls, year: int, columns: Iterable[str]) -> Generator['CsvColumn', Any, None]:
        for column in sorted(columns):
            yield cls(name=column, year=year)

    @staticmethod
    def get_column_names(items: list['CsvColumn']) -> list[str]:
        return list(x.name for x in items)

    @staticmethod
    def get_renamed_columns(items: list['CsvColumn']) -> dict[str, str]:
        return OrderedDict((x.name, x.name_without_year) for x in items)


class OnSSetFilename(BaseModel):
    cc: str = Field(min_length=2, max_length=2, title='Country code')
    v: int = Field(ge=2, le=2, default=2, title='GEP model version')
    t: int = Field(ge=0, le=2, title='Target electricity consumption level')
    s: int = Field(ge=0, le=1, title='Social & Commercial uses')
    g: int = Field(ge=0, le=1, title='Grid generating cost of electricity')
    p: int = Field(ge=0, le=1, title='PV System cost')
    i: int = Field(ge=0, le=1, title='Intermediate investment plan')
    r: int = Field(ge=0, le=1, title='Rollout plan')

    @classmethod
    def parse(cls, filename: str) -> 'OnSSetFilename':
        m = _regex.match(filename)
        if m:
            return cls(**m.groupdict())
        raise Exception(f'filename {filename} not valid!')

    @property
    def scenario(self) -> str:
        return f'{self.v}-{self.t}_{self.s}_{self.g}_{self.p}_{self.i}_{self.r}'
