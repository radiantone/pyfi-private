/**
 * @module jsPlumbToolkit
 */
declare module jsPlumbToolkit {

    type ObjectId = string;
    type ObjectType = "Node" | "Port" | "Edge" | "Group";

    type FactoryCallback = (data:object) => void;
    type FactoryFunction = (type:string, data:object, callback:FactoryCallback)=>void;

    type NodeFactory = FactoryFunction;
    type PortFactory = FactoryFunction;
    type EdgeFactory = FactoryFunction;
    type GroupFactory = FactoryFunction;

    type NodeRef = Node | ObjectId;
    type PortRef = Port | ObjectId;

    type SelectionCapacityPolicy = "discardExisting" | "discardNew";

    type SurfaceMode = "pan" | "select" | "disabled";
    type ZoomRange = [number, number];

    type BackgroundType = "simple" | "tiled";

    type BoundingRectangle = {x:number, y:number, w:number, h:number};

    type CanvasLocation = { left:number, top:number };
    type PointArray = [ number, number ];

    interface IntersectingObjectData {
        el:HTMLElement;
        r:BoundingRectangle;
        id:string;
    }

    module Dialogs {
        function show(options:any):void;
        function initialize(options:any):void;
        function apply(target: any, data: any):void;
        function extract(target: any):any;
    }

    interface Dictionary<T> {
        [Key: string]: T;
    }

    module jsPlumbToolkitIO {
        type Parser = (data:any, toolkit:jsPlumbToolkit, parameters?:any) => any;
        type Exporter = (toolkit:jsPlumbToolkit, parameters:any) => any;

        const exporters:Dictionary<Exporter>;
        const parsers:Dictionary<Parser>;
        const managers:Dictionary<Dictionary<Function>>;
        
        function parse(type:string, data:any, toolkit:jsPlumbToolkit, parameters?:any):any;
        function exportData(type:string, toolkit:jsPlumbToolkit, parameters?:any):any;
    }

    module jsPlumbToolkit {
        function newInstance(params:jsPlumbToolkitOptions):jsPlumbToolkit;
        function ready(fn:Function):void;
    }

    interface AutoSaveOptions {
        autoSave?:boolean;
        autoSaveDebounceTimeout?:number;
        saveUrl?:string;
        saveHeaders?:Map<string, string>;
        onAutoSaveSuccess?:Function;
        onAutoSaveError?:Function;
        onBeforeAutoSave?:Function;
        onAfterAutoSave?:Function;
        autoSaveHandler?: (instance: jsPlumbToolkit) => any;
    }

    interface jsPlumbToolkitOptions extends AutoSaveOptions {
        idFunction?:(data:object)=> string;
        typeFunction?:(data:object) => string;
        typeProperty?:string;
        edgeIdFunction?:(data:object) => string;
        edgeTypeFunction?:(data:object) => string;
        edgeTypeProperty?:string;
        portIdFunction?:(data:object) => string;
        portTypeFunction?:(data:object) => string;
        beforeConnect?:(source:Node | Port | Group, target:Node | Port | Group, data:object)=>boolean;
        beforeMoveConnection?:Function;
        beforeStartConnect?:(source:Node | Port | Group, edgeType:string)=>any;
        beforeDetach?:Function;
        beforeStartDetach?:Function;
        nodeFactory?:FactoryFunction;
        edgeFactory?:FactoryFunction;
        portFactory?:FactoryFunction;
        groupFactory?:FactoryFunction;
        portExtractor?:Function;
        portUpdater?:Function;
        portDataProperty?:string;
        doNotUpdateOriginalData?:boolean;
        maxSelectedEdges?:number;
        maxSelectedNodes?:number;
        selectionCapacityPolicy?:SelectionCapacityPolicy;
        createMissingGroups?:boolean;
    }

    interface ConnectOptions {
        source:AbstractEdgeTerminus | ObjectId;
        target:AbstractEdgeTerminus | ObjectId;
        cost?:number;
        directed?:boolean;
        data?:any;
    }

    interface ProgrammaticConnectOptions extends ConnectOptions {
        doNotCreateMissingNodes?:boolean;
    }

    interface PathRetrievalOptions {
        source: Node | Port | ObjectId;
        target: Node | Port | ObjectId;
        strict?: boolean;
        nodeFilter?: (data:any)=>boolean;
        edgeFilter?: (data:any)=>boolean;
    }

    interface PathSpec {
        source: Node | Port | ObjectId;
        target:Node | Port | ObjectId;
    }

    interface LoadSaveOptions {
        type?:string;
        url?:string;
        parameters?:any;
        error?:Function;
        headers?:Map<string, string>
    }

    interface LoadOptions extends LoadSaveOptions {
        data?:object;
        jsonp?:boolean;
        onload?:Function;
    }

    interface SaveOptions extends LoadSaveOptions {
        success?:Function;
    }

    interface ExportOptions {
        type?:string;
        parameters?:any;
    }

    interface ObjectInfo {
        obj?:Node|Port|Edge|Group;
        id?:ObjectId;
        type?:ObjectType;
        el?:Element;
        els?:Map<Surface, Element>;
    }

    interface Cluster {
        vertices:Array<NodeOrGroup>;
    }

    interface LayoutSpec {
        type:string;
    }

    interface SpringLayoutSpec extends LayoutSpec {
        type:"Spring",
        padding?:[number, number]
    }

    /**
     * @class Graph
     */
    class Graph {
        getPortSeparator():string;
        serialize():string;
        getVertexByPortId(portId:string):Node|Group;
        splitPortId(portId:string):Array<string>;
    }

    /**
     * @class jsPlumbToolkit
     */
    class jsPlumbToolkit extends AbstractSelectionHolder {

        load(options:LoadOptions):jsPlumbToolkit;
        append(options:LoadOptions):jsPlumbToolkit;
        save(options:SaveOptions):jsPlumbToolkit;
        bind(event:string, handler:Function):void;
        unbind(event:string, handler:Function):void;
        exportData(options?:ExportOptions):any;

        addNode(data:any, eventInfo?:ViewEventOptions):Node;
        addFactoryNode(type:string, dataOrCallback1:any|NodeHandler, dataOrCallback2?:any|NodeHandler):void;
        addNodes(data:Array<any>):jsPlumbToolkit;
        addEdge(data:ConnectOptions):Edge;
        addGroup(data:any, eventInfo?:ViewEventOptions):Group;
        addFactoryGroup(type:string, dataOrCallback1:any|GroupHandler, dataOrCallback2?:any|GroupHandler):void;
        addToGroup(node:Node, group:Group):boolean;
        addNewPort (obj:Node|ObjectId, type:string, initialPortData?:object):void;
        addPort (obj:Node|ObjectId|Group, portData?:any):Port;

        removeEdge(edge:Edge|ObjectId):jsPlumbToolkit;
        removeNode(node:Node|ObjectId):jsPlumbToolkit;
        removeGroup(group:Group, removeChildNodes?:boolean):jsPlumbToolkit;
        removeFromGroup(node:Node):Group;
        removePort(node:Node|ObjectId|Group, portId:ObjectId):boolean;
        remove(obj:Node|Group|Edge|Selection|Path):void;

        updateGroup(group:Group|ObjectId|any, data?:any):void;
        updateNode(node:Node|ObjectId|any, data?:any):void;
        updatePort(port:Port|ObjectId|any, data?:any):void;
        updateEdge(edge:Edge|ObjectId|any, data?:any):void;
        update(obj:Node|Port|Edge|Group|ObjectId, data?:any):Node|Port|Edge;

        getNodeFactory():NodeFactory;
        getPortFactory():PortFactory;
        getEdgeFactory():EdgeFactory;
        getGroupFactory():GroupFactory;

        getGraph():Graph;

        setNodeFactory(factory:NodeFactory):void;
        setPortFactory(factory:PortFactory):void;
        setEdgeFactory(factory:EdgeFactory):void;
        setGroupFactory(factory:GroupFactory):void;

        setDebugEnabled(enabled:boolean):void;
        isDebugEnabled():boolean;

        setDoNotUpdateOriginalData(value:boolean):void;

        getTypeFunction():Function;

        connect(options:ProgrammaticConnectOptions):Edge;

        setEdgeGeometry (edge:Edge, geometry:any):void;

        /**
         * Fires a 'graphClearStart' event, clears the graph, then fires a `graphClearEnd` event.
         * @method clear
         * @return {jsPlumbToolkit} The current Toolkit instance.
         */
        clear():jsPlumbToolkit;

        getEdge(id:ObjectId):Edge;
        getEdges(options:PathSpec):Array<Edge>;
        getAllEdges():Array<Edge>;
        getAllEdgesFor(obj:Node|Port|Group, filter?:Function):Array<Edge>;
        getGroup(id:ObjectId):Group;
        eachNode(nodeCallback:Function):void;
        eachGroup(groupCallback:Function):void;
        eachEdge(edgeCallback:Function):void;
        getPort(fullPortId:string):Port;

        selectAllEdges():Selection;
        addAllEdgesToSelection():void;
        setSelection(obj:Node|Edge|Array<Node>|Array<Edge>|Path|string):Selection;
        select(obj:Node|Port|Edge|Array<Node>|Array<Port>|Array<Edge>|Path|string, includeEdges?:boolean):Selection;
        selectDescendants(obj:Node|Port|Edge|Array<Node>|Array<Port>|Array<Edge>|Path|string, includeRoot?:boolean, includeEdges?:boolean):Selection;
        filter(spec:Function|object, includePartials?:boolean):Selection;
        addToSelection(obj:Node|Edge|Array<Node>|Array<Edge>|Path|string):void;
        toggleSelection(obj:Node|Edge|Array<Node>|Array<Edge>|Path|string):void;
        removeFromSelection(obj:Node|Edge|Array<Node>|Array<Edge>|Path|string):void;
        addPathToSelection(spec:PathSpec):void;
        clearSelection():void;
        getSelection():Selection;

        getEdgeCount():number;
        getGroupCount():number;

        getGroupAt(index:number):Group;

        getClusters():Array<Cluster>;

        getType(obj:Node|Port|Edge|object):string;

        exists(...ids:Array<string>):boolean;

        setTarget(edge:Edge, target:Node|Port|ObjectId):void;
        setSource(edge:Edge, target:Node|Port|ObjectId):void;

        render(params:SurfaceOptions):Surface;
        setSuspendRendering(suspend:boolean, thenRefresh:boolean):void;
        getRenderer(id:string):Surface;
        getRenderers():Map<string, Surface>;

        batch(fn:Function):void;

        getPath(options:PathRetrievalOptions):Path;

        setMaxSelectedNodes(max:number):void;
        setMaxSelectedEdges(max:number):void;

        setAutoSave(options:AutoSaveOptions):void;

        getVersion():string;

    }

    /**
     * Base class for all objects in a Graph.
     * @class GraphObject
     * @abstract
     */
    abstract class GraphObject {
        getFullId():string
        data:any;
        objectType:ObjectType;
        id:string;
    }

    /**
     * Base class for objects in a Graph that can act as the terminus for an Edge. 
     * @class AbstractEdgeTerminus
     * @abstract
     */
    abstract class AbstractEdgeTerminus extends GraphObject {
        getSourceEdges():Array<Edge>;
        getTargetEdges():Array<Edge>;
        getAllEdges():Array<Edge>;
    }

    /**
     * Base class for objects that can manage a selection: the jsPlumbToolkit class, and
     * the Selection class.
     * @class AbstractSelectionHolder
     * @abstract
     */
    abstract class AbstractSelectionHolder {

        getNodeId(obj:Node|object):string;
        getEdgeId(obj:Edge|object):string;
        getPortId(obj:Port|object):string;

        getNodeType(obj:Node|object):string;
        getEdgeType(obj:Edge|object):string;
        getPortType(obj:Port|object):string;

        getObjectInfo(obj:string|Element|Node|Port, elementResolver?:Function):ObjectInfo;

        getNodeCount():number;
        getNodeAt(index:number):Node;
        getNode(id:string):Node;
        getNodes():Array<Node>;

        getGroupCount():number;
        getGroupAt(index:number):Group;
        getGroup(id:string):Group;
        getGroups():Array<Group>;

        getEdgeCount():number;

        getEdge(id:string):Edge;

    }

    class Node extends AbstractEdgeTerminus {
        getPorts():Array<Port>;
        addPort(data:any):Port;
        getPort(portId:String):Port;
    }

    class Port extends AbstractEdgeTerminus {
        getNode():Node;
    }

    class Group extends AbstractEdgeTerminus {
        getPorts():Array<Port>;
        addPort(data:any):Port;
        getPort(portId:String):Port;
    }

    class Edge extends GraphObject {
        source:AbstractEdgeTerminus;
        target:AbstractEdgeTerminus;
        getId():string;
        setId(id:string):void;
    }

    class Path { }
    class UIPath extends Path {
        setVisible(visible:boolean):void;
        addNodeClass(clazz:string):void;
        removeNodeClass(clazz:string):void;
        addEdgeClass(clazz:string):void;
        removeEdgeClass(clazz:string):void;
        addClass(clazz:string):void;
        removeClass(clazz:string):void;
    }

    type NodeOrGroup = Node | Group;
    type NodeOrGroupFilter = (obj:NodeOrGroup) => boolean;

    type NodeHandler = (node:Node) => void;
    type GroupHandler = (group:Group) => void;

    interface SelectionOptions {
        toolkit:jsPlumbToolkit;
        generator?:Function;
        onBeforeReload?:Function;
        onReload?:Function;
        autoFill?:boolean;
        onClear?:Function;
    }

    class Selection extends AbstractSelectionHolder {

        constructor(options:SelectionOptions);

        remove(obj:Node|Edge|Array<Node>|Array<Edge>|Path):void;
        append(obj:Node|Edge|Array<Node>|Array<Edge>|Path):void;
        toggle(obj:Node|Edge|Array<Node>|Array<Edge>|Path):void;

        setMaxNodes(max:number):void;
        setMaxEdges(max:number):void;

        setCapacityPolicy(policy:SelectionCapacityPolicy):void;

        clear():void;

        reload():void;

        each(fn:Function, type:ObjectType):void;

        eachNode(fn: (idx: number, obj:Node) => void):void;
        eachGroup(fn: (idx: number, obj:Group) => void):void;
        eachNodeOrGroup(fn:(idx: number, obj:NodeOrGroup)=>void):void;
        eachEdge(fn:(idx: number, obj:Edge)=>void):void;

        getAll():Array<Node|Edge|Group>;

        getAllEdgesFor(node:Node):Array<Edge>;

        getEdgeAt(index:number):Edge;
        getEdges():Array<Edge>;

    }


// --------- Rendering types/classes -------------------------

    interface jsPlumbOptions {
        Endpoint?: EndpointSpec;
        Endpoints?:[ EndpointSpec, EndpointSpec ];
        Anchor?:AnchorSpec;
        Anchors?:[ AnchorSpec, AnchorSpec ];
        PaintStyle?: PaintStyle;
        HoverPaintStyle?: PaintStyle;
    }

    interface BackgroundOptions {
        url?:string;
        type?:BackgroundType;
        tileSize?:number[];
        width?:number;
        height?:number;
        maxZoom?:number;
    }

    type ViewOptionsEntry<T> = Dictionary<T>;

    interface ViewOptions {
        nodes?:ViewOptionsEntry<ViewNodeOptions>;
        edges?:ViewOptionsEntry<ViewEdgeOptions>;
        groups?:ViewOptionsEntry<ViewGroupOptions>;
        ports?:ViewOptionsEntry<ViewPortOptions>;
    }

    interface ViewOptionsCommon {
        parent?:string;
        events?:ViewEventOptions;
    }

    interface ViewNodeOrPortOptions extends ViewOptionsCommon {
        allowLoopback?:boolean;
        component?:any;
    }

    interface ViewNodeOptions extends ViewNodeOrPortOptions {
        template?:string;
        dragOptions?:DragOptions;
        allowNodeLoopback?:boolean;
    }

    interface ViewEdgeOptions extends ViewOptionsCommon  {
        connector?:ConnectorSpec;
        anchor?:AnchorSpec;
        anchors?:[AnchorSpec, AnchorSpec];
        paintStyle?:PaintStyle;
        hoverPaintStyle?:PaintStyle;
        overlays?:Array<OverlaySpec>;
        endpoint?:EndpointSpec;
        endpoints?:[EndpointSpec, EndpointSpec];
        cssClass?:string;
        label?:string;
        labelLocation?:number;
        labelLocationAttribute?:string;
    }

    interface ViewGroupOptions {
        template?:string;
        component?:any;
        droppable?:boolean;
        constrain?:boolean;
        revert?:boolean;
        prune?:boolean;
        orphan?:boolean;
        dropOverride?:boolean;
        endpoint?:EndpointSpec;
        anchor?:AnchorSpec;
    }

    interface ViewPortOptions extends ViewNodeOrPortOptions  {
        template?:string;
        edgeType?:string;
        maxConnections?:number;
        isSource?:boolean;
        isTarget?:boolean;
        isEndpoint?:boolean;
        endpoint?:EndpointSpec;
        anchor?:AnchorSpec;
        uniqueEndpoint?:boolean;
        paintStyle?:PaintStyle;
        overlays?:Array<OverlaySpec>;
    }

    interface LayoutOptions {
        type:string;
        parameters?:any;
    }

    type BindableEvent = "click" | "dblclick" | "mouseover" | "mouseout" | "mousedown" | "mouseup" | "tap" | "dbltap" | "contextmenu";
    type SurfaceEvent = "nodeAdded" | "nodeRendered" | "nodeRemoved" | "nodeMoveStart" | "nodeMoveEnd" | "edgeAdded" | "edgeRemoved" | "portAdded" | "portRemoved" | "anchorChanged" | "modeChanged" | "objectRepainted"
                                | "pan" | "zoom" | "canvasClick" | "canvasDblClick" | "relayout";

    type SurfaceBindableEvent = BindableEvent | SurfaceEvent;

    type ViewEventOptions = { [K in BindableEvent]?: Function };
    type SurfaceEventOptions = { [K in SurfaceBindableEvent]?: Function };

    interface AbstractRendererParams {
        elementsDraggable?:boolean;
        elementsDroppable?:boolean;
        id?:string;
        enhancedView?:boolean;
        modelLeftAttribute?:string;
        modelTopAttribute?:string;
        assignPosse?:Function;
        relayoutOnGroupUpdate?:boolean;
        objectFilter?:(obj:Node|Group)=>boolean;
        ignoreGroups?:boolean;
        refreshLayoutOnEdgeConnect?:boolean;
    }

    interface SurfaceRenderParams extends AbstractRendererParams {
        dragOptions?:DragOptions;
        events?:SurfaceEventOptions;
        miniview?:MiniviewOptions;
        mode?:SurfaceMode;
        panDistance?:number;
        zoom?:number;
        zoomRange?:ZoomRange;
        enablePan?:boolean;
        enableWheelZoom?:boolean;
        enableAnimation?:boolean;

        wheelFilter?:Selector;
        panFilter?:Selector|EventTargetFilter;
        lassoFilter?:Selector;

        wheelSensitivity?:number;
        wheelReverse?:boolean;
        wheelZoomMetaKey?:boolean;
        enablePanButtons?:boolean;
        padding?:number[];

        lassoInvert?:boolean;
        lassoSelectionFilter?: (obj:NodeOrGroup)=>boolean;
        lassoEdges?:boolean;

        consumeRightClick?:boolean;

        stateHandle?:string;

        clamp?:boolean;
        clampToBackground?:boolean;
        clampToBackgroundExtents?:boolean;

        background?:BackgroundOptions;

        jsPlumb?:jsPlumbOptions;

        autoExitSelectMode?:boolean;

        zoomToFit?:boolean;
        zoomToFitIfNecessary?:boolean;

        storePositionsInModel?:boolean;

        layout?:LayoutOptions;

        tags?:Dictionary<CustomTagSpec>;
    }

    interface SurfaceOptions extends SurfaceRenderParams {
        container:ElementRef | Selector;
        view:ViewOptions;
    }

    interface MiniviewOptions {
        container:ElementRef | Selector;
        elementFilter?: (obj: Node|Group) => boolean;
    }

    interface PathTracingOptions {
        path?:Path;
        source?:Node|Port|ElementRef;
        target?:Node|Port|ElementRef;
        overlay:OverlaySpec;
    }

    interface DroppableNodesOptions {
        typeExtractor?:(data:any) => string;
        dataGenerator?:(data:any) => any;
        droppables?:Array<Element>;
        source?:Element;
        selector?:string;
        dragOptions?:DragOptions;
        dropOptions?:DropOptions;
        start?:Function;
        drag?:Function;
        stop?:Function;
        drop?:Function;
        locationSetter?:Function;
    }

    type EventTargetFilter = (el:Element, e:Event) => boolean;

    interface ZoomOptions {
        fill?:number;//0.90
        padding?:number //20
        onComplete?:Function;
        onStep?:Function;
        doNotAnimate?:boolean; //true
        doNotZoomIfVisible?:boolean;//false
        doNotFirePanEvent?:boolean;//false
    }

    interface CustomTagOptions {
        template:string;
        rendered?:(el:Element, data:any, instance:any)=>void;
        updated?:(el:Element, data:any, instance:any)=>void;
    }

    type CustomTagSpec = [ string, CustomTagOptions ]

    type SurfaceBounds = {
        w: number,
        h: number,
        x: number,
        y: number,
        vw: number,
        vh: number,
        padding: number,
        z: number,
        zoom: number
    }

    interface PathTransport {
        play():void;
        pause():void;
        cancel():void;
        bind(event:string, callback:Function):void;
        state:string;
    }

    class Surface {
        _ngId:string;

        addClass(target: ElementRef|Node|Group, clazz:string):void;
        removeClass(target: ElementRef|Node|Group, clazz:string):void;
        hasClass(target: ElementRef|Node|Group, clazz:string):boolean;

        getToolkit():jsPlumbToolkit;
        getJsPlumb():jsPlumbInstance;

        getModelPositionAttributes():[string, string];
        getLabelLocationAttribute(edge: Edge):string;

        bind(event:string, handler:Function):void;
        
        zoomToFit(params?:ZoomOptions):void;
        zoomToFitIfNecessary(params?:ZoomOptions):void;
        zoomToSelection(params?:{ fill?:number, selection?:Selection }):void;
        zoomToBackground(params?:{onComplete?:Function; onStep?:Function; doNotAnimate?:boolean}):void;

        centerOn(obj:Node | ElementRef, params?:{horizontal?:boolean, vertical?:boolean, doNotAnimate?:boolean, onComplete?:Function, onStep?:Function}):void;
        centerOnHorizontally(obj:Node | ElementRef):void;
        centerOnVertically(obj:Node | ElementRef):void;
        centerOnAndZoom(obj:Node | ElementRef, fillRatio:number):void;

        centerContent(params?:{doNotAnimate?:boolean, onComplete?:Function, onStep?:Function}):void;
        centerContentHorizontally(params?:{doNotAnimate?:boolean, onComplete?:Function, onStep?:Function}):void;
        centerContentVertically(params?:{doNotAnimate?:boolean, onComplete?:Function, onStep?:Function}):void;

        destroy():void;

        getViewportCenter():[ number, number ];
        getZoom():number;

        getBoundsInfo():SurfaceBounds;

        getApparentCanvasLocation():[number, number];
        setApparentCanvasLocation(left:number, top:number):[number, number];

        mapLocation(x:number, y:number):CanvasLocation;
        mapEventLocation(event:Event):CanvasLocation;

        pageLocation(event:Event):[number, number ];

        getPan():[number, number ];
        pan(dx:number, dy:number, animate?:boolean):void;

        setClamping(clamping: boolean): void;
        isClamping(): boolean;

        setFilter(filter:EventTargetFilter):void;
        setPan(left:number, top:number, animate?:boolean, onComplete?:()=>void, onStep?:Function):void;
        setPanAndZoom(left:number, top:number, zoom:number, doNotAnimate?:boolean):void;
        setPanFilter(filter:Selector|EventTargetFilter):void;
        setViewportCenter(center:[ number, number] ):void;
        setWheelFilter(filter:Selector):void;
        setZoom(zoom:number):number;

        relayoutGroup(group:Group):void;

        snapToGrid (el?:Node|ElementRef, x?:number, y?:number):void;

        nudgeZoom(delta:number, originalEvent?:Event):number;
        nudgeWheelZoom(delta:number, originalEvent?:Event):number;

        setZoomRange(range:ZoomRange, doNotClamp?:boolean):ZoomRange;
        getZoomRange():ZoomRange;

        setStateHandle(handle:string):void;
        getStateHandle():string;

        setLassoSelectionFilter(filter:NodeOrGroupFilter):void;

        findNearbyNodes(xy:number[], radius:number, mustBeInViewport?:boolean, filter?:(id:string, node:Node, bounds:BoundingRectangle)=>true):Array<Node>;
        findIntersectingNodes(xy:number[], wh:number[], enclosed?:boolean):Array<IntersectingObjectData>;

        isInViewport(x:number, y:number):boolean;
        getViewportCenter():[number, number ];

        positionElementAt(domEl:Selector|Element, x:number, y:number, xShift?:number, yShift?:number):void;
        positionElementAtEventLocation(domEl:Selector|Element, event:Event, xShift?:number, yShift?:number):void;
        positionElementAtPageLocation(domEl:Selector|Element, x:number, y:number, xShift?:number, yShift?:number):void;

        floatElement(domEl:Element, xy:[ number, number ]):void;
        fixElement(domEl:Element, constraints:{left?:boolean, top?:boolean}, xy:[ number, number ]):void;

        tracePath(options:PathTracingOptions):PathTransport;

        setMode(mode:SurfaceMode):void;

        createMiniview(options:MiniviewOptions):Miniview;
        getMiniview(): Miniview;

        getObjectInfo(obj:string|Element|Node|Port, elementResolver?:(obj:NodeOrGroup)=>Element):ObjectInfo;

        /**
         * Repaints the element for the given object.
         * @method repaint
         * @param {string|Port|Node|Element} obj Object to repaint, including any associated connections. This can be
         * a Toolkit Node or Port, a String (representing a Node or Node.Port id) or a DOM element.
         */
        repaint(obj:string | PortRef | NodeRef | Element ):void;
        
        repaintEverything():void;

        toggleGroup(group:string|Group):void;
        expandGroup(group:string|Group):void;
        collapseGroup(group:string|Group):void;
        autoSizeGroups():void;

        setElementsDraggable(draggable:boolean):void;

        registerDroppableNodes(params:DroppableNodesOptions):void;

        relayout(newParameters:any):void;
        setRefreshAutomatically(refreshAutomatically:boolean):void;

        /**
         * When the component is rendering a Selection (as opposed to an entire Toolkit instance), this causes the Selection to
         * reload, and the component to be cleared and everything redrawn.
         * @method reload
         */
        reload():void;

        /**
         * Incrementally update the layout, without a reset. If rendering is suspended, this method does nothing.
         * @method refresh
         */
        refresh():void;

        magnetize(params:{event?:Event, origin?:CanvasLocation, options?:any}):void;

        /**
         * Sets the current layout.
         * @method setLayout
         * @param {Object} layoutParams Parameters for the layout, including type and constructor parameters.
         * @param {Boolean} [doNotRefresh=false] Do not refresh the UI after setting the new layout.
         */
        setLayout(layoutParams:LayoutSpec, doNotRefresh?:boolean):void;

        /**
         * Applies the given layout one time to the content.
         * @method adHocLayout
         * @param {LayoutSpec} layoutParams Parameters for the layout, including type and constructor parameters.
         */
        adHocLayout(layoutParams:LayoutSpec):void;

        /**
         * Gets the underlying jsPlumb connection that was rendered for the Edge with the given id.
         * @method getRenderedConnection
         * @param {string} edgeId ID of the Edge to retrieve the Connection for.
         * @return {Connection} A jsPlumb Connection, null if not found.
         */
        getRenderedConnection(edgeId:string):Connection;

        /**
         * Gets the DOM node that was rendered for the Node with the given id.
         * @method getRenderedNode
         * @param {string} nodeId Node id for which to retrieve the rendered element.
         * @return {HTMLElement} DOM element for the given Node id, null if not found.
         */
        getRenderedNode(nodeId:string):HTMLElement;

        /**
         * Gets the DOM node that was rendered for the Group with the given id.
         * @method getRenderedGroup
         * @param {string} groupId Group id for which to retrieve the rendered element.
         * @return {HTMLElement} DOM element for the given Group id, null if not found.
         */
        getRenderedGroup(groupId:string):HTMLElement;

        /**
         * Gets the DOM node that was rendered for the Port with the given id.
         * @method getRenderedPort
         * @param {string} portId Port id for which to retrieve the rendered element. Note that you must supply the "full" id here, that is in dotted
         * notation with the id of the Node on which the port resides.
         * @return {HTMLElement} DOM element for the given Port id, null if not found.
         */
        getRenderedPort(portId:string):HTMLElement;

        /**
         * Gets the DOM node that was rendered for the given Node/Port/Group.
         * @method getRenderedElement
         * @param {AbstractEdgeTerminus} obj Node, Port or Group for which to retrieve the rendered element.
         * @return {HTMLElement} DOM element for the given Node/Port/Group, null if not found.
         */
        getRenderedElement(obj:AbstractEdgeTerminus):HTMLElement;

        /**
         * Gets the Endpoint that was rendered for the given Node/Port/Group
         * @method getRenderedEndpoint
         * @param {AbstractEdgeTerminus} obj Node, Port or Group for which to retrieve the rendered endpoint.
         * @return {Endpoint} Endpoint for the given Node/Port/Group, null if not found.
         */
        getRenderedEndpoint(obj:AbstractEdgeTerminus):Endpoint;

        getContainer():HTMLElement;

        /**
         * Activates the UI state with the given ID on the objects contained in the given target. If target is not supplied, the state is
         * activated against the entire dataset.
         * @method activateState
         * @param {string} stateId ID of the state to activate. States are defined inside a `states` member of your `view` definition.
         * @param {Selection|Path|jsPlumbToolkitInstance|Element} [target] Set of objects to activate the state on. If null, the entire dataset (Nodes, Edges and Ports) is used. If you provide an Element here, a Selection is created that consists of the Node representing the element, plus all Edges to and from the given Node.
         */
        activateState(stateId:string, target:Selection|Path|jsPlumbToolkit|HTMLElement):void;

        /**
         * Deactivates the UI state with the given ID on the objects contained in the given target. If target is not supplied, the state is
         * deactivated against the entire dataset.
         * @method deactivateState
         * @param {String} stateId ID of the state to deactivate. States are defined inside a `states` member of your `view` definition.
         * @param {Selection|Path|jsPlumbToolkitInstance} [target] Set of objects to deactivate the state on. If null, the entire dataset (Nodes, Edges and Ports) is used.
         */
        deactivateState(stateId:string, target:Selection|Path|jsPlumbToolkit|HTMLElement):void;

        /**
         * Resets (clears) the UI state of all objects in the current dataset.
         * @method resetState
         */
        resetState():void;

        /**
         * Wraps the underlying Toolkit's `batch` function with the added step of first suspending events being
         * fired from this renderer.
         * @method batch
         * @param fn Function to run while rendering and events are both suspended.
         */
        batch(fn:Function):void;

        /**
         * Gets a Path from some source Node/Port to some target Node/Port. This method is a wrapper around the
         * Toolkit's `getPath` method, adding a `setVisible` function to the result.
         * @method getPath
         * @param {Object} params Path spec params
         * @param {Node|Port|string} params.source Source node or port, or id of source node/port
         * @param {Node|Port|string} params.target Target node or port, or id of target node/port
         * @param {Boolean} [params.strict=true] Sets whether or not paths are searched strictly by the given source/target. If, for instance, you supply a node as the source, but there are only edges connected to ports on that node, by default these edges will be ignored. Switching `strict` to false will mean these edges are considered.
         * @param {Function} [params.nodeFilter] Optional function that is given each Node's backing data and asked to return true or false - true means include the Node, false means exclude it.
         * @param {Function} [params.edgeFilter] Optional function that is given each Edge's backing data and asked to return true or false - true means include the Edge, false means exclude it.
         * @return {UIPath} a UIPath object. Even if no path exists you will get a return value - but it will just be empty.
         */
        getPath(params:PathRetrievalOptions):UIPath;

        /**
         * Gets the position of an element that is being managed by the Surface.
         * @method getPosition
         * @param {string|Element|Selector|Node} el Element id, element, selector or Node to get position for.
         * @return {Number[]|Null} [left,top] position array if element found, otherwise null.
         */
        getPosition(el:string|Element|Selector|Node):[ number, number ];

        /**
         * Gets the size of an element that is being managed by the Surface.
         * @method getSize
         * @param {string|Element|Selector|Node} el Element id, element, selector or Node to get position for.
         * @return {Number[]|Null} [width, height] Array if element found, otherwise null.
         */
        getSize(el:string|Element|Selector|Node):[ number, number ];

        /**
         * Gets the origin and size of an element that is being managed by the Surface.
         * @method getCoordinates
         * @param {String|Element|Selector|Node} el Element id, element, selector or Node to get position for.
         * @return {Object} {x:.., y:..., w:..., h:...} if element found, otherwise null.
         */
        getCoordinates(el:string|Element|Selector|Node):[ number, number ];

        /**
         * Writes the current left/top for each node into the data model. A common use case is to run an auto layout the first time
         * some dataset is seen, and then to save the locations of all the nodes once a human being has moved things around.
         * @method storePositionsInModel
         * @param {Object} params Parameters
         * @param {string} [params.leftAttribute] Name of the attribute to use for the left position. Default is 'left'
         * @param {string} [params.topAttribute] Name of the attribute to use for the top position. Default is 'top'
         */
        storePositionsInModel(params?:{leftAttribute:string, topAttribute:string}):void;

        /**
         * Writes the current left/top for some Node or Group into the data model. A common use case is to run an auto layout the first time
         * some dataset is seen, and then to save the locations of all the Nodes/Groups once a human being has moved things around. Note that this method
         * takes either a String, representing the Node or Group's ID, and uses the default values for left/top attribute names, or an Object, in which
         * you provide the id and the left/top attribute names.
         * @method storePositionInModel
         * @param {string} id ID of the Node or Group for which to store the position. Either supply this, or an object containing id and values for the left/top attribute names.
         * @param {Object} params Parameters. An object containing id and values for the left/top attribute names. Supply this or just supply the node id as a string.
         * @param {string} params.id Node or Group id
         * @param {boolean} [params.group=false] If true, the ID given is for a Group, not a Node.
         * @param {string} [params.leftAttribute] Name of the attribute to use for the left position. Default is 'left'.
         * @param {string} [params.topAttribute] Name of the attribute to use for the top position. Default is 'top'.
         * @return {number[]} The current position as [left, top].
         */
        storePositionInModel(idOrParams:string | {id:string, group?:boolean, leftAttribute?:string, topAttribute?:string}):[number, number];

        /**
         * Sets the position of the given Node or Group, storing the position in the model if the Surface is setup to do that automatically.
         * @method setPosition
         * @param {string|Node|Element} node Either a Node/Group id, a DOM element representing a Node/Group, or a Node/Group.
         * @param {number} x left position for the element.
         * @param {number} y top position for the element.
         */
        setPosition(node:string|Node|Group|Element, x:number, y:number):ObjectInfo;

        /**
         * Sets the position of the given Node or Group and magnetizes afterwards to push away anything that it is overlapping
         * @method setMagnetizedPosition
         * @param {string|Node|Element} node Either a Node/Group id, a DOM element representing a Node/Group, or a Node/Group.
         * @param {number} x left position for the element.
         * @param {number} y top position for the element.
         */
        setMagnetizedPosition(node:string|Node|Group|Element, x:number, y:number):ObjectInfo;

        /**
         * Sets the position of the given Node/Group, animating the element to that position.
         * @method animateToPosition
         * @param {string|Node|Element} node Either a Node/Group id, a DOM element representing a Node/Group, or a Node/Group.
         * @param {number} x left position for the element.
         * @param {number} y top position for the element.
         * @param {Object} [animateOptions] Options for the animation.
         */
        animateToPosition(node:string|Node|Element, x:number, y:number, animateOptions?:any):void;

        /**
         * Checks the visibility of a node, edge, port.
         * @method isVisible
         * @param obj:Node|Edge|Port
         */
        isVisible(obj:Node|Edge|Port):boolean;

        /**
         * Sets the visibility of some Node/Port or Edge.
         * @method setVisible
         * @param {Selection|Path|Edge|Node|Port|String|Node[]|Port[]|Edge[]|String[]} obj An Edge, Port, Node or - in the case of String - a  Node/Port id.
         * @param {boolean} state Whether the object should be visible or not.
         * @param {boolean} [doNotCascade=false] If true, the method does not cascade visibility changes down from a Node to its connected Edges, or from an Edge to its Ports. The default is for this to happen.
         */
        setVisible(obj:Selection|Path|Edge|Node|Port|string|Node[]|Port[]|Edge[]|string[], state:boolean, doNotCascade?:boolean):void;

        /**
         * Add the given Node to the posse with the given name
         * @method addToPosse
         * @param {Element|string|Node} obj A DOM element representing a Node, or a Node id, or a Node.
         * @param {string} posseId ID of the posse to add the Node to.
         * @param {boolean} [active=true] If true (which is the default), the Node causes all other Nodes in the Posse
         * to be dragged. If false, this Node drags independently but is dragged whenever an _active_ member of the Posse
         * is dragged,
         */
        addToPosse(obj:string|Node|Element, posseId:string, active?:boolean):void;

        /**
         * Sets the posse(s) for the element with the given id, creating those that do not yet exist, and removing from
         * the element any current Posses that are not specified by this method call. This method will not change the
         * active/passive state if it is given a posse in which the element is already a member.
         * @method setPosse
         * @param {Element|string|Node} obj A DOM element representing a Node, or a Node id, or a Node.
         * @param {string...|Object...} spec Variable args parameters. Each argument can be a either a String, indicating
         * the ID of a Posse to which the element should be added as an active participant, or an Object containing
         * `{ id:"posseId", active:false/true}`. In the latter case, if `active` is not provided it is assumed to be
         * true.
         */
        setPosse(obj:string|Node|Element, ...spec:Array<string|{posseId:string, activeInPosse:boolean}>):void;

        /**
         * Remove the given Node from the given Posse.
         * @method removeFromPosse
         * @param {Element|string|Node} obj A DOM element representing a Node, or a Node id, or a Node.
         * @param {string} posseId ID of the posse from which to remove the Node from.
         */
        removeFromPosse(obj:string|Node|Element, posseId:string):void;

        /**
         * Remove the given Node from all Posses to which it belongs.
         * @method removeFromAllPosses
         * @param {Element|String|Node} obj A DOM element representing a Node, or a Node id, or a Node.
         */
        removeFromAllPosses(obj:string|Node|Element):void;

        /**
         * Changes the participation state for the given Node in the Posse with the given ID.
         * @param {Element|String|Node} obj A DOM element, node ID or Node to change state for.
         * @param {String} posseId ID of the Posse to change element state for.
         * @param {Boolean} active True to make active, false to make passive.
         */
        setPosseState(obj:string|Node|Element, posseId:string, active:boolean):void;

        /**
         * Sets whether or not a given Node or Port is currently enabled as a connection target in the UI.
         * @method setTargetEnabled
         * @param {string|Node|Port|Element} obj Node/Port or Node/Port ID, or a DOM element to disable as a connection target.
         * @param {boolean} enabled true if enabled, false if not.
         */
        setTargetEnabled(obj:string|Node|Port|Element, enabled:boolean):void;
        /**
         * Sets whether or not a given Node or Port is currently enabled as a connection source in the UI.
         * @method setSourceEnabled
         * @param {string|Node|Port|Element} obj Node/Port or Node/Port ID, or a DOM element to disable as a connection source.
         * @param {boolean} enabled true if enabled, false if not.
         */
        setSourceEnabled(obj:string|Node|Port|Element, enabled:boolean):void;
        /**
         * Sets whether or not a given Node or Port is currently enabled as a connection target and source in the UI.
         * @method setEnabled
         * @param {String|Node|Port|Element} obj Node/Port or Node/Port ID, or a DOM element to disable as both a connection target and source.
         * @param {boolean} enabled true if enabled, false if not.
         */
        setEnabled(obj:string|Node|Port|Element, enabled:boolean):void;

        asynchronousPortRendered(el:Element, nodeOrGroup:Node|Group, portData:any):Port;
        addUnrenderedEdge(edge:Edge, connectFunction:Function):void;

        /**
         * Registers a custom tag on the Surface.
         * @param tagName
         * @param options
         * @param isGlobal
         */
        registerTag(tagName:string, options:CustomTagOptions, isGlobal?:boolean):void;

    }   

    class Miniview {
        invalidate(id?:string):void;
    }

    class DrawingTools {
        constructor(options:{
            renderer:Surface;
            widthAttribute?:string; // "w"
            heightAttribute?:string// "h"
            leftAttribute?:string; // "left"
            topAttribute?:string; // "top"
        })
    }

    interface PaintStyle {
        stroke?: string;
        fill?: string;
        strokeWidth?: number;
        outlineWidth?:number;
        outlineStroke?:string;
    }

    module jsPlumb {
        function extend(target: Object, source: Object): any;

        function addClass(el: HTMLElement | NodeListOf<HTMLElement>, clazz: string): void;

        function removeClass(el: HTMLElement | NodeListOf<HTMLElement>, clazz: string): void;

        function toggleClass(el: HTMLElement | NodeListOf<HTMLElement>, clazz: string): void;

        function on(el: any, event: string, delegateSelector: string, handler: Function): void;
        function on(el: any, event: string, handler: Function): void;

        function off(el: any, event: string, handler: Function): void;

        function revalidate(el: Element): void;

        function getInstance(_defaults?: Defaults): jsPlumbInstance;

        function getSize(elId:string):[number, number];

        module Overlays {

        }
    }

    module jsPlumbUtil {
        function isArray(obj:any):boolean;
        function isNumber(obj:any):boolean;
        function isString(obj:any):boolean;
        function isBoolean(obj:any):boolean;
        function isNull(obj:any):boolean;
        function isObject(obj:any):boolean;
        function isDate(obj:any):boolean;
        function isFunction(obj:any):boolean;
        function isNamedFunction(obj:any):boolean;
        function isEmpty(obj:any):boolean;
        function extend(target: Object, source: Object): any;
        function uuid():UUID;
        function findWithFunction(list:Array<any>, fn:(obj:any)=>boolean):number;
        function addWithFunction(list:Array<any>, item:any, fn:(obj:any)=>boolean):void;
        function removeWithFunction(list:Array<any>, fn:(obj:any)=>boolean):number;
        function suggest(list:Array<any>, item:any, insertAtHead?:boolean):boolean;
        function fastTrim(s:string):string;
        function each(list:Array<any>, fn:(obj:any)=>any):void;

        function consume(e: Event):void;

        function fastTrim(s:string):string;
        function log(msg:string):void;
        function map(l:Array<any>, fn:(i:any)=>any):Array<any>;

        function ajax(params:any):void;

        type SelectionOptions = {
            id?:string,
            generator?:Function,
            toolkit:jsPlumbToolkit,
            onClear?:Function
        }

        class Selection {
            constructor(params:SelectionOptions);
            remove(obj:any):void;
            append(obj:any):void;
            toggle(obj:any):void;
        }

        class EventGenerator {
            bind(evt: string, fn:(params: any)=>void):void;
        }

    }

    module Biltong {
        function intersects(r1:BoundingRectangle, r2:BoundingRectangle):boolean;
    }


    type Selector = string;
    type UUID = string;
    type ElementId = string;
    type ElementRef = ElementId | Element;
    type ElementGroupRef = ElementId | Element | Array<ElementId> | Array<Element>;
    type ConnectionId = string;

    class jsPlumbInstance {

        getId(el:Element):string;

        getSize(elId:string|Element):[number, number];

        getOffset(el:string|Element, relativeToRoot?:boolean, container?:Element):{left:number, top:number};

        addClass(el: HTMLElement | NodeListOf<HTMLElement>, clazz: string): void;

        removeClass(el: HTMLElement | NodeListOf<HTMLElement>, clazz: string): void;

        addEndpoint(el: ElementGroupRef, params?: EndpointOptions, referenceParams?: EndpointOptions): Endpoint | Array<Endpoint>;

        addEndpoints(target: ElementGroupRef, endpoints: Array<EndpointOptions>, referenceParams?: EndpointOptions): Array<Endpoint>;

        animate(el: ElementRef, properties?: Object, options?: Object): void;

        batch(fn: Function, doNotRepaintAfterwards?: boolean/* =false */): void;

        bind(event: "connection", callback: (info: ConnectionMadeEventInfo, originalEvent: Event) => void, insertAtStart?: boolean/* =false */): void;
        bind(event: "click", callback: (info: Connection, originalEvent: Event) => void, insertAtStart?: boolean/* =false */): void;
        bind(event: string, callback: (info: OnConnectionBindInfo, originalEvent: Event) => void, insertAtStart?: boolean/* =false */): void;

        cleanupListeners(): void;

        connect(params: ConnectParams, referenceParams?: Object): Connection;

        deleteEndpoint(object: UUID | Endpoint, doNotRepaintAfterwards?: boolean/* =false */): jsPlumbInstance;

        deleteEveryEndpoint(): jsPlumbInstance;

        deleteConnection(conn: Connection): void;

        doWhileSuspended(): jsPlumbInstance;

        draggable(el: Object, options?: DragOptions): jsPlumbInstance;
        destroyDraggable(el:any):void;

        empty(el: string | Element | Selector): void;

        fire(event: string, value: Object, originalEvent: Event): void;

        getAllConnections(): Object;

        getConnections(scope: string, options: Object, scope2?: string | string, source?: string | string | Selector, target?: string | string | Selector, flat?: boolean/* =false */): Array<any> | Map<any, any>;

        getContainer(): Element;

        getDefaultScope(): string;

        getEndpoint(uuid: string): Endpoint;

        getScope(Element: Element | string): string;

        getSelector(context?: Element | Selector, spec?: string): void;

        getSourceScope(Element: Element | string): string;

        getTargetScope(Element: Element | string): string;

        getType(id: string, typeDescriptor: string): Object;

        hide(el: string | Element | Selector, changeEndpoints?: boolean/* =false */): jsPlumbInstance;

        importDefaults(defaults: Object): jsPlumbInstance;

        isHoverSuspended(): boolean;

        isSource(el: string | Element | Selector): boolean;

        isSourceEnabled(el: string | Element | Selector, connectionType?: string): boolean;

        isSuspendDrawing(): boolean;

        isSuspendEvents(): boolean;

        isTarget(el: string | Element | Selector): boolean;

        isTargetEnabled(el: string | Element | Selector): boolean;

        makeSource(el: string | Element | Selector, params: Object, endpoint?: string | Array<any>, parent?: string | Element, scope?: string, dragOptions?: Object, deleteEndpointsOnEmpty?: boolean/* =false */, filter?: Function): void;

        makeTarget(el: string | Element | Selector, params: Object, endpoint?: string | Array<any>, scope?: string, dropOptions?: Object, deleteEndpointsOnEmpty?: boolean/* =true */, maxConnections?: number/* =-1 */, onMaxConnections?: Function): void;

        off(el: Element | Element | string, event: string, fn: Function): jsPlumbInstance;

        on(el: Element | Element | string, childrenOrEvent?: string, eventOrHandler?: string|Function, handler?: Function): jsPlumbInstance;

        ready(fn: Function): void;

        recalculateOffsets(el: string | Element | Selector): void;

        registerConnectionType(typeId: string, type: Object): void;

        registerConnectionTypes(types: Object): void;

        registerEndpointType(typeId: string, type: Object): void;

        registerEndpointTypes(types: Object): void;

        remove(el: string | Element | Selector): void;
        removeElement(el: string | Element | Selector): void;

        removeAllEndpoints(el: string | Element | Selector, recurse?: boolean/* =false */): jsPlumbInstance;

        repaint(el: string | Element | Selector): jsPlumbInstance;

        repaintEverything(clearEdits?: boolean/* =false */): jsPlumbInstance;

        reset(): void;

        restoreDefaults(): jsPlumbInstance;

        revalidate(el: string | Element | Selector): void;

        select(params?: Object, scope?: string | string, source?: string | string, target?: string | string, connections?: Connection[]): { each(fn: (conn: Connection) => void): void };

        getHoverPaintStyle(params?: Object, scope?: string | string/* =jsPlumb.DefaultScope */, source?: string | Element | Selector | Array<any>, target?: string | Element | Selector | Array<any>, element?: string | Element | Selector | Array<any>): Selection;

        setContainer(el: string | Element | Selector): void;

        setHover(container: string | Element | Selector): void;

        setDefaultScope(scope: string): jsPlumbInstance;

        setDraggable(el: string | Object | Array<any>, draggable: boolean): void;

        setHoverSuspended(hover: boolean): void;

        setIdChanged(oldId: string, newId: string): void;

        setParent(el: Selector | Element, newParent: Selector | Element | string): void;

        setScope(el: Element | string, scope: string): void;

        setSource(connection: Connection, source: string | Element | Endpoint, doNotRepaint?: boolean/* =false */): jsPlumbInstance;

        setSourceEnabled(el: string | Element | Selector, state: boolean): jsPlumbInstance;

        setSourceScope(el: Element | string, scope: string, connectionType?: string): void;

        setSuspendDrawing(val: boolean, repaintAfterwards?: boolean/* =false */): boolean;

        setSuspendEvents(val: boolean): void;

        setTarget(connection: Connection, target: string | Element | Endpoint, doNotRepaint?: boolean/* =false */): jsPlumbInstance;

        setTargetEnabled(el: string | Element | Selector, state: boolean): jsPlumbInstance;

        setTargetScope(el: Element | string, scope: string, connectionType?: string): void;

        show(el: string | Element | Selector, changeEndpoints?: boolean/* =false */): jsPlumbInstance;

        toggleDraggable(el: string | Element | Selector): boolean;

        toggleSourceEnabled(el: string | Element | Selector): boolean;

        toggleTargetEnabled(el: string | Element | Selector): boolean;

        toggleVisible(el: string | Element | Selector, changeEndpoints?: boolean/* =false */): void;

        unbind(eventOrListener?: string | Function, listener?: Function): void;

        unmakeEverySource(): jsPlumbInstance;

        unmakeEveryTarget(): jsPlumbInstance;

        unmakeSource(el: string | Element | Selector): jsPlumbInstance;

        unmakeTarget(el: string | Element | Selector): jsPlumbInstance;
    }

    interface ConnectionMadeEventInfo {
        connection: Connection;
        source: HTMLDivElement;
        sourceEndpoint: Endpoint;
        sourceId: string;
        target: HTMLDivElement;
        targetEndpoint: Endpoint;
        targetId: string;
    }

    interface OnConnectionBindInfo {
        connection: Connection;// the new Connection.you can register listeners on this etc.
        sourceId: string;// - id of the source element in the Connection
        originalSourceId: string;
        newSourceId: string;
        targetId: string;// - id of the target element in the Connection
        originalTargetId: string;
        newTargetId: string;
        source: Element;// - the source element in the Connection
        target: Element;//- the target element in the Connection
        sourceEndpoint: Endpoint;//- the source Endpoint in the Connection
        newSourceEndpoint: Endpoint;
        targetEndpoint: Endpoint;//- the targetEndpoint in the Connection
        newTargetEndpoint: Endpoint;
    }

    interface Defaults {
        Endpoint?: EndpointSpec;
        Endpoints?: [ EndpointSpec, EndpointSpec ];
        Anchor?: AnchorSpec;
        Anchors?: [ AnchorSpec, AnchorSpec ];
        PaintStyle?: PaintStyle;
        HoverPaintStyle?: PaintStyle;
        ConnectionsDetachable?: boolean;
        ReattachConnections?: boolean;
        ConnectionOverlays?: Array<OverlaySpec>;
        Container?: any; // string(selector or id) or element
        DragOptions?: DragOptions;
        Connector?:ConnectorSpec;
    }

    interface Connections {
        detach(): void;
        length: number;
        each(e: (c: Connection) => void): void;
    }

    interface ConnectParams {
        uuids?: [UUID, UUID];
        source?: ElementRef | Endpoint;
        target?: ElementRef | Endpoint;
        detachable?: boolean;
        deleteEndpointsOnDetach?: boolean;
        endpoint?: EndpointSpec;
        anchor?: AnchorSpec;
        anchors?: [AnchorSpec, AnchorSpec];
        label?: string;
    }

    interface DragEventCallbackOptions {
        drag: KatavorioDrag; // The associated Drag instance
        e: MouseEvent;
        el: HTMLElement; // element being dragged
        pos: [number, number]; // x,y location of the element. drag event only.
    }

    interface KatavorioDrag {
        size:[number, number];
        el:HTMLElement;
        getDragElement:(retrieveOriginalElement?:boolean) => HTMLElement;
    }

    interface DragOptions {
        containment?: string;
        start?: (params:DragEventCallbackOptions) => void;
        drag?: (params:DragEventCallbackOptions) => void;
        stop?: (params:DragEventCallbackOptions) => void;
        cursor?: string;
        zIndex?: number;
        filter?:string;
    }

    interface DropOptions {
        hoverClass: string;
    }

    // interface SourceOptions {
    //     parent: string;
    //     endpoint?: string;
    //     anchor?: string;
    //     connector?: any[];
    //     connectorStyle?: PaintStyle;
    // }
    //
    // interface TargetOptions {
    //     isTarget?: boolean;
    //     maxConnections?: number;
    //     uniqueEndpoint?: boolean;
    //     deleteEndpointsOnDetach?: boolean;
    //     endpoint?: string;
    //     dropOptions?: DropOptions;
    //     anchor?: any;
    // }


    // interface SelectParams {
    //     scope?: string;
    //     source: string;
    //     target: string;
    // }

    interface Connection {
        id: ConnectionId;
        setDetachable(detachable: boolean): void;
        setParameter(name: string, value: any): void;
        endpoints: [Endpoint, Endpoint];
        getOverlay(s: string): Overlay;
        showOverlay(s: string): void;
        hideOverlay(s: string): void;
        setLabel(s: string): void;
        getElement(): Connection;
        getConnector():Connector;
        source:Element;
        target:Element;
        sourceId:string;
        targetId:string;
        repaint():void;

        updateConnectedClass():void;

        paint(params:any):void;
    }

    interface Connector {
        editor:ConnectorEditor;
        isEditable():boolean;
        type:string;
        setAnchorOrientation(index:number, orientation:number[]):void;
        clearEdits():void;
        canvas:any;
        findSegmentForPoint(x:number, y:number):{
            d:number,
            l:number,
            x:number,
            y:number,
            s:number,
            x1:number,
            y1:number,
            x2:number,
            y2:number,
            index:number
        };
        boundingBoxIntersection(box:BoundingRectangle):Array<[number, number]>;
        lineIntersection(x1:number, y1:number, x2:number, y2:number):Array<[number, number]>;
        boxIntersection(x:number, y:number, w:number, h:number):Array<[number, number]>;
    }

    interface ConnectorEditor {
        cleanup():void;
        update():void;
        reset():void;
        activate(surface:Surface, connection:Connection, params?:any):void;
        deactivate(e?:Event):void;
        isActive():boolean;
    }


    /* -------------------------------------------- CONNECTORS ---------------------------------------------------- */

    interface ConnectorOptions {
    }
    type UserDefinedConnectorId = string;
    type ConnectorId = "Bezier" | "StateMachine" | "Flowchart" | "Straight" | UserDefinedConnectorId;
    type ConnectorSpec = ConnectorId | [ConnectorId, ConnectorOptions];


    /* -------------------------------------------- ENDPOINTS ------------------------------------------------------ */

    type EndpointId = "Rectangle" | "Dot" | "Blank" | UserDefinedEndpointId;
    type UserDefinedEndpointId = string;
    type EndpointSpec = EndpointId | [EndpointId, EndpointOptions];

    interface EndpointOptions {
        anchor?: AnchorSpec;
        endpoint?: Endpoint;
        enabled?: boolean;//= true
        paintStyle?: PaintStyle;
        hoverPaintStyle?: PaintStyle;
        cssClass?: string;
        hoverClass?: string;
        maxConnections?: number;//= 1?
        dragOptions?: DragOptions;
        dropOptions?: DropOptions;
        connectorStyle?: PaintStyle;
        connectorHoverStyle?: PaintStyle;
        connector?: ConnectorSpec;
        connectorOverlays?: Array<OverlaySpec>;
        connectorClass?: string;
        connectorHoverClass?: string;
        connectionsDetachable?: boolean;//= true
        isSource?: boolean;//= false
        isTarget?: boolean;//= false
        reattach?: boolean;//= false
        parameters?: object;
        "connector-pointer-events"?: string;
        connectionType?: string;
        dragProxy?: string | Array<string>;
        id?: string;
        scope?: string;
        reattachConnections?: boolean;
        type?: string; // "Dot", etc.
        radius?:number;
    }

    class Endpoint {
        anchor: Anchor;
        connections?: Array<Connection>;
        maxConnections: number;//= 1?
        id: string;
        scope: string;
        type: EndpointId;

        setEndpoint(spec: EndpointSpec): void;

        connectorSelector(): Connection;

        isEnabled(): boolean;

        setEnabled(enabled: boolean): void;

        setHover(hover: boolean): void;

        getElement(): Element;

        setElement(el: Element): void;
        paint(params:any):void;

        readonly elementId:string;
        readonly canvas:Element;
        _continuousAnchorEdge:string;
    }

    /* -------------------------------------------- ANCHORS -------------------------------------------------------- */

    interface AnchorOptions {
    }

    type AnchorOrientationHint = -1 | 0 | 1;

    interface Anchor {
        type: AnchorId;
        cssClass: string;
        elementId: string;
        id: string;
        locked: boolean;
        offsets: [number, number];
        orientation: [AnchorOrientationHint, AnchorOrientationHint];
        x: number;
        y: number;
        isContinuous:boolean;
        isDynamic:boolean;
        isEdgeSupported(edge:string):boolean;
        getCurrentLocation(params:any):Array<number>;
        lock():void;
        unlock():void;
    }

    interface DynamicAnchor extends Anchor {
        locked:boolean;
        getAnchors():Array<Anchor>;
        setAnchor(anchor:Anchor):void;
        setAnchorCoordinates(coords:[number, number, AnchorOrientationHint, AnchorOrientationHint]):boolean;
    }

    type AnchorFace = "left" | "right" | "top" | "bottom";
    type AnchorLocation = [ number, number, number, number ];

    interface ContinuousAnchor extends Anchor {
        setCurrentFace(face:AnchorFace, overrideLock?:boolean):void;
        getCurrentFace():AnchorFace;
        getSupportedFaces():Array<AnchorFace>;
        getDefaultFace():AnchorFace;
    }

    type AnchorId =
        "Assign" |
        "AutoDefault" |
        "Bottom" |
        "BottomCenter" |
        "BottomLeft" |
        "BottomRight" |
        "Center" |
        "Continuous" |
        "ContinuousBottom" |
        "ContinuousLeft" |
        "ContinuousRight" |
        "ContinuousTop" |
        "Left" |
        "LeftMiddle" |
        "Perimeter" |
        "Right" |
        "RightMiddle" |
        "Top" |
        "TopCenter" |
        "TopLeft" |
        "TopRight";


    type AnchorSpec = AnchorId | [AnchorId, AnchorOptions]


    /* --------------------------------------- OVERLAYS ------------------------------------------------------------- */

    interface OverlayOptions {
    }

    interface ArrowOverlayOptions extends OverlayOptions {
        width?: number; // 20
        length?: number; // 20
        location?: number; // 0.5
        direction?: number; // 1
        foldback?: number; // 0.623
        paintStyle?: PaintStyle;
    }

    interface LabelOverlayOptions extends OverlayOptions {
        label: string;
        cssClass?: string;
        location?: number; // 0.5
        labelStyle?: {
            font?: string;
            color?: string;
            fill?: string;
            borderStyle?: string;
            borderWidth?: number;// integer
            padding?: number; //integer
        };
    }

    type OverlayId = "Label" | "Arrow" | "PlainArrow" | "Custom";

    type OverlaySpec = OverlayId | [OverlayId, OverlayOptions];

    interface Overlay { }

}

export = jsPlumbToolkit

