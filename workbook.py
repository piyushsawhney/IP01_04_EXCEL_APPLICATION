from openpyxl import Workbook

directory = "files/"
wb = Workbook()


def get_workbook():
    return wb


def save_workbook(file_name):
    file_name = f'{directory}{file_name.upper()}.xlsx'
    wb.save(file_name)
