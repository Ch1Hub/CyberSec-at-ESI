// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SimpleStorage {
    // Q2.1 Add a public state variable named valeur of type uint256
    uint256 public valeur;

    // Q2.2 Add a function setValeur(uint256 nouvelleValeur) that updates this variable
    function setValeur(uint256 nouvelleValeur) public {
        valeur = nouvelleValeur;
    }

    // Q2.3 Add a view function getValeur() that returns the stored value
    function getValeur() public view returns (uint256) {
        return valeur;
    }
}
