// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// The same vault, hardened against the flagged vulnerability classes.

contract Vault {
    address public owner;
    mapping(address => uint256) public balances;

    constructor() {
        owner = msg.sender;
    }

    function deposit() public payable {
        balances[msg.sender] += msg.value;
    }

    // Checks-effects-interactions: update state before the external call,
    // and use transfer() which reverts on failure.
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount, "insufficient");
        balances[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);
    }

    // Access-controlled mint.
    function mint(uint256 amount) public {
        require(msg.sender == owner, "not owner");
        balances[msg.sender] += amount;
    }

    // msg.sender, not tx.origin.
    function isSender(address who) public view returns (bool) {
        return who == msg.sender;
    }
}
