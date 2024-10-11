# How to use Crew AI

i have created a nenv python environment using the command "python3.12 -m venv agent_researcher_python_env"

to use it 
- run the command "source agent_researcher_python_env/bin/activate"
- from the command line cd into "05_agent_company_researcher" folder

to deploy to VM
- ssh into the vm 
````
ssh -i /Users/vitomargiotta/.ssh/id_rsa root@188.245.180.119
````

- copy code into VM, run this in a new terminal (no need of already be SSH into VM)
````
scp -i /Users/vitomargiotta/.ssh/id_rsa -r "/Users/vitomargiotta/DF-Development/LF Prototyping/05_agent_company_researcher/agent_researcher" root@188.245.180.119:/root/
````

- Build the docker image
````
docker compose up --build
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

