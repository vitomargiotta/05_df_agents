#!/usr/bin/env python
import sys
import os
import json
from agents.crews.crew_company_research.crew_company_research import CompanyResearchCrew
from agents.crews.crew_competitor_research.crew_competitors_research import CompetitorsResearchCrew
from agents.flow_test import CompetitorResearchFlow
from agents.flow_test2 import LeadScoreFlow

# SETUP THE FastAPI SERVER

from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import uuid
import asyncio
import concurrent.futures

# Setup connection to database

import psycopg2
from psycopg2 import sql

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = 5432

# Start app
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

class ReportRequest(BaseModel):
    user_id: int
    account_id: int
    agent_slug: str
    user_request: dict

analysis_status = {} 

# Possible job statuses
STATUS_NOT_STARTED = "Not Started"
STATUS_IN_PROGRESS = "In Progress"
STATUS_COMPLETED = "Completed"
STATUS_FAILED = "Failed"

@app.get("/agents")
async def get_agents():
    try:
        # Connect to the PostgreSQL database
        try:
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
            return {"error": str(e)}
        cur = conn.cursor()

        # Query to select all rows from the agents table
        cur.execute("SELECT * FROM agents;")
        agents = cur.fetchall()

        # Close the connection
        cur.close()
        conn.close()

        # Transform the result into a list of dictionaries
        agent_list = []
        for agent in agents:
            agent_dict = {
                "id": agent[0],
                "name": agent[1],
                "description": agent[2],
                "icon": agent[3],
                "categories": agent[4],
                "slug": agent[5],
                "status": agent[6],
                "visibility": agent[7],
                "metadata": agent[8],
                "created_at": agent[9],
                "updated_at": agent[10]
            }
            agent_list.append(agent_dict)

        # Return the agents
        return {"agents": agent_list}

    except Exception as e:
        # Handle any errors that occur
        return {"error": str(e)}
    





@app.get("/agents/{slug}")
async def get_agent(slug: str):
    try:
        # Connect to the PostgreSQL database
        try:
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
            raise HTTPException(status_code=500, detail="Database connection error")

        cur = conn.cursor()

        # Query to select the agent with the given slug
        cur.execute("SELECT * FROM agents WHERE slug = %s;", (slug,))
        agent = cur.fetchone()

        # Close the connection
        cur.close()
        conn.close()

        # If no agent is found, return a 404 Not Found error
        if agent is None:
            print(f"No agent found with slug: {slug}")
            raise HTTPException(status_code=404, detail="Agent not found")

        # If agent is found, return the agent as a dictionary
        agent_dict = {
            "id": agent[0],
            "name": agent[1],
            "description": agent[2],
            "icon": agent[3],
            "categories": agent[4],
            "slug": agent[5],
            "status": agent[6],
            "visibility": agent[7],
            "metadata": agent[8],
            "created_at": agent[9],
            "updated_at": agent[10]
        }
        return {"agent": agent_dict}

    except psycopg2.Error as db_error:
        print(f"Database error: {db_error}")
        raise HTTPException(status_code=500, detail="Database error: " + str(db_error))

    except HTTPException as http_exc:
        # Re-raise HTTP exceptions such as 404 to avoid turning them into 500
        raise http_exc

    except Exception as e:
        print(f"Unhandled exception: {e}")
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))
    

@app.get("/agents_count") 
async def get_agents_count():
    try:
        # Connect to the PostgreSQL database
        try:
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            # conn = psycopg2.connect(DB_URL)
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
            return {"error": str(e)}
        cur = conn.cursor()

        # Query to count the rows in the agents table
        cur.execute("SELECT COUNT(*) FROM agents;")
        count = cur.fetchone()[0]

        # Close the connection
        cur.close()
        conn.close()

        # Return the count
        return {"agents_count": count}

    except Exception as e:
        # Handle any errors that occur
        return {"error": str(e)}
    
@app.get("/agents/reports/{report_id}")
async def get_report_status_and_result(report_id: str):
    try:
        # Convert report_id to integer
        report_id = int(report_id)

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()

        # Query to select the report with the given report_id
        cur.execute("SELECT * FROM reports WHERE id = %s;", (report_id,))
        report = cur.fetchone()
        print(f"Report fetched: {report}")

        # If no report is found, return a 404 Not Found error
        if report is None:
            raise HTTPException(status_code=404, detail=f"Report with ID {report_id} not found")

        # If report is found, return all the report details as a dictionary
        report_dict = {
            "id": report[0],
            "agent_id": report[1],
            "user_id": report[2],
            "account_id": report[3],
            "status": report[4],
            "result": report[5],  # Assuming result is JSONB
            "created_at": report[6],
            "updated_at": report[7]
        }
        return {"report": report_dict}

    except ValueError as ve:
        print(f"ValueError: {ve}")  # Debugging ValueError
        # Handle cases where report_id is not a valid integer
        raise HTTPException(status_code=400, detail="Invalid report ID format. Report ID must be an integer.")

    except psycopg2.Error as db_error:
        print(f"Database Error: {db_error}")  # Debugging database error
        # Handle database errors and return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail=f"Database error: {db_error}")

    except Exception as e:
        print(f"General Error: {e}")  # Debugging any other general error
        # Handle any other unhandled exceptions and return a 500 Internal Server Error
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@app.post("/agents/request_report")
async def request_report(request: ReportRequest, background_tasks: BackgroundTasks):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()

        # Insert the new job into the reports table (assuming a table structure that includes these fields)
        cur.execute(
            """
            INSERT INTO reports (agent_id, user_id, account_id, status, result, created_at, updated_at)
            VALUES (
                (SELECT id FROM agents WHERE slug = %s), 
                %s, %s, %s, %s, NOW(), NOW()
            ) RETURNING id;
            """,
            (request.agent_slug, request.user_id, request.account_id, STATUS_IN_PROGRESS, None)
        )

        # Fetch the report_id of the newly inserted job (this will be the job ID)
        report_id = cur.fetchone()[0]

        # Commit the transaction and close the connection
        conn.commit()
        cur.close()
        conn.close()

        # Select the appropriate crew based on the agent_slug
        if request.agent_slug == "company-research-agent":
            crew_instance = CompanyResearchCrew()
        elif request.agent_slug == "competitors-research-agent":
            # crew_instance = CompetitorsResearchCrew()
            # crew_instance = CompetitorResearchFlow()
            crew_instance = LeadScoreFlow()
        else:
            raise HTTPException(status_code=400, detail="Invalid agent slug")

        # Message to be returned
        message = f"Report job started!"
        user_input = request.user_request.get('input')
        print(f"USER INPUT {user_input}!")

        background_tasks.add_task(run_analysis, user_input, report_id, crew_instance)
        return {"message": message, "report_id": report_id}

    except psycopg2.Error as e:
        # Handle any database-related errors
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database error: " + str(e))

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error: " + str(e))

async def run_analysis(user_input: str, job_id: str, crew_instance):
    try:
        # print(f"Running analysis for {user_input} with job ID {job_id}")

        # Start the flow directly with inputs containing job_id and user_input
        inputs = {"job_id": job_id, "topic": user_input}
        # crew_instance.kickoff(inputs=inputs)
        await crew_instance.kickoff()

        # print(f"Analysis initiation complete for {user_input} with job ID {job_id}")
    except Exception as e:
        print(f"Error in analysis for {user_input} with job ID {job_id}: {e}")
