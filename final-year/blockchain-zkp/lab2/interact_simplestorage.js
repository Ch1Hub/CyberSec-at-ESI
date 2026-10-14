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
    console.log("=== Part 2: Deploying & Interacting with SimpleStorage ===");
    
    // Get accounts
    const accounts = await rpcCall("eth_accounts");
    const deployer = accounts[0];
    console.log(`Deployer Account: ${deployer}`);

    const initialBlockHex = await rpcCall("eth_blockNumber");
    console.log(`Initial block number: ${parseInt(initialBlockHex, 16)}`);

    // Bytecode
    const bin = "0x" + fs.readFileSync('/home/chihab/Documents/study/cys3CS/emerginTech/lab2/SimpleStorage_sol_SimpleStorage.bin', 'utf8').trim();

    // 1. Deploy SimpleStorage
    console.log("\n[1] Deploying SimpleStorage contract...");
    const deployTxHash = await rpcCall("eth_sendTransaction", [{
        from: deployer,
        data: bin,
        gas: "0x2DC6C0" // 3,000,000 gas
    }]);
    console.log(`Deployment Tx Hash: ${deployTxHash}`);

    const deployReceipt = await rpcCall("eth_getTransactionReceipt", [deployTxHash]);
    const contractAddress = deployReceipt.contractAddress;
    console.log(`Deployed Contract Address: ${contractAddress}`);
    console.log(`Block Number after deploy: ${parseInt(deployReceipt.blockNumber, 16)}`);

    // 2. Initial getValeur()
    // selector for getValeur(): 0x378d7a6e
    console.log("\n[2] Calling getValeur() (Initial view call)...");
    const val0Hex = await rpcCall("eth_call", [{
        to: contractAddress,
        data: "0x378d7a6e"
    }, "latest"]);
    console.log(`getValeur() result: ${parseInt(val0Hex, 16)}`);
    const blockAfterView1 = await rpcCall("eth_blockNumber");
    console.log(`Block Number after view call: ${parseInt(blockAfterView1, 16)} (No new block created)`);

    // 3. Call setValeur(10)
    // selector for setValeur(uint256): 0x7f00b062
    // 10 in 32-byte hex: 000000000000000000000000000000000000000000000000000000000000000a
    console.log("\n[3] Sending transaction setValeur(10)...");
    const setValData = "0x7f00b062000000000000000000000000000000000000000000000000000000000000000a";
    const setTxHash = await rpcCall("eth_sendTransaction", [{
        from: deployer,
        to: contractAddress,
        data: setValData,
        gas: "0x100000"
    }]);
    console.log(`setValeur(10) Tx Hash: ${setTxHash}`);
    const setReceipt = await rpcCall("eth_getTransactionReceipt", [setTxHash]);
    console.log(`Block Number after setValeur(10): ${parseInt(setReceipt.blockNumber, 16)}`);

    // 4. Call getValeur() again
    console.log("\n[4] Calling getValeur() again...");
    const val1Hex = await rpcCall("eth_call", [{
        to: contractAddress,
        data: "0x378d7a6e"
    }, "latest"]);
    console.log(`getValeur() updated result: ${parseInt(val1Hex, 16)}`);

    const finalBlockHex = await rpcCall("eth_blockNumber");
    console.log(`Final block number: ${parseInt(finalBlockHex, 16)}`);
    console.log("Total new blocks created: 2 (1 for deployment + 1 for setValeur)");
}

run().catch(console.error);
