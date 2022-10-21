# To run:
# $ . examples/pipes.sh
#

# Create alias' for the run task commands
alias pyfi.processors.sample.do_something="flow task run -s proc1.do_something"
alias pyfi.processors.sample.do_this="flow task run -s proc2.do_this"

echo "HI THERE!" | pyfi.processors.sample.do_something 

echo "HI THERE!" | pyfi.processors.sample.do_something | echo "$(cat -)string" | pyfi.processors.sample.do_this

echo "Parallel test"
# Echo a string as input to two different processors and they run in parallel
echo "HI THERE!" | tee -a >(pyfi.processors.sample.do_something) tee -a >(pyfi.processors.sample.do_this)
