from dataclasses import dataclass

from models.base import BaseTable, BaseRow


class Extras(BaseTable):

    def _parse_xlsx_worksheet(self, sheet):
        self.rows = []
        i = 1  # 1 if there is a header
        while True:
            i += 1
            id = sheet['A%d' % i].value
            if id is None:
                break
            source_component = sheet['B%d' % i].value
            message_name = sheet['C%d' % i].value
            signal_in_message = sheet['D%d' % i].value
            label = sheet['E%d' % i].value
            self.rows.append(
                ExtraRow(
                    id,
                    source_component,
                    message_name,
                    signal_in_message,
                    label,
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
            message_name = sheet[i]['values'][2]['effectiveValue']['stringValue']
            signal_in_message = sheet[i]['values'][3]['effectiveValue']['stringValue']
            label = sheet[i]['values'][4]['effectiveValue']['stringValue']
            self.rows.append(
                ExtraRow(
                    id,
                    source_component,
                    message_name,
                    signal_in_message,
                    label,
                )
            )
            i += 1


@dataclass
class ExtraRow(BaseRow):
    id: str
    source_component: str
    message_name: str
    signal_in_message: str
    label: str
