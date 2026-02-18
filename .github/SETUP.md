# Quick Setup Guide for Repository Administrators

This guide helps repository administrators quickly set up essential protections for the Criminal Appeal repository.

## 🔒 Step 1: Enable Branch Protection (CRITICAL)

The main branch needs protection to prevent accidental force pushes or deletions.

### Option A: Automated Setup (Recommended)

Run the provided script:
```bash
./.github/setup-branch-protection.sh
```

### Option B: Manual Setup via GitHub Web UI

1. Go to https://github.com/djkingy79-yo/Criminal-Appeal/settings/branches
2. Click "Add rule" under "Branch protection rules"
3. Enter `main` as the branch name pattern
4. Enable these settings:
   - ✅ Require a pull request before merging
     - Set "Required approvals" to 1
   - ✅ Require conversation resolution before merging
   - ✅ Dismiss stale pull request approvals when new commits are pushed
   - ⛔ Allow force pushes - **LEAVE UNCHECKED**
   - ⛔ Allow deletions - **LEAVE UNCHECKED**
5. Click "Create" to save

### Option C: Using GitHub CLI

```bash
gh api repos/djkingy79-yo/Criminal-Appeal/branches/main/protection \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  --input .github/branch-protection-config.json
```

## ✅ Step 2: Verify Protection is Active

Check the branch protection status:

```bash
# Using GitHub CLI
gh api repos/djkingy79-yo/Criminal-Appeal/branches/main/protection

# Or visit:
# https://github.com/djkingy79-yo/Criminal-Appeal/settings/branches
```

You should see a lock icon 🔒 next to the main branch protection rule.

## 📋 Step 3: Test the Protection

Try to force push to main (this should fail):
```bash
# This command should be rejected
git push --force origin main
# Expected: "protected branch hook declined"
```

## 📚 Additional Resources

- Full documentation: [BRANCH_PROTECTION.md](../BRANCH_PROTECTION.md)
- Contributing guidelines: [CONTRIBUTING.md](../CONTRIBUTING.md)
- Security policy: [SECURITY.md](../SECURITY.md)

## 🆘 Troubleshooting

**Problem**: "403 Forbidden" or "Permission denied"
- **Solution**: Ensure you have admin access to the repository

**Problem**: Script fails with "gh not found"
- **Solution**: Install GitHub CLI from https://cli.github.com/

**Problem**: "Not authenticated"
- **Solution**: Run `gh auth login` first

## 🎯 Next Steps

After setting up branch protection:
1. ✅ Update team members about the new workflow
2. ✅ Ensure CI/CD workflows are configured (if applicable)
3. ✅ Consider adding required status checks
4. ✅ Review and update CODEOWNERS file if needed
