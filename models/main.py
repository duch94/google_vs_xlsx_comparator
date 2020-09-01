from dataclasses import dataclass

from models.base import BaseTable, BaseRow


class Mains(BaseTable):

    def _parse_xlsx_worksheet(self, sheet):
        self.rows = []
        i = 1  # 1 if there is a header
        while True:
            i += 1
            id = sheet['A%d' % i].value
            if id is None:
                break
            source_component = sheet['B%d' % i].value
            label = sheet['C%d' % i].value
            version = sheet['D%d' % i].value
            type = sheet['E%d' % i].value
            description = sheet['F%d' % i].value
            self.rows.append(
                MainRow(
                    id,
                    source_component,
                    label,
                    version,
                    type,
                    description,
                )
            )

    def _parse_google_worksheet(self, sheet):
        self.rows = []
        i = 1  # 1 if there is a header
        while True:
            if i >= (len(sheet) - 1):
                break
            id = sheet[i]['values'][0]['effectiveValue']['stringValue']
            source_component = sheet[i]['values'][1]['effectiveValue']['stringValue']
            label = sheet[i]['values'][2]['effectiveValue']['stringValue']
            version = sheet[i]['values'][3]['effectiveValue']['numberValue']
            type = sheet[i]['values'][4]['effectiveValue']['stringValue']
            description = sheet[i]['values'][5]['effectiveValue']['stringValue']
            self.rows.append(
                MainRow(
                    id,
                    source_component,
                    label,
                    version,
                    type,
                    description,
                )
            )
            i += 1


@dataclass
class MainRow(BaseRow):
    id: str
    source_component: str
    label: str
    version: str
    type: str
    description: str
