# To run:
# $ . examples/pipes2.sh
#

alias pyfi.processors.sample.do_something="pyfi task run -s pyfi.processors.sample.do_something"
alias pyfi.processors.sample.do_this="pyfi task run -s pyfi.processors.sample.do_this"

# Distributed function pipeline
(pyfi.processors.sample.do_something -d "$(pyfi.processors.sample.do_this -d $(pyfi.processors.sample.do_something -d "HI!"))")

