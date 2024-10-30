import os
import psycopg2
import json
from dotenv import load_dotenv
from crewai.flow.flow import Flow, listen, start
from agents.crews.crew_competitor_research.crew_competitors_research import CompetitorsResearchCrew
from typing import Dict

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = 5432

STATUS_IN_PROGRESS = "In Progress"
STATUS_COMPLETED = "Completed"
STATUS_FAILED = "Failed"


class CompetitorResearchFlow(Flow):
    def __init__(self):
        super().__init__()
        self.job_id = None
        self.user_input = None

    async def kickoff(self, inputs: Dict[str, str] = None):
        if inputs is not None:
            self.job_id = inputs.get("job_id")
            self.user_input = inputs.get("topic")
            print(f"Flow started with Job ID: {self.job_id} and User Input: {self.user_input}")
            self.update_status(STATUS_IN_PROGRESS)
        
        await super().kickoff()

    @start()
    def start_flow(self):
        print(f"AAAAAAAAAA")
        print(f"AAAAAAAAAA  Starting flow for Job ID {self.job_id} with User Input: {self.user_input}")
        print(f"AAAAAAAAAA")
        # No need to call run_crew manually here
    
    @listen("start_flow")
    def start_flow2(self):
        print(f"BBBBBBBBBBB")
        print(f"BBBBBBBBBBB")
        print(f"BBBBBBBBBBB")
        # No need to call run_crew manually here

    @listen("start_flow2")
    async def run_crew(self):
        try:
            print(f"CCCCCCCCC")
            
            # Run the crew and get the result
            # result = await (
            #     CompetitorsResearchCrew()
            #     .crew()
            #     .kickoff_async(inputs={"topic": self.user_input})
            # )
            
            # print("Crew Result BELOW")
            # print(result)
            # print("Crew Result ABOVE")

            # # Update database with success status and result
            # result_json = {"overview": str(result)}
            result_json = {"overview": "All good"}
            self.update_status(STATUS_COMPLETED, result_json)
        except Exception as e:
            print(f"Error in flow for Job ID {self.job_id}: {e}")
            # Update database with failed status if an error occurs
            self.update_status(STATUS_FAILED)