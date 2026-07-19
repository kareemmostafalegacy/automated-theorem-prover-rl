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
