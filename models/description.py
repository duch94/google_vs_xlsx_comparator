from dataclasses import dataclass

from models.base import BaseTable, BaseRow


class Descriptions(BaseTable):

    def _parse_xlsx_worksheet(self, sheet):
        self.rows = []
        i = 0  # 1 if there is a header
        while True:
            i += 1
            text = sheet['A%d' % i].value
            if text is None:
                break
            self.rows.append(
                DescriptionRow(
                    text
                )
            )

    def _parse_google_worksheet(self, sheet):
        self.rows = []
        i = 0  # 1 if there is a header
        while True:
            if i >= len(sheet):
                break
            text = sheet[i]['values'][0]['effectiveValue']['stringValue']
            self.rows.append(
                DescriptionRow(
                    text
                )
            )
            i += 1


@dataclass
class DescriptionRow(BaseRow):
    text: str
