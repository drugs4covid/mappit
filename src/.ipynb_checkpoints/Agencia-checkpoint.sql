CREATE TABLE AGENCY (`agency_id` VARCHAR(200),
				`agency_name` VARCHAR(200),
				`agency_url` VARCHAR(200),
				`agency_timezone` VARCHAR(200),
				`agency_lang` VARCHAR(200),
				`agency_phone` VARCHAR(200) DEFAULT NULL,
				`agency_fare_url` VARCHAR(200) DEFAULT NULL,
				PRIMARY KEY (agency_id));
				LOAD DATA LOCAL INFILE 'examples/datasets/sql/1/AGENCY.csv'
				INTO TABLE AGENCY FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS
					SET agency_phone = IF(agency_phone = '', NULL, agency_phone),
					agency_fare_url = IF(agency_fare_url = '', NULL, agency_fare_url);