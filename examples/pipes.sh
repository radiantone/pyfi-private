# Create alias' for the run task commands
alias pyfi.processors.sample.do_something="pyfi task run -s pyfi.processors.sample.do_something"
alias pyfi.processors.sample.do_this="pyfi task run -s pyfi.processors.sample.do_this"

echo "HI THERE!" | pyfi.processors.sample.do_something 

echo "HI THERE!" | pyfi.processors.sample.do_something | echo "$(cat -)string" | pyfi.processors.sample.do_this

# Echo a string as input to two different processors and they run in parallel
echo "HI THERE!" | tee -a >(pyfi.processors.sample.do_something) tee -a >(pyfi.processors.sample.do_this)