# Add agent nodes to scheduler
flow scheduler -n sched1 add -nd agent3.agent.node
flow scheduler -n sched1 add -nd agent2.agent.node

# Create deployments manually. This is optional because
# once nodes are added to a scheduler and the scheduler is running
# It will try to satisfy the processor CPU requirements by creating
# deployments across its nodes

flow add deployment -n proc1 -d deploy1.proc1 -h agent3 -c 5
#flow add deployment -n proc1 -d deploy2.proc1 -h agent2 -c 1
flow add deployment -n proc2 -d deploy1.proc2 -h agent2 -c 1
flow add deployment -n proc3 -d deploy1.proc3 -h agent3 -c 1
