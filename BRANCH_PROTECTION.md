# Branch Protection Setup

This document provides instructions for setting up branch protection rules for the main branch to prevent force pushes, deletions, and enforce quality checks before merging.

## Why Branch Protection?

Branch protection rules help ensure:
- Code quality through required reviews and status checks
- Protection against accidental deletions or force pushes
- Consistent development workflow
- Better collaboration and code review process

## Required Protection Rules for Main Branch

### 1. Protect Against Force Push and Deletion

**Via GitHub Web UI:**
1. Go to your repository on GitHub
2. Click on **Settings** > **Branches**
3. Under "Branch protection rules", click **Add rule**
4. In "Branch name pattern", enter: `main`
5. Enable the following settings:
   - ☑️ **Require a pull request before merging**
     - ☑️ Require approvals (minimum 1)
   - ☑️ **Require status checks to pass before merging**
     - ☑️ Require branches to be up to date before merging
   - ☑️ **Do not allow bypassing the above settings**
   - ☑️ **Restrict who can push to matching branches** (optional, for stricter control)
   - ☑️ **Allow force pushes** - Keep this **UNCHECKED**
   - ☑️ **Allow deletions** - Keep this **UNCHECKED**
6. Click **Create** or **Save changes**

### 2. Using GitHub CLI (gh)

If you have the GitHub CLI installed and authenticated:

```bash
# Basic protection - prevent force push and deletion
gh api repos/:owner/:repo/branches/main/protection \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  --input - <<EOF
{
  "required_status_checks": null,
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
```

### 3. Using GitHub API

If you prefer using the REST API directly:

```bash
curl -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.github.com/repos/djkingy79-yo/Criminal-Appeal/branches/main/protection \
  -d '{
    "required_status_checks": null,
    "enforce_admins": true,
    "required_pull_request_reviews": {
      "required_approving_review_count": 1
    },
    "restrictions": null,
    "allow_force_pushes": false,
    "allow_deletions": false
  }'
```

## Recommended Additional Settings

### Status Checks

If you have CI/CD workflows (GitHub Actions, etc.), you should require them to pass:

1. In branch protection settings, enable **Require status checks to pass before merging**
2. Select the specific checks that must pass (e.g., "build", "test", "lint")

### Code Review Requirements

- **Require approvals**: Set to at least 1
- **Dismiss stale pull request approvals when new commits are pushed**: Recommended
- **Require review from Code Owners**: If you have a CODEOWNERS file

### Additional Restrictions

- **Restrict who can push to matching branches**: Limit direct pushes to specific teams
- **Require signed commits**: For enhanced security
- **Require linear history**: Prevent merge commits

## Verification

To verify branch protection is active:

```bash
# Using GitHub CLI
gh api repos/djkingy79-yo/Criminal-Appeal/branches/main/protection

# Check in UI
# Go to Settings > Branches and verify the rule shows the lock icon
```

## Quick Start (Recommended Minimal Setup)

For this repository, at minimum, enable:
1. ✅ Require pull request before merging (1 approval)
2. ✅ Prevent force pushes
3. ✅ Prevent deletions
4. ✅ Require branches to be up to date before merging

## Support

If you encounter issues setting up branch protection:
- Check that you have admin permissions on the repository
- Ensure you're on a GitHub plan that supports branch protection (available on all plans)
- Review GitHub's [branch protection documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
