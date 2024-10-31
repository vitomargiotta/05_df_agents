from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import sys
from pydantic import BaseModel

class CompanyTargetIndustries(BaseModel):
    target_industries: str


@CrewBase
class CompanyTargetIndustriesCrew():
	"""CompanyTargetIndustriesCrew crew"""

	agents_config = "config/agents.yaml"
	tasks_config = "config/tasks.yaml"

	@agent
	def company_target_industries_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['company_target_industries_writer'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@task
	def company_target_industries_creation_task(self) -> Task:
		return Task(
			config=self.tasks_config['company_target_industries_creation_task'],
            output_pydantic=CompanyTargetIndustries,
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the CompanyTargetIndustriesCrew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
	
# Helper functions for CompanyTargetIndustriesCrew

def runCompanyTargetIndustriesCrew(input):
    """
    Run the CompanyTargetIndustriesCrew.
    """
    result = CompanyTargetIndustriesCrew().crew().kickoff(input)
    return result


def trainCompanyTargetIndustriesCrew():
    """
    Train the CompanyTargetIndustriesCrew for a given number of iterations.
    """
    inputs = {
        "topic": "Competitor AI Analysis"
    }
    try:
        CompanyTargetIndustriesCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the Competitor Research crew: {e}")


def replayCompanyTargetIndustriesCrew():
    """
    Replay the Competitor Research crew execution from a specific task.
    """
    try:
        CompanyTargetIndustriesCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the Competitor Research crew: {e}")


def testCompanyTargetIndustriesCrew():
    """
    Test the Competitor Research crew execution and return the results.
    """
    inputs = {
        "topic": "Competitor AI Analysis"
    }
    try:
        CompanyTargetIndustriesCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the Competitor Research crew: {e}")