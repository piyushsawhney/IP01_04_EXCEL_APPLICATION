import datetime
import os

import pandas as pd

import financial_functions
import sql_scripts
import summary_sheet
import transaction_sheet
from database import execute_query
from process_transactions import get_folio_transactions, get_folio_summary
from workbook import save_workbook


def generate_statement(pan, name):
    statement = sql_scripts.DISTINCT_FOLIO_SCHEME_CODE.replace('(panNumber)', pan)
    distinct_schemes = execute_query(statement)
    summary_sheet.create_summary_sheet(pan, name)
    transaction_sheet.create_transaction_sheet()
    total_current_value = 0
    list_of_transactions = []
    for scheme in distinct_schemes:
        transactions = get_folio_transactions(scheme[0], scheme[1])
        summary = get_folio_summary(scheme[0], scheme[1], scheme[3], scheme[4], transactions.copy())

        summary_sheet.update_summary_sheet(summary[:-2], pan)
        list_of_tupple = transaction_sheet.update_transaction_sheet(summary, transactions)
        list_of_transactions = list_of_tupple + list_of_transactions
        total_current_value = total_current_value + summary[6]
    print(total_current_value)
    list_of_transactions.append((datetime.date.today(), -total_current_value))
    df = pd.DataFrame(list_of_transactions,
                      columns=["date", "gross_amount"])
    df['amount'] = df['gross_amount'].astype(float)

    summary_sheet.finish_summary_page(financial_functions.xirr(df))

    transaction_sheet.finish_transaction_page()
    save_workbook(pan)
    return True


if __name__ == '__main__':
    investor_name = input("Enter Investor Name: ")
    result = execute_query(sql_scripts.CLIENT_PAN_SEARCH.replace("(investorName)", investor_name))
    for row in result:
        print(row)
    user_pan = input("Enter Pan Number: ")[:10]
    name = [item for item in result if item[0] == user_pan.upper()][0][1]
    if generate_statement(user_pan, name):
        file_name = f"files\\{user_pan.upper()}.xlsx"
        os.startfile(file_name)
