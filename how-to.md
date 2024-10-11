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
docker build -t agent_researcher .
````

- Run the Docker Container
````
docker run -d -p 8000:8000 agent_researcher
````

- Test the api
````
http://188.245.180.119:8000
````

- 
````
````


Else, if done with venv, use this:
- Run the Docker Container
````
PYTHONPATH=/root/agent_researcher/src uvicorn agent_researcher.main:app --host 0.0.0.0 --port 8000
````