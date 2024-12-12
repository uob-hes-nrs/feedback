#!/bin/bash
function all_tests {
    return 0
}

function run_test {
    echo "TEST START: $1"
    if python3 "$1.py"; then
        echo "TEST PASS: $1"
    else
        fail=true
        echo "TEST FAIL: $1"
    fi
}

cd "$(dirname "${BASH_SOURCE[0]}")"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt --upgrade > /dev/null

exec 3< <(python3 app.py 2>&1)
app=$!
running=false
while read line; do
    echo "$line"
    case "$line" in
    *"Press CTRL+C to quit"*)
        running=true
        break
        ;;
    esac
done <&3
if ! $running; then
    echo "REJECT: app could not start :("
    exit 1
fi
fail=false
all_tests
kill $app
if $fail; then
    echo "REJECT: some tests failed :("
    exit 1
fi
echo "ACCEPT: all tests passed :)"
exit 0
