# GitHub Workflows

## Auto Update Submodules

### Overview

This repository contains two workflows for automatically updating submodules:

1. **`update-submodules.yml`** - Basic automatic submodule updater
2. **`auto-update-submodules.yml`** - Smart submodule updater with upstream detection and testing

### Smart Auto Update Workflow (`auto-update-submodules.yml`)

#### Features

- **Upstream Detection**: Automatically detects if upstream repositories have updates
- **Safe Testing**: Tests submodule updates before committing changes
- **Selective Updates**: Only updates when changes are available and safe to apply
- **Comprehensive Logging**: Provides detailed logs of what was updated and why

#### Workflow Steps

1. **Checkout**: Clones the repository with all submodules
2. **Upstream Check**: Fetches latest updates and compares current vs remote commits
3. **Update Testing**: Creates a temporary branch to test submodule updates
4. **Safe Update**: Only applies updates if testing passes
5. **Commit & Push**: Commits changes with detailed commit messages
6. **Pull Request**: Creates a PR for review (optional)

#### Trigger Conditions

- **Scheduled**: Runs daily at 2 AM UTC
- **Manual**: Can be triggered manually from GitHub Actions tab

#### Safety Features

- **Pre-flight Testing**: Tests updates in a temporary branch before applying
- **Rollback Capability**: If testing fails, no changes are committed
- **Detailed Logging**: Clear logs showing what was updated and why
- **Status Reporting**: Final status report showing success/failure

### Basic Update Workflow (`update-submodules.yml`)

#### Features

- Simple and straightforward submodule updates
- Automatic commit and push
- Pull request creation (optional)

#### Use Cases

- When you want simple, direct updates
- When testing is not required
- When you trust all upstream repositories

### 功能说明

`update-submodules.yml` 是一个自动化的 GitHub Workflow，用于定期检查和更新项目中的所有 submodule。

### Configuration Requirements

Ensure your repository has the following settings:

1. **Repository Permissions**: GitHub Actions must have push permissions
2. **Branch Protection**: If enabled, configure to allow GitHub Actions to push
3. **Submodule Configuration**: Ensure `.gitmodules` file is correctly configured

### Customization Options

#### Schedule Configuration

```yaml
# Daily at 2 AM UTC
- cron: '0 2 * * *'

# Weekly on Monday at 2 AM UTC
- cron: '0 2 * * 1'

# Every 6 hours
- cron: '0 */6 * * *'

# Every hour
- cron: '0 * * * *'
```

#### Commit Message Customization

You can modify the commit message format in the workflow files:

```yaml
COMMIT_MSG="🤖 Auto-update submodules

Updated submodules: $UPDATED_SUBMODULES

This update was automatically triggered by GitHub Actions
Timestamp: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
```

### Monitoring and Debugging

#### Workflow Monitoring

- **GitHub Actions Tab**: View workflow runs and logs
- **Repository Commits**: Check automatic commits
- **Pull Requests**: Review auto-created PRs

#### Common Issues

1. **Permission Errors**: Ensure GitHub Actions has write permissions
2. **Network Issues**: Check if submodule repositories are accessible
3. **Branch Protection**: Verify branch protection rules allow GitHub Actions
4. **Submodule URLs**: Validate URLs in `.gitmodules` file

#### Debugging Steps

1. Check workflow logs in GitHub Actions tab
2. Verify submodule URLs are correct and accessible
3. Test submodule updates manually
4. Check repository permissions and branch protection settings

### Best Practices

1. **Use Smart Workflow**: Prefer `auto-update-submodules.yml` for production
2. **Monitor Regularly**: Check workflow runs and logs periodically
3. **Review PRs**: Always review auto-created pull requests
4. **Test Manually**: Periodically test submodule updates manually
5. **Backup Strategy**: Keep backups of important submodule states

### Example Output

#### Successful Update
```
✅ Submodules updated successfully
Updated modules: rcd, run, causalrca
```

#### No Updates Available
```
ℹ️ No submodule updates available
```

#### Failed Test
```
❌ Submodule updates failed tests - no changes committed
``` 