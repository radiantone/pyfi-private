# To run:
# $ . examples/pipes2.sh
#

alias ext.processors.sample.do_something="flow task run -s ext.processors.sample.do_something"
alias ext.processors.sample.do_this="flow task run -s ext.processors.sample.do_this"

# Distributed function pipeline
(ext.processors.sample.do_something -d "$(ext.processors.sample.do_this -d "$(ext.processors.sample.do_something -d '"HI!"')")")

