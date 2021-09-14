pyfi add queue -n pyfi.queue1 -t direct
pyfi add processor -n proc1 -g https://radiantone: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@github.com/radiantone/pyfi-processors#egg=pyfi-processor -m pyfi.processors.sample -h phoenix
pyfi add socket -n proc1.socket1 -q pyfi.queue1 -pn proc1 -t do_something
pyfi add socket -n proc1.socket2 -q pyfi.queue1 -pn proc1 -t do_this
pyfi task run --socket proc1.socket2 --data "['some data']"
