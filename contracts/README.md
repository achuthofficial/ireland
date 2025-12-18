# Vendor Contracts

## Place the 61 vendor contract HTML files here

This folder should contain the original vendor contract files that were analyzed in Phase 1.

**Expected files:**
- 61 vendor contract files in HTML format
- From companies like: AWS, Google, Microsoft, Adobe, Oracle, SAP, Salesforce, etc.

**File naming convention:**
- `[vendor_name]_contract.html`
- Example: `aws_contract.html`, `google_contract.html`, etc.

**To analyze a contract:**
```bash
cd /workspaces/ireland/code
python assess_contract.py --file /workspaces/ireland/contracts/[vendor]_contract.html
```

**To batch process all contracts:**
```bash
cd /workspaces/ireland/code
python assess_contract.py --directory /workspaces/ireland/contracts/
```
