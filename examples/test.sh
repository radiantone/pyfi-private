flow add processor -n proc1 -g https://github.com/radiantone/pyfi-processors -m ext.processors.sample
flow add queue -n pyfi.queue1 -t direct
flow add socket -n proc1.socket1 -q pyfi.queue1 -pn proc1 -t do_something
flow add processor -n agent1proc1 -g https://github.com/radiantone/pyfi-processors -m ext.processors.sample -h agent1
flow add socket -n proc1a.socket1 -q pyfi.queue1 -pn agent1proc1 -t do_something
