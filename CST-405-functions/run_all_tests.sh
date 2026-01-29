#!/bin/bash
# Test runner for the minimal compiler
# Runs all test files and shows results

echo "╔════════════════════════════════════════════════════════════╗"
echo "║           RUNNING ALL COMPILER TESTS                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo

# Check if compiler exists
if [ ! -f "./minicompiler" ]; then
    echo "Error: minicompiler not found. Run 'make' first."
    exit 1
fi

# Array to track results
passed=0
failed=0

# Function to run a single test
run_test() {
    local test_file=$1
    local base_name="${test_file%.c}"
    local output_file="${base_name}.s"

    echo "┌────────────────────────────────────────────────────────────┐"
    echo "│ Testing: $test_file"
    echo "└────────────────────────────────────────────────────────────┘"

    # Run compiler
    if ./minicompiler "$test_file" "$output_file" > /dev/null 2>&1; then
        echo "  ✓ Compilation successful"

        # Check if TAC files were created
        if [ -f "${base_name}.tac" ] && [ -f "${base_name}.optimized.tac" ]; then
            echo "  ✓ TAC files generated"

            # Count optimizations (constants in optimized TAC)
            opt_count=$(grep -c "\[constant:" "${base_name}.optimized.tac" 2>/dev/null || echo 0)
            echo "  ✓ Optimizations applied: $opt_count constant foldings"
        fi

        # Check if MIPS file was created
        if [ -f "$output_file" ]; then
            echo "  ✓ MIPS assembly generated: $output_file"
        fi

        passed=$((passed + 1))
        echo
    else
        echo "  ✗ Compilation FAILED"
        failed=$((failed + 1))
        echo
    fi
}

# Run all test files
for test in test*.c; do
    if [ -f "$test" ]; then
        run_test "$test"
    fi
done

# Summary
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    TEST SUMMARY                            ║"
echo "╠════════════════════════════════════════════════════════════╣"
printf "║  ✓ Passed: %-4d                                           ║\n" $passed
printf "║  ✗ Failed: %-4d                                           ║\n" $failed
echo "╚════════════════════════════════════════════════════════════╝"

# Exit with appropriate code
if [ $failed -eq 0 ]; then
    echo "All tests passed! 🎉"
    exit 0
else
    echo "Some tests failed."
    exit 1
fi
