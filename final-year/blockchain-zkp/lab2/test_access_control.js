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

function encodeModify(value) {
    const valHex = value.toString(16).padStart(64, '0');
    return "0x916adad0" + valHex;
}

async function run() {
    console.log("=== Part 3.A: Missing Access Control Demonstration ===");
    const accounts = await rpcCall("eth_accounts");
    const account0 = accounts[0]; // Owner
    const account1 = accounts[1]; // Attacker / Unauthorized user

    console.log(`Account(0) [Owner]:      ${account0}`);
    console.log(`Account(1) [Unauthorized]: ${account1}`);

    // --- STEP 1: TEST VULNERABLE CONTRACT ---
    console.log("\n--- Testing CoffreVulnerable ---");
    const binVuln = "0x" + fs.readFileSync('/home/chihab/Documents/study/cys3CS/emerginTech/lab2/CoffreVulnerable_sol_CoffreVulnerable.bin', 'utf8').trim();
    
    // Deploy vulnerable contract with account(0)
    const txDeployVuln = await rpcCall("eth_sendTransaction", [{
        from: account0,
        data: binVuln,
        gas: "0x2DC6C0"
    }]);
    const receiptVuln = await rpcCall("eth_getTransactionReceipt", [txDeployVuln]);
    const addrVuln = receiptVuln.contractAddress;
    console.log(`CoffreVulnerable deployed at: ${addrVuln}`);

    // Q3.1: Call modify(10) from account(0)
    console.log("\n[Q3.1] Account(0) calls modify(10)...");
    const txVuln10 = await rpcCall("eth_sendTransaction", [{
        from: account0,
        to: addrVuln,
        data: encodeModify(10),
        gas: "0x100000"
    }]);
    await rpcCall("eth_getTransactionReceipt", [txVuln10]);
    let valVuln = await rpcCall("eth_call", [{ to: addrVuln, data: "0x5d2c2e73" }, "latest"]);
    console.log(`valeur is now: ${parseInt(valVuln, 16)}`);

    // Q3.2: Select account(1) and call modify(999)
    console.log("\n[Q3.2] Account(1) calls modify(999)...");
    const txVuln999 = await rpcCall("eth_sendTransaction", [{
        from: account1,
        to: addrVuln,
        data: encodeModify(999),
        gas: "0x100000"
    }]);
    await rpcCall("eth_getTransactionReceipt", [txVuln999]);
    valVuln = await rpcCall("eth_call", [{ to: addrVuln, data: "0x5d2c2e73" }, "latest"]);
    console.log(`valeur is now: ${parseInt(valVuln, 16)}`);
    console.log("-> Observation: Call SUCCEEDED! Any external account can overwrite the stored value because modify() lacks access control.");

    // --- STEP 2: TEST SECURE CONTRACT ---
    console.log("\n--- Testing CoffreSecurise ---");
    const binSec = "0x" + fs.readFileSync('/home/chihab/Documents/study/cys3CS/emerginTech/lab2/CoffreSecurise_sol_CoffreSecurise.bin', 'utf8').trim();

    // Deploy secure contract with account(0)
    const txDeploySec = await rpcCall("eth_sendTransaction", [{
        from: account0,
        data: binSec,
        gas: "0x2DC6C0"
    }]);
    const receiptSec = await rpcCall("eth_getTransactionReceipt", [txDeploySec]);
    const addrSec = receiptSec.contractAddress;
    console.log(`CoffreSecurise deployed at: ${addrSec}`);

    // Verify proprietaire
    const ownerHex = await rpcCall("eth_call", [{ to: addrSec, data: "0x79583ee5" }, "latest"]);
    const ownerAddress = "0x" + ownerHex.slice(26);
    console.log(`Contract proprietaire: ${ownerAddress} (Matches Account(0): ${ownerAddress.toLowerCase() === account0.toLowerCase()})`);

    // Q3.5: Test with owner account(0) -> modify(50)
    console.log("\n[Q3.5 - Test 1] Owner Account(0) calls modify(50)...");
    const txSec50 = await rpcCall("eth_sendTransaction", [{
        from: account0,
        to: addrSec,
        data: encodeModify(50),
        gas: "0x100000"
    }]);
    await rpcCall("eth_getTransactionReceipt", [txSec50]);
    let valSec = await rpcCall("eth_call", [{ to: addrSec, data: "0x5d2c2e73" }, "latest"]);
    console.log(`valeur is now: ${parseInt(valSec, 16)} (SUCCESS)`);

    // Q3.5: Test with unauthorized account(1) -> modify(999)
    console.log("\n[Q3.5 - Test 2] Unauthorized Account(1) calls modify(999)...");
    try {
        await rpcCall("eth_sendTransaction", [{
            from: account1,
            to: addrSec,
            data: encodeModify(999),
            gas: "0x100000"
        }]);
        console.log("Unexpected success!");
    } catch (err) {
        console.log("-> Transaction REVERTED as expected!");
        console.log(`Error message: ${err.message || JSON.stringify(err)}`);
    }

    valSec = await rpcCall("eth_call", [{ to: addrSec, data: "0x5d2c2e73" }, "latest"]);
    console.log(`valeur remains unchanged: ${parseInt(valSec, 16)}`);
    console.log("-> Observation: Access control successfully blocks unauthorized callers.");
}

run().catch(console.error);
