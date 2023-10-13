# To run:
# $ . examples/pipes2.sh
#

alias proc1.do_something="flow task run -s proc1.do_something"
alias proc2.do_this="flow task run -s proc2.do_this"

# Distributed function pipeline
(proc1.do_something -d "$(proc2.do_this -d "$(proc1.do_something -d '"HI!"')")")

