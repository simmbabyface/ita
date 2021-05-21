import psycopg2
import pandas as pd
import numpy as np
import os


conn = psycopg2.connect(user = "babyface", password = "5555", host = "localhost", port = "5432", database = "ita")
conn.set_client_encoding('utf-8')
cur = conn.cursor()


def create_sample_table():
	clause1 = 'CREATE SEQUENCE sample_id_seq;'
	clause2 = """CREATE TABLE sample(sample_id CHAR(10) NOT NULL DEFAULT to_char(nextval('sample_id_seq'),
	 '"S"0000000FM') PRIMARY KEY,
	 sampling_name VARCHAR (50) NOT NULL,
	 sampling_location VARCHAR (50),
	 sampling_time TIMESTAMP,
	 sample_type VARCHAR,
	 sample_weight VARCHAR,
	 pretreatment_method VARCHAR,
	 AES_extraction VARCHAR,
	 nitrogen_flow VARCHAR,
	 three_line_processing VARCHAR,
	 lc_preparation VARCHAR,
	 sampling_person VARCHAR (10)
	 );"""
	clause3 = 'ALTER SEQUENCE sample_id_seq OWNED BY sample.sample_id;'
	cur.execute(clause1)
	cur.execute(clause2)
	cur.execute(clause3)
	conn.commit()

def create_component_table():
	clause1 = 'CREATE SEQUENCE component_id_seq;'
	clause2 = """CREATE TABLE component(
	 component_id CHAR(10) NOT NULL DEFAULT to_char(nextval('component_id_seq'), '"CP"0000000FM') PRIMARY KEY,
	 chemical_type VARCHAR,
	 MS_Type VARCHAR,
	 MS_Level VARCHAR
	 );"""
	clause3 = 'ALTER SEQUENCE component_id_seq OWNED BY component.component_id;'
	cur.execute(clause1)
	cur.execute(clause2)
	cur.execute(clause3)
	conn.commit()

def create_chemical_table():
	clause1 = 'CREATE SEQUENCE chemical_id_seq;'
	clause2 = """CREATE TABLE chemical(
	 chemical_id CHAR(10) NOT NULL DEFAULT to_char(nextval('chemical_id_seq'), 
	 '"C"0000000FM') PRIMARY KEY,
	 chemical_type VARCHAR,
	 MS_Type VARCHAR,
	 Chemical_mz VARCHAR,
	 chemical_name VARCHAR(50),
	 molecular_formula VARCHAR(50),
	 CAS VARCHAR(20),
	 canonical_smiles VARCHAR(100)
	);"""
	clause3 = 'ALTER SEQUENCE chemical_id_seq OWNED BY chemical.chemical_id;'
	cur.execute(clause1)
	cur.execute(clause2)
	cur.execute(clause3)
	conn.commit()

def create_assay_table():
	clause1 = 'CREATE SEQUENCE assay_id_seq;'
	clause2 = """CREATE TABLE assay(
 	 assay_id CHAR(10) NOT NULL DEFAULT to_char(nextval('assay_id_seq'), 
 	 '"A"0000000FM') PRIMARY KEY,
 	 Toxicity VARCHAR,
 	 Assay_name VARCHAR,
 	 Biological_process_target VARCHAR,
 	 Target_biomarker VARCHAR,
 	 Timepoint VARCHAR,
 	 Species VARCHAR, 
 	 Tissue_of_origin VARCHAR,
 	 Cell_type VARCHAR,
 	 Assay_footprint VARCHAR,
 	 Assay_format_type VARCHAR,
 	 Dilution_solvent VARCHAR,
 	 Bioactivity_type VARCHAR,
 	 Model VARCHAR,
 	 Detection_technology VARCHAR,
 	 Signal_type VARCHAR,
 	 Endpoint_description VARCHAR,
 	 Positive_control VARCHAR,
 	 Negative_control VARCHAR,
 	 Assay_provider VARCHAR
	 );"""
	clause3 = 'ALTER SEQUENCE assay_id_seq OWNED BY assay.assay_id;'
	cur.execute(clause1)
	cur.execute(clause2)
	cur.execute(clause3)
	conn.commit()

def create_sample_assay_table():
	clause1 = """CREATE TABLE sample_assay (
	 sample_assay_id SERIAL PRIMARY KEY,
	 sample_id CHAR(10) NOT NULL,
	 assay_id CHAR(10) NOT NULL,
	 FOREIGN KEY (sample_id) REFERENCES sample(sample_id) ON DELETE CASCADE,
	 FOREIGN KEY (assay_id) REFERENCES assay(assay_id) ON DELETE CASCADE,
	 assay_time TIMESTAMP,
	 model VARCHAR(10),
	 bottom VARCHAR,
	 top VARCHAR,
	 logEC50 VARCHAR,
	 hill_slope VARCHAR,
	 span VARCHAR,
	 EC50 VARCHAR,
	 conc_unit VARCHAR(20)
	 );"""
	cur.execute(clause1)
	conn.commit()

def create_chemical_assay_table():
	clause1 = """CREATE TABLE chemical_assay (
	 chemical_assay_id SERIAL PRIMARY KEY,
	 chemical_id CHAR(10) NOT NULL,
	 assay_id CHAR(10) NOT NULL,
	 FOREIGN KEY (chemical_id) REFERENCES chemical(chemical_id) ON DELETE CASCADE,
	 FOREIGN KEY (assay_id) REFERENCES assay(assay_id) ON DELETE CASCADE,
	 assay_time TIMESTAMP,
	 model VARCHAR(10),
	 bottom VARCHAR,
	 top VARCHAR,
	 logEC50 VARCHAR,
	 hill_slope VARCHAR,
	 span VARCHAR,
	 EC50 VARCHAR,
	 conc_unit VARCHAR(20)
	 );
	"""
	cur.execute(clause1)
	conn.commit()

def create_sample_chemical_table():
	clause1 = """CREATE TABLE sample_chemical (
	 sample_chemical_id SERIAL PRIMARY KEY,
	 sample_id CHAR(10) NOT NULL,
	 chemical_id CHAR(10) NOT NULL,
	 FOREIGN KEY (sample_id) REFERENCES sample(sample_id) ON DELETE CASCADE,
	 FOREIGN KEY (chemical_id) REFERENCES chemical(chemical_id) ON DELETE CASCADE,
	 assay_time TIMESTAMP,
	 concentration VARCHAR(10),
	 conc_unit VARCHAR(10)
	 );
	"""
	cur.execute(clause1)
	conn.commit()

def create_sample_component_table():
	clause1 = """CREATE TABLE sample_component (
	 sample_component_id SERIAL PRIMARY KEY,
	 sample_id CHAR(10) NOT NULL,
	 component_id CHAR(10) NOT NULL,
	 FOREIGN KEY (sample_id) REFERENCES sample(sample_id) ON DELETE CASCADE,
	 FOREIGN KEY (component_id) REFERENCES component(component_id) ON DELETE CASCADE,
	 assay_time TIMESTAMP
	 );
	"""
	cur.execute(clause1)
	conn.commit()

def create_component_assay_table():
	clause1 = """CREATE TABLE component_assay (
	 component_assay_id SERIAL PRIMARY KEY,
	 component_id CHAR(10) NOT NULL,
	 assay_id CHAR(10) NOT NULL,
	 FOREIGN KEY (component_id) REFERENCES component(component_id) ON DELETE CASCADE,
	 FOREIGN KEY (assay_id) REFERENCES assay(assay_id) ON DELETE CASCADE,
	 assay_time TIMESTAMP,
	 model VARCHAR(10),
	 bottom VARCHAR,
	 top VARCHAR,
	 logEC50 VARCHAR,
	 hill_slope VARCHAR,
	 span VARCHAR,
	 EC50 VARCHAR,
	 conc_unit VARCHAR(20)
	 );
	"""
	cur.execute(clause1)
	conn.commit()

def create_component_chemical_table():
	clause1 = """CREATE TABLE component_chemical (
	 component_chemical_id SERIAL PRIMARY KEY,
	 component_id CHAR(10) NOT NULL,
	 chemical_id CHAR(10),
	 FOREIGN KEY (component_id) REFERENCES component(component_id) ON DELETE CASCADE,
	 assay_time TIMESTAMP,
	 concentration VARCHAR(10),
	 conc_unit VARCHAR(20)
	 );
	"""
	cur.execute(clause1)
	conn.commit()

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
		print(values)
		clause = 'INSERT INTO %s (%s) VALUES (%s);' % (table_name, columns, values)
		cur.execute(clause)
	conn.commit()


def main():	
	# Clean Database
	cur.execute('drop owned by babyface;')
	conn.commit()
	
	table_names = [
		'sample',
		'component',
		'chemical',
		'assay',
		'sample_assay',
		'chemical_assay',
		'sample_chemical',
		'sample_component',
		'component_assay',
		'component_chemical'
	]
	# for table_name in table_names:
	# 	clause = 'select \'drop table if exists \"\' || %s || \'\" cascade;\'' % (table_name)
	# 	cur.execute(clause)
	# 	conn.commit()

	# Create Tables
	create_sample_table()
	create_component_table()
	create_chemical_table()
	create_assay_table()

	create_sample_assay_table()
	create_chemical_assay_table()
	create_sample_chemical_table()
	create_sample_component_table()
	create_component_assay_table()
	create_component_chemical_table()

	# Insert data
	for table_name in table_names:
		file_name = os.path.join('..', 'data', table_name + '.csv')
		print(file_name)
		table_df = pd.read_csv(file_name, header=0, index_col=None, encoding='utf-8')
		insert_data(table_name, table_df)

if __name__ == '__main__':
	main()
