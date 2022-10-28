flow add processor -n proc1 -g https://github.com/radiantone/pyfi-processors -m ext.processors.sample -h agent2 --cpus 1 #-d
flow add queue -n pyfi.queue1 -t direct
flow add socket -n proc1.socket1 -q pyfi.queue1 -pn proc1 -t do_something
flow add processor -n agent1proc1 -g https://github.com/radiantone/pyfi-processors -m ext.processors.sample -h agent2 --cpus 1 #-d
flow add socket -n proc1a.socket1 -q pyfi.queue1 -pn agent1proc1 -t do_this
flow add plug -q pyfi.queue1 -s proc1.socket1 -t proc1a.socket1 -n plug1
#flow task run -s proc1.socket1 -n do_this -d "\"Hello\""
#flow task run -s proc1a.socket1  -d "\"Hello there\""
#flow task run -s proc1.socket1 -n do_something -d "\"Hello\"" -sy
