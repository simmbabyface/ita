ITA
=======
Integrated Toxicity Analysis System

Dependency
----------------
- PostgresSQL 11
- Python 3.0+
- bottle-pgsql (pip install bottle-pgsql)
- bottle (pip install bottle)
- psycopg2 (pip install psycopg2)
- Marvin JS
- JChem base

Database Setup
----------------
```
psql -U postgres
postgres=# create database ita;
postgres=# create user babyface with encrypted password '5555';
postgres=# grant all privileges on database ita to babyface;
postgres=# exit;
```

Start the server
----------------
Under the server folder, run

	python server.py
	open the url: http://localhost:8080/
Then your server should be up and running. Have fun!
