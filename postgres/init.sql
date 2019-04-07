-- psql -U babyface -f init.sql ita

DROP TABLE if exists sample_assay;
DROP TABLE if exists component_assay;
DROP TABLE if exists sample_component;
DROP TABLE if exists sample;
DROP TABLE if exists component;
DROP TABLE if exists assay;
DROP TABLE if exists users;

DROP SEQUENCE if exists sample_id_seq;
DROP SEQUENCE if exists component_id_seq;
DROP SEQUENCE if exists assay_id_seq;
DROP SEQUENCE if exists user_id_seq;

CREATE SEQUENCE sample_id_seq;
CREATE TABLE sample(
 sample_id CHAR(8) NOT NULL DEFAULT to_char(nextval('sample_id_seq'), '"S"0000000FM') PRIMARY KEY,
 sampling_name VARCHAR (50) UNIQUE NOT NULL,
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
);
ALTER SEQUENCE sample_id_seq OWNED BY sample.sample_id;

CREATE SEQUENCE component_id_seq;
CREATE TABLE component(
 component_id CHAR(8) NOT NULL DEFAULT to_char(nextval('component_id_seq'), '"C"0000000FM') PRIMARY KEY,
 chemical_type VARCHAR,
 MS_Type VARCHAR(50),
 MS_Level VARCHAR(10),
 precursor_mz VARCHAR(10),
 Total_Peaks VARCHAR(10),
 mz_Top_Peak VARCHAR(10),
 mz_2nd_Highest VARCHAR(10),
 mz_3rd_Highest VARCHAR(10),
 molecular_formula VARCHAR,
 suspected_structure VARCHAR,
 chemical_name VARCHAR UNIQUE NOT NULL,
 CAS VARCHAR,
 canonical_smiles VARCHAR
);
ALTER SEQUENCE component_id_seq OWNED BY component.component_id;

CREATE SEQUENCE assay_id_seq;
CREATE TABLE assay(
 assay_id CHAR(8) NOT NULL DEFAULT to_char(nextval('assay_id_seq'), '"A"0000000FM') PRIMARY KEY,
 toxicity VARCHAR,
 assay_name VARCHAR UNIQUE NOT NULL,
 timepoint VARCHAR,
 organism VARCHAR,
 tissue VARCHAR,
 cell_name VARCHAR,
 assay_footprint VARCHAR,
 assay_format_type VARCHAR,
 dilution_solvent VARCHAR,
 biological_process_target VARCHAR,
 detection_technology VARCHAR,
 gene_symbol VARCHAR,
 endpoint_description VARCHAR,
 signal_type VARCHAR,
 positive_control VARCHAR,
 negative_control VARCHAR
);
ALTER SEQUENCE assay_id_seq OWNED BY assay.assay_id;

CREATE TABLE sample_assay (
  sample_assay_id SERIAL PRIMARY KEY,
  sample_id CHAR(8) NOT NULL,
  assay_id CHAR(8) NOT NULL,
  FOREIGN KEY (sample_id) REFERENCES sample(sample_id) ON DELETE CASCADE,
  FOREIGN KEY (assay_id) REFERENCES assay(assay_id) ON DELETE CASCADE,
  assay_time TIMESTAMP,
  model VARCHAR(10),
  n VARCHAR(10),
  ac50 VARCHAR(10),
  conc_unit VARCHAR(5)
);

CREATE TABLE component_assay (
  component_assay_id SERIAL PRIMARY KEY,
  component_id CHAR(8) NOT NULL,
  assay_id CHAR(8) NOT NULL,
  FOREIGN KEY (component_id) REFERENCES component(component_id) ON DELETE CASCADE,
  FOREIGN KEY (assay_id) REFERENCES assay(assay_id) ON DELETE CASCADE,
  assay_time TIMESTAMP,
  model VARCHAR(10),
  n VARCHAR(10),
  ac50 VARCHAR(10),
  conc_unit VARCHAR(5)
);

CREATE TABLE sample_component (
  sample_component_id SERIAL PRIMARY KEY,
  sample_id CHAR(8) NOT NULL,
  component_id CHAR(8) NOT NULL,
  FOREIGN KEY (sample_id) REFERENCES sample(sample_id) ON DELETE CASCADE,
  FOREIGN KEY (component_id) REFERENCES component(component_id) ON DELETE CASCADE,
  assay_time TIMESTAMP,
  concentration VARCHAR(10),
  conc_unit VARCHAR(5)
);
