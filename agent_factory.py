def spawn_agent(agent_id, agent_list, dbs=None, allow_db_ref=True):
    # Local import to avoid circular import at module load time
    from agent import Agent

    # Look up the agent configuration by the provided agent_id
    agent_config = agent_list[agent_id]
    subagents = [
        {**agent_list[subagent_id], "id": subagent_id}
        for subagent_id in agent_config.get('sub_agents', [])
        if subagent_id in agent_list
    ]
    tools = agent_config.get('tools', [])
    if (allow_db_ref):
        tools.append('vector_db_search')

    # Pass `db` explicitly (Agent expects db as the 4th arg)
    return Agent(
        agent_id,
        agent_config.get('description'),
        agent_config.get('goal'),
        dbs,
        model=agent_config.get('model'),
        tools=tools,
        subagents=subagents,
        agents_list=agent_list
    )
