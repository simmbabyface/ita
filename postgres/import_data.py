import psycopg2
import pandas as pd
import numpy as np


conn = psycopg2.connect(user = "babyface", password = "5555", host = "localhost", port = "5432", database = "ita")
conn.set_client_encoding('GBK')
cur = conn.cursor()


def insert_data(table_name, table_df):
	columns = table_df.columns.tolist()
	columns = ','.join(columns)
	print(columns)
	for index in table_df.index:
		values = ""
		for item in list(table_df.loc[index,:]):
			if type(item) != str and np.isnan(item):
				values += "'', "
			else:
				item = str(item)
				values += "'" + item.strip() + "', "
		values = values[:-2]
		clause = 'INSERT INTO %s (%s) VALUES (%s);' % (table_name, columns, values)
		cur.execute(clause)
	conn.commit()



def main():
	# connect to database
	# table for sample
	# file_name = 'assay_update.csv'
	# file_name = 'component.csv'
	# file_name = 'sample.csv'
	# file_name = 'sample_component.csv'
	# file_name = 'sample_assay.csv'
	# file_name = 'component_assay.csv'
	file_name = 'chemical.csv'
	file_name = 'chemical_assay.csv'
	file_name = 'sample_chemical.csv'



	table_name = file_name.split('.')[0]
	table_df = pd.read_csv(file_name, header = 0, index_col=None, encoding='utf-8')
	insert_data(table_name, table_df)

	# # table for component
	# table = pd.read_csv('Target_summary.csv', header = 0, index_col=None, encoding='utf-8')


if __name__ == '__main__':
	main()
