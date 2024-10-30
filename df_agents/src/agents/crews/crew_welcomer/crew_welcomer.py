from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import sys

from pydantic import BaseModel

class WelcomeMessage(BaseModel):
    overview: str

# Uncomment the following line to use an example of a custom tool
# from agents.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class WelcomerCrew():
	"""Welcomer crew"""

	agents_config = "config/agents.yaml"
	tasks_config = "config/tasks.yaml"

	@agent
	def welcomer_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['welcomer_agent'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

	@task
	def welcome_message_task(self) -> Task:
		return Task(
			config=self.tasks_config['welcome_message_task'],
            output_pydantic=WelcomeMessage,
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the WelcomerCrew crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
	
# Helper functions for CompetitorsResearchCrew

def runCompetitorsResearchCrew():
    """
    Run the Competitor Research crew.
    """
    # inputs = {
    #     'topic': company
    # }
    print(f"********** Starting to write a welcome message")
    result = WelcomerCrew().crew().kickoff()
    return result


def trainCompetitorsResearchCrew():
    """
    Train the Competitor Research crew for a given number of iterations.
    """
    inputs = {
        "topic": "Competitor AI Analysis"
    }
    try:
        WelcomerCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the Competitor Research crew: {e}")


def replayCompetitorsResearchCrew():
    """
    Replay the Competitor Research crew execution from a specific task.
    """
    try:
        WelcomerCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the Competitor Research crew: {e}")


def testCompetitorsResearchCrew():
    """
    Test the Competitor Research crew execution and return the results.
    """
    inputs = {
        "topic": "Competitor AI Analysis"
    }
    try:
        WelcomerCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the Competitor Research crew: {e}")