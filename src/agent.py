"""
Core classes for the Tri-Hemisphere Agent Architecture.
"""
from src.knowledge import KnowledgeBase

class HemisphereA:
    """Primary technology great hemisphere."""
    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base

    def decide(self, problem):
        # Query the knowledge base for relevant information
        results = self.knowledge_base.query(problem, n_results=1)

        # Placeholder for decision logic using knowledge
        if results and results['documents'] and results['documents'][0]:
            decision = f"HemiA decides based on: {results['documents'][0][0]}"
        else:
            decision = "HemiA_decide_no_knowledge"

        return {"decision": decision, "confidence": 0.8}

class HemisphereB:
    """Complementary #2 great hemisphere."""
    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base

    def decide(self, problem):
        # Query the knowledge base for relevant information
        results = self.knowledge_base.query(problem, n_results=1)

        # Placeholder for decision logic using knowledge
        if results and results['documents'] and results['documents'][0]:
            decision = f"HemiB decides based on: {results['documents'][0][0]}"
        else:
            decision = "HemiB_decide_no_knowledge"

        return {"decision": decision, "confidence": 0.75}

class HemisphereC:
    """Arbitration logic engine."""
    def __init__(self, fallback_heuristic='A'):
        self.fallback_heuristic = fallback_heuristic

    def arbitrate(self, decision_a, decision_b, weights={'A': 1.0, 'B': 1.0}):
        """
        Arbitrates between the decisions from Hemisphere A and B using
        weighted scoring and a fallback heuristic.

        Args:
            decision_a (dict): The decision from Hemisphere A.
            decision_b (dict): The decision from Hemisphere B.
            weights (dict): The weights to apply to each hemisphere's confidence score.
            fallback_heuristic (str): The hemisphere to prefer in case of a tie ('A' or 'B').

        Returns:
            The final arbitrated decision.
        """
        score_a = decision_a["confidence"] * weights.get('A', 1.0)
        score_b = decision_b["confidence"] * weights.get('B', 1.0)

        if score_a > score_b:
            return decision_a["decision"]
        elif score_b > score_a:
            return decision_b["decision"]
        else:
            # Conflict resolution: In case of a tie, use the fallback heuristic.
            if self.fallback_heuristic == 'A':
                return decision_a["decision"]
            else:
                return decision_b["decision"]

class Agent:
    """
    A tri-hemisphere agent that combines the strengths of three sub-agents.
    """
    def __init__(self, name, role, employee_id, hourly_rate, physical_description, skill_matrix, knowledge_sources, tool_access):
        self.name = name
        self.role = role
        self.employee_id = employee_id
        self.hourly_rate = hourly_rate
        self.physical_description = physical_description
        self.skill_matrix = skill_matrix
        self.knowledge_sources = knowledge_sources
        self.tool_access = tool_access
        self.decision_logs = []

        # Each agent gets its own knowledge base instance.
        self.knowledge_base = KnowledgeBase()
        self.hemisphere_a = HemisphereA(self.knowledge_base)
        self.hemisphere_b = HemisphereB(self.knowledge_base)
        self.hemisphere_c = HemisphereC()

    def process(self, problem, weights={'A': 1.0, 'B': 1.0}):
        """
        Processes a problem by getting decisions from hemispheres A and B,
        and then arbitrating to get a final decision.
        """
        decision_a = self.hemisphere_a.decide(problem)
        decision_b = self.hemisphere_b.decide(problem)
        final_decision = self.hemisphere_c.arbitrate(decision_a, decision_b, weights)
        self.decision_logs.append({
            "problem": problem,
            "decision_a": decision_a,
            "decision_b": decision_b,
            "final_decision": final_decision
        })
        return final_decision