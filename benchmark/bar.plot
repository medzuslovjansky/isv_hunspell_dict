set term png
set output "out/bench.png"
set title "Spellchecking speed (chars/sec)\n(more means better)"
NormalText = "#99ffff"; WithSpellingErrors = "#4671d5"
set auto x
set auto y
set style data histogram
set style histogram cluster gap 1
set style fill solid border -1
set boxwidth 0.9
set xtic scale 0

plot 'out/bench.dat' using 2:xtic(1) ti col fc rgb NormalText, '' u 3 ti col fc rgb WithSpellingErrors
