awk '
/^[[:space:]]*\[/ { if ($0 ~ /\[[[:space:]]*(Test|Fact|Theory|RetryTest|CiTest|TestCase|TestCaseSource|InlineData|MemberData|TestDescription|Ignore|Explicit)[][(,]/) pend=1; next }
/^[[:space:]]*(public|private|protected|internal)[^;]*\(/ { if (pend) { n++; pend=0 } next }
/^[[:space:]]*$/ { next }
/^[[:space:]]*(\/\/|\*|\/\*)/ { next }
{ pend=0 }
END { print n+0 }
' "$1"
