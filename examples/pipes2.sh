# To run:
# $ . examples/pipes2.sh
#

alias pyfi.processors.sample.do_something="flow task run -s proc1.socket1"
alias pyfi.processors.sample.do_this="flow task run -s proc1a.socket1"

# Distributed function pipeline
(pyfi.processors.sample.do_something -d "$(pyfi.processors.sample.do_this -d "$(pyfi.processors.sample.do_something -d '"HI!"')")")

