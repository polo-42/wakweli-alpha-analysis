import csv, numpy as np, psycopg2

db_params = {
        'host': '165.227.135.43',
        'port': 5432,
        'database': 'wakweli_alpha_name',  
        'user': 'postgres',
        'password': 'DyW0BQ5MtZ7EtJk'  
    }

    
connection = psycopg2.connect(**db_params)
cursor = connection.cursor()

with open("assets_tf.csv",newline='') as fr:
    spam = csv.DictReader(fr)
    all = [(row['Contract address'],row['Token ID'], row['Blockchain'],row['V/F']) for row in spam]
    obloquies = [row for row in all if row[3] == 'F']
    certificates = [row for row in all if row[3] == 'V']

total = 0
true = 0
false = 0
for ob in obloquies:
    
    sql_request = f"""
        SELECT status
        FROM certificates
        WHERE contract_address = '{ob[0]}' AND token_id = '{ob[1]}'
        AND (status = 'rejected' OR status = 'granted');
    """
    cursor.execute(sql_request)
    response = cursor.fetchone()

    if response == None:
        continue
    else:
        total+=1
        if response[0] == 'rejected':
            true += 1
        else:
            false += 1
obloquies_stats = {
    "total":total,
    "true":true,
    "false":false,
    "accuracy":true/total,
}

total = 0
true = 0
false = 0
for cert in certificates:
    
    sql_request = f"""
        SELECT status
        FROM certificates
        WHERE contract_address = '{cert[0]}' AND token_id = '{cert[1]}'
        AND (status = 'rejected' OR status = 'granted');
    """
    cursor.execute(sql_request)
    response = cursor.fetchone()

    if response == None:
        continue
    else:
        total+=1
        if response[0] == 'granted':
            true += 1
        else:
            false += 1
certificates_stats = {
    "total":total,
    "true":true,
    "false":false,
    "accuracy":true/total,
}

cursor.close()
connection.close()

print(obloquies_stats)
print(certificates_stats)