
#!/usr/bin/env python
import os
import json
import asyncio
from typing import List

from agents.db_utils import fetch_job_details, update_job_status

from agents.crews.crew_user_onboarding_emails.crew_user_onboarding_emails import UserOnboardingEmailsCrew

from crewai.flow.flow import Flow, listen, or_, router, start
from pydantic import BaseModel


# DEFINE SCHEMA

class UserOnboardingEmailsState(BaseModel):
    overview: str = ""


# LOGIC FOR THE ACTUAL FLOW

class UserOnboardingEmailsFlow(Flow[UserOnboardingEmailsState]):
    def __init__(self, job_id):
        super().__init__()
        self.job_id = job_id
        self.job_details = None

    initial_state = UserOnboardingEmailsState

    @start()
    async def load_job_document(self):
        print("Loading job document...")
        
        self.job_details = fetch_job_details(self.job_id)
        
        if self.job_details:
            print(f"Retrieving content for job_id: {self.job_id}:")
            print(self.job_details)
        else:
            print(f"Error: impossible to retrive content from job_id: {self.job_id}")

    
    # BASED ON ACCOUNT ID, GET DETAILS ON ACCOUNT. ESLSE ACCEPT JSON FROM METABASE.
    # CREATE EMAIL BODY

    @listen("load_job_document")
    async def call_user_onboarding_emails_crew(self):
        print("START EXECUTING: USER ONBOARDING EMAILS CREW")

        job_id = self.job_id
        user_input = self.job_details[5] if self.job_details else None
        print("User input:")
        print(user_input)

        async def generate_user_onboarding_emails_single_user(user_input):
            conn = None
            try:
                result = await (
                    UserOnboardingEmailsCrew()
                    .crew()
                    .kickoff_async(user_input)
                )
                print("RESULT BELOW")
                print(result)
                # print("PYDANTIC RESULT BELOW")
                
                result_json = result.pydantic.dict() if hasattr(result.pydantic, 'dict') else {"overview": result.pydantic.company_overview}
                self.state.overview = result.pydantic.overview
                
                update_successful = update_job_status(self.job_id, "Completed", result=result_json)
                if update_successful:
                    print(f"Job {self.job_id} updated successfully.")
                else:
                    print(f"Error: could not update job_id: {self.job_id}.")

            except Exception as e:
                print(f"An error occurred: {e}")
                error_result = {"error": str(e)}
                update_job_status(self.job_id, "Failed", result=error_result)

        asyncio.create_task(generate_user_onboarding_emails_single_user(user_input))

        print("FINISHED EXECUTING: USER ONBOARDING EMAILS CREW")



    @listen("call_user_onboarding_emails_crew")
    async def step4(self):
        print(f"DONE WITH ENTIRE FLOW")


def kickoff():
    """
    Run the flow.
    """
    lead_score_flow = UserOnboardingEmailsFlow()
    lead_score_flow.kickoff()


def plot():
    """
    Plot the flow.
    """
    lead_score_flow = UserOnboardingEmailsFlow()
    lead_score_flow.plot()


if __name__ == "__main__":
    kickoff()