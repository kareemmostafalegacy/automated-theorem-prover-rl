import numpy as np
from typing import Tuple, Dict, Any, List
from lean_project.ai_agent import LeanCompilerProcessManager

# 1/4: Markov Decision Process & Cryptographic Reward Shaping Environment

class LeanProverEnv:
    """
    Custom Reinforcement Learning environment formalizing the proof search 
    as a Markov Decision Process (MDP) over Lean 4 state graphs.
    """
    def __init__(self, target_theorem: str, max_steps: int = 10):
        self.theorem = target_theorem
        self.max_steps = max_steps
        self.current_step = 0
        self.ipc_manager = LeanCompilerProcessManager()
        self.tactic_pool: List[str] = ["ext x", "simp only [LinearMap.mem_ker]", "constructor", "rcases lem_check with h_zero | h_nonzero", "contradiction", "exact False.elim h_final_absurdity"]
        self.state_history: List[str] = []

    async def reset(self) -> str:
        """Resets the environment and initiates a hot compiler REPL session."""
        self.current_step = 0
        self.state_history.clear()
        await self.ipc_manager.spawn_interactive_session()
        # Initialize the environment by feeding the target theorem statement
        initial_state = await self.ipc_manager.send_tactic_and_await_state(f"theorem target_search : {self.theorem} := by")
        self.state_history.append(initial_state)
        return initial_state

    def _calculate_shaped_reward(self, raw_response: str, is_done: bool) -> float:
        """
        Calculates mathematical reward semantics based on dense state analysis.
        Encourages proof depth compaction and penalizes compilation friction.
        """
        # Base penalty for taking a processing step to enforce proof minimization
        reward = -0.05 
        
        # Severe penalty for syntax/type mismatches from the compiler kernel
        if "error:" in raw_response.lower() or "unsolved goals" in raw_response.lower():
            reward += -1.5
            return reward

        # High-magnitude positive reward for solving a sub-goal or completing the proof
        if "goals accomplished" in raw_response.lower() or is_done:
            reward += 10.0 + (self.max_steps - self.current_step) * 0.5  # Efficiency bonus
            
        return reward

    async def step(self, action_idx: int) -> Tuple[str, float, bool, Dict[str, Any]]:
        """Executes a single structural tactic transformation inside the Lean kernel."""
        self.current_step += 1
        tactic = self.tactic_pool[action_idx]
        
        # Pipe the chosen action directly into the running compiler process
        compiler_state = await self.ipc_manager.send_tactic_and_await_state(tactic)
        self.state_history.append(compiler_state)

        # Termination Criteria Check
        is_done = "goals accomplished" in compiler_state.lower() or self.current_step >= self.max_steps
        
        # Calculate the highly scalarized reward
        reward = self._calculate_shaped_reward(compiler_state, is_done)
        
        info = {"step": self.current_step, "applied_tactic": tactic, "raw_kernel_state": compiler_state}
        
        if is_done:
            await self.ipc_manager.terminate_session()

        return compiler_state, reward, is_done, info
