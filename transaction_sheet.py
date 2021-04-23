from openpyxl.styles import Font
from openpyxl.styles.numbers import FORMAT_NUMBER_00, FORMAT_DATE_XLSX15
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.dimensions import ColumnDimension

import workbook

wb = workbook.get_workbook()


def create_transaction_sheet():
    transaction = wb.create_sheet("Transactions")
    ColumnDimension(transaction, bestFit=True)
    transaction.append(
        (("NAV Date", "Transaction Type", "Units", "NAV", "Amount", "Total Units")))
    row = transaction.row_dimensions[transaction.max_row]
    row.font = Font(bold=True)


def update_transaction_sheet(summary_details, transactions):
    transaction = wb["Transactions"]
    transaction.append((summary_details[1],))
    for transaction_tupple in transactions:
        transaction.append((transaction_tupple))
    transaction.append(())
    transaction.append(("", "Current NAV: ", summary_details[8], "Left Over Cost: ", ""))
    transaction.append(("", "NAV Date: ", summary_details[7], "Current Value: ", summary_details[4]))
    transaction.append(())


def finish_transaction_page():
    ws = wb["Transactions"]
    ws.page_setup.fitToHeight = 1
    ws.page_setup.fitToWidth = 1
    for row in range(1, ws.max_row + 1):
        ws.cell(row=row, column=5).number_format = FORMAT_NUMBER_00

    for i in range(1, ws.max_column + 1):
        letter = get_column_letter(i)
        ws.column_dimensions[get_column_letter(i)].best_fit = False
        ws.column_dimensions[get_column_letter(i)].auto_size = True

        ColumnDimension(ws, index=letter, width=16)
