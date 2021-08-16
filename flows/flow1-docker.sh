
pyfi add node -n node1 -h agent1
pyfi add node -n node2 -h agent2 
pyfi add node -n node3 -h agent3

pyfi add scheduler --name sched1

pyfi scheduler -n sched1  add --node node1
pyfi scheduler -n sched1  add --node node2
pyfi scheduler -n sched1  add --node node3

pyfi add processor -n proc1 -g https://github.com/radiantone/pyfi-processors -m pyfi.processors.sample -t do_something -h agent1
pyfi add processor -n proc2 -g https://github.com/radiantone/pyfi-processors -m pyfi.processors.sample -t do_this -h agent2
pyfi add processor -n proc3 -g https://github.com/radiantone/pyfi-processors -m pyfi.processors.sample -t do_this -h agent3

# Add tasks to processor

# Outlets associated with tasks

pyfi add queue -n pyfi.queue1 -t direct
pyfi add queue -n pyfi.queue2 -t direct
pyfi add queue -n pyfi.queue3 -t direct

# Inbound sockets
pyfi add socket -n proc1.socket1 -q pyfi.queue1 -pn proc1
pyfi add socket -n proc2.socket1 -q pyfi.queue1 -pn proc2
pyfi add socket -n proc2.socket2 -q pyfi.queue2 -pn proc2
pyfi add socket -n proc3.socket1 -q pyfi.queue3 -pn proc3

# Outbound plugs
pyfi add plug -n plug2 -q pyfi.queue2 -pn proc1
pyfi add plug -n plug3 -q pyfi.queue3 -pn proc1


# When one processor (procA) plug (plugA) with name (queueA) is connected to another processor (procB) socket (socketB), this transaction will happen
#
# pyfi add queue -n pyfi.queueA -t direct
# pyfi add socket -n procB.socketB -q pyfi.queueA -pn procB
# pyfi add plug -n procA.plugA -q pyfi.queueA -pn procA
# 
# Agent will get 'update' status request for procB. Upon restart, it will look at procB sockets and subscribe
# to those queues, in this case, pyfi.queueA and dispatch messages to its module.task
# 
# procA.plugA and procB.socketB must always agree which queue to communicate if they are connected via the GUI.
# This is why it is updated as a transaction
#
# Whenever the connection between procA and procB is renamed, then this transaction occurs 
# 
# pyfi update socket --id 123456 -n procB.socketB.NEWNAME 
# pyfi update plug --id 56789 -n procA.plugA.NEWNAME 
# 
# The connection in the GUI is associated with a pre-existing queue (e.g. pyfi.queueA)
# If the user changes that, then this transaction happens, along with a processor update
#
# pyfi update socket --id 123456 -q pyfi.queueA.NEWQUEUE
# pyfi update plug --id 56789 -q pyfi.queueA.NEWQUEUE 
# 
# The old queue will eventually be auto-deleted
