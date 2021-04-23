import json

db_config_path = f'config/db_config.json'
with open(db_config_path, "r") as json_file:
    config = json.load(json_file)

SCHEMA = config['schema']
TRANSACTION_TABLE = config['transaction_table']
NAV_TABLE = config['nav_table']

CLIENT_PAN_SEARCH = f"select distinct pan, UPPER(investor_name) from {SCHEMA}.{TRANSACTION_TABLE} where investor_name ilike '%(investorName)%';"
CLIENT_DISTINCT_SCHEME = f"SELECT distinct scheme_code,folio_number from {SCHEMA}.{TRANSACTION_TABLE} where pan ilike '(panNumber)' ORDER BY folio_number,scheme_code;"

CLIENT_SCHEME_DETAILS = f"SELECT scheme_name from {SCHEMA}.{TRANSACTION_TABLE} where folio_number = '(folioNumber)' and scheme_code = '(schemeCode)' ORDER BY nav_date LIMIT 1;"
CLIENT_SCHEME_UNITS = f"SELECT folio_number,scheme_code, sum(units) from {SCHEMA}.{TRANSACTION_TABLE} where folio_number = '(folioNumber)' and scheme_code = '(schemeCode)' GROUP BY folio_number,scheme_code;"

SCHEME_DETAILS = f"SELECT scheme_type, nav,nav_date,scheme_category from {SCHEMA}.{NAV_TABLE} where rta_product_code = '(schemeCode)';"

CLIENT_TRANSACTION_GROUP = f"SELECT transaction_code, SUM(gross_amount) as amount, SUM(units) as units FROM {SCHEMA}.{TRANSACTION_TABLE} WHERE folio_number = '(folioNumber)' and scheme_code = '(schemeCode)' GROUP BY transaction_code;"
CLIENT_TRANSACTION_DETAILS = f"SELECT nav_date, transaction_prefix, units, nav, gross_amount, sum(units) over (PARTITION BY scheme_code ORDER BY nav_date) from {SCHEMA}.{TRANSACTION_TABLE} where folio_number = '(folioNumber)' and scheme_code = '(schemeCode)' ORDER BY nav_date;"

yearly_sum = f"SELECT SUM(gross_amount) as amount, SUM(units) as units, transaction_code, to_char(nav_date, 'YYYY') as year_month FROM mf_reports.consolidated_transactions WHERE pan = '(panNumber)' GROUP BY transaction_code, year_month ORDER BY year_month;"
