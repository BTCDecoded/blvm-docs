# TODO Resolution Plan

## Phase 1: RPC Calculations (High Priority)
- [ ] Difficulty calculation from chainstate
- [ ] Chainwork calculation (use existing calculate_total_work)
- [ ] Mediantime calculation (from recent headers)
- [ ] Confirmations calculation (height difference)
- [ ] Block height indexing
- [ ] Next block hash lookup

## Phase 2: Transaction Validation (High Priority)
- [ ] Use consensus.validate_transaction in sendrawtransaction
- [ ] Implement testmempoolaccept with proper validation
- [ ] Add UTXO set checks for transaction inputs

## Phase 3: Merkle Proofs (Medium Priority)
- [ ] Build transaction merkle proof function
- [ ] Implement gettxoutproof
- [ ] Implement verifytxoutproof

## Phase 4: Chain Verification (Medium Priority)
- [ ] Implement verifychain using consensus.validate_block
- [ ] Add block-by-block validation loop

## Phase 5: Network Features (Medium Priority)
- [ ] Persistent peer list storage
- [ ] Ban list implementation in NetworkManager
- [ ] Track bytes sent/received
- [ ] Fix ping to send actual messages

## Phase 6: Testing
- [ ] Add tests for all new RPC calculations
- [ ] Add tests for transaction validation
- [ ] Add tests for merkle proofs
- [ ] Add tests for chain verification

