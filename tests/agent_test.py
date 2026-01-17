import yaml
from ..agent import Agent

from dotenv import load_dotenv

load_dotenv()

# 1. Load Configuration
with open("test1.yaml", "r") as f:
    config_data = yaml.safe_load(f)

# Convert list to dict for easy lookup (needed for delegation)
# Map:  "researcher" -> {role: ..., tools: ...}
all_agents_map = {a['id']: a for a in config_data['agents']}

if __name__ == "__main__":
    # 2. Initialize the Manager (or any starting agent)
    # Let's say we start with the 'manager' defined in your YAML
    manager_config = all_agents_map.get('manager') 
    
    # If you don't have a manager, pick 'researcher'
    if not manager_config:
        manager_config = config_data['agents'][0]

    # 3. Create the Agent
    # This automatically calls prompter.py -> api_client.py
    main_agent = Agent(manager_config, all_agents_map)
    
    final_result = main_agent.run(task)
    
    print("\n" + "="*40)
    print(f"FINAL OUTPUT:\n{final_result}")
    print("="*40)
