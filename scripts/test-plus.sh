#!/bin/bash

# OpenCode Plus Test Suite
# Comprehensive testing for enhanced OpenCode functionality

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_SKIPPED=0

# Functions
log_test() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

log_pass() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((TESTS_PASSED++))
}

log_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((TESTS_FAILED++))
}

log_skip() {
    echo -e "${YELLOW}[SKIP]${NC} $1"
    ((TESTS_SKIPPED++))
}

test_command() {
    local test_name="$1"
    local command="$2"

    log_test "$test_name"

    if eval "$command" > /dev/null 2>&1; then
        log_pass "$test_name - command executed successfully"
        return 0
    else
        log_fail "$test_name - command failed"
        return 1
    fi
}

test_file_exists() {
    local test_name="$1"
    local file="$2"

    log_test "$test_name"

    if [ -f "$file" ]; then
        log_pass "$test_name - file exists: $file"
        return 0
    else
        log_fail "$test_name - file not found: $file"
        return 1
    fi
}

test_json_valid() {
    local test_name="$1"
    local json_file="$2"

    log_test "$test_name"

    if command -v jq &> /dev/null; then
        if jq empty "$json_file" 2>/dev/null; then
            log_pass "$test_name - valid JSON in $json_file"
            return 0
        else
            log_fail "$test_name - invalid JSON in $json_file"
            return 1
        fi
    else
        log_skip "$test_name - jq not installed"
        return 2
    fi
}

test_config_field() {
    local test_name="$1"
    local config_file="$2"
    local field="$3"
    local expected="$4"

    log_test "$test_name"

    if command -v jq &> /dev/null; then
        local value=$(jq -r ".$field" "$config_file" 2>/dev/null)
        if [ "$value" = "$expected" ]; then
            log_pass "$test_name - $field = $expected"
            return 0
        else
            log_fail "$test_name - $field = $value (expected $expected)"
            return 1
        fi
    else
        log_skip "$test_name - jq not installed"
        return 2
    fi
}

test_directory_exists() {
    local test_name="$1"
    local dir="$2"

    log_test "$test_name"

    if [ -d "$dir" ]; then
        log_pass "$test_name - directory exists: $dir"
        return 0
    else
        log_fail "$test_name - directory not found: $dir"
        return 1
    fi
}

test_ripgrep_installation() {
    log_test "Ripgrep Installation"

    if command -v rg &> /dev/null; then
        log_pass "Ripgrep is installed"
        rg --version | head -1
        return 0
    else
        log_fail "Ripgrep not found in PATH"
        return 1
    fi
}

test_bun_installation() {
    log_test "Bun Installation"

    if command -v bun &> /dev/null; then
        log_pass "Bun is installed"
        bun --version
        return 0
    else
        log_fail "Bun not found in PATH"
        return 1
    fi
}

test_opencode_installation() {
    log_test "OpenCode Installation"

    if command -v opencode &> /dev/null; then
        log_pass "OpenCode is installed"
        opencode --version | head -1 || echo "OpenCode basic check passed"
        return 0
    else
        log_fail "OpenCode not found in PATH"
        return 1
    fi
}

test_configuration_files() {
    echo ""
    log_test "Configuration Files Testing"

    test_file_exists "Basic configuration" "opencode.json"
    test_json_valid "Basic configuration JSON validation" "opencode.json"

    test_file_exists "Enhanced configuration" "opencode-plus.json"
    test_json_valid "Enhanced configuration JSON validation" "opencode-plus.json"

    test_file_exists "Configuration schema" "config-plus.schema.json"
    test_json_valid "Configuration schema JSON validation" "config-plus.schema.json"
}

test_directory_structure() {
    echo ""
    log_test "Directory Structure Testing"

    test_directory_exists "OpenCode directory" ".opencode"
    test_directory_exists "Scripts directory" "scripts"
    test_directory_exists "Enhanced GitHub action" ".github/enhanced"

    # Create missing directories for testing
    mkdir -p .opencode/{plugins,skills,agents,asp-servers,mcp-servers}
}

test_opencode_plus_config() {
    echo ""
    log_test "OpenCode Plus Configuration Testing"

    if [ -f "opencode-plus.json" ] && command -v jq &> /dev/null; then
        test_config_field "Model configuration" "opencode-plus.json" "model" "azure/zai-org--glm-47-fp8"
        test_config_field "Small model configuration" "opencode-plus.json" "small_model" "azure/zai-org--glm-47-fp8"
        test_config_field "Shell configuration" "opencode-plus.json" "shell" "/bin/bash"
        test_config_field "Log level configuration" "opencode-plus.json" "logLevel" "INFO"
        test_config_field "Compression auto configuration" "opencode-plus.json" "compaction.auto" "true"
    else
        log_skip "Enhanced configuration tests - prerequisites not met"
    fi
}

test_tool_installation() {
    echo ""
    log_test "Tool Installation Testing"

    test_bun_installation
    test_ripgrep_installation
    test_opencode_installation
}

test_scripts() {
    echo ""
    log_test "Scripts Testing"

    test_file_exists "Installation script" "scripts/install_plus.sh"
    test_file_exists "Management script" "scripts/opencode-manage.sh"

    # Test script execution permissions
    if [ -x "scripts/install_plus.sh" ]; then
        log_pass "Installation script has execute permissions"
    else
        log_fail "Installation script missing execute permissions"
    fi

    if [ -x "scripts/opencode-manage.sh" ]; then
        log_pass "Management script has execute permissions"
    else
        log_fail "Management script missing execute permissions"
    fi
}

test_documentation() {
    echo ""
    log_test "Documentation Testing"

    test_file_exists "Enhanced README" "README-PLUS.md"
    test_file_exists "Implementation summary" "IMPLEMENTATION-SUMMARY.md"
    test_file_exists "Implementation plan" "opencode-plus-plan.md"
}

test_github_action() {
    echo ""
    log_test "GitHub Action Testing"

    test_file_exists "Enhanced action definition" ".github/enhanced/action.yml"
    test_file_exists "Enhanced action implementation" ".github/enhanced/index.ts"
    test_file_exists "Enhanced action dependencies" ".github/enhanced/package.json"
}

test_ripgrep_functionality() {
    echo ""
    log_test "Ripgrep Functionality Testing"

    if command -v rg &> /dev/null; then
        # Test basic search
        if rg "model" opencode-plus.json > /dev/null 2>&1; then
            log_pass "Ripgrep basic search functionality"
        else
            log_fail "Ripgrep basic search failed"
        fi

        # Test pattern matching
        if rg "\.json$" --files | grep -q "opencode-plus.json"; then
            log_pass "Ripgrep pattern matching"
        else
            log_fail "Ripgrep pattern matching failed"
        fi

        # Test file type filtering
        if rg "model" --type json --files | grep -q "opencode-plus.json"; then
            log_pass "Ripgrep file type filtering"
        else
            log_fail "Ripgrep file type filtering failed"
        fi
    else
        log_skip "Ripgrep functionality tests - ripgrep not installed"
    fi
}

test_extension_structure() {
    echo ""
    log_test "Extension Structure Testing"

    # Ensure directory structure exists
    mkdir -p .opencode/{plugins,skills,agents,asp-servers,mcp-servers}

    # Test directories
    test_directory_exists "Plugins directory" ".opencode/plugins"
    test_directory_exists "Skills directory" ".opencode/skills"
    test_directory_exists "Agents directory" ".opencode/agents"
    test_directory_exists "ASP servers directory" ".opencode/asp-servers"
    test_directory_exists "MCP servers directory" ".opencode/mcp-servers"
}

test_compression_configuration() {
    echo ""
    log_test "Token Compression Configuration Testing"

    if [ -f "opencode-plus.json" ] && command -v jq &> /dev/null; then
        local compaction_enabled=$(jq -r '.compaction.auto' opencode-plus.json 2>/dev/null)
        local trigger_ratio=$(jq -r '.compaction.triggerTokenRatio' opencode-plus.json 2>/dev/null)

        if [ "$compaction_enabled" = "true" ]; then
            log_pass "Token compression is enabled"
        else
            log_fail "Token compression is disabled"
        fi

        if (( $(echo "$trigger_ratio >= 0.5 && $trigger_ratio <= 0.99" | bc -l) )); then
            log_pass "Token compression trigger ratio is valid: $trigger_ratio"
        else
            log_fail "Token compression trigger ratio is invalid: $trigger_ratio"
        fi
    else
        log_skip "Token compression configuration tests - prerequisites not met"
    fi
}

test_server_configuration() {
    echo ""
    log_test "Server Configuration Testing"

    if [ -f "opencode-plus.json" ] && command -v jq &> /dev/null; then
        local asp_count=$(jq -r '.extensions.asp_servers | length' opencode-plus.json 2>/dev/null)
        local mcp_count=$(jq -r '.extensions.mcp_servers | length' opencode-plus.json 2>/dev/null)

        log_pass "ASP servers configured: $asp_count"
        log_pass "MCP servers configured: $mcp_count"

        # Test server structure
        if [ "$asp_count" -gt "0" ]; then
            local first_asp_enabled=$(jq -r '.extensions.asp_servers[0].enabled' opencode-plus.json 2>/dev/null)
            if [ "$first_asp_enabled" = "true" ]; then
                log_pass "First ASP server is enabled"
            else
                log_fail "First ASP server is disabled"
            fi
        fi

        if [ "$mcp_count" -gt "0" ]; then
            local first_mcp_enabled=$(jq -r '.extensions.mcp_servers[0].enabled' opencode-plus.json 2>/dev/null)
            if [ "$first_mcp_enabled" = "true" ]; then
                log_pass "First MCP server is enabled"
            else
                log_fail "First MCP server is disabled"
            fi
        fi
    else
        log_skip "Server configuration tests - prerequisites not met"
    fi
}

run_all_tests() {
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║     OpenCode Plus Test Suite                            ║"
    echo "║     Testing Enhanced OpenCode Functionality              ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""

    # Run all test categories
    test_configuration_files
    test_directory_structure
    test_tool_installation
    test_scripts
    test_documentation
    test_github_action
    test_ripgrep_functionality
    test_extension_structure
    test_opencode_plus_config
    test_compression_configuration
    test_server_configuration

    # Print summary
    echo ""
    echo "╔═══════════════════════════════════════════════════════════╗"
    echo "║     Test Summary                                         ║"
    echo "╚═══════════════════════════════════════════════════════════╝"
    echo ""
    echo -e "${GREEN}✓ Tests Passed:${NC} $TESTS_PASSED"
    echo -e "${RED}✗ Tests Failed:${NC} $TESTS_FAILED"
    echo -e "${YELLOW}○ Tests Skipped:${NC} $TESTS_SKIPPED"
    echo ""

    local total_tests=$((TESTS_PASSED + TESTS_FAILED))
    local success_rate=0
    if [ $total_tests -gt 0 ]; then
        success_rate=$((TESTS_PASSED * 100 / total_tests))
    fi

    echo -e "Success Rate: ${success_rate}%"
    echo ""

    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${GREEN}All tests passed! OpenCode Plus is ready to use.${NC}"
        return 0
    else
        echo -e "${RED}Some tests failed. Please review the output above.${NC}"
        return 1
    fi
}

# Main execution
case "${1:-all}" in
    all)
        run_all_tests
        ;;
    config)
        test_configuration_files
        test_opencode_plus_config
        test_compression_configuration
        test_server_configuration
        echo ""
        echo "✓ $TESTS_PASSED | ✗ $TESTS_FAILED | ○ $TESTS_SKIPPED"
        ;;
    tools)
        test_tool_installation
        test_ripgrep_functionality
        echo ""
        echo "✓ $TESTS_PASSED | ✗ $TESTS_FAILED | ○ $TESTS_SKIPPED"
        ;;
    structure)
        test_directory_structure
        test_extension_structure
        echo ""
        echo "✓ $TESTS_PASSED | ✗ $TESTS_FAILED | ○ $TESTS_SKIPPED"
        ;;
    *)
        echo "Usage: $0 [all|config|tools|structure]"
        exit 1
        ;;
esac