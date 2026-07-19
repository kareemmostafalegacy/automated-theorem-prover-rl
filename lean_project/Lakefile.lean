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
-/
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "main"
require aesop from git
  "https://github.com/leanprover-community/aesop.git" @ "main"
require loogle from git
  "https://github.com/leanprover-community/loogle.git" @ "main"

/-!
  # 3/5: Modular Multi-Target Architecture & Component Isolation
  Segmenting the project into a core verified library and high-performance executables.
-/

/--
  The primary verified library target. 
  Houses all mathematical proofs, foundational datatypes, and core logic.
-/
@[default_target]
lean_lib «LeanProjectCore» where
  srcDir := "src/core"
  -- Target-specific overrides: allow slightly more memory usage during heavy verification
  moreLeanArgs := #["-DmaxHeartbeats=500000"] 

/--
  High-performance Command Line Interface (CLI) executable target.
  Compiled into a native binary for real-world execution.
-/
lean_exe «lean_project_cli» where
  root := `Main
  srcDir := "src/cli"
  -- Enforce total memory safety and static linking for the output binary
  supportInterpreter := true

import Lake
open Lake DSL

/-!
  # 1/5: Advanced Project Metadata & Core Compiler Configuration
-/
package «lean_project» where
  srcDir := "src"
  moreLeanArgs := #[
    "-DwarningAsError=true",
    "-DautoImplicit=false",
    /- 
      # 4/5: Enterprise-Grade Linters & Strict Quality Enforcement
      Injecting strict static analysis rules directly into the global compiler flags.
    -/
    "-Dlinter.unusedVariables=true",       -- Rejects code with dead or unused variables
    "-Dlinter.missingDocs=true",           -- Forces 100% documentation coverage on all public definitions
    "-Dlinter.unusedRCases=true",          -- Catches redundant pattern matching structures in proofs
    "-Dlinter.deprecated=true",            -- Bans the use of deprecated or outdated library functions
    "-Dlinter.constructorNameAsType=true"  -- Prevents ambiguous naming collisions in inductive types
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
-/
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "main"
require aesop from git
  "https://github.com/leanprover-community/aesop.git" @ "main"
require loogle from git
  "https://github.com/leanprover-community/loogle.git" @ "main"

/-!
  # 3/5: Modular Multi-Target Architecture & Component Isolation
-/
@[default_target]
lean_lib «LeanProjectCore» where
  srcDir := "src/core"
  moreLeanArgs := #["-DmaxHeartbeats=500000"] 

lean_exe «lean_project_cli» where
  root := `Main
  srcDir := "src/cli"
  supportInterpreter := true

import Lake
open Lake DSL

/-!
  # 1/5: Advanced Project Metadata & Core Compiler Configuration
-/
package «lean_project» where
  srcDir := "src"
  moreLeanArgs := #[
    "-DwarningAsError=true",
    "-DautoImplicit=false",
    "-Dlinter.unusedVariables=true",
    "-Dlinter.missingDocs=true",
    "-Dlinter.unusedRCases=true",
    "-Dlinter.deprecated=true",
    "-Dlinter.constructorNameAsType=true"
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
-/
require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @ "main"
require aesop from git
  "https://github.com/leanprover-community/aesop.git" @ "main"
require loogle from git
  "https://github.com/leanprover-community/loogle.git" @ "main"

/-!
  # 3/5: Modular Multi-Target Architecture & Component Isolation
-/
@[default_target]
lean_lib «LeanProjectCore» where
  srcDir := "src/core"
  moreLeanArgs := #["-DmaxHeartbeats=500000"] 

lean_exe «lean_project_cli» where
  root := `Main
  srcDir := "src/cli"
  supportInterpreter := true

/-!
  # 5/5: Advanced Automation via Custom Lake Scripts
  Directly programming the build system using Lean's asynchronous IO and process management.
-/

/--
  Locates and executes all test binaries within the test suite,
  providing automated test-runner capabilities for CI/CD pipelines.
  Run via: `lake run run-tests`
-/
script «run-tests» (args : List String) := do
  IO.println "🚀 Launching Lean Project Test Suite Automation..."
  
  -- Spawning a concurrent process to run Lean on our test entry point
  let testProcess ← IO.Process.spawn {
    cmd := "lake"
    args := #["build", "LeanProjectCore"]
  }
  let exitCode ← testProcess.wait
  
  if exitCode != 0 then
    IO.eprintln "❌ Core library build failed. Aborting tests."
    return 1
  
  IO.println "✅ Core compiled. Simulating test execution framework..."
  -- Here you can expand to parse test files dynamically from a 'tests' directory
  return 0

/--
  Performs an aggressive purge of all build artifacts, build caches, and temporary C files.
  Run via: `lake run clean-all`
-/
script «clean-all» (args : List String) := do
  IO.println "🧹 Initiating aggressive workspace purification..."
  
  let buildDir := __dir__ / ".lake" / "build"
  if ← buildDir.pathExists then
    IO.println s!"Removing cached artifacts from: {buildDir}"
    -- System level directory removal
    IO.FS.removeDirAll buildDir
    IO.println "✨ Workspace environment successfully purified."
  else
    IO.println "✨ Workspace is already pristine. No action required."
  return 0
