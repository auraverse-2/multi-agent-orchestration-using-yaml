# test_validator.py

from pprint import pprint
from validator import validate_yaml   # <-- change filename if needed


# =====================================================
# Test cases: key = name, value = YAML string
# =====================================================

TEST_CASES = {

    "valid_sequential_workflow": """
agents:
  - id: researcher
    role: Research Assistant
    goal: Find key insights

  - id: writer
    role: Content Writer
    goal: Write summary

workflow:
  type: sequential
  steps:
    - agent: researcher
    - agent: writer
""",

    "valid_parallel_workflow": """
agents:
  - id: backend
    role: Backend Engineer
    goal: Design API

  - id: frontend
    role: Frontend Engineer
    goal: Design UI

  - id: reviewer
    role: Tech Lead
    goal: Review designs

workflow:
  type: parallel
  branches:
    - backend
    - frontend
  then:
    agent: reviewer
""",

    "valid_tool_enabled_agent": """
agents:
  - id: analyst
    role: Data Analyst
    goal: Analyze CSV
    tools:
      - python
""",

    "valid_root_helper_example": """
agents:
  - id: root
    model: claude
    description: Main coordinator agent
    instruction: |
      You coordinate tasks.
    sub_agents: ["helper"]

  - id: helper
    model: claude
    description: Helper agent
    instruction: |
      You assist the root agent.

models:
  claude:
    provider: anthropic
    model: claude-sonnet-4-0
""",

    "invalid_missing_agents": """
workflow:
  type: sequential
  steps:
    - agent: a
""",

    "invalid_duplicate_agent_ids": """
agents:
  - id: a
    role: R1
  - id: a
    role: R2
""",

    "invalid_unknown_agent_in_workflow": """
agents:
  - id: only_agent
    role: Test

workflow:
  type: sequential
  steps:
    - agent: missing_agent
""",

    "invalid_bad_yaml_syntax": """
agents:
  - id: a
    role Test   # missing colon
""",

    "warning_unused_agent": """
agents:
  - id: used
    role: Used agent
  - id: unused
    role: Unused agent

workflow:
  type: sequential
  steps:
    - agent: used
"""
}


# =====================================================
# Run tests
# =====================================================

def run_tests():
    for name, yaml_text in TEST_CASES.items():
        print("\n" + "=" * 80)
        print(f"TEST CASE: {name}")
        print("=" * 80)

        result = validate_yaml(yaml_text)
        print(result)

        # if not result["valid"]:
        #     print("❌ INVALID YAML")
        #     print("Errors:")
        #     pprint(result["errors"])
        # else:
        #     print("✅ VALID YAML")

        #     if result.get("warnings"):
        #         print("\nWarnings:")
        #         pprint(result["warnings"])
        #     else:
        #         print("\nWarnings: None")

        #     print("\nNormalized Config:")
        #     pprint(result["normalized_config"])


# =====================================================
# Entry point
# =====================================================

if __name__ == "__main__":
    run_tests()