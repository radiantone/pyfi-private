
flow add node -n node0 -h phoenix
flow add node -n node1 -h agent1
flow add node -n node2 -h agent2

flow add queue -n pyfi.queue1 -t direct
flow add queue -n pyfi.queue2 -t direct

flow add processor -n proc1 -g https://github.com/radiantone/pyfi-processors#egg=ext-processor -m ext.processors.sample -h phoenix
flow add processor -n proc2 -g https://github.com/radiantone/pyfi-processors#egg=ext-processor -m ext.processors.sample -h agent1
flow add processor -n proc3 -g https://github.com/radiantone/pyfi-processors#egg=ext-processor -m ext.processors.sample -h agent2

flow add socket -n proc1.do_something -q pyfi.queue1 -pn proc1 -t do_something
flow add socket -n proc2.do_this -q pyfi.queue2 -pn proc2 -t do_this
flow add socket -n proc3.do_that -q pyfi.queue2 -pn proc3 -t do_that

flow add plug -n plug4 --source proc1.do_something --target proc2.do_this
flow add plug -n plug5 --source proc2.do_this --target proc3.do_that
#flow task run --socket proc1.do_something --data "['some data']"
