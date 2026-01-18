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



def run_workflow(normalized_input):
    agent_list = normalized_input['agents']
    if normalized_input['workflow']['type'] == 'sequential':
        print(normalized_input['workflow']['order'])
        for step in normalized_input['workflow']['order']:
            agent = spawn_agent(step, agent_list)
            agent.run()

    print(normalized_input)
