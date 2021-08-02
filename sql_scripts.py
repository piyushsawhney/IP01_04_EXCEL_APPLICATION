import json

db_config_path = f'config/db_config.json'
with open(db_config_path, "r") as json_file:
    config = json.load(json_file)

MF_CLIENT = config['mf_client_schema']
RTA_SCHEMA = config['rta_schema']
TRANSACTION_TABLE = config['transaction_table']
FOLIO_TABLE = config['folio_table']
COST_TABLE = config['cost_table']
NAV_TABLE = config['nav_table']

CLIENT_PAN_SEARCH = f"select distinct pan, UPPER(investor_name) from {MF_CLIENT}.{FOLIO_TABLE} where investor_name ilike '%(investorName)%';"
CLIENT_DISTINCT_SCHEME = f"SELECT distinct scheme_code,folio_number from {MF_CLIENT}.{TRANSACTION_TABLE} where pan ilike '(panNumber)' ORDER BY folio_number,scheme_code;"

CLIENT_SCHEME_DETAILS = f"SELECT scheme_name from {MF_CLIENT}.{TRANSACTION_TABLE} where folio_number = '(folioNumber)' and scheme_code = '(schemeCode)' ORDER BY nav_date LIMIT 1;"
CLIENT_SCHEME_UNITS = f"SELECT folio_number,scheme_code, sum(units) from {MF_CLIENT}.{TRANSACTION_TABLE} where folio_number = '(folioNumber)' and scheme_code = '(schemeCode)' GROUP BY folio_number,scheme_code;"

SCHEME_DETAILS = f"SELECT scheme_type, nav,nav_date,scheme_category from {RTA_SCHEMA}.{NAV_TABLE} where rta_product_code = '(schemeCode)';"

CLIENT_TRANSACTION_GROUP = f"SELECT transaction_code, SUM(gross_amount) as amount, SUM(units) as units FROM {MF_CLIENT}.{TRANSACTION_TABLE} WHERE folio_number = '(folioNumber)' and scheme_code = '(schemeCode)' GROUP BY transaction_code ORDER BY transaction_code;"
CLIENT_TRANSACTION_DETAILS = f"SELECT nav_date, concat(transaction_type,transaction_suffix), units, nav, gross_amount, sum(units) over (PARTITION BY scheme_code ORDER BY nav_date,transaction_id) from {MF_CLIENT}.{TRANSACTION_TABLE} where folio_number = '(folioNumber)' and scheme_code = '(schemeCode)' ORDER BY nav_date;"

yearly_sum = f"SELECT SUM(gross_amount) as amount, SUM(units) as units, transaction_code, to_char(nav_date, 'YYYY') as year_month FROM mf_reports.consolidated_transactions WHERE pan = '(panNumber)' GROUP BY transaction_code, year_month ORDER BY year_month;"

DISTINCT_FOLIO_SCHEME_CODE = f"select f.scheme_code,f.folio_number, f.arn, f.scheme_name, f.total_units from {MF_CLIENT}.{FOLIO_TABLE} f where f.pan ilike '(panNumber)' order by f.current_value DESC"
FOLIO_COST_VALUE = f"SELECT sum(cost_value) from {MF_CLIENT}.{COST_TABLE} WHERE folio_number = '(folioNumber)' and scheme_code = '(schemeCode)' AND (transaction_code = 'P' OR transaction_code = 'PR')"
FOLIO_SWITCH_IN_VALUE = f"SELECT sum(cost_value) from {MF_CLIENT}.{COST_TABLE} WHERE folio_number = '(folioNumber)' and scheme_code = '(schemeCode)' AND (transaction_code = 'SI' OR transaction_code = 'SIR')"
FOLIO_SWITCH_OUT_VALUE = f"SELECT sum(cost_value) from {MF_CLIENT}.{COST_TABLE} WHERE folio_number = '(folioNumber)' and scheme_code = '(schemeCode)' AND (transaction_code = 'SO' OR transaction_code = 'SOR')"
FOLIO_REDEMPTION_VALUE = f"SELECT sum(cost_value) from {MF_CLIENT}.{COST_TABLE} WHERE folio_number = '(folioNumber)' and scheme_code = '(schemeCode)' AND transaction_code = 'R'"
NAV_DETAILS = f"SELECT scheme_type, nav,nav_date,scheme_category from {RTA_SCHEMA}.{NAV_TABLE} where rta_product_code = '(schemeCode)';"
