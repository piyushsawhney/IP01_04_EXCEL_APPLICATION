import datetime

import pandas as pd

import database
import financial_functions
import sql_scripts


def group_transactions(list):
    my_dict = {}
    for transaction_type in list:
        my_dict[transaction_type[0]] = {}
        my_dict[transaction_type[0]]['amount'] = transaction_type[1]
        my_dict[transaction_type[0]]['units'] = transaction_type[2]
    return my_dict


def calculate_current_value(current_nav, total_units):
    return float(current_nav) * float(total_units)


def thread_based_database_query(statement):
    return database.execute_query(statement)


def get_folio_transactions(scheme_code, folio_no):
    statement_5 = sql_scripts.CLIENT_TRANSACTION_DETAILS.replace('(folioNumber)', folio_no).replace(
        '(schemeCode)', scheme_code)
    return database.execute_query(statement_5)


def get_folio_systematic_plans(scheme_code, folio_no):
    statement_1 = sql_scripts.SYSTEMATIC_DETAILS.replace('(folioNumber)', folio_no).replace(
        '(schemeCode)', scheme_code)
    return database.execute_query(statement_1)


def get_folio_scheme_summary(scheme_code, folio_no, list_of_tuple):
    statement_1 = sql_scripts.CLIENT_SCHEME_UNITS.replace('(folioNumber)', folio_no).replace(
        '(schemeCode)', scheme_code)
    statement_2 = sql_scripts.CLIENT_SCHEME_DETAILS.replace('(folioNumber)', folio_no).replace(
        '(schemeCode)', scheme_code)
    statement_3 = sql_scripts.CLIENT_TRANSACTION_GROUP.replace('(folioNumber)', folio_no).replace(
        '(schemeCode)', scheme_code)
    statement_4 = sql_scripts.SCHEME_DETAILS.replace(
        '(schemeCode)', scheme_code)

    scheme_details_with_units = database.execute_query(statement_1)[0]
    scheme_name = database.execute_query(statement_2)[0]
    transaction_groups = database.execute_query(statement_3)

    groupings = group_transactions(transaction_groups)
    current_value = 0
    current_nav = None
    nav_date = None
    if scheme_details_with_units[2] < -0.01 or scheme_details_with_units[2] > 0.01:
        scheme_details = database.execute_query(statement_4)
        if scheme_details is not None and len(scheme_details) > 0:
            current_value = calculate_current_value(scheme_details[0][1], scheme_details_with_units[2])
            my_tupple = (datetime.date.today(), None, None, None, -float(current_value), None)
            list_of_tuple.append(my_tupple)
            current_nav = scheme_details[0][1]
            nav_date = scheme_details[0][2]

    cost_value = groupings['P']['amount'] if 'P' in groupings.keys() and 'amount' in groupings['P'].keys() else 0
    purchase_rejection = groupings['PR']['amount'] if 'PR' in groupings.keys() and 'amount' in groupings[
        'PR'].keys() else 0
    redemption_value = groupings['R']['amount'] if 'R' in groupings.keys() and 'amount' in groupings['R'].keys() else 0
    df = pd.DataFrame(list_of_tuple, columns=["date", "transaction_prefix", "units", "nav", "gross_amount", "units"])
    df['amount'] = df['gross_amount'].astype(float)

    # FOLIO Number, Scheme Name, Cost Value, Redemptions, Current Value, Total Units, Returns, Nav Date, Current NAV
    return (
        scheme_details_with_units[0], scheme_name[0], cost_value + purchase_rejection, redemption_value, current_value,
        scheme_details_with_units[2],
        financial_functions.xirr(df), nav_date, current_nav)


def get_folio_summary(scheme_code, folio_number, scheme_name, unit_balance, list_of_tuple):
    df = pd.DataFrame()
    statement_1 = sql_scripts.FOLIO_COST_VALUE.replace('(folioNumber)', folio_number).replace(
        '(schemeCode)', scheme_code)
    statement_2 = sql_scripts.NAV_DETAILS.replace(
        '(schemeCode)', scheme_code)
    statement_3 = sql_scripts.FOLIO_REDEMPTION_VALUE.replace('(folioNumber)', folio_number).replace(
        '(schemeCode)', scheme_code)
    statement_4 = sql_scripts.FOLIO_SWITCH_IN_VALUE.replace('(folioNumber)', folio_number).replace(
        '(schemeCode)', scheme_code)
    statement_5 = sql_scripts.FOLIO_SWITCH_OUT_VALUE.replace('(folioNumber)', folio_number).replace(
        '(schemeCode)', scheme_code)

    cost_value = database.execute_query(statement_1)[0][0]
    redemption_value = database.execute_query(statement_3)[0][0]
    switch_in_value = database.execute_query(statement_4)[0][0]
    switch_out_value = database.execute_query(statement_5)[0][0]
    nav_details = database.execute_query(statement_2)
    current_value = 0
    current_nav = None
    nav_date = None
    if nav_details is not None and len(nav_details) > 0:
        current_nav = nav_details[0][1]
        nav_date = nav_details[0][2]
        current_value = calculate_current_value(nav_details[0][1], unit_balance)
        if unit_balance > 0.01:
            xirr_last_row = (datetime.date.today(), None, None, None, -float(current_value), None)
            list_of_tuple.append(xirr_last_row)
    if list_of_tuple:
        df = pd.DataFrame(list_of_tuple,
                          columns=["date", "transaction_prefix", "units", "nav", "gross_amount", "units"])
        df['amount'] = df['gross_amount'].astype(float)

    # FOLIO Number, Scheme Name, Cost Value, Redemptions, Switch In, Switch Out, Current Value, Total Units, Returns, Nav Date, Current NAV
    return (
        folio_number, scheme_name, cost_value if cost_value else 0.0, redemption_value if redemption_value else 0.0,
        switch_in_value if switch_in_value else 0.0,
        switch_out_value if switch_out_value else 0.0, current_value, unit_balance,
        financial_functions.xirr(df) if not df.empty else 0.0, nav_date, current_nav)
