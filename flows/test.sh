pyfi add processor -n proc1 -g https://github.com/radiantone/pyfi-processors -m pyfi.processors.sample 
pyfi add queue -n pyfi.queue1 -t direct
pyfi add socket -n proc1.socket1 -q pyfi.queue1 -pn proc1 -t do_something
pyfi add processor -n agent1proc1 -g https://github.com/radiantone/pyfi-processors -m pyfi.processors.sample -h agent1
pyfi add socket -n proc1a.socket1 -q pyfi.queue1 -pn agent1proc1 -t do_something
