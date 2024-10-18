from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import sys
import yaml
import os

# Uncomment the following line to use an example of a custom tool
# from agents.tools.custom_tool import MyCustomTool

# Check our tools documentation for more information on how to use them
# from crewai_tools import SerperDevTool

# Utility function to load only the necessary agents from YAML
def load_agents_config(agent_names):
    script_dir = os.path.dirname(__file__)  # Get the directory of the current script
    agents_file_path = os.path.join(script_dir, 'config', 'agents.yaml')  # Path to agents.yaml

    if not os.path.exists(agents_file_path):
        raise FileNotFoundError(f"The file {agents_file_path} does not exist.")

    with open(agents_file_path, 'r') as file:
        agents_config = yaml.safe_load(file)

    selected_agents = {}
    for agent_name in agent_names:
        if agent_name in agents_config:
            selected_agents[agent_name] = agents_config[agent_name]
        else:
            raise ValueError(f"Agent {agent_name} not found in agents.yaml")
    return selected_agents


@CrewBase
class CompanyResearchCrew():
    """AgentResearcher crew"""

    def __init__(self):
        # Only load the agents relevant to this crew
        agent_names = ['researcher', 'company_overview_generation_analyst', 'reporting_analyst']
        self.agents_config = load_agents_config(agent_names)

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            # tools=[MyCustomTool()],  # Example of custom tool, loaded on the beginning of the file
            verbose=True
        )

    @agent
    def company_overview_generation_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['company_overview_generation_analyst'],
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def company_overview_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['company_overview_generation_task'],
            output_file='report.md'
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AgentResearcher crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical,  # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )


# Helper functions for CompanyResearchCrew

def runCompanyResearchCrew(company):
    """
    Run the Company Research crew.
    """
    inputs = {
        'topic': company
    }
    print(f"Starting Company Research for: {company}")
    result = CompanyResearchCrew().crew().kickoff(inputs=inputs)
    return result


def trainCompanyResearchCrew():
    """
    Train the Company Research crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CompanyResearchCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the Company Research crew: {e}")


def replayCompanyResearchCrew():
    """
    Replay the Company Research crew execution from a specific task.
    """
    try:
        CompanyResearchCrew().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the Company Research crew: {e}")


def testCompanyResearchCrew():
    """
    Test the Company Research crew execution and return the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CompanyResearchCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the Company Research crew: {e}")