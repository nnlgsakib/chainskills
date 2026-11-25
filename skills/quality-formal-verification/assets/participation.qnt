// Starter model: bonded participants, commit-reveal tasks, slashing, bounded rewards.
// Adapt names/IDs to your spec (docs/spec/<component>.md). Invariant names follow INV_<COMP>_<n>.
//
//   quint typecheck participation.qnt
//   quint run participation.qnt --max-steps=40 --max-samples=2000       # random simulation, checks all `invariant`s
//   quint verify participation.qnt --invariant=INV_PART_1 --max-steps=10 # bounded model checking (needs Java; Apalache is fetched)
module participation {
  type Node = str

  pure val NODES: Set[Node] = Set("n1", "n2", "n3")
  pure val INITIAL_BALANCE = 100
  pure val MIN_BOND = 10
  pure val EPOCH_BUDGET = 30
  pure val SLASH = 5

  // --- state ---
  var balance: Node -> int        // liquid tokens
  var bond: Node -> int           // bonded tokens (slashable)
  var committed: Set[Node]        // committed a result this epoch
  var revealedOk: Set[Node]       // revealed a result matching its commitment
  var paid: int                   // rewards paid this epoch
  var burned: int                 // total slashed (burned)
  var minted: int                 // total rewards minted

  // --- helpers ---
  pure def sumOf(m: Node -> int): int = NODES.fold(0, (acc, n) => acc + m.get(n))

  // --- actions ---
  action init = all {
    balance' = NODES.mapBy(_ => INITIAL_BALANCE),
    bond' = NODES.mapBy(_ => 0),
    committed' = Set(),
    revealedOk' = Set(),
    paid' = 0,
    burned' = 0,
    minted' = 0,
  }

  action register(n: Node, amount: int): bool = all {
    amount >= MIN_BOND,
    balance.get(n) >= amount,
    balance' = balance.setBy(n, b => b - amount),
    bond' = bond.setBy(n, b => b + amount),
    committed' = committed, revealedOk' = revealedOk, paid' = paid, burned' = burned, minted' = minted,
  }

  action commit(n: Node): bool = all {
    bond.get(n) >= MIN_BOND,
    not(committed.contains(n)),
    committed' = committed.union(Set(n)),
    balance' = balance, bond' = bond, revealedOk' = revealedOk, paid' = paid, burned' = burned, minted' = minted,
  }

  // honest reveal: matches the commitment
  action reveal(n: Node): bool = all {
    committed.contains(n),
    not(revealedOk.contains(n)),
    revealedOk' = revealedOk.union(Set(n)),
    balance' = balance, bond' = bond, committed' = committed, paid' = paid, burned' = burned, minted' = minted,
  }

  // provable fraud (reveal does not match commitment): slash, never more than the bond
  action slash(n: Node): bool = all {
    committed.contains(n),
    not(revealedOk.contains(n)),
    bond.get(n) > 0,
    val s = if (bond.get(n) < SLASH) bond.get(n) else SLASH
    all {
      bond' = bond.setBy(n, b => b - s),
      burned' = burned + s,
      balance' = balance, committed' = committed, revealedOk' = revealedOk, paid' = paid, minted' = minted,
    }
  }

  // pay one verified unit of work, within the epoch budget
  action payReward(n: Node, amount: int): bool = all {
    revealedOk.contains(n),
    amount > 0,
    paid + amount <= EPOCH_BUDGET,
    balance' = balance.setBy(n, b => b + amount),
    paid' = paid + amount,
    minted' = minted + amount,
    bond' = bond, committed' = committed, revealedOk' = revealedOk, burned' = burned,
  }

  action newEpoch = all {
    committed' = Set(), revealedOk' = Set(), paid' = 0,
    balance' = balance, bond' = bond, burned' = burned, minted' = minted,
  }

  action step = {
    nondet n = NODES.oneOf()
    nondet amount = 1.to(20).oneOf()
    any {
      register(n, amount),
      commit(n),
      reveal(n),
      slash(n),
      payReward(n, amount),
      newEpoch,
    }
  }

  // --- invariants (map to docs/spec/invariants.md) ---
  // INV-PART-1: rewards paid in an epoch never exceed the epoch budget
  invariant INV_PART_1 = paid <= EPOCH_BUDGET
  // INV-PART-2: only nodes with a verified reveal are paid (paid > 0 implies someone revealed)
  invariant INV_PART_2 = paid > 0 implies revealedOk.size() > 0
  // INV-PART-4: bonds never go negative (slash <= bond)
  invariant INV_PART_4 = NODES.forall(n => bond.get(n) >= 0)
  // INV-TOKEN-1: supply conservation: liquid + bonded == initial + minted - burned
  invariant INV_TOKEN_1 = sumOf(balance) + sumOf(bond) == NODES.size() * INITIAL_BALANCE + minted - burned

  // --- observations (reachability sanity checks) ---
  observation someoneSlashed = burned > 0
  observation budgetExhausted = paid == EPOCH_BUDGET
}
