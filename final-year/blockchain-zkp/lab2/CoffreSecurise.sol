// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CoffreSecurise {
    uint256 public valeur;
    // Q3.3 Add an attribute address public proprietaire
    address public proprietaire;

    // In constructor, store msg.sender as the owner
    constructor() {
        proprietaire = msg.sender;
    }

    // Q3.4 Modify modify() so that it begins with:
    // require(msg.sender == proprietaire, "Access denied");
    function modify(uint256 nouvelleValeur) public {
        require(msg.sender == proprietaire, "Access denied");
        valeur = nouvelleValeur;
    }
}
