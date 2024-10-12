# RUN PROJECT LOCALLY

- Clone the repository

- Ask Vito for the .env file

- Build the docker image
````
docker compose up
````

- Create database schema and seed initial data
````
cd df_agents
cd database
python 01_check_db_connection.py
python 02_create_db_tables.py
python 03_seed_db.py
````

and confirm all is fine
````
python 04_check_agents_table_content.py
````

- Test the api
````
If locally: http://0.0.0.0:8000
If on VM: http://188.245.180.119:8000
````

- If content in db is messed up and you want to clean it up
````
python drop_all_tables.py
````


# DEPLOY TO VM

- ssh into the vm 
````
ssh -i /Users/vitomargiotta/.ssh/id_rsa root@188.245.180.119
````

- copy code into VM, run this in a new terminal (in a new terminal, should not be already SSH into VM)
````
scp -i /Users/vitomargiotta/.ssh/id_rsa -r "/Users/vitomargiotta/DF-Development/prototyping/05_df_agents/df_agents" root@188.245.180.119:/root/
````



- add the .env file and use the content from .env.production
````
cd df_agents
nano .env
````


- Build the docker image
````
docker compose up --build
````

- Create database schema and seed initial data
````
cd df_agents
cd database
python setup_database.py
````

and confirm all is fine
````
python see_content_agents_table.py
````

- Test the api
````
If locally: http://0.0.0.0:8000
If on VM: http://188.245.180.119:8000
````

- Example POST request to research a company
````
curl -X POST http://0.0.0.0:8000/company_research \
-H "Content-Type: application/json" \
-d '{"company_name": "Dealfront"}'
````

