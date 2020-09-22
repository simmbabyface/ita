import psycopg2
import pandas as pd
import numpy as np


conn = psycopg2.connect(user = "babyface", password = "5555", host = "localhost", port = "5432", database = "ita")
conn.set_client_encoding('GBK')
cur = conn.cursor()


def creat_sample_table():
	clause1 = 'CREATE SEQUENCE sample_id_seq;'
	clause2 = """CREATE TABLE sample(sample_id CHAR(10) NOT NULL DEFAULT to_char(nextval('sample_id_seq'),
	 '"S"0000000FM') PRIMARY KEY,
	 sampling_name VARCHAR (50) NOT NULL,
	 sampling_location VARCHAR (50),
	 sampling_person VARCHAR (10),
	 sampling_time TIMESTAMP,
	 sample_type VARCHAR,
	 sample_weight VARCHAR,
	 pretreatment_method VARCHAR,
	 AES_extraction VARCHAR,
	 nitrogen_flow VARCHAR,
	 three_line_processing VARCHAR,
	 lc_preparation VARCHAR
	 );"""
	clause3 = 'ALTER SEQUENCE sample_id_seq OWNED BY sample.sample_id;'
	cur.execute(clause1)
	cur.execute(clause2)
	cur.execute(clause3)
	conn.commit()


def creat_component_table():
	clause1 = 'CREATE SEQUENCE component_id_seq;'
	clause2 = """CREATE TABLE component(
	 component_id CHAR(10) NOT NULL DEFAULT to_char(nextval('component_id_seq'), '"CP"0000000FM') PRIMARY KEY,
	 component_name VARCHAR);"""
	clause3 = 'ALTER SEQUENCE component_id_seq OWNED BY component.component_id;'
	cur.execute(clause1)
	cur.execute(clause2)
	cur.execute(clause3)
	conn.commit()


def creat_chemical_table():
	clause1 = 'CREATE SEQUENCE chemical_id_seq;'
	clause2 = """CREATE TABLE chemical(
	 chemical_id CHAR(10) NOT NULL DEFAULT to_char(nextval('chemical_id_seq'), 
	 '"C"0000000FM') PRIMARY KEY,
	 chemical_type VARCHAR,
	 MS_Type VARCHAR,
	 MS_Level VARCHAR,
	 precursor_mz VARCHAR,
	 Total_Peaks VARCHAR,
	 mz_Top_Peak VARCHAR,
	 mz_2nd_Highest VARCHAR,
	 mz_3rd_Highest VARCHAR,
	 molecular_formula VARCHAR(50),
	 suspected_structure VARCHAR(50),
	 chemical_name VARCHAR(50),
	 CAS VARCHAR(20),
	 canonical_smiles VARCHAR(100)
	);"""
	clause3 = 'ALTER SEQUENCE chemical_id_seq OWNED BY chemical.chemical_id;'
	cur.execute(clause1)
	cur.execute(clause2)
	cur.execute(clause3)
	conn.commit()


def creat_assay_table():
	clause1 = 'CREATE SEQUENCE assay_id_seq;'
	clause2 = """CREATE TABLE assay(
 	 assay_id CHAR(10) NOT NULL DEFAULT to_char(nextval('assay_id_seq'), 
 	 '"A"0000000FM') PRIMARY KEY,
 	 toxicity VARCHAR,
 	 assay_name VARCHAR,
 	 biological_process_target VARCHAR,
 	 Target_biomarker VARCHAR,
 	 timepoint VARCHAR,
 	 Species VARCHAR, 
 	 Tissue_of_origin VARCHAR,
 	 Cell_type VARCHAR,
 	 assay_footprint VARCHAR,
 	 assay_format_type VARCHAR,
 	 dilution_solvent VARCHAR,
 	 Bioactivity_type VARCHAR,
 	 Model VARCHAR,
 	 detection_technology VARCHAR,
 	 Signal_type VARCHAR,
 	 endpoint_description VARCHAR,
 	 positive_control VARCHAR,
 	 negative_control VARCHAR,
 	 Assay_provider VARCHAR
	 );"""
	clause3 = 'ALTER SEQUENCE assay_id_seq OWNED BY assay.assay_id;'
	cur.execute(clause1)
	cur.execute(clause2)
	cur.execute(clause3)
	conn.commit()


def creat_user_table():
	clause1 = 'CREATE SEQUENCE user_id_seq;'
	clause2 = """CREATE TABLE users(
	 user_id CHAR(10) NOT NULL DEFAULT to_char(nextval('user_id_seq'), '"U"0000000FM') PRIMARY KEY,
	 user_name VARCHAR(10),
	 country VARCHAR(10),
	 password VARCHAR(10),
	 email VARCHAR(30),
	 organization VARCHAR(20),
	 date TIMESTAMP
	 );""" 
	clause3 = 'ALTER SEQUENCE user_id_seq OWNED BY users.user_id;'
	cur.execute(clause1)
	cur.execute(clause2)
	cur.execute(clause3)
	conn.commit()


def creat_analytical_method_table():
	clause1 = 'CREATE SEQUENCE anmethod_id_seq;'
	clause2 = """CREATE TABLE anmethod (
	 anmethod_id CHAR(10) NOT NULL DEFAULT to_char(nextval('anmethod_id_seq'), '"AM"0000000FM') PRIMARY KEY,
	 Separation_Phase VARCHAR(10),
	 Separation_System VARCHAR(10),
	 Separation_Mechanism VARCHAR(10),
	 Separation_Cycle VARCHAR(10),
	 Ionization_Polarity VARCHAR(20),
	 Ionization_Mode VARCHAR(10)
	 );""" 
	clause3 = 'ALTER SEQUENCE user_id_seq OWNED BY user.user_id;'
	cur.execute(clause1)
	cur.execute(clause2)
	cur.execute(clause3)
	conn.commit()


def creat_sample_assay_table():
	clause1 = """CREATE TABLE sample_assay (
	 sample_assay_id SERIAL PRIMARY KEY,
	 sample_id CHAR(10) NOT NULL,
	 assay_id CHAR(10) NOT NULL,
	 FOREIGN KEY (sample_id) REFERENCES sample(sample_id) ON DELETE CASCADE,
	 FOREIGN KEY (assay_id) REFERENCES assay(assay_id) ON DELETE CASCADE,
	 assay_time TIMESTAMP,
	 model VARCHAR(10),
	 n VARCHAR(10),
	 ac50 VARCHAR(10),
	 conc_unit VARCHAR(10)
	 );"""
	cur.execute(clause1)
	conn.commit()


def creat_chemical_assay_table():
	clause1 = """CREATE TABLE chemical_assay (
	 chemical_assay_id SERIAL PRIMARY KEY,
	 chemical_id CHAR(10) NOT NULL,
	 assay_id CHAR(10) NOT NULL,
	 FOREIGN KEY (chemical_id) REFERENCES chemical(chemical_id) ON DELETE CASCADE,
	 FOREIGN KEY (assay_id) REFERENCES assay(assay_id) ON DELETE CASCADE,
	 assay_time TIMESTAMP,
	 model VARCHAR(10),
	 n VARCHAR(10),
	 ac50 VARCHAR(10),
	 conc_unit VARCHAR(10)
	 );
	"""
	cur.execute(clause1)
	conn.commit()


def creat_sample_chemical_table():
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


def creat_sample_component_table():
	clause1 = """CREATE TABLE sample_component (
	 sample_component_id SERIAL PRIMARY KEY,
	 sample_id CHAR(10) NOT NULL,
	 component_id CHAR(10) NOT NULL,
	 FOREIGN KEY (sample_id) REFERENCES sample(sample_id) ON DELETE CASCADE,
	 FOREIGN KEY (component_id) REFERENCES chemical(component_id) ON DELETE CASCADE,
	 assay_time TIMESTAMP,
	 concentration VARCHAR(10),
	 conc_unit VARCHAR(10)
	 );
	"""
	cur.execute(clause1)
	conn.commit()


def creat_sample_analytical_method_table():
	clause1 = """CREATE TABLE sample_anmethod (
	 sample_anmethod_id SERIAL PRIMARY KEY,
	 sample_id CHAR(10) NOT NULL,
	 component_id CHAR(10) NOT NULL,
	 FOREIGN KEY (sample_id) REFERENCES sample(sample_id) ON DELETE CASCADE,
	 FOREIGN KEY (anmethod_id) REFERENCES chemical(anmethod_id) ON DELETE CASCADE,
	 assay_time TIMESTAMP,
	 concentration VARCHAR(10),
	 conc_unit VARCHAR(10)
	 );"""
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
	
	table_names = ['sample','chemical','assay','sample_assay','chemical_assay','sample_chemical']
	# for table_name in table_names:
	# 	clause = 'select \'drop table if exists \"\' || %s || \'\" cascade;\'' % (table_name)
	# 	cur.execute(clause)
	# 	conn.commit()

	# Creat Table
	creat_sample_table()
	creat_chemical_table()
	creat_assay_table()
	# creat_user_table()
	creat_sample_assay_table()
	creat_chemical_assay_table()
	creat_sample_chemical_table()

	# Insert data
	for table_name in table_names:
		file_name = table_name+'.csv'
		table_df = pd.read_csv(file_name, header = 0, index_col=None, encoding='utf-8')
		insert_data(table_name, table_df)

if __name__ == '__main__':
	main()
