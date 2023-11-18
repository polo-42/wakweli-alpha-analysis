import psycopg2
import pandas as pd

db_params = {
    'host': '165.227.135.43',
    'port': 5432,
    'database': 'wakweli_alpha_name',  
    'user': 'postgres',
    'password': 'DyW0BQ5MtZ7EtJk'
}

try:
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

except Exception as e:
    print(f"Error: {e}")
        
csv_file_path = 'asset_list.csv'

df = pd.read_csv(csv_file_path, delimiter='\t')

contract_address = df.iloc[:, 0]
contract_id = df.iloc[:, 1]
contract_state = df.iloc[:, 2]

count_good=0
count_bad=0
for i in range(len(contract_address)):
    address = contract_address[i]
    ids = contract_id[i]

    query = "SELECT status FROM certificates WHERE contract_address=%s AND token_id=%s"
    cursor.execute(query, (address, ids))

    rows = cursor.fetchall()
    if rows:
        rows = rows[-1][0]
        if rows == 'granted':
            if contract_state[i]=='V':
                count_good += 1
            else:
                count_bad += 1
        elif rows == 'rejected':
            if contract_state[i]=='F':
                count_good += 1
            else:
                count_bad += 1
            
print(count_good/(count_good+count_bad))


connection.close()