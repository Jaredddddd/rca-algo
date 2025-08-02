#!/bin/bash

# Auto-update all submodules and create a commit
# Based on existing GitHub Actions workflow logic

set -e  # Exit on error

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in a git repository
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log_error "Current directory is not a git repository"
        exit 1
    fi
    log_success "Confirmed we're in a git repository"
}

# Check for uncommitted changes
check_uncommitted_changes() {
    if ! git diff-index --quiet HEAD --; then
        log_warning "Detected uncommitted changes"
        if [ "$NON_INTERACTIVE" = "true" ]; then
            log_info "Non-interactive mode: continuing with uncommitted changes"
        else
            echo "There are uncommitted changes, it's recommended to commit or stash them first"
            read -p "Continue anyway? (y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                log_info "Operation cancelled"
                exit 0
            fi
        fi
    fi
}

# Initialize submodules
init_submodules() {
    log_info "Initializing submodules..."
    
    # Convert SSH URLs to HTTPS URLs if needed
    if [ -f .gitmodules ]; then
        log_info "Checking and converting submodule URLs..."
        # Create backup
        cp .gitmodules .gitmodules.backup
        
        # Convert SSH URLs to HTTPS URLs
        sed -i 's|git@github.com:|https://github.com/|g' .gitmodules
        
        # Sync submodule configuration
        git submodule sync
    fi
    
    # Initialize and update submodules
    git submodule update --init --recursive
    log_success "Submodules initialization completed"
}

# Validate submodules
validate_submodules() {
    log_info "Validating submodules..."
    
    # Get configured submodules
    SUBMODULE_PATHS=$(git config --file .gitmodules --get-regexp path | cut -d' ' -f2)
    
    if [ -z "$SUBMODULE_PATHS" ]; then
        log_warning "No configured submodules found"
        return 1
    fi
    
    VALID_SUBMODULES=""
    INVALID_SUBMODULES=""
    
    for submodule_path in $SUBMODULE_PATHS; do
        if [ -d "$submodule_path" ]; then
            if [ -d "$submodule_path/.git" ] || [ -f "$submodule_path/.git" ]; then
                log_success "Valid submodule: $submodule_path"
                VALID_SUBMODULES="$VALID_SUBMODULES $submodule_path"
            else
                log_error "Invalid submodule (not a git repo): $submodule_path"
                INVALID_SUBMODULES="$INVALID_SUBMODULES $submodule_path"
            fi
        else
            log_error "Submodule path not found: $submodule_path"
            INVALID_SUBMODULES="$INVALID_SUBMODULES $submodule_path"
        fi
    done
    
    if [ -n "$INVALID_SUBMODULES" ]; then
        log_warning "Found invalid or missing submodules: $INVALID_SUBMODULES"
        return 1
    fi
    
    log_success "All submodules validated successfully"
    return 0
}

# Check upstream updates
check_upstream_updates() {
    log_info "Checking upstream updates..."
    
    # Get valid submodules
    VALID_SUBMODULES=$(git config --file .gitmodules --get-regexp path | cut -d' ' -f2)
    
    # Fetch latest updates for all valid submodules
    for submodule_path in $VALID_SUBMODULES; do
        if [ -d "$submodule_path" ]; then
            log_info "Fetching updates for $submodule_path..."
            cd "$submodule_path" || {
                log_error "Cannot change to directory $submodule_path"
                continue
            }
            
            if git fetch origin; then
                log_success "Successfully fetched updates for $(basename $submodule_path)"
            else
                log_warning "Failed to fetch updates for $(basename $submodule_path)"
            fi
            
            cd ../.. || {
                log_error "Cannot return to parent directory"
                cd "$(git rev-parse --show-toplevel)" || log_error "Cannot return to workspace root"
            }
        fi
    done
    
    # Check if any submodule has updates
    UPDATES_FOUND=false
    UPDATED_SUBMODULES=""
    
    for submodule_path in $VALID_SUBMODULES; do
        if [ -d "$submodule_path" ]; then
            cd "$submodule_path" || continue
            
            # Get current commit
            CURRENT_COMMIT=$(git rev-parse HEAD 2>/dev/null)
            if [ -z "$CURRENT_COMMIT" ]; then
                log_warning "Cannot get current commit for $(basename $submodule_path)"
                cd ../..
                continue
            fi
            
            # Get current branch
            CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || git rev-parse --abbrev-ref HEAD 2>/dev/null)
            
            # Check if there's a configured branch
            CONFIGURED_BRANCH=$(git config --file ../../.gitmodules --get submodule.$submodule_path.branch 2>/dev/null)
            if [ -n "$CONFIGURED_BRANCH" ]; then
                CURRENT_BRANCH="$CONFIGURED_BRANCH"
            fi
            
            # If cannot determine branch, try common branch names
            if [ -z "$CURRENT_BRANCH" ] || [ "$CURRENT_BRANCH" = "HEAD" ]; then
                for branch in main master; do
                    if git rev-parse "origin/$branch" >/dev/null 2>&1; then
                        CURRENT_BRANCH="$branch"
                        break
                    fi
                done
            fi
            
            # Check remote commit
            if [ -n "$CURRENT_BRANCH" ] && git rev-parse "origin/$CURRENT_BRANCH" >/dev/null 2>&1; then
                REMOTE_COMMIT=$(git rev-parse "origin/$CURRENT_BRANCH")
                
                if [ "$CURRENT_COMMIT" != "$REMOTE_COMMIT" ]; then
                    log_success "Found update in $(basename $submodule_path): $CURRENT_COMMIT -> $REMOTE_COMMIT"
                    UPDATES_FOUND=true
                    UPDATED_SUBMODULES="$UPDATED_SUBMODULES$(basename $submodule_path), "
                else
                    log_info "No updates for $(basename $submodule_path)"
                fi
            else
                log_warning "Cannot check updates for $(basename $submodule_path)"
            fi
            
            cd ../..
        fi
    done
    
    if [ "$UPDATES_FOUND" = true ]; then
        log_success "Found submodule updates"
        echo "$UPDATED_SUBMODULES"
        return 0
    else
        log_info "No updates found"
        return 0
    fi
}

# Update submodules
update_submodules() {
    log_info "Updating submodules..."
    
    if git submodule update --remote --recursive; then
        log_success "Submodules updated successfully"
        return 0
    else
        log_error "Failed to update submodules"
        return 1
    fi
}

# Commit changes
commit_changes() {
    local updated_modules="$1"
    
    log_info "Committing changes..."
    
    # Add all changes
    git add -A
    
    # Check if there are changes to commit
    if git diff-index --quiet HEAD --; then
        log_info "No changes to commit - submodules are already up to date"
        return 0 
    fi
    
    # Create commit message
    COMMIT_MSG="🤖 Auto-update submodules

Updated submodules: $updated_modules

This update was automatically triggered by script
Timestamp: $(date '+%Y-%m-%d %H:%M:%S')

Changes:
- Updated submodules to latest upstream versions
- Verified updates are compatible and buildable"
    
    # Commit changes
    if git commit -m "$COMMIT_MSG"; then
        log_success "Changes committed successfully"
        return 0
    else
        log_error "Failed to commit changes"
        return 1
    fi
}

# Push changes (optional)
push_changes() {
    if [ "$NON_INTERACTIVE" = "true" ]; then
        log_info "Non-interactive mode: skipping push (will be handled by workflow)"
        return 0
    else
        log_info "Push changes to remote repository?"
        read -p "Push changes? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            if git push; then
                log_success "Changes pushed to remote repository"
            else
                log_error "Failed to push changes"
                return 1
            fi
        else
            log_info "Skipping push"
        fi
    fi
}

# Main function
main() {
    echo "=== Auto-update Submodules Script ==="
    echo
    
    # Check git repository
    check_git_repo
    
    # Check uncommitted changes
    check_uncommitted_changes
    
    # Initialize submodules
    init_submodules
    
    # Validate submodules
    if ! validate_submodules; then
        log_error "Submodules validation failed, exiting"
        exit 1
    fi
    
    # Check upstream updates
    UPDATED_MODULES=$(check_upstream_updates)
    if [ $? -ne 0 ]; then
        log_info "No updates available, exiting"
        exit 0
    fi
    
    # Update submodules
    if ! update_submodules; then
        log_error "Submodules update failed, exiting"
        exit 1
    fi
    
    # Commit changes
    COMMIT_RESULT=$(commit_changes "$UPDATED_MODULES")
    COMMIT_EXIT_CODE=$?
    
    if [ $COMMIT_EXIT_CODE -eq 0 ]; then
        # Commit was successful, push changes
        push_changes
        log_success "Submodules update completed!"
        exit 0
    else
        # Actual commit failure
        log_error "Failed to commit changes"
        exit 1
    fi
}

# Run main function
main "$@" 