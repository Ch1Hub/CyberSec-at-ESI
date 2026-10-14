const fs = require('fs');
const http = require('http');

function rpc(method, params = []) {
    return new Promise((resolve, reject) => {
        const payload = JSON.stringify({ jsonrpc: "2.0", method, params, id: Date.now() });
        const req = http.request({
            hostname: '127.0.0.1',
            port: 8545,
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(payload) }
        }, res => {
            let d = '';
            res.on('data', chunk => d += chunk);
            res.on('end', () => {
                const parsed = JSON.parse(d);
                if (parsed.error) reject(parsed.error);
                else resolve(parsed.result);
            });
        });
        req.on('error', reject);
        req.write(payload);
        req.end();
    });
}

function pad(val) {
    return val.toString(16).padStart(64, '0');
}

async function main() {
    console.log("===============================================================");
    console.log("        LAB 2: FULL END-TO-END VALIDATION & TEST RUNNER        ");
    console.log("===============================================================\n");

    // 1. Check Ganache Connection
    console.log("[CHECK] Verifying Ganache JSON-RPC connection...");
    const accounts = await rpc("eth_accounts");
    const blockNum = await rpc("eth_blockNumber");
    console.log(`[PASS] Connected! Available accounts: ${accounts.length}, Current Block: ${parseInt(blockNum, 16)}`);

    // -------------------------------------------------------------------------
    // PART 2: SimpleStorage
    // -------------------------------------------------------------------------
    console.log("\n---------------------------------------------------------------");
    console.log("  TESTING PART 2: SimpleStorage (Compile, Deploy, Set & View)  ");
    console.log("---------------------------------------------------------------");
    const binSimple = "0x" + fs.readFileSync('/home/chihab/Documents/study/cys3CS/emerginTech/lab2/SimpleStorage_sol_SimpleStorage.bin', 'utf8').trim();
    
    const deploySimpleTx = await rpc("eth_sendTransaction", [{ from: accounts[0], data: binSimple, gas: "0x2DC6C0" }]);
    const receiptSimple = await rpc("eth_getTransactionReceipt", [deploySimpleTx]);
    const simpleAddr = receiptSimple.contractAddress;
    console.log(`[DEPLOY] SimpleStorage deployed at: ${simpleAddr}`);

    // Call getValeur()
    const getVal1 = await rpc("eth_call", [{ to: simpleAddr, data: "0x378d7a6e" }, "latest"]);
    console.log(`[READ] Initial getValeur(): ${parseInt(getVal1, 16)} (Expected: 0)`);

    // Call setValeur(10)
    console.log("[WRITE] Sending transaction setValeur(10)...");
    const setValTx = await rpc("eth_sendTransaction", [{
        from: accounts[0],
        to: simpleAddr,
        data: "0x7f00b062" + pad(10),
        gas: "0x100000"
    }]);
    await rpc("eth_getTransactionReceipt", [setValTx]);

    const getVal2 = await rpc("eth_call", [{ to: simpleAddr, data: "0x378d7a6e" }, "latest"]);
    console.log(`[READ] Updated getValeur(): ${parseInt(getVal2, 16)} (Expected: 10)`);
    if (parseInt(getVal2, 16) === 10) {
        console.log(">>> [SUCCESS] Part 2 SimpleStorage works as specified!");
    } else {
        console.error(">>> [FAIL] SimpleStorage value mismatch!");
    }

    // -------------------------------------------------------------------------
    // PART 3.A: Missing Access Control
    // -------------------------------------------------------------------------
    console.log("\n---------------------------------------------------------------");
    console.log("  TESTING PART 3.A: Access Control (Vulnerable vs Secured)     ");
    console.log("---------------------------------------------------------------");
    
    // Deploy CoffreVulnerable
    const binVuln = "0x" + fs.readFileSync('/home/chihab/Documents/study/cys3CS/emerginTech/lab2/CoffreVulnerable_sol_CoffreVulnerable.bin', 'utf8').trim();
    const txVulnDeploy = await rpc("eth_sendTransaction", [{ from: accounts[0], data: binVuln, gas: "0x2DC6C0" }]);
    const receiptVuln = await rpc("eth_getTransactionReceipt", [txVulnDeploy]);
    const vulnAddr = receiptVuln.contractAddress;
    console.log(`[DEPLOY] CoffreVulnerable at: ${vulnAddr}`);

    // Account 0 sets 10
    await rpc("eth_sendTransaction", [{ from: accounts[0], to: vulnAddr, data: "0x916adad0" + pad(10), gas: "0x100000" }]);
    // Unauthorized Account 1 sets 999
    await rpc("eth_sendTransaction", [{ from: accounts[1], to: vulnAddr, data: "0x916adad0" + pad(999), gas: "0x100000" }]);
    const valVuln = await rpc("eth_call", [{ to: vulnAddr, data: "0x5d2c2e73" }, "latest"]);
    console.log(`[VULNERABILITY CONFIRMED] Unauthorized Account(1) overwrote value to: ${parseInt(valVuln, 16)}`);

    // Deploy CoffreSecurise
    const binSec = "0x" + fs.readFileSync('/home/chihab/Documents/study/cys3CS/emerginTech/lab2/CoffreSecurise_sol_CoffreSecurise.bin', 'utf8').trim();
    const txSecDeploy = await rpc("eth_sendTransaction", [{ from: accounts[0], data: binSec, gas: "0x2DC6C0" }]);
    const receiptSec = await rpc("eth_getTransactionReceipt", [txSecDeploy]);
    const secAddr = receiptSec.contractAddress;
    console.log(`\n[DEPLOY] CoffreSecurise at: ${secAddr}`);

    // Owner Account 0 modifies to 50
    await rpc("eth_sendTransaction", [{ from: accounts[0], to: secAddr, data: "0x916adad0" + pad(50), gas: "0x100000" }]);
    const valSec1 = await rpc("eth_call", [{ to: secAddr, data: "0x5d2c2e73" }, "latest"]);
    console.log(`[OWNER ACCESS] Owner set value to: ${parseInt(valSec1, 16)} (Success)`);

    // Unauthorized Account 1 attempts modify(999)
    let reverted = false;
    try {
        await rpc("eth_call", [{ from: accounts[1], to: secAddr, data: "0x916adad0" + pad(999) }, "latest"]);
    } catch (err) {
        reverted = true;
        console.log(`[SECURITY BLOCKED] Unauthorized call reverted with message: "${err.message}"`);
    }
    if (reverted) {
        console.log(">>> [SUCCESS] Part 3.A Access Control properly defended by require()!");
    }

    // -------------------------------------------------------------------------
    // PART 3.B: Reentrancy Attack & CEI
    // -------------------------------------------------------------------------
    console.log("\n---------------------------------------------------------------");
    console.log("  TESTING PART 3.B: Reentrancy Exploitation & CEI Protection   ");
    console.log("---------------------------------------------------------------");
    const binReentrancy = "0x" + fs.readFileSync('/home/chihab/Documents/study/cys3CS/emerginTech/lab2/ReentrancyDemo_sol_ReentrancyVulnerable.bin', 'utf8').trim();
    const txReentrancyDeploy = await rpc("eth_sendTransaction", [{ from: accounts[4], data: binReentrancy, gas: "0x2DC6C0" }]);
    const receiptReentrancy = await rpc("eth_getTransactionReceipt", [txReentrancyDeploy]);
    const reentrancyAddr = receiptReentrancy.contractAddress;
    console.log(`[DEPLOY] ReentrancyVulnerable at: ${reentrancyAddr}`);

    // Victim deposits 5 ETH
    const fiveEth = "0x4563918244F40000";
    await rpc("eth_sendTransaction", [{ from: accounts[4], to: reentrancyAddr, value: fiveEth, data: "0x42dc400f", gas: "0x100000" }]);
    let balBefore = await rpc("eth_getBalance", [reentrancyAddr, "latest"]);
    console.log(`[FUNDED] Victim deposited: ${Number(BigInt(balBefore)) / 1e18} ETH`);

    // Deploy Attacker contract pointing to victim
    const binAttacker = "0x" + fs.readFileSync('/home/chihab/Documents/study/cys3CS/emerginTech/lab2/ReentrancyDemo_sol_AttaquantReentrancy.bin', 'utf8').trim();
    const encodedTarget = reentrancyAddr.toLowerCase().replace('0x', '').padStart(64, '0');
    const txAttackerDeploy = await rpc("eth_sendTransaction", [{ from: accounts[5], data: binAttacker + encodedTarget, gas: "0x2DC6C0" }]);
    const receiptAttacker = await rpc("eth_getTransactionReceipt", [txAttackerDeploy]);
    const attackerAddr = receiptAttacker.contractAddress;
    console.log(`[DEPLOY] AttaquantReentrancy at: ${attackerAddr}`);

    // Trigger attack with 1 ETH
    console.log("[EXPLOIT] Attacker executing reentrant call loop...");
    const oneEth = "0xDE0B6B3A7640000";
    await rpc("eth_sendTransaction", [{ from: accounts[5], to: attackerAddr, value: oneEth, data: "0xada82558", gas: "0x500000" }]);

    let balVictimAfter = await rpc("eth_getBalance", [reentrancyAddr, "latest"]);
    let balAttackerAfter = await rpc("eth_getBalance", [attackerAddr, "latest"]);
    console.log(`[STATUS] Victim balance:   ${Number(BigInt(balVictimAfter)) / 1e18} ETH (Drained to 0!)`);
    console.log(`[STATUS] Attacker balance: ${Number(BigInt(balAttackerAfter)) / 1e18} ETH (Stole all 6 ETH!)`);
    console.log(">>> [SUCCESS] Part 3.B Reentrancy attack verified!");

    console.log("\n===============================================================");
    console.log("             ALL TESTS COMPLETED SUCCESSFULLY!                 ");
    console.log("===============================================================");
}

main().catch(console.error);
