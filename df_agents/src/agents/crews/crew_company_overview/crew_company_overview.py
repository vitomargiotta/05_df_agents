from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import sys

# Uncomment the following line to use an example of a custom tool
# from agents.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

from pydantic import BaseModel

class CompanyOverview(BaseModel):
    overview: str


@CrewBase
class CompanyOverviewCrew():
	"""CompanyOverviewCrew crew"""

	agents_config = "config/agents.yaml"
	tasks_config = "config/tasks.yaml"

	@agent
	def company_overview_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['company_overview_writer'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@task
	def company_overview_creation_task(self) -> Task:
		return Task(
			config=self.tasks_config['company_overview_creation_task'],
            output_pydantic=CompanyOverview,
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the CompanyOverviewCrew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
	
# Helper functions for CompanyOverviewCrew

def runCompanyOverviewCrew(input):
    """
    Run the CompanyOverviewCrew.
    """
    result = CompanyOverviewCrew().crew().kickoff(input)
    return result


def trainCompanyOverviewCrew():
    """
    Train the CompanyOverviewCrew for a given number of iterations.
    """
    inputs = {
        "topic": "Competitor AI Analysis"
    }
    try:
        CompanyOverviewCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the Competitor Research crew: {e}")


def replayCompanyOverviewCrew():
    """
    Replay the Competitor Research crew execution from a specific task.
    """
    try:
        CompanyOverviewCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the Competitor Research crew: {e}")


def testCompanyOverviewCrew():
    """
    Test the Competitor Research crew execution and return the results.
    """
    inputs = {
        "topic": "Competitor AI Analysis"
    }
    try:
        CompanyOverviewCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the Competitor Research crew: {e}")