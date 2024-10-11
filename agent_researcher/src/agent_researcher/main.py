#!/usr/bin/env python
import sys
from agent_researcher.crew import AgentResearcherCrew
import os


# SETUP THE FastAPI SERVER

from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import uuid
import asyncio
import concurrent.futures

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/hello")
async def hello():
    return {"message": "Welcome my friend!"}

class CompanyResearchRequest(BaseModel):
    company_name: str

analysis_status = {} 

# Possible job statuses
STATUS_NOT_STARTED = "Not Started"
STATUS_IN_PROGRESS = "In Progress"
STATUS_COMPLETED = "Completed"
STATUS_FAILED = "Failed"


@app.get("/status/{job_id}")
async def get_status(job_id: str):
    status = analysis_status.get(job_id, STATUS_NOT_STARTED)
    return {"status": status}

@app.get("/result/{job_id}")
async def get_result(job_id: str):
    results_folder = "results"
    filename = os.path.join(results_folder, f"{job_id}.txt")
    if os.path.exists(filename):
        with open(filename, "r") as file:
            content = file.read()
        return {"result": content}
    return {"result": "Analysis not complete or file not found"}

@app.post("/company_research")
async def company_research(request: CompanyResearchRequest, background_tasks: BackgroundTasks):
    if not request.company_name:
        raise HTTPException(status_code=400, detail="company_name is required")

    job_id = str(uuid.uuid4())[:8]
    background_tasks.add_task(run_analysis, request.company_name, job_id)

    message = f"Company research started for {request.company_name}!"
    return {"message": message, "job_id": job_id}

def runAgentResearcherCrew_sync(company_name: str):
    try:
        # raise Exception("Simulated failure")
        result = runAgentResearcherCrew(company_name)
        return result
    except Exception as e:
        print(f"Error running analysis for {company_name}: {e}")
        raise

async def run_analysis(company_name: str, job_id: str):
    try:
        print(f"Running analysis for {company_name} with job ID {job_id}")

        analysis_status[job_id] = STATUS_IN_PROGRESS
        
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            result = await loop.run_in_executor(pool, runAgentResearcherCrew_sync, company_name)
        
        result_str = str(result)
        
        analysis_status[job_id] = STATUS_COMPLETED

        # Write the result to a file
        results_folder = "results"
        os.makedirs(results_folder, exist_ok=True)
        filename = os.path.join(results_folder, f"{job_id}.txt")
        with open(filename, "w") as file:
            file.write(result_str)
        
        print(f"Analysis complete for {company_name} with job ID {job_id}")
    except Exception as e:
        print(f"Error in analysis for {company_name} with job ID {job_id}: {e}")
        analysis_status[job_id] = STATUS_FAILED

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def runAgentResearcherCrew(company):
    """
    Run the crew.
    """
    inputs = {
        'topic': company
    }
    print(f"GOING TO START WITH THE FOLLOWING: {company}")
    result = AgentResearcherCrew().crew().kickoff(inputs=inputs)
    return result


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        AgentResearcherCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AgentResearcherCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        AgentResearcherCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
