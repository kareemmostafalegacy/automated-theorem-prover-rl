"""
ai_agent Package Initializer.

This module acts as an enterprise-grade API facade for the automated 
theorem-proving AI subsystem, isolating architectural internals from client exposure.
"""

import sys
from typing import List

# 1/4: Unified API Facade & Export Control
# Dynamically resolving and elevating core engine components to the package root.

try:
    # Simulating the absolute architectural imports from the package submodules
    from .engine import AIAgentCore, TheoremProverBridge
    from .models import ProofState, TacticProposal
except ImportError as error:
    # Fail-fast mechanism if the structural submodules are corrupted
    raise ImportError(
        f"Critical Failure: package initialization aborted due to missing internal components: {error}"
    ) from error

# Defining the strict public interface boundary of the Python package
__all__: List[str] = [
    "AIAgentCore",
    "TheoremProverBridge",
    "ProofState",
    "TacticProposal",
]

# Package Semantic Versioning (SemVer) Invariant
__version__: str = "1.0.0-alpha.4"

# Prevent pollution of the namespace by removing helper primitives
del sys

import os
import sys
import asyncio
from typing import List, Dict, Any

# [1/4: Unified API Facade & Export Control - Pre-defined]
try:
    from .engine import AIAgentCore, TheoremProverBridge
    from .models import ProofState, TacticProposal
except ImportError as error:
    raise ImportError(
        f"Critical Failure: package initialization aborted due to missing internal components: {error}"
    ) from error

__all__: List[str] = ["AIAgentCore", "TheoremProverBridge", "ProofState", "TacticProposal"]
__version__: str = "1.0.0-alpha.4"

# ==========================================
# 2/4: Asynchronous Runtime Initialization & Environment Validation
# ==========================================

class RuntimeEnvironment:
    """Manages secure validation and async bootstrap protocols for the AI Agent."""
    
    _global_registry: Dict[str, Any] = {}

    @classmethod
    async def verify_infrastructure(cls) -> bool:
        """
        Performs non-blocking validation of the underlying OS environment 
        and critical cryptographic LLM credentials.
        """
        # 1. Verify existence of the primary LLM API orchestrator key
        if "OPENAI_API_KEY" not in os.environ and "ANTHROPIC_API_KEY" not in os.environ:
            raise RuntimeError(
                "Environment Corruption: Missing LLM provider credentials. "
                "Ensure either 'OPENAI_API_KEY' or 'ANTHROPIC_API_KEY' is exported."
            )

        # 2. Asynchronously check Lean 4 compiler visibility in system paths
        process = await asyncio.create_subprocess_exec(
            "elan", "--version",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await process.communicate()
        
        if process.returncode != 0:
            raise RuntimeError(
                "Dependency Gap: 'elan' manager or Lean 4 toolchain not detected in system PATH. "
                "Verify lean-toolchain configuration before initiating the AI lifecycle."
            )

        cls._global_registry["initialized"] = True
        cls._global_registry["toolchain_signature"] = stdout.decode().strip()
        return True

# Initialize execution of environment verification gates safely
# Client runtimes can await this directly before triggering agent inference loops
asyncio.ensure_future(RuntimeEnvironment.verify_infrastructure())
