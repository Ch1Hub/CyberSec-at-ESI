#!/bin/bash

# TP6 Part 1 (n8n) - Verification Checklist
# This script verifies that the FIM workflow is properly set up and working

echo "════════════════════════════════════════════════════════════════"
echo "  TP6 Part 1 - n8n File Integrity Monitoring - Verification"
echo "════════════════════════════════════════════════════════════════"
echo ""

PASSED=0
FAILED=0

# Function to print test result
print_result() {
    if [ $1 -eq 0 ]; then
        echo "  ✅ $2"
        ((PASSED++))
    else
        echo "  ❌ $2"
        ((FAILED++))
    fi
}

# Test 1: Docker is installed
docker --version &> /dev/null
print_result $? "Docker installed and accessible"

# Test 2: n8n container is running
docker ps | grep -q n8n-tp6
print_result $? "n8n container (n8n-tp6) is running"

# Test 3: Port 5678 is accessible
nc -z localhost 5678 &> /dev/null
print_result $? "Port 5678 is accessible (n8n UI)"

# Test 4: n8n API responds
curl -s http://localhost:5678/api/v1/workflows &> /dev/null
print_result $? "n8n API is responding"

# Test 5: Workflow file exists
[ -f /home/chihab/Documents/cys2CS/s2/opSysSec/tp/lab62/n8n-lab/file-integrity-monitoring-workflow.json ]
print_result $? "Workflow JSON file exists"

# Test 6: Target file exists
[ -f /home/chihab/Documents/cys2CS/s2/opSysSec/tp/lab62/n8n-lab/fim_target.txt ]
print_result $? "Target file (fim_target.txt) exists"

# Test 7: Alert log file exists
[ -f /home/chihab/Documents/cys2CS/s2/opSysSec/tp/lab62/n8n-lab/fim_alert.log ]
print_result $? "Alert log file (fim_alert.log) exists"

# Test 8: Alert log has content (workflow has run)
[ -s /home/chihab/Documents/cys2CS/s2/opSysSec/tp/lab62/n8n-lab/fim_alert.log ]
print_result $? "Alert log has been populated (workflow executed)"

# Test 9: Get workflow ID
WORKFLOW_ID=$(curl -s http://localhost:5678/api/v1/workflows | jq -r '.data[0].id' 2>/dev/null)
if [ ! -z "$WORKFLOW_ID" ] && [ "$WORKFLOW_ID" != "null" ]; then
    print_result 0 "Workflow found (ID: $WORKFLOW_ID)"
else
    print_result 1 "Could not retrieve workflow ID"
fi

# Test 10: Check if workflow is activated
curl -s http://localhost:5678/api/v1/workflows | jq '.data[] | select(.name == "TP6 - File Integrity Monitoring Alert")' | grep -q "TP6"
print_result $? "Workflow 'TP6 - File Integrity Monitoring Alert' is registered"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  Results"
echo "════════════════════════════════════════════════════════════════"
echo "  ✅ Passed: $PASSED"
echo "  ❌ Failed: $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo "  🎉 ALL CHECKS PASSED - Part 1 (n8n) is fully operational!"
    echo ""
    echo "  📋 Quick Test:"
    echo "    1. Modify the target file:"
    echo "       echo 'TEST' >> /home/chihab/Documents/cys2CS/s2/opSysSec/tp/lab62/n8n-lab/fim_target.txt"
    echo ""
    echo "    2. Wait ~65 seconds for scheduled execution"
    echo ""
    echo "    3. Check alert log:"
    echo "       cat /home/chihab/Documents/cys2CS/s2/opSysSec/tp/lab62/n8n-lab/fim_alert.log"
    echo ""
    echo "  🌐 Access n8n:"
    echo "    http://localhost:5678"
    exit 0
else
    echo "  ⚠️  Some checks failed. Please review the setup."
    exit 1
fi
