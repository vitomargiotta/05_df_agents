#!/usr/bin/env python
import asyncio
from typing import List

from agents.crews.crew_welcomer.crew_welcomer import WelcomerCrew

from crewai.flow.flow import Flow, listen, or_, router, start
from pydantic import BaseModel

class WelcomeMessageState(BaseModel):
    emailContent: str = ""

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

        async def score_single_candidate():
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
            print(result.pydantic)
            print("DONE WITH RESULTS")

        asyncio.create_task(score_single_candidate())


        # candidate_scores = await asyncio.gather(*tasks)
        print("FINISHED EXECUTING CREW")

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