import sql_scripts
import summary_sheet
import transaction_sheet
from database import execute_query
from process_transactions import get_folio_scheme_summary, get_folio_transactions
from workbook import save_workbook


def generate_statement(pan, name):
    statement = sql_scripts.CLIENT_DISTINCT_SCHEME.replace('(panNumber)', pan)
    distinct_schemes = execute_query(statement)
    summary_sheet.create_summary_sheet(pan, name)
    transaction_sheet.create_transaction_sheet()
    for scheme in distinct_schemes:
        transactions = get_folio_transactions(scheme[0], scheme[1])
        summary = get_folio_scheme_summary(scheme[0], scheme[1], transactions.copy())
        summary_sheet.update_summary_sheet(summary[:-2], pan)
        transaction_sheet.update_transaction_sheet(summary, transactions)
    summary_sheet.finish_summary_page()
    transaction_sheet.finish_transaction_page()
    save_workbook(pan)


if __name__ == '__main__':
    investor_name = input("Enter Investor Name: ")
    result = execute_query(sql_scripts.CLIENT_PAN_SEARCH.replace("(investorName)", investor_name))
    for row in result:
        print(row)
    user_pan = input("Enter Pan Number: ")[:10]
    name = [item for item in result if item[0] == user_pan.upper()][0][1]
    generate_statement(user_pan, name)
