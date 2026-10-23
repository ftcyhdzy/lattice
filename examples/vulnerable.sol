// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Demonstrates several vulnerability classes detected by the Lattice engine.
// DO NOT DEPLOY this contract.

contract Vault {
    mapping(address => uint256) public balances;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    // LAT-001 reentrancy + LAT-002 unchecked call:
    // state is updated only after the value-bearing external call,
    // and the call's return value is ignored.
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount, "insufficient");
        msg.sender.call{value: amount}("");
        balances[msg.sender] -= amount;
    }

    // LAT-006: privileged operation with no access control.
    function mint(uint256 amount) public {
        balances[msg.sender] += amount;
    }

    // LAT-003: tx.origin used for authentication.
    function onlyOrigin() public view returns (bool) {
        return tx.origin == msg.sender;
    }

    // LAT-007: block.timestamp used as a gate.
    function timestampGate() public view returns (uint256) {
        return block.timestamp;
    }

    // LAT-008: explicit unchecked arithmetic.
    function uncheckedMath(uint256 a, uint256 b) public pure returns (uint256) {
        unchecked {
            return a - b;
        }
    }
}
