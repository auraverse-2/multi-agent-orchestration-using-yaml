yaml = """
agents:
  - id: researcher
    role: Research Assistant
    goal: Find key insights about the given topic
  - id: writer
    role: Content Writer
    goal: Create a concise summary based on research

workflow:
  type: sequential
  steps:
    - agent: researcher
    - agent: writer
"""

from agent_factory import spawn_agent
import time
from models.google_adapter import GoogleAdapter
from vector_db import VectorDB



def run_workflow(normalized_input):
    agent_list = normalized_input['agents']
    print(normalized_input)
    res = ""
    if normalized_input['workflow']['type'] == 'sequential':
        db = VectorDB()
        for step in normalized_input['workflow']['order']:
            agent = spawn_agent(step, agent_list, [db])
            res = agent.run()

    elif normalized_input['workflow']['type'] == 'parallel':
        dbList = []
        for step in normalized_input['workflow']['branches']:
            dbList.append(VectorDB())
            agent = spawn_agent(step, agent_list, [dbList[-1]])
            agent.run()
        agent = spawn_agent(normalized_input['workflow']['then'], agent_list, dbList)
        res = agent.run()
    return res
