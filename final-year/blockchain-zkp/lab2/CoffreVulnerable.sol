// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CoffreVulnerable {
    uint256 public valeur;

    function modify(uint256 nouvelleValeur) public {
        valeur = nouvelleValeur;
    }
}
