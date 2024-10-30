#!/usr/bin/env python
import os
from dotenv import load_dotenv
import json
import psycopg2
from psycopg2 import sql
import asyncio
from typing import List

from agents.crews.crew_welcomer.crew_welcomer import WelcomerCrew

from crewai.flow.flow import Flow, listen, or_, router, start
from pydantic import BaseModel

class WelcomeMessageState(BaseModel):
    overview: str = ""


load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = 5432

# from lead_score_flow.constants import JOB_DESCRIPTION
# from lead_score_flow.crews.lead_response_crew.lead_response_crew import LeadResponseCrew
# from lead_score_flow.crews.lead_score_crew.lead_score_crew import LeadScoreCrew
# from lead_score_flow.types import Candidate, CandidateScore, ScoredCandidate
# from lead_score_flow.utils.candidateUtils import combine_candidates_with_scores


# class LeadScoreState(BaseModel):
#     candidates: List[Candidate] = []
#     candidate_score: List[CandidateScore] = []
#     hydrated_candidates: List[ScoredCandidate] = []
#     scored_leads_feedback: str = ""


class LeadScoreFlow(Flow[WelcomeMessageState]):
    initial_state = WelcomeMessageState

    @start()
    def load_leads(self):
        print(f"1111111111")
        print(f"1111111111")
        print(f"1111111111")

    @listen("load_leads")
    async def load_leads2(self):
        print(f"BBBBBBBBBB")
        print(f"BBBBBBBBBB")
        print(f"BBBBBBBBBB")

    @listen("load_leads2")
    async def start_crew(self):
        print("About to start the crew")

        async def score_single_candidate(job_id=96):
            conn = None
            try:
                result = await (
                    WelcomerCrew()
                    .crew()
                    .kickoff_async(
                        # inputs={
                        #     "candidate_id": candidate.id,
                        #     "name": candidate.name,
                        #     "bio": candidate.bio,
                        #     "job_description": JOB_DESCRIPTION,
                        #     "additional_instructions": self.state.scored_leads_feedback,
                        # }
                    )
                )
                print("RESULT BELOW")
                print(result)
                print("PYDANTIC RESULT BELOW")
                
                # Convert pydantic result to a JSON-serializable dictionary
                result_json = result.pydantic.dict() if hasattr(result.pydantic, 'dict') else {"overview": result.pydantic.overview}

                # Connect to the PostgreSQL database and update the report with success status
                conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
                cur = conn.cursor()
                cur.execute(
                    """
                    UPDATE reports
                    SET status = %s, result = %s, updated_at = NOW()
                    WHERE id = %s;
                    """,
                    ("Completed", json.dumps(result_json), job_id)
                )
                conn.commit()
                cur.close()

            except Exception as e:
                print(f"An error occurred: {e}")
                
                # Define error_result to capture the exception details
                error_result = {"error": str(e)}

                # Connect to the PostgreSQL database and update the report with error status
                if conn is None:
                    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
                cur = conn.cursor()
                cur.execute(
                    """
                    UPDATE reports
                    SET status = %s, result = %s, updated_at = NOW()
                    WHERE id = %s;
                    """,
                    ("Failed", json.dumps(error_result), job_id)
                )
                conn.commit()
                cur.close()

            finally:
                if conn:
                    conn.close()

        job_id = 99  # Temporary job ID
        asyncio.create_task(score_single_candidate(job_id))

        print("FINISHED EXECUTING CREW")

    # @listen("load_leads2")
    # async def start_crew(self):
    #     print("About to start the crew")

    #     async def score_single_candidate():
    #         result = await (
    #             WelcomerCrew()
    #             .crew()
    #             .kickoff_async(
    #                 # inputs={
    #                 #     "candidate_id": candidate.id,
    #                 #     "name": candidate.name,
    #                 #     "bio": candidate.bio,
    #                 #     "job_description": JOB_DESCRIPTION,
    #                 #     "additional_instructions": self.state.scored_leads_feedback,
    #                 # }
    #             )
    #         )

    #         print("RESULT BELOW")
    #         print(result)
    #         print("PYDANTIC RESULT BELOW")
    #         print(result.pydantic)
    #         print("DONE WITH RESULTS")

    #     asyncio.create_task(score_single_candidate())


    #     # candidate_scores = await asyncio.gather(*tasks)
    #     print("FINISHED EXECUTING CREW")

    @listen("start_crew")
    async def load_leads3(self):
        print(f"CCCCCCCCCC")
        print(f"CCCCCCCCCC")
        print(f"CCCCCCCCCC")


def kickoff():
    """
    Run the flow.
    """
    lead_score_flow = LeadScoreFlow()
    lead_score_flow.kickoff()


def plot():
    """
    Plot the flow.
    """
    lead_score_flow = LeadScoreFlow()
    lead_score_flow.plot()


if __name__ == "__main__":
    kickoff()