#!/bin/bash

# Script to apply branch protection rules to the main branch
# This script requires GitHub CLI (gh) to be installed and authenticated

set -e

REPO="djkingy79-yo/Criminal-Appeal"
BRANCH="main"

echo "========================================="
echo "Branch Protection Setup Script"
echo "========================================="
echo ""
echo "Repository: $REPO"
echo "Branch: $BRANCH"
echo ""

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo "❌ Error: GitHub CLI (gh) is not installed."
    echo "Please install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Error: Not authenticated with GitHub CLI."
    echo "Please run: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI is installed and authenticated"
echo ""

# Check current branch protection status
echo "Checking current branch protection status..."
if gh api "repos/$REPO/branches/$BRANCH/protection" &> /dev/null; then
    echo "⚠️  Branch protection already exists. This will update it."
else
    echo "ℹ️  No branch protection currently set."
fi
echo ""

# Apply branch protection rules
echo "Applying branch protection rules..."

gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  "repos/$REPO/branches/$BRANCH/protection" \
  --input .github/branch-protection-config.json

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================="
    echo "✅ SUCCESS!"
    echo "========================================="
    echo ""
    echo "Branch protection rules have been applied to the '$BRANCH' branch."
    echo ""
    echo "Protection includes:"
    echo "  ✓ Require pull request reviews (1 approval)"
    echo "  ✓ Dismiss stale reviews on new commits"
    echo "  ✓ Require conversation resolution"
    echo "  ✓ Prevent force pushes"
    echo "  ✓ Prevent deletions"
    echo "  ✓ Enforce for administrators"
    echo ""
    echo "You can verify the settings at:"
    echo "https://github.com/$REPO/settings/branches"
else
    echo ""
    echo "❌ Failed to apply branch protection rules."
    echo "Please check your permissions and try again."
    echo ""
    echo "For manual setup, see BRANCH_PROTECTION.md"
    exit 1
fi
