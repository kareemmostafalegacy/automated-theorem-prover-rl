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

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical
from typing import Tuple

# ==========================================
# 2/4: Actor-Critic Neural Network Architecture (PyTorch)
# ==========================================

class LeanActorCritic(nn.Module):
    """
    Deep Neural Network utilizing a joint embedding backbone with decoupled 
    Actor (Policy) and Critic (Value) projection heads for proof search optimization.
    """
    def __init__(self, vocab_size: int = 5000, embedding_dim: int = 128, hidden_dim: int = 256, action_dim: int = 6):
        super(LeanActorCritic, self).__init__()
        
        # 1. Text Representation Backbone (Processes Lean compiler output text)
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        
        # 2. Shared Dense Representation Layer
        self.shared_dense = nn.Linear(hidden_dim, hidden_dim)
        
        # 3. Actor Head (Policy Network - Output probabilities over tactics)
        self.actor_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, action_dim)
        )
        
        # 4. Critic Head (Value Network - Evaluates how close the state is to 'goals accomplished')
        self.critic_head = nn.Sequential(
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 1)
        )

    def _tokenize_and_pad(self, raw_text: str, max_len: int = 64) -> torch.Tensor:
        """Helper to naively tokenize, numericalize, and pad raw compiler text into tensors."""
        # Custom numerical translation layer mapping text characters/words to indices
        tokens = [ord(char) % 4999 + 1 for char in raw_text] # Vocabulary hashing gate
        if len(tokens) < max_len:
            tokens += [0] * (max_len - len(tokens))
        else:
            tokens = tokens[:max_len]
        return torch.tensor(tokens, dtype=torch.long).unsqueeze(0) # Dimensions: [1, max_len]

    def forward(self, state_text: str) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Executes a forward mathematical pass. 
        Returns: Action Probabilities (Tensor) and State Value Estimation (Tensor).
        """
        # Convert state text to device-compatible long tensor
        state_tensor = self._tokenize_and_pad(state_text)
        
        # Feature extraction via Embedding and LSTM recurrent architecture
        embedded = self.embedding(state_tensor)
        lstm_out, (hidden, _) = self.lstm(embedded)
        
        # Compress temporal sequence representation using the final hidden state
        features = F.relu(self.shared_dense(hidden[-1])) # Dimensions: [1, hidden_dim]
        
        # Compute policy logits and transform via Softmax into exact probability distribution
        policy_logits = self.actor_head(features)
        action_probs = F.softmax(policy_logits, dim=-1)
        
        # Compute scalar value projection
        state_value = self.critic_head(features)
        
        return action_probs, state_value

    def select_action(self, state_text: str) -> Tuple[int, torch.Tensor, torch.Tensor]:
        """Samples an action index based on policy probabilities and tracks log probabilities."""
        action_probs, state_value = self.forward(state_text)
        
        # Construct categorical distribution over the action workspace
        dist = Categorical(action_probs)
        action = dist.sample()
        
        return action.item(), dist.log_prob(action), state_value
