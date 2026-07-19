import Lake
open Lake DSL

/-!
  # 1/5: Advanced Project Metadata & Core Compiler Configuration
  This section establishes a production-grade package configuration with strict 
  pre-compiler options, thread management, and optimization tailoring.
-/

package «lean_project» where
  -- Core Source Directory
  srcDir := "src"
  
  -- Strict checking flags passed to the Lean compiler
  moreLeanArgs := #[
    "-DwarningAsError=true",  -- Treats all compiler warnings as fatal errors
    "-DautoImplicit=false"     -- Forces explicit identification of implicit variables for mathematical safety
  ]
  
  -- Low-level C compiler arguments for performance heavy environments
  moreLeancArgs := #[
    "-O3",                    -- Maximum optimization level for the generated C code
    "-march=native",          -- Compiles binaries tailored specifically to the host CPU architecture
    "-flto"                   -- Enables Link-Time Optimization for cross-module performance
  ]
  
  -- Linker arguments to ensure LTO is handled cleanly during assembly
  moreLinkArgs := #[
    "-flto"
  ]

import Lake
open Lake DSL

/-!
  # 1/5: Advanced Project Metadata & Core Compiler Configuration
-/
package «lean_project» where
  srcDir := "src"
  moreLeanArgs := #[
    "-DwarningAsError=true",
    "-DautoImplicit=false"
  ]
  moreLeancArgs := #[
    "-O3",
    "-march=native",
    "-flto"
  ]
  moreLinkArgs := #[
    "-flto"
  ]

/-!
  # 2/5: Enterprise Dependency Management & Toolchain Alignment
  Configuring remote high-performance packages and proof automation tooling.
-/

-- The foundational mathematical library for Lean 4
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "main"

-- Advanced rule-based auto-tactic framework for automated theorem proving
require aesop from git
  "https://github.com/leanprover-community/aesop.git" @ "main"

-- High-performance pattern-based search engine tool for theorem discovery
require loogle from git
  "https://github.com/leanprover-community/loogle.git" @ "main"
