import Lean

/-!
  # 1/3: Classical & Non-Constructive Axioms
  This section injects foundational, non-constructive mathematical truths into the system.
  We bypass Lean's constructive kernel safely by encapsulating foundational postulates.
-/

namespace AdvancedAxioms

/--
  The Law of Excluded Middle (LEM) for arbitrary propositions.
  Asserts that for any logical statement `P`, it is either logically true or its negation is true.
  This unlocks classical proof techniques like double-negation elimination.
-/
axiom law_of_excluded_middle (P : Prop) : P ∨ ¬P

/--
  The Axiom of Choice (AoC) formulated across higher type universes.
  Given a non-empty collection of non-empty sets represented by a type `α` and a predicate `P`,
  there exists a universal choice function that can extract an element safely.
-/
axiom axiom_of_choice {α : Type u} {β : α → Type v} (h : ∀ x : α, Nonempty (β x)) : 
  Nonempty (∀ x : α, β x)

/--
  Propositional Extensionality (PropExt).
  States that if two logical propositions imply each other (are logically equivalent),
  they are definitionally equal. This allows rewriting logical equivalences as equality.
-/
axiom prop_extensionality {P Q : Prop} (h1 : P → Q) (h2 : Q → P) : P = Q

end AdvancedAxioms
