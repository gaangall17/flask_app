from google.cloud import bigquery

client = bigquery.Client()

# Perform a query.
QUERY = (
    'SELECT * FROM `ec-ist-ve-operation-dev.00003_dist_aapp_anc.t_asset_reg` LIMIT 100' )
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print(row.name)