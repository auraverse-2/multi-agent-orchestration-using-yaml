def spawn_agent(agent_id, agent_list, db=None):
    # Local import to avoid circular import at module load time
    from agent import Agent

    # Look up the agent configuration by the provided agent_id
    agent_config = agent_list[agent_id]

    subagents = [
        {**agent_list[subagent_id], "id": subagent_id}
        for subagent_id in agent_config.get('subagents', [])
        if subagent_id in agent_list
    ]

    # Pass `db` explicitly (Agent expects db as the 4th arg)
    return Agent(
        agent_id,
        agent_config.get('description'),
        agent_config.get('goal'),
        db,
        model=agent_config.get('model'),
        tools=agent_config.get('tools', []),
        subagents=subagents,
    )
