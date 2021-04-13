from simple_ddl_parser import DDLParser


ddl = """
CREATE TABLE sqlserverlist (

id INT IDENTITY (1,1) PRIMARY KEY, -- NOTE THE IDENTITY (1,1) IS SIMILAR TO serial in postgres - Format for IDENTITY [ (seed , increment) ]
company_id BIGINT ,
primary_id INT FOREIGN KEY REFERENCES Persons(PersonID), -- ADD THIS COLUMN FOR THE FOREIGN KEY
age TINYINT NULL UNIQUE,
days_active SMALLINT NOT NULL,
user_origin_of_birth char(255),
user_account VARCHAR(8000) NOT NULL,
birth_date DATE NOT NULL,
time_of_birth TIME(7),
enrollment_date SMALLDATETIME,
delete_date DATETIME NULL,
create_date DATETIME2(7) NOT NULL,
user_time_zone DATETIMEOFFSET(7),
oder_date date DEFAULT GETDATE(), -- added to demonstrate sql sever Defaults
country varchar(255) DEFAULT 'Sandnes', -- added to demonstrate sql sever Defaults
active bit NULL,
home_size GEOMETRY, -- Sql Server Defaults to Null
user_photo IMAGE, -- Sql Server Defaults to Null
--UNIQUE (id),
CONSTRAINT UC_sqlserverlist_last_name UNIQUE (company_id,user_last_name),
CONSTRAINT CHK_Person_Age_under CHECK (days_active<=18 AND user_city='New York'),
FOREIGN KEY (id) REFERENCES Persons(PersonID),
CONSTRAINT FK_Person_Age_under  FOREIGN KEY (id)REFERENCES Persons(PersonID)
);

CREATE INDEX i1 ON sqlserverlist (extra_funds);
CREATE CLUSTERED INDEX i2 ON sqlserverlist  (delete_date,create_date); --- This line is commented because TSQL doesnt allow two index on table added as an example
CREATE UNIQUE INDEX i1 ON sqlserverlist (delete_date DESC, create_date ASC, ending_funds  DESC); --- This line is commented because TSQL doesnt allow two index on table added as an example
CREATE INDEX test2_info_nulls_low ON sqlserverlist (info NULLS FIRST);
CREATE INDEX test3_desc_index ON sqlserverlist (id DESC NULLS LAST);
"""

result = DDLParser(ddl).run(group_by_type=True, output_mode='mssql')
import pprint

pprint.pprint(result)
