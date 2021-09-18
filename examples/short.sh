
pyfi add node -n node0 -h phoenix
pyfi add node -n node1 -h agent1
pyfi add node -n node2 -h agent2

pyfi add queue -n pyfi.queue1 -t direct
pyfi add queue -n pyfi.queue2 -t direct

pyfi add processor -n proc1 -g https://radiantone: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@github.com/radiantone/pyfi-processors#egg=pyfi-processor -m pyfi.processors.sample -h phoenix
pyfi add processor -n proc2 -g https://radiantone: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@github.com/radiantone/pyfi-processors#egg=pyfi-processor -m pyfi.processors.sample -h agent1
pyfi add processor -n proc3 -g https://radiantone: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@github.com/radiantone/pyfi-processors#egg=pyfi-processor -m pyfi.processors.sample -h agent2

pyfi add socket -n proc1.do_something -q pyfi.queue1 -pn proc1 -t do_something
pyfi add socket -n proc2.do_this -q pyfi.queue2 -pn proc2 -t do_this
pyfi add socket -n proc3.do_that -q pyfi.queue2 -pn proc3 -t do_that

pyfi add plug -n plug4 --source proc1.do_something --target proc2.do_this
pyfi add plug -n plug5 --source proc2.do_this --target proc3.do_that
#pyfi task run --socket proc1.do_something --data "['some data']"
