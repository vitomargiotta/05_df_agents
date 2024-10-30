#!/usr/bin/env python
import asyncio
from typing import List
from typing import Dict

from crewai.flow.flow import Flow, listen, or_, router, start
# from pydantic import BaseModel

from agents.crews.crew_competitor_research.crew_competitors_research import CompetitorsResearchCrew

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

# Find the example code here: https://github.com/crewAIInc/crewAI-examples/blob/main/lead-score-flow/src/lead_score_flow/main.py


class CompetitorResearchFlow(Flow):
    def __init__(self):
        super().__init__()
        self.job_id = None
        self.user_input = None

    def kickoff(self, inputs: Dict[str, str] = None):
        """
        Kickoff the flow with inputs, expecting 'job_id' and 'user_input'.
        """
        if inputs is not None:
            self.job_id = inputs.get("job_id")
            self.user_input = inputs.get("topic")
            print(f"Flow started with Job ID: {self.job_id} and User Input: {self.user_input}")
        
        super().kickoff()
# class CompetitorResearchFlow(Flow[LeadScoreState]):
    # initial_state = LeadScoreState

    @start()
    def print_something(self):
       
        print("SOMETHING")
        print("SOMETHING")
        print("SOMETHING")
        print("SOMETHING")
        print("SOMETHING")
        print("SOMETHING")
        print(f"Running crew for Job ID: {self.job_id} with User Input: {self.user_input}")
        print("SOMETHING")
        print("SOMETHING")
        print("SOMETHING")
        print("SOMETHING")
        print("SOMETHING")
        
        # Update the state with the loaded candidates
        # self.state.candidates = candidates

    @listen("print_something")
    async def run_crew(self):
        print("STARTING TO RUN CREW")
        print("STARTING TO RUN CREW")
        print("STARTING TO RUN CREW")
        print("STARTING TO RUN CREW")

        result = await (
                CompetitorsResearchCrew()
                .crew()
                .kickoff_async(
                    inputs={
                        "topic": "KINDLE"
                    }
                )
            )
        
        print("RESULT BELOW")
        print(result)
        print("RESULT ABOVE")
            


    @listen("run_crew")
    def print_something(self):
       
        print("SOMETHING AGAIN")
        print("SOMETHING AGAIN")
        print("SOMETHING AGAIN")
        print("SOMETHING AGAIN")
        print("SOMETHING AGAIN")
        print("SOMETHING AGAIN")
        print("SOMETHING AGAIN")
        print("SOMETHING AGAIN")
        print("SOMETHING AGAIN")


def kickoff(inputs):
    """
    Run the flow.
    """
    print("inputs BELOW")
    print(inputs)
    print("inputs ABOVE")
    competitor_research_flow = CompetitorResearchFlow()
    competitor_research_flow.kickoff()


def plot():
    """
    Plot the flow.
    """
    competitor_research_flow = CompetitorResearchFlow()
    competitor_research_flow.plot()


if __name__ == "__main__":
    kickoff()