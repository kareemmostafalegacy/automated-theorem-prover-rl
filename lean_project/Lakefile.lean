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
