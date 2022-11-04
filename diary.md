## Nov 4, 2022
- Initial event driven browser-only dataflow 80%
- DataTemplate 90%
- ScriptTemplate 70%
- Emit object data on trigger DONE
- Execute code on receiving data 35%
- Storing argument until all are present
- BUG: Cut and paste or load flow needs to rebuild portobjects list etc
- Visual indicators for trigger data flow
- Remove queue box on edge for local data/script nodes

## Oct 30, 2022

- New Data Processor. Define data as named objects in module
- "Add Socket" becomes "Add Data" using named objects in list
- Socket is created and a pre-defined code template is used for the function, which reads the named object from the module and emits it
- "Settings"->"Schedule" becomes a table with sockets and CRON string for each socket that controls when the socket will fire (task executes)
- Data Processor doesn't need concurrency.
  - "results" for data processor are stored whenever it emits.
  - "output" for data processor reflect any stdout the module might generate
  - Clicking "run" icon for data processor will emit all its sockets
  - "error" socket will remain
  - Only "out" bandwidth is needed
  - no plugs
  - 

## Oct 29, 2022

- Fixed tool palette text wrapping DONE
- Added pre-load screen, updated logo DONE
- new "elastic CODE" SVG logo and branding DONE
- Adjustable python interpreter card with scrolling DONE
- Fixed worker startup, sockets running again DONE
- Updated "update processor" command DONE
- Added "Run Flow" button to run the flow either on backend or in browser DONE
- Added line separators between groups of tool icons DONE

## Oct 21, 2022

- Get linting, formatting and typing in place FIXED
- Need to update sphinx docs DONE

## Aug 18, 2022

- When API starts, create rabbit queues from queue models. 
- Load queue models in Queue component
- When existing processor is dragged and dropped fetch the sockets connected to it and add the ports
  - Adding port methods doesn't do anything
- Queues don't update unless streaming mode is on
- Adding a method port without an argument creates a css glitch
- Monitor tab plots a graph for each processor on the current flow
- Errors tab shows any aggregate error logs from any processor on the current canvas

## Aug 16, 2022

- BUG: When syncing a processor, it overwrites id and won't load after save FIXED

## Aug 15, 2022

- Scheduler needs to spread deployments across agents to not overfill FIXED
- Cannot delete processor that has workers: stop and delete worker first?
- BUG: When deployment is removed, UI list doesn't update? FIXED
- BUG: Drop from processors tab doesn't place under mouse

## Aug 14, 2022

- FIX: Need to resolve pgbouncer/sqlalchemy closing/releasing connections
- 

## Aug 12, 2022

- RabbitMQ cluster now entirely concealed behind nginx TBD
- TODO: Fix rabbitmq2 join cluster DONE
- 

## Aug 10, 2022

- BUG: After syncing, search click on processor doesn't jump to that processor
- Processors read-only mode?
- Refresh processor clears error messages
- Add "receipt" field to base models. This is used by UI to track whether to update with incoming changes or not.
  - When the UI saves a processor, it updates the receipt in the payload. If the streaming data for that processor does
  - not have the same receipt id, then it is "old" and do not update it until the receipt ids match.
    - When an object is waiting on its receipt, save is disabled and message indicator says "Syncing...." in blue
  - When a refresh occurs the receipt id is pulled from the database along with entire object.

EPICS

- Seamless data state management, streaming etc. Has to be obvious to the user what's happening with the flow state
  - Is it saved? Is it updated? Is it dirty? Is it pending?
- Statistics viewing
- Monitoring Charts
- Task Management
- Queue Management
- Starting/Stopping Processors & Flows
- Render current state of a network
- 

## Aug 9, 2022

LEFT TO DO

- ~~Servers~~, Monitor, Errors tab
- Exception handling in processors, errors tab in console?
- Upper right menu options
- Environment UI gets injected into processors
  - Processor loads flow state JSON and inspects the "environment" field
- Ingress/Egress activity dots on script templates
- Create/Manage queues *PENDING*
- Processor decorator classes
- Drag n drop from library and other panels
- Edit file names in various panels
- Selection panel buttons
- Add config and environment to flow state
- Statistics table dialog
- Processor Tool types (using decorator classes and modified scriptemplate UI)
- Save processor updates models and triggers reactive behavior from scheduler DONE
- Publish flow. Creates all the objects in the flow and submits transactionally.
- Stream database updates back to browser DONE
- Execution state in UI
- Get queues (from db) API endpoint
- Empty Queue button on items in Queue list, with confirmation
- Network panel quick view card
- More status bar messages. Status bar messages go to Messages panel
- More message panel messages
- System usage toolbar graph
- Queue drop down chart showing messages over time *50%*
- When Queue model changes in database, update rabbitmq queue
- Make sure queues in database reflect what message broker sees
- Queue message rates in queues table *75%*
- Message queue dialog & service. Return all messages current page messages, server side paging.
- Restart Flow 
     - Find workers for all processors in a flow and kill them
- Restart Network
     - Find workers for all node agents and set requested_status = 'kill'
- Restart Processor
     - Find all workers for processor deployments and set status to kill
~~- Task throttling. @celery task lifecycle callbacks can be throttling by sleeping~~
- View tasks in queue, then be able to view data or delete task entirely.
- View errored tasks in queue dialog. Be able to delete or retry them.
- Script Template object attributes update in real time based on streaming data feed.
- Add Pinia to Vue 2. All inbound objects are stored in Pinia and UI reacts to that?



## Aug 8, 2022

- Agent and worker lifecycle reliability improved
- Scheduled dispatcher jobs now obtain their own session and objects
- Individual processor scaling tests work
- Agent only restarts the worker for the changed processor
- Database change events showing up in browser, but seems to have redundant duplicates FIXED

## Aug 7, 2022

- Re-writes of agent.py and worker.py to remove stale object references
- Scheduler should read lock tables when making changes
- There is a deadlock between scheduler and agent after 2 scaling events FIXED
- BUG: Agent kills proc3 and proc1 workers when it should only scale one FIXED

## Aug 6, 2022

-  OSError: [Errno 8] Exec format error: 'venv/bin/flow', after worker restarts from scaling
- 
## Aug 5, 2022

- Scheduler elastic scaling, out and in.
- Agent/Worker tweaks, fixed nested session issue
- *BUG* Still experiencing isolation deadlock at some point
- Agents scale workers up and down based on scheduler updates
- Can now create a socket using the module and name of a task. In this case, any eligible socket is chosen
- Need more testing for multiple deployments per agent
- Shortfall for a processor
  - CPUs are added to wrong deployment. needs to go on deployments that match the processor?
  
## Aug 4 2002

- *FIXED* Scheduler logic to compute available cpus on agent, does not take into account deployments it just created.

## Sun Jul 31 2022

- Dialogs for stat buttons DONE
- Endpoints for stat buttons DONE
- UI tweaks
- Add 3rd processor to example17.py setup with its own queue into proc2. Give its own schedule
- Agent loop needs to populate server resource stats to database
- Ensure delete cascade works. e.g. delete network then deletes everything connected to it
    - Same with agent, node, etc
- Save processor config, updates database. Stores UI state as field *95%*
- Refresh processor pulls state from database for processor and merges it on top of the UI state passed in.
- Queue details table *DONE*
- Message log adds date/time stamp *DONE*
- Processor save *DONE*

## Sat Jul 30 2022

- Fixed message queue return [] bug
- Queued messages that are not "Ready" don't show up in UI. They go into "Unacked" state.
    - UI needs to separate "Ready","Unacked"
- Add queue bandwidth stats to Queue table and edges

## Fri Jul 29 2022

- BUG: Nested function calls are hanging for some reason.  *FIXED*
    - Something to do with mixing pipeline and parallel
    - When a parallel is nested in a pipeline

## Thu Jul 28 2022

- Implemented plug specific queues for all flow calls. The task socket queue is still available *DONE*

## Wed Jul 27 2022

- If worker task queue is socket.queue.name only then user can create queues and then
select the queue name on the socket port in the ScriptTemplate and that name will be
consistent with the KQueue queue name associated with the task routing key.

- If the queue name on the socket port changes and is republished, then the new Queue model
is associated with the Socket model in the database and workers are restarted, which will
rebuild the task based on the new KQueue (name) and routing key for the task.
    - Clients invoking the task shouldn't know the difference? Or the queue is pulled from
    the socket during invocation and the proper KQueue is created behind the scenes (within Socket class)


- Currently, rate limiting is handled at the processor level, which translates to a single celery worker
that can host multiple tasks within it. Each celery task within a given worker is thus ratelimited according
to its parent Processor value. This granularity might change in the future whereby rate limiting is per task.


## Tue Jul 26 2022

LEFT TO DO

- Servers, Monitor, Errors tab
- Exception handling in processors, errors tab in console?
- Upper right menu options
- Create/Manage queues *PENDING*
- Processor decorator classes
- Drag n drop from library and other panels
- Edit file names in various panels
- Selection panel buttons
- Dialog tables for stats in header
- Statistics table dialog
- Processor Tool types (using decorator classes and modified scriptemplate UI)
- Save processor updates models
- Publish flow
- Execution state in UI
- Get queues (from db) API endpoint
- Empty Queue button on items in Queue list, with confirmation
- Network panel quick view card
- More status bar messages. Status bar messages go to Messages panel
- More message panel messages
- System usage toolbar graph
- Queue drop down chart showing messages over time *50%*
- When Queue model changes in database, update rabbitmq queue
- Make sure queues in database reflect what message broker sees
- Queue message rates in queues table *75%*
- Message queue dialog & service. Return all messages up to 20000, server side paging.
- Restart Flow 
     - Find workers for all processors in a flow and kill them
- Restart Network
     - Find workers for all node agents and set requested_status = 'kill'
- Restart Processor
     - Find all workers for processor deployments and set status to kill


## Mon Jul 25 2022

- TODO: Graceful recover from database reboot

- Added Environment table for script processor *DONE*
- Moved version text to left side of processor *DONE*
- Added Save button on processor face *DONE*
- Fixed Variables table editing for flow *DONE*
- BUG: Workers table should update when shown. 
- TODO: History table for processors. uses undostack *DONE*
- TODO: Notes view, use ace editor with text format *DONE*
- TODO: Git view: top panel shows git log and tags, bottom panel shows code
- TODO: Lock uses API to check password against database and returns OK to unlock UI
- TODO: Git panel

## Sun Jul 24 2022

- Download button on console.
- Resize console
- API server restarts on cycle to load new task routes
    - In a cluster, these restarts will be staggered
    - Maybe gunicorn can restart workers without terminating process?
- Library view.
    - New directory
    - Add processor to library
- Processor title tab with edit
- TODO: Processor icon field in settings
- consolelogs capped at 100 entries
- 


## Sat Jul 23 2022

- Add history to flow "history"
- Add config to flow "configuration"
- Add variables to flow "variables"

- Create Database processor from ScriptProcessor.
    - No function ports?
    - Ports defined in processor class methods

- Save Processor in Library

## Fri Jul 22 2022

- Added console output to redis for tasks *DONE*
- Added Output column to results table *DONE*
- Need to add error handling for tasks and stacktrace output to redis

- Console renderer for processors
- Add links to results in console output
- Add buttons to expand/shrink console output
- Get command history from flow and save it?
- Added History to Designer

## Thu Jul 21 2022

- TODO: System Usage
- 
- Click stat names for table of results

- Added new ini to separate redis and mongo from backend *DONE*
- New backend is mongo with user/pass *DONE*
- TODO: Change redis result calls to use mongo
- TODO: Get result stats for UI. status:"SUCCESS"
- Console panel for script processors.
    - Will contain stdout/stderr from the task. The worker will post the stdout to redis and it will arrive at the browser. the processor will check for type 'output' for that processor id.
- stdout/stderr for running python task will be stored and associated with the call object.
- Upload Flow - Selects and uploads a flow json, stores in redis using uuid key chosen by the app. Then retrieves the json from API server and applies it to the canvas. Cached flow json in redis, expires after 2 minutes.

THOUGHTS:
- UI getting near a MVP status!
- Enabled/Disable processor status requires processor login
- Begin adding boilerplate processors such as database, parallel, router.
    - These processors have some pre-defined behavior around your code that control flow and state
        - For example, the router processor will provide your function
        with a "routes={}" kwarg that contains the names of output routes
        your code will set those keys to true for routes that its return
        value should propagate.
        - This behavior is loaded by a class inside the worker and wrapped around the method invocation.


## Tue Jul 19 2022

- Load Python menu. Only enabled if python not already loaded  *DONE*
- Python button in code viewer only enabled if python loaded
- TODO: Modify store to maintain python loaded state  *DONE*
- BUG: Have to switch tabs for run all to work
- Fixed Queue name bug *DONE*
- UI tweaks with results editor height

Notes:
- Full data result and queued message visibility
- Queue status visibility
- Real-time data/queue streaming metrics
-

## Mon Jul 18 2022

- Added connected, streaming to designer.store
- BUG: Pasted nodes cannot be saved in new flow (circular reference?)
- Add streaming, connected toggle UI
- 

## Fri Jul 15 2022

- Implemented search
- BUG: Adding error or output port throws exception in Queue.Vue *FIXED*
- TODO: Store celery results as JSON in redis or index celery string results, then search on "status\x94\x8c\aSUCCESS" from scheduler
- Scheduler performs stats queries and publishes to redis/pubsub for browsers
- TODO: Selection panel buttons
- TODO: Messages


## Tue Jul 12 2022

- Shuffled some menu items around
- Node centering, cornering
- Implemented numerous stat bar icons
    - Running processors
    - Stopped processors
    - Process Groups
    - Stop Nodes
    - Run Nodes
    - Context Menu: Start, Stop, Versions
    - 
- TODO: Reactive designer buttons. Only enabled when usable
- TODO: Database drag node type
- TODO: Disallow closing the scratch flow *DONE*
- TODO: Edge queue/config stored in edge->data object *DONE*

## Sun Jul 10 2022

- Result viewer dialog and service for processors
- Version service and dialog for flows
- BUG: Pattern group bounds is not big enough for nodes
- BUG: Saving patterns no longer works


## Fri Jul 08 2022

- Dymamic port menu with functions from code *DONE*
- Load code from git repo *DONE*
- Rearrange some UI buttons *DONE*
- Dynamic task mapping to swagger on API service *DONE*
- Copy Node from context menu *DONE*
    - Add status bar message *DONE*

- SQLAlchemy change event handler *DONE*
    - Will store status changes in history table TBD
    - Change events published to redis/socket.io *DONE*

- SchemaTemplate updates
- 

- Editing schema node updates schema list dropdown
- TODO: Dynamic port schema dropdown from schema nodes present *DONE*
- TODO: Requirements UI needs its own editor
- TODO: Dynamic arguments on new port *DONE*
- TODO: GIT flag determines if code is loaded from git or taken literally from code field
- 


## Tue Jul 05 2022

- Added config for git python module file path
- Removed schema for function port
- Added Throttling processor config
    - rate_limit
    - perworker
- Added rate limiting logic in scheduler
- Swapped refresh and workers commands on processor
- Added 'Results' menu option on processor
- BUG: Scheduler not adding deployments for shortfall
- Scheduler not running all deployments. One stuck in pending

- Add PyScript integration

## Sun Jul 03 2022

- BUG: redundant worker being created .1 becomes active worker *FIXED*
- BUG: redundant assignment of deployment to workers on agent *FIXED*


## Wed Jun 29 2022

- Add function ports with arguments
- Can only connect function ports to argument ports
- Argument ports are input only
- Function ports are output only
- Schema select for function (output) and args (input)
- Remove Plug port type
- Update Queue edge UI. Add close button, menu button for data, drop down to select queue


- Add type selector icon to data template (e.g. table, json, csv, etc)


## Fri Jun 24 2022

- BUG: QueuePool limit of size <x> overflow <y> reached, connection timed out, timeout *FIXED*
- Fixed worker_model query selection using deployment relation instead of implied name
- Workers are now created based on multiple deployments for same host/agent
    - e.g. agent2.agent.proc1.worker.1, agent2.agent.proc1.worker.2

    - This allows for multiple deployments of same processor on same host.
        - e.g. one deployment with 2 CPUs and another (comes later) needing 3 CPUs
        - Scheduler may combine these deployments later into one with 5 CPUs
- Improved worker session management

## Tue Jun 21 2022

- Deployment not getting bound to worker inside worker.py and committed properly. 
- cli.py workerproc used before it was set


## Sun Jun 19 2022

- Pipeline, chord and parallel script nodes operate on the ports. For example, you would
add a port for each function call from the node module. For parallel they all execute in parallel.
A special "completed" port is added and used to link to another process. You cannot link the function ports.

For pipeline, the "start" port collects the input, passes to first function. Each result is passed down
the list of function ports until the "complete" port is reached and the result is passed along that plug.

- Router acts like a special "parallel" node where each port evaluates a function in parallel and if true,
the input data is forwarded to any outbound plugs on that port.

-  Added new templates for Pipeline, Parallel, Chord and Segment
- Added "Messages" box with scrolling for server messages based on UI actions. For example, saving and deploying
a processor. Publishing a flow, etc.

- If loading a flow, make the title name uneditable. Must rename using the Flows panel.

- Added DataTemplate, SchemaTemplate

## Fri Jun 17 2022

- Restart API if processor status changes so endpoints can be removed

## Thu Jun 16 2022

- Implied worker names need tweaking
- BUG: QueuePool limit of size <x> overflow <y> reached, connection timed out, timeout
- flow cli kill agent requested_status='kill' agent reacts to requested_status='kill' *DONE*
- API process *DONE*

## Wed Jun 15 2022

- Scheduler has a new WatchPlugin that monitors state of objects and updates their status
- Add a Flow node type for emitting data (e.g. json) and triggering a flow from the UI
    - Drag and drop a data node. Add some JSON to the code dialog, click the emit buttons
    - Open dialog for json-schema for the data 
    - Can use this node to validate data passing through it
        - Add special port for inbound data validation
        - Add special port for validated vs not validated

- Delete plugs -> cascade to calls & events?
- Plug state connected, disconnected

## Wed Jun 08 2022

- Add --cpus to add processor cli to imply deployment or not *DONE*


## Tue Jun 07 2022

- Add two tasks with socket for same processor:git:module *DONE*
- Invoke each task separately *DONE*
- Add watchdog to scheduler that sets whether processors, workers, agents are running or not. *DONE*
- Ensure celery worker uses same name as worker object in database
- Endpoint to get status of workers, compare to database workers, return results
- Add watcher to api process that monitors processes and if they don't exist in database, then remove them from api/swagger

## Sat Jun 04 2022

- Need watcher process that checks health of deployments by checking on worker


## Thu Jun 02 2022

- Add flask_restx APIs to pyfi.server.api *DONE*
- Get deployments for processor endpoint

- POSTMAN for getting queued messages from rabbitmq *DONE*
- Flower API to get results of tasks *DONE*


## Wed Jun 01 2022

- Add modal dialog table for viewing queue messages and clicking on them to view results. UNDERWAY
- Add table in processor concurrency showing active deployments UNDERWAY
    - When concurrency value is increased and processor saved, new deployments should appear


## Tue May 24 2022

- Added splitter on main layout for top level message traffic, queues, monitoring charts and errors *DONE*
- BUG Setting color of group panel is not restored when re-loaded *FIXED*
- 


## Mon May 23 2022

- Added Label node type
- Updated redis to redismod for searching, json, etc *DONE*
    - This will be used to pull data for monitoring and reports

- Add a "chart" node type, where data feeds into a selected chart type *DONE*
    - The chart is then available for drag and drop on the App
- App<->Designer route toggler *DONE*
    - App is where you can drag and drop charts and arrange them
    - The available charts are derived from the chart nodes in the underlying flows
- BUG Dropping a pattern on the canvas does not locate it where the mouseup occurred 
- BUG Deleting only group leaves nodes undraggable on canvas *FIXED*

## Sun May 22 2022

- Added "App" toolpalette icon, jump to App page and back to designer *DONE*
- Queues data is now flowing through designer
- Queue widget on edges showing real data
- Processors and edges now rendering real-time metrics
- Queue widget data window (below) TBD

## Sat May 21 2022

- example20.py
    - Making full network creation easier by adding a transient object creation registry
    that can be used during network creation to reference previous created objects to establish
    relations UNDERWAY

- Right click menu copy selected nodes. Then canvas paste selected nodes
- Add status message when selecting, copying, pasting nodes, etc.
- Bottom menu drawer, with tabs: shows high level message traffic etc *DONE*
- Make edge labels a component with queue selection, config, queued messages, etc *DONE*

## Mon May 16 2022

- Added globalsocket container *DONE*
- Updated worker to post to global streaming channel
- server.ts now sends inbound websocket messages to their intended channels (multiplexor)
- Need container for server.ts (front end multiplexor)
    - globalsocket and websocket containers are microservices that connect to redis pub/sub and repost messages on websockets
    - server.ts listens on backend websockets and reposts to socket.io channels for front-end clients


## Tue May 10 2022



## Wed May 04 2022

- Settings tabs updated when switching type of processor
DESIGN:
Fields in settings tabs are visible to script. Wrapper script is shown in the code dialog
Depending on the type of processor, the sockets and plugs will have different meanings.
For example, for a script processor, the plugs are return value fields. For a database, it 
might be individual queries or result sets or events.


## Mon May 02 2022

- Add configuration tab based on type of processor UNDERWAY
- Update uuids before adding patterns


## Sat Apr 30 2022

- Networks tab object card
- Flow name should fade or slide in after initial rendering to mask font style glitch
- When opening multiple tabs, getting duplicate ID errors BUG
- Processors tab creates directories in Flows tab BUG
- Copy button should be disabled unless there is something selected
- Paste button should be disabled unless there is something on the clipboard
- Various event messages should appear in the status bar, but after a few seconds, revert to connection status
- 

## Sat Apr 23 2022

- Navigate button to set zoom level to 100% so editor displays properly *DONE*
- FileModel key needs to be combination of name and path
BUGS
- Timer function calls are overwriting processor records in database with the agents local version *FIXED*
- Add an API processor endpoint dispatcher to `flow api start` server

## Thu Apr 21 2022

- Switch to tab when flow is already open
- Error handling (e.g. flow name already exists) *DONE*
- Error messages
- Add folders, click folders, breadcrumbs *DONE*
- Delete flows *DONE*
- Rename flows
- Need draggable handles on edge arrows

## Wed Apr 20 2022

- Flow tabs now generated from data list *DONE*
- New Flow menu option *DONE*
- Save and load flow tabs *DONE*
- Close Flow Tabs *DONE*

## Tue Apr 19 2022



## Sun Apr 17 2022

- Object list UI for Flows *DONE*
    - Add folder input
- Configure dialog with tabs for
    - Settings
    - Concurrency
    - Schedule
    - Security
    - Scaling


## Mon Apr 11 2022

- Add flow commands to CLI. stores JSON for flow along with name.
- A flow can span networks
- Front end will receive streaming events for all processors to avoid
    maintaining any server<->client state or pub sub that could get out of sync
    - Front end will store state in its various stores as stream events occur
        whether or not the UI is currently viewing those objects. This way,
        the state is always updating in the background and if the UI present those
        objects they will already be updating.
- 

## Sat Apr 09 2022

- Rebrand to lambdaflow.ai
- User security to grant or revoke executing tasks involves updating the pyfi.polar
- pyfi.polar policy file located behind URL
- Create generic container for pyfi
    - Run various CLI commands from it like "flow api start"


- Run UI behind nginx *DONE*
- UI can contact api backend: flow api start *DONE*
- UI connects to socket server and receives messages from server *DONE*
- Single domain
    - socket -> localhost/...
    - API -> localhost/api
    - app -> localhost

## Thu Apr 07 2022

- Code viewer *DONE*
- 


## Wed Apr 06 2022

- Need to remove fixed id for groups and patterns *DONE*
- Added draggable patterns and separate pattern template that will load the pattern 70%
- Add ability to save a pattern from selected nodes
- Finish copy/paste buttons
- Got selection and zooming to work *DONE*
- Removed spurrious buttons on upper toolbar. *DONE*
- Added color picker for groups *DONE*
- Finish code viewing dialog to view the JSON for the flow *DONE*

- Notion of flow is "connected" or "disconnected". Connected means it is reacting live to the running objects in the database and receiving live telemetry. Disconnected means the flow is not receiving live data and any changes to the flow are not immediately pushed back to the server.

## Tue Mar 29 2022

- PYFI UI development. 
    - Build global vuex store for all components to be reactive to server side messages
    - Build DataService API object
    - Build socket.io component to receive streaming messages from server and update vuex store, which will update all reactive components.
    - Existing ObjectService will remain to manage remote virtual directories to store assets
    - DataService.ts will provide API to flow backend
    - Only one page/route for entire app
    - Quasar 1.15, Vue 2, Composition API, typescript, jsplumb 2
    - axios, apexcharts, vue-type-mixins
    - Create typescript taxonomy of objects for processors with built in support for vuex, etc


## Fri Mar 25 2022



## Wed Mar 16 2022

- Blazer: explore use of shared variables 

## Wed Mar 09 2022

- PYFI - Improvements to new plugin scheduler
    - Now queries processors whose deployments fall short of the processor concurrency property
    - Will create new deployments on agents that have free CPUs
    - Fixed bug with agent and node CPU settings and hostnames
        - Nodes now reflect hardware CPU count
        - Agents are (logical) and can have less CPUs than node
            - Currently only one agent per node


## Tue Mar 08 2022

- blazer: need to add data generator that introspects data file and reads in chunks send them out to ranks
    as it streams off disk, it sends tasks to individual ranks


## Sat Feb 26 2022



## Thu Feb 24 2022

- Add plugs and sockets to ls_task
- Add plugs to ls_socket
- 

## Tue Feb 22 2022

- Working plugin agent service - testing

## Sat Feb 19 2022

- Updated logging
- Convert logging.info to logger.info
- Re-write of agent using plugins and scheduler vs. loops and sleep
    - Stable memory consumption
    - Ephemeral sessions

## Sun Feb 06 2022

- Lots of website work *DONE*
- Added captcha to website *DONE*
- Review NGINX settings and API server (from cli) *DONE*
   - redundantly added "flow server start" for debug mode API server start. Probably will remove
- Need to update nginx conf to route to API server *DONE*
- Test UI connects to API server *DONE*
- Confirm Flower UI records all tasks, workers, etc *DONE*

## Tue Feb 01 2022

- When agent stops, worker record remains and scheduler thinks the CPUs are taken.
Either, worker record needs to be reset or the worker needs to be restarted based on the record, which points to the processor.
   - scheduler needs to check depoyment for worker to determine if CPUs are taken

## Mon Jan 31 2022



## Sun Jan 30 2022

- Worker concurrency now matches deployment cpus
- 


## Sat Jan 22 2022

- Scheduler work
- Scheduler will spread CPU shortfall across available nodes
- Fixed session.close() not being called in scheduler


## Fri Jan 21 2022

- Fixed duplicate lifecycle emission *DONE*
- Properly catches exceptions and stores task FAILED status and exception trace *DONE*
- Pub/sub emits error with trace *DONE*

## Wed Jan 19 2022

- Plug types ERROR, RESULT
    - Route exceptions to error plugs *DONE*
    - Route good results to result plugs *DONE*

## Tue Jan 18 2022

- Website prototype UNDERWAY
- Agent/Worker debugging *DONE*

## Fri Jan 14 2022

- Class decorators working
- Can instantiate class, invoke methods (local or remote) and combine with pipes
- Can retrieve task value using id from another process
- CLI updates. calls now show result ids
- New examples for decorator API, retrieving task results by id etc

TODO:
- Agent workerprocs need to be stored in list
- @processor decorater needs to wrap class/method into harness function and embed with task.
    harness function will instantiate the class and execute the method passing in the parameters
        - Need to strip decorators

## Mon Jan 10 2022

- NetworkModel *DONE*
- Add network relation *DONE*
- Delete entire network *DONE*
- ls network by name *DONE*
- ls networks *DONE*
- add scheduler to yaml for network *DONE*

## Sun Jan 09 2022

- Scheduler plugins
- Timed events

## Fri Jan 07 2022

- Stopping a processor needs to stop all distributed workers

- ls queues and ls queue show rabbit message info and bindings *DONE*
- Deployment controlling cpus/concurrency for workers
- Agent/Node record CPUs for scheduler
- Scheduler reviews processors selected for 'deploy'ment
- When running flow compose, if an action will overwrite an existing object, prompt user
   unless they have -y set
- Rename Agent to AgentService and Worker to WorkerService to avoid clashing with objects API classes

## Thu Jan 06 2022

- Worker health service *DONE*
- CLI agent,worker port selection *DONE*

## Wed Jan 05 2022

- Show reliable, load balancing across deployments *DONE*
- When agent detects new processor, deployment is not associated with worker *FIXED*
- Remove deployments *DONE*

## Tue Jan 04 2022

- Attach to same container if running, when worker starts. *DONE*
- Run agent with provided hostname *DONE*

## Sun Jan 02 2022

- Overhaul Processor model. Add Deployment Model. *DONE*

Processor is now a logical construct not bound to specific host. Deployments are entries that represent physical attachment of a logical processor. This makes the processor "elastic" and virtual.

Sending invocations to "the processor" load balances across all the deployments. Scheduler can grow or shrink deployments depending on frequency of calls along with resource utilization reported by the agent.

## Sat Jan 01 2022

- Processors now can have multiple hostnames
    - Test task load balancing with multiple hostnames
    - Show that adding a hostname to an existing processor deploys it on that server. Then run tasks

## Fri Dec 31 2021

- Added arguments to calls
- Updated processor container to python:3-slim-buster
- Tested multiple plugs into one function
- Add arguments to graph view in ls processor

## Thu Dec 30 2021

- Adding data flows doc page
- Add emit_one and emit_two to phoenix agent
- Add do_something to phoenix
- Add do_this to agent2
- Show multiple processors running on same hosts
    - start/stop/remove/update
- Start building bigger networks
- Start assembling library of components
- Container support in workers
- Fix agent kills worker pids on exit
    - Also kills containers

## Wed Dec 29 2021
 
 - Got multi processor plugs and arguments working
 - Changed agent.worker to agent.workers
 - Need to add plugs to ls network etc.
 - compose build improvements and testing
 - basic pytest structure
 - Updated celery to 5.2.3


## Tue Dec 28 2021

- Improvements to compose build. --nodeploy
    - Now constructs all object placeholders such as 'pyfi ls network' works
- Improvements to various cli commands like delete, ls, etc
- pyfi task code : show code of task (loaded or assigned)
- Added Worker class and model
- Added Node class and model
- Dockerfile agent updates


## Thu Dec 23 2021

- Impl stop agent cli
- Impl compose *args for nodes
- Fixed kill worker bug
- Added --nodeploy to compose
- Added global exception catch for cli errors
- Code formatting with pycharm

## Wed Dec 22 2021

TODO
- "ls queues" needs to pull message counts from rabbit

STATUS
- Got graph data flowing across processors/tasks
- Implemented wrapped_function and argument passing. Will allow for tasks to trigger when arguments have all arrived (at different times)
- docker for redis result subscribe<->websocket bridge working fine
    - node clients for listening on websockets and posting to influxdb working well
    - grafana charts plotting from influxdb working well.
- removed data passing using kwargs plugs (commented out)
- Return value from task is passed to next task over plug
- Plugs can be attached to an argument or just a socket
    - argument selection is attribute of plug
    - an argument will have list of attached plugs
- Added "add argument" cli
- Implemented "ls task" that shows arguments
- Implemented "ls plug" that shows source/target tasks and connected arguments'
- Updated "ls network" to show arguments beneath tasks
- New Yaml fields to skip cleaning and deployments (e.g. just to create database objects)
    - Convert to CLI option?

## Sat Dec 18 2021

- Got custom task code working. Updates processor
- Got docker agents working again
- Additional properties to pyfi.yaml


## Fri Dec 17 2021


