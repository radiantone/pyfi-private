# To run:
# $ . examples/pipes.sh
#

# Create alias' for the run task commands
alias ext.processors.sample.do_something="flow task run -s proc1.do_something"
alias ext.processors.sample.do_this="flow task run -s proc2.do_this"

echo "HI THERE!" | ext.processors.sample.do_something

echo "HI THERE!" | ext.processors.sample.do_something | echo "$(cat -)string" | ext.processors.sample.do_this

echo "Parallel test"
# Echo a string as input to two different processors and they run in parallel
echo "HI THERE!" | tee -a >(ext.processors.sample.do_something) tee -a >(ext.processors.sample.do_this)
