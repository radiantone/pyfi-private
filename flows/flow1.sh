pyfi add processor -n proc1 -g https://github.com/radiantone/pyfi-processors -m pyfi.processors.sample -t do_something
pyfi add queue -n pyfi.queue1 -t direct
pyfi add queue -n pyfi.queue2 -t direct
pyfi add outlet -n outlet1 -q pyfi.queue1 -pn proc1
pyfi add plug -n plug1 -q pyfi.queue2 -pn proc1
pyfi add processor -n proc2 -g https://github.com/radiantone/pyfi-processors -m pyfi.processors.sample -t do_this -h radiant
pyfi add outlet -n outlet1 -q pyfi.queue2 -pn proc2

pyfi add processor -n proc4 -g https://github.com/radiantone/pyfi-processors -m pyfi.processors.sample -t do_something -h radiant
pyfi add outlet -n outlet1 -q pyfi.queue1 -pn proc4

pyfi add processor -n proc3 -g https://github.com/radiantone/pyfi-processors -m pyfi.processors.sample -t do_this -h miko
pyfi add outlet -n outlet1 -q pyfi.queue2 -pn proc3
