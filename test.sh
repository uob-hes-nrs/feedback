#!/bin/bash

function all_tests {
    run_test "test_app"
    run_test "test_auth"
}

function run_test {
    echo "TESTING NOW: $1"
    if .venv/bin/python3 "$1.py"; then
        echo "TEST PASS: $1"
        return 0
    else
        fail=true
        echo "TEST FAIL: $1"
        return 1
    fi
}

cd "$(dirname "${BASH_SOURCE[0]}")"
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt --upgrade > /dev/null
exec 3< <(.venv/bin/python3 app.py 2>&1)
app=$!
running=false
while read line; do
    case "$line" in
    *"Press CTRL+C to quit"*)
        running=true
        break
        ;;
    esac
done <&3
if ! $running; then
    echo "TEST FAIL: app could not start :("
    exit 1
fi
fail=false
all_tests
kill $app
if $fail; then
    echo "TEST FAIL: some tests failed :("
    exit 1
fi
echo "TEST PASS: all tests passed :)"
exit 0