import yaml
from typing import Any, Dict, List, Set, Tuple

# =====================================================
# Error / Warning helpers
# =====================================================

def error(err_type: str, message: str) -> Dict[str, str]:
    return {"type": err_type, "message": message}

def warning(warn_type: str, message: str) -> Dict[str, str]:
    return {"type": warn_type, "message": message}


# =====================================================
# 1. YAML Parsing
# =====================================================

def parse_yaml(yaml_text: str) -> Tuple[Any, List[Dict]]:
    try:
        data = yaml.safe_load(yaml_text)
        if data is None:
            return None, [error("SyntaxError", "YAML document is empty")]
        if not isinstance(data, dict):
            return None, [error("SchemaError", "Top-level YAML must be a mapping/object")]
        return data, []
    except yaml.YAMLError as e:
        return None, [error("SyntaxError", str(e))]


# =====================================================
# 2. Top-level Validation
# =====================================================

def validate_top_level(data: Dict) -> List[Dict]:
    errors = []

    if "agents" not in data:
        errors.append(error("SchemaError", "Missing required 'agents' section"))
    elif not isinstance(data["agents"], list):
        errors.append(error("SchemaError", "'agents' must be a list"))

    if "workflow" in data and not isinstance(data["workflow"], dict):
        errors.append(error("SchemaError", "'workflow' must be an object if present"))

    if "models" in data and not isinstance(data["models"], dict):
        errors.append(error("SchemaError", "'models' must be an object/map"))

    return errors


# =====================================================
# 3. Agent Validation
# =====================================================

def validate_agents(agents: List[Dict]) -> Tuple[List[Dict], Set[str]]:
    errors = []
    agent_ids = set()

    for idx, agent in enumerate(agents):
        if not isinstance(agent, dict):
            errors.append(error(
                "AgentError",
                f"Agent at index {idx} must be an object"
            ))
            continue

        agent_id = agent.get("id")
        if not agent_id or not isinstance(agent_id, str):
            errors.append(error(
                "AgentError",
                "Each agent must have a string 'id'"
            ))
            continue

        if agent_id in agent_ids:
            errors.append(error(
                "AgentError",
                f"Duplicate agent id '{agent_id}'"
            ))
        agent_ids.add(agent_id)

        # At least ONE defining field must exist
        required_any = {"role", "goal", "instruction", "description"}
        if not any(key in agent for key in required_any):
            errors.append(error(
                "AgentError",
                f"Agent '{agent_id}' must define at least one of {sorted(required_any)}"
            ))

        # Validate sub_agents
        if "sub_agents" in agent:
            if not isinstance(agent["sub_agents"], list):
                errors.append(error(
                    "AgentError",
                    f"'sub_agents' of '{agent_id}' must be a list"
                ))

        # Validate tools
        if "tools" in agent and not isinstance(agent["tools"], list):
            errors.append(error(
                "AgentError",
                f"'tools' of '{agent_id}' must be a list"
            ))

    return errors, agent_ids


# =====================================================
# 4. Workflow Validation (Optional)
# =====================================================

def validate_workflow(workflow: Dict, agent_ids: Set[str]) -> List[Dict]:
    errors = []

    if "type" not in workflow:
        return [error("SchemaError", "Workflow missing 'type'")]

    wf_type = workflow["type"]

    if wf_type == "sequential":
        steps = workflow.get("steps")
        if not isinstance(steps, list):
            errors.append(error("SchemaError", "'steps' must be a list"))
        else:
            for step in steps:
                if not isinstance(step, dict) or "agent" not in step:
                    errors.append(error(
                        "SchemaError",
                        "Each step must be an object with 'agent'"
                    ))
                    continue
                if step["agent"] not in agent_ids:
                    errors.append(error(
                        "ReferenceError",
                        f"Unknown agent '{step['agent']}' in workflow"
                    ))

    elif wf_type == "parallel":
        branches = workflow.get("branches")
        then = workflow.get("then")

        if not isinstance(branches, list):
            errors.append(error("SchemaError", "'branches' must be a list"))
        else:
            for br in branches:
                agent = br["agent"] if isinstance(br, dict) else br
                if agent not in agent_ids:
                    errors.append(error(
                        "ReferenceError",
                        f"Unknown agent '{agent}' in parallel branches"
                    ))

        if not isinstance(then, dict) or "agent" not in then:
            errors.append(error(
                "SchemaError",
                "'then' must be an object with 'agent'"
            ))
        elif then["agent"] not in agent_ids:
            errors.append(error(
                "ReferenceError",
                f"Unknown 'then' agent '{then['agent']}'"
            ))

    else:
        errors.append(error(
            "SchemaError",
            f"Unknown workflow type '{wf_type}'"
        ))

    return errors


# =====================================================
# 5. Normalization
# =====================================================

def normalize(data: Dict) -> Dict:
    normalized_agents = {}
    for agent in data["agents"]:
        normalized_agents[agent["id"]] = {
            "model": agent.get("model"),
            "role": agent.get("role"),
            "goal": agent.get("goal"),
            "description": agent.get("description"),
            "instruction": agent.get("instruction"),
            "tools": agent.get("tools", []),
            "sub_agents": agent.get("sub_agents", [])
        }

    normalized = {
        "agents": normalized_agents,
        "models": data.get("models", {})
    }

    if "workflow" in data:
        wf = data["workflow"]
        if wf["type"] == "sequential":
            normalized["workflow"] = {
                "type": "sequential",
                "order": [s["agent"] for s in wf["steps"]]
            }
        elif wf["type"] == "parallel":
            normalized["workflow"] = {
                "type": "parallel",
                "branches": [
                    b["agent"] if isinstance(b, dict) else b
                    for b in wf["branches"]
                ],
                "then": wf["then"]["agent"]
            }

    return normalized


# =====================================================
# 6. Warnings
# =====================================================

def find_warnings(agent_ids: Set[str], normalized: Dict) -> List[Dict]:
    warnings = []
    used = set()

    workflow = normalized.get("workflow")
    if workflow:
        if workflow["type"] == "sequential":
            used |= set(workflow["order"])
        elif workflow["type"] == "parallel":
            used |= set(workflow["branches"])
            used.add(workflow["then"])

    for agent, cfg in normalized["agents"].items():
        for sub in cfg.get("sub_agents", []):
            used.add(sub)

    for unused in agent_ids - used:
        warnings.append(warning(
            "UnusedAgent",
            f"Agent '{unused}' is defined but never referenced"
        ))

    return warnings


# =====================================================
# 7. Public API
# =====================================================

def validate_yaml(yaml_text: str) -> Dict:
    data, parse_errors = parse_yaml(yaml_text)
    if parse_errors:
        return {"valid": False, "errors": parse_errors}

    errors = validate_top_level(data)
    if errors:
        return {"valid": False, "errors": errors}

    agent_errors, agent_ids = validate_agents(data["agents"])
    errors.extend(agent_errors)

    if "workflow" in data:
        errors.extend(validate_workflow(data["workflow"], agent_ids))

    if errors:
        return {"valid": False, "errors": errors}

    normalized = normalize(data)
    warnings = find_warnings(agent_ids, normalized)

    return {
        "valid": True,
        "normalized_config": normalized,
        "warnings": warnings
    }
