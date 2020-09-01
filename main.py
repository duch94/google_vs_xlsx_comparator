from typing import Dict
import argparse
import logging
import sys

from openpyxl import load_workbook
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import gspread

from models.main import Mains
from models.description import Descriptions
from models.extra import Extras
from models.base import BaseTable

log_format = '[%(levelname)s][%(name)s][line:%(lineno)d][%(asctime)s]: %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=log_format)
logger = logging.getLogger(__name__)


def load_google_spreadsheet(sheet_id: str, creds_path: str) -> dict:
    scopes = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scopes)
    service = discovery.build('sheets', 'v4', credentials=creds)
    resp = service.spreadsheets().get(spreadsheetId=sheet_id, includeGridData=True).execute()

    for sheet in resp['sheets']:
        if sheet['properties']['title'] == 'Description':
            description_gs = Descriptions(sheet['data'][0]['rowData'])
        elif sheet['properties']['title'] == 'Main':
            main_gs = Mains(sheet['data'][0]['rowData'])
        elif sheet['properties']['title'] == 'Extra':
            extra_gs = Extras(sheet['data'][0]['rowData'])
    return {
        'Description': description_gs,
        'Main': main_gs,
        'Extra': extra_gs,
    }


def parse_sheet_id(gs_url: str):
    if 'https://docs.google.com' not in gs_url:
        raise ValueError('Invalid google spreadsheet url: domain must be docs.google.com and protocol should be https')
    sheet_id = gs_url.split('/')[5]
    return sheet_id


def load_xlsx(path: str) -> Dict[str, BaseTable]:
    wb = load_workbook(path)
    for sheet in wb.worksheets:
        if sheet.title == 'Main':
            main_xlsx = Mains(sheet)
        elif sheet.title == 'Description':
            description_xlsx = Descriptions(sheet)
        elif sheet.title == 'Extra':
            extra_xlsx = Extras(sheet)
    return {
        'Description': description_xlsx,
        'Main': main_xlsx,
        'Extra': extra_xlsx,
    }


def update_gs_with_new_data(tables: Dict[str, BaseTable], sheet_id: str, path_to_creds: str):
    gs = gspread.service_account(
        filename=path_to_creds,
        scopes=['https://www.googleapis.com/auth/spreadsheets'],
    )
    remote_sheets = gs.open_by_key(sheet_id)
    for table in tables.keys():
        sh = remote_sheets.worksheet(table)
        current_table = tables[table].get_table()
        if table == 'Description':
            sh.update('A1', current_table)
        else:
            sh.update('A2', current_table)


def get_difference(xlsx: Dict[str, BaseTable], gs: Dict[str, BaseTable], update_gs_with_xlsx: bool) \
        -> Dict[str, BaseTable]:
    tables = ['Description', 'Main', 'Extra']
    new_gs: Dict[str, BaseTable] = {}
    gs_changed = False
    for table_name in tables:
        if table_name == 'Description':
            new_gs[table_name] = Descriptions(None)
        elif table_name == 'Main':
            new_gs[table_name] = Mains(None)
        elif table_name == 'Extra':
            new_gs[table_name] = Extras(None)
        table_xlsx = xlsx[table_name]
        table_gs = gs[table_name]
        for i in range(len(table_xlsx)):
            xlsx_row = table_xlsx.get(i)
            gs_row = table_gs.get(i)
            equals = xlsx_row == gs_row
            if not equals:
                logger.info('Row in xlsx is different from google spreadsheet:\n'
                            '  xlsx = %s\n'
                            '    gs = %s' % (xlsx_row, gs_row))
                if update_gs_with_xlsx:
                    new_gs[table_name].append(xlsx_row)
                    gs_changed = True
                    continue
                new_gs[table_name].append(gs_row)
                continue
            new_gs[table_name].append(xlsx_row)
    if gs_changed and update_gs_with_xlsx:
        return new_gs
    return {}


def main(xlsx_path: str, gs_url: str, gs_creds_path: str, update_gs: bool):
    gs = load_google_spreadsheet(parse_sheet_id(gs_url), gs_creds_path)
    xlsx = load_xlsx(xlsx_path)
    new_gs = get_difference(gs=gs, xlsx=xlsx, update_gs_with_xlsx=update_gs)
    if update_gs:
        update_gs_with_new_data(new_gs, parse_sheet_id(gs_url), gs_creds_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--xl',
        required=True,
        help='Path to xlsx file',
    )
    parser.add_argument(
        '--gs',
        required=True,
        help='URL where google spreadsheet can be found',
    )
    parser.add_argument(
        '--gs_creds_path',
        required=True,
        help='Path to credentials for service account which has access to google sheets.\n'
             'Service account can be crated here https://console.cloud.google.com/apis/credentials',
    )
    parser.add_argument(
        '--update_gs',
        default=False,
        help='If set, then google spreadsheet will be updated with xlsx data',
        type=bool,
    )
    args = parser.parse_args()
    main(args.xl, args.gs, args.gs_creds_path, args.update_gs)
