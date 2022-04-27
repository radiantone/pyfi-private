# Build the network
# Add a scheduler
bin/setup.sh

# Start agents
read -p 'Start agents...' cont

# Add agent nodes to network objectscheduler
bin/agents.sh

# Add agents to scheduler
# Create deployments
bin/deploy.sh

flow ls network -n network-1
