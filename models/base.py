from typing import Union, List
from abc import ABC, abstractmethod
from dataclasses import dataclass

from openpyxl.worksheet.worksheet import Worksheet


@dataclass
class BaseRow:

    def __eq__(self, other):
        equals = True
        for k in self.__dict__.keys():
            equals *= bool(self.__dict__[k] == other.__dict__[k])
        return equals

    def get_row(self):
        row = []
        for k in self.__dict__.keys():
            row.append(self.__dict__[k])
        return row


class BaseTable(ABC):
    rows: List[BaseRow]

    def __init__(self, worksheet: Union[Worksheet, list, None]):
        if type(worksheet) == Worksheet:
            self._parse_xlsx_worksheet(worksheet)
        elif type(worksheet) == list:
            self._parse_google_worksheet(worksheet)
        elif worksheet is None:
            self.rows: List[BaseRow] = []

    def __len__(self):
        return len(self.rows)

    @abstractmethod
    def _parse_xlsx_worksheet(self, worksheet):
        pass

    @abstractmethod
    def _parse_google_worksheet(self, worksheet):
        pass

    def get(self, index: int) -> BaseRow:
        if index >= (len(self.rows) - 1):
            self.append(BaseRow())
        return self.rows[index]

    def get_by_id(self, identity: str):
        if "id" not in self.__dict__.keys():
            raise NotImplemented('There is no field ID in Row class %s' % type(self.rows[0]))
        for r in self.rows:
            if r.id == identity:
                return r

    def append(self, row: BaseRow):
        self.rows.append(row)

    def get_table(self) -> dict:
        table = []
        for r in self.rows:
            table.append(r.get_row())
        return table
