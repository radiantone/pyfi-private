;(function() {

    var CONTAINER_ID = "jtk-test-support-container";

    var getContainer = function() {
        var c = document.getElementById(CONTAINER_ID);
        if (c == null) {
            c = document.createElement("div");
            c.id = CONTAINER_ID;
            document.body.appendChild(c);
        }
        return c;
    };

    var _divs = [],  _toolkits = [],
    _addDiv = function (id, parent, className, styles) {
        var d1 = document.createElement("div");
        d1.style.position = "absolute";
        if (parent) parent.appendChild(d1); else getContainer().appendChild(d1);
        d1.setAttribute("id", id);
        if (className) d1.className = className;
        d1.style.left = (Math.floor(Math.random() * 1000)) + "px";
        d1.style.top = (Math.floor(Math.random() * 1000)) + "px";
        _divs.push({id: id, el: d1});

        styles = styles || {};
        for (var s in styles) {
            d1.style[s] = styles[s];
        }

        return d1;
    },
    _addDivs = function (ids, parent) {
        for (var i = 0; i < ids.length; i++)
            _addDiv(ids[i], parent);
    },
    _remove = function(n) {
        n = n.length == undefined && typeof n !== "string" ? [ n ] : n;
        for (var i = 0; i < n.length; i++) {
            var _n = typeof n[i] == "string" ? document.getElementById(n[i]) : n[i];
            _n.parentNode && _n.parentNode.removeChild(_n);
        }
    },
    _removeBySelector = function(s) {
        _remove(document.querySelectorAll(s));
    },
    _cleanup = function() {
    	for (var i=0; i < _divs.length; i++) {
            _divs[i].el.parentNode.removeChild(_divs[i].el);
    	}
    	_divs.length = 0;
    	
    	_removeBySelector("circle");
        _removeBySelector(".jtk-node");
        _removeBySelector(".jtk-surface-canvas");
        _removeBySelector("svg");
        _removeBySelector(".jtk-lasso");

        getContainer().innerHTML = '';
    },
    /**
     * Tests that the two values are no further than `amount` apart.
     * @param v1 First value to compare
     * @param v2 Second value to compare
     * @param amount Optional, defaults to 0.0005.
     * @returns {boolean}
     */
    delta = function (v1, v2, amount) {
        v1 = typeof v1 == "string" ? parseFloat(v1.substring(0, v1.length - 2)) : v1;
        v2 = typeof v2 == "string" ? parseFloat(v2.substring(0, v2.length - 2)) : v2;
        return Math.abs(v2 - v1) < (amount || 0.0005);
    };

    /**
     * Make an event for the given element. Events use page coordinates so we just use the getBoundingClientRect()
     * method on the given element. The event is positioned on the center of the given element.
     * @param surface
     * @param el
     * @returns {{clientY: *, clientX: *, pageY: *, screenX: *, pageX: *, screenY: *}}
     * @private
     */
    var _makeEvt = function (surface, el) {
        var o = el.getBoundingClientRect(),
            s = surface.getJsPlumb().getSize(el),
                l = o.x + (s[0] / 2),
                t = o.y + (s[1] / 2);


        return _evt(l, t);
    };

    /**
     * Transpose the given event by dx + dy
     * @param evt event to transpose
     * @param dx amount to shift in x axis
     * @param dy amount to shift in y axis
     * @returns {{clientY: *, clientX: *, pageY: *, screenX: *, pageX: *, screenY: *}}
     * @private
     */
    var _transposeEvent = function(evt, dx, dy) {
        return {
            clientX: evt.clientX + dx,
            clientY: evt.clientY + dy,
            screenX: evt.screenX + dx,
            screenY: evt.screenY + dy,
            pageX: evt.pageX + dx,
            pageY: evt.pageY + dy
        };
    };

    var _distantPointEvent = {
        clientX: 50000,
        clientY: 50000,
        screenX: 50000,
        screenY: 50000,
        pageX: 50000,
        pageY: 50000
    };

    var _randomEvent = function() {
        var x = parseInt(Math.random() * 2000), y = parseInt(Math.random() * 2000);
        return _evt(x,y);
    };

    var _dragAnElementAround = function(surface, el) {
        var _jsPlumb = surface.getJsPlumb();
        _jsPlumb.trigger(el, "mousedown", _makeEvt(surface, el));
        var steps = Math.random() * 50;
        for (var i = 0; i < steps; i++) {
            var evt = _randomEvent();
            el.style.left = evt.screenX + "px";
            el.style.top= evt.screenY + "px";
            _jsPlumb.trigger(document, "mousemove", evt);
        }
        _jsPlumb.trigger(document, "mouseup", _distantPointEvent);
    };

    var _makeARenderer = function(toolkit, renderParams, containerParams) {
        var s = _addDiv("div");
        s.style.position = "absolute";
        s.style.left = "0px";
        s.style.top = "0px";
        s.style.width = (containerParams && containerParams.width ? containerParams.width : 500) + "px";
        s.style.height = (containerParams && containerParams.height ? containerParams.height : 500) + "px";

        var p = jsPlumb.extend({container: s}, renderParams);
        var surface = toolkit.render(p);

        return { surface: surface, container: s, jsplumb:surface.getJsPlumb() };
    };

    var _makeAToolkit = function(toolkitParams, renderParams, containerParams) {

        var toolkit = jsPlumbToolkit.newInstance(toolkitParams), surface, s, jsplumb;

        if (renderParams != null) {

            var renderer = _makeARenderer(toolkit, renderParams, containerParams);
            s = renderer.container;
            surface = renderer.surface;
            jsplumb = renderer.jsplumb;
        }

        var out = {toolkit:toolkit, surface:surface, container:s, jsplumb:jsplumb};

        _toolkits.push(out);
        return out;
    };

    var _clickOnEdge = function(b, edgeId) {
        var c = b.surface.getRenderedConnection(edgeId);
        var e = _makeEvt(b.surface, c.canvas);
        b.jsplumb.trigger(c.canvas.querySelector("path"), "click", e);
    };

    var _clickOnNode = function(b, nodeId) {
        var node = b.toolkit.getNode(nodeId);
        var n = b.surface.getRenderedElement(node);
        var e = _makeEvt(b.surface, n);
        b.jsplumb.trigger(n, "click", e);
    };

    var _clickOnElementInsideNode = function(b, nodeId, selector) {
        var node = b.toolkit.getNode(nodeId);
        var n = b.surface.getRenderedElement(node);
        var el = n.querySelector(selector);
        if (!el) {
            throw new Error("could not find element inside node with selector [" + selector  + "]")
        }
        var e = _makeEvt(b.surface, el);
        b.jsplumb.trigger(n, "click", e);
    };

    var _clickOnOverlay = function(b, edgeId, overlayId) {
        var c = b.surface.getRenderedConnection(edgeId);
        var l = c.getOverlay(overlayId || "lbl");
        var e2 = _makeEvt(b.surface, l.canvas);
        b.jsplumb.trigger(l.canvas, "click", e2);
    };

    var _clickOnPort = function(b, nodeId, portId) {
        var node = b.toolkit.getNode(nodeId);
        var port = node.getPort(portId);
        if (port) {
            var n = b.surface.getRenderedEndpoint(port) || b.surface.getRenderedElement(port);
            var e = _makeEvt(b.surface, n.canvas || n);
            b.jsplumb.trigger(n.canvas || n, "click", e);
        }
    };

    var _dragConnection = function (surface, d1, d2, callbacks) {
        var _jsPlumb = surface.getJsPlumb();
        var el1 = d1.canvas || d1, el2 = d2.canvas || d2;
        var e1 = _makeEvt(surface, el1), e2 = _makeEvt(surface, el2);

        callbacks = callbacks || {};

        var conns = _jsPlumb.select().length;

        callbacks.start && callbacks.start();
        _jsPlumb.trigger(el1, DOWN_EVENT, e1);
        callbacks.down && callbacks.down();
        _jsPlumb.trigger(document, MOVE_EVENT, e2);
        callbacks.move && callbacks.move();
        _jsPlumb.trigger(el2, UP_EVENT, e2);
        callbacks.up && callbacks.up();

        return _jsPlumb.select().get(conns);
    };

    /**
     * Drag the given element to the given x,y on the canvas. We adjust for the container's page position, but the
     * x,y passed in here is the position on the canvas. This is important to remember.
     * @param surface
     * @param el
     * @param x
     * @param y
     * @private
     */
    var _dragElementTo = function(surface, el, x, y) {
        var _jsPlumb = surface.getJsPlumb();
        // make a mousedown event, using page coords
        var e = _makeEvt(surface, el);
        _jsPlumb.trigger(el, DOWN_EVENT, e);
        var s = _jsPlumb.getSize(el);

        // find the origin of the canvas in page coordinates - events have to be in page coords.
        var acl = surface.getApparentCanvasLocation();
        var b = surface.getJsPlumb().getContainer().parentNode.getBoundingClientRect();
        var ox = b.x + acl[0], oy = b.y + acl[1];

        _jsPlumb.trigger(document, MOVE_EVENT, _evt(Math.floor(x + ox + (s[0] / 2)), Math.floor(y + oy + (s[1] / 2))));
        _jsPlumb.trigger(document, UP_EVENT);
    };

    /**
     * Drag the element by the given dx,dy.
     * @param surface The Surface instance we're operating on.
     * @param el DOM Element to move
     * @param dx Distance in X axis to move
     * @param dy Distance in Y axis to move
     * @private
     */
    var _dragElementBy = function(surface, el, dx, dy) {
        var _jsPlumb = surface.getJsPlumb();
        // make a mousedown event, using page coords
        var e = _makeEvt(surface, el);
        _jsPlumb.trigger(el, DOWN_EVENT, e);
        // move the event the desired amount and fire a move event
        _jsPlumb.trigger(document, MOVE_EVENT, _transposeEvent(e, dx, dy));
        _jsPlumb.trigger(document, UP_EVENT);
    };

    var isTouchDevice = "ontouchstart" in document.documentElement;
    var DOWN_EVENT = isTouchDevice ? "touchstart" : "mousedown";
    var MOVE_EVENT = isTouchDevice ? "touchmove" : "mousemove";
    var UP_EVENT = isTouchDevice ? "touchend" : "mouseup";

    /**
     * Synthesize an event
     * @param l
     * @param t
     * @returns {{clientY: *, clientX: *, pageY: *, screenX: *, pageX: *, screenY: *}}
     * @private
     */
    var _evt = function(l, t) {
        return {
            clientX: l,
            clientY: t,
            screenX: l,
            screenY: t,
            pageX: l,
            pageY: t
        };
    };

    var _nudgeEvent = function(evt, dx, dy) {
        evt.clientX += dx;
        evt.clientY += dy;
        evt.screenX += dx;
        evt.screenY += dy;
        evt.pageX += dx;
        evt.pageY += dy;
    };


	window.jsPlumbToolkitTestSupport = {
        addDiv:_addDiv,
        addDivs:_addDivs,
        cleanup:_cleanup,
        delta:delta,
        DOWN_EVENT : DOWN_EVENT,
        UP_EVENT:UP_EVENT,
        MOVE_EVENT:MOVE_EVENT,
        isTouchDevice:isTouchDevice,
        makeEvent:_makeEvt,
        makeEventAt:_evt,
        nudgeEvent:_nudgeEvent,

        attachToSurface:function(surface) {
            return new jsPlumbToolkitTestHarness(surface.getToolkit(), surface);
        },

        create:function(toolkitParams, renderParams, containerParams) {
            var handler = _makeAToolkit(toolkitParams, renderParams, containerParams);
            return new jsPlumbToolkitTestHarness(handler.toolkit, handler.surface);
        }
    };

    var jsPlumbToolkitTestHarness = function(toolkit, surface) {

        this.toolkit = toolkit;
        var _surface = surface;

        this.eventManager = new Mottle();

        Object.defineProperty(this, "surface", { get: function() {
            if (_surface == null) {
                throw new Error("Test harness not rendered. Use `render` method or provide render params in constructor");
            } else {
                return _surface;
            }
        }});

        Object.defineProperty(this, "jsplumb", { get: function() {
            return this.surface.getJsPlumb();
        }});

        Object.defineProperty(this, "container", { get: function() {
            return this.jsplumb.getContainer();
        }});

        this.render = function(renderParams, containerParams) {
            var renderer = _makeARenderer(this.toolkit, renderParams, containerParams);
            _surface = renderer.surface;
            return _surface;
        };

    };

    jsPlumbToolkitTestHarness.prototype.addMiniview = function(miniviewOptions) {

        miniviewOptions = miniviewOptions || {};
        var s = _addDiv("div");
        s.style.position = "absolute";
        s.style.left = "0px";
        s.style.top = "0px";
        s.style.width = (miniviewOptions && miniviewOptions.width ? miniviewOptions.width : 250) + "px";
        s.style.height = (miniviewOptions && miniviewOptions.height ? miniviewOptions.height : 250) + "px";
        miniviewOptions.container = s;

        return this.surface.createMiniview(miniviewOptions);
    };

    jsPlumbToolkitTestHarness.prototype.querySelectorAll = function(selector) {
        return this.container.querySelectorAll(selector);
    };

    /**
     * Randomly drag a node around. Can be useful to ensure the model is being updated, or you're getting
     * callbacks you expect, etc. We use this internally when we just want a node to move and we don't care where
     * it moves to.
     * @param obj
     */
    jsPlumbToolkitTestHarness.prototype.dragANodeAround = function(obj) {
        _dragAnElementAround(this.surface, this.surface.getObjectInfo(obj).el);
    };

    /**
     * Randomly drag a DOM element around
     * @param el
     */
    jsPlumbToolkitTestHarness.prototype.dragAnElementAround = function(el) {
        _dragAnElementAround(this.surface, el);
    };

    /**
     * Connect, using the mouse, `obj1` to `obj2`. This will throw an Error if either or both of the arguments cannot be
     * resolved. Any interceptors you have setup on the underlying Toolkit
     * instance will be invoked - this functions just as if the user had used the mouse to drag a connection from
     * one object to the other.
     * @param obj1 An node/group/port ID, or node/group/port, or a DOM element.
     * @param obj2 An node/group/port ID, or node/group/port, or a DOM element.
     * @param [callbacks] Optional map of callbacks for the connection.
     */
    jsPlumbToolkitTestHarness.prototype.dragConnection = function(obj1, obj2, callbacks) {
        // decode `obj1` and `obj2`
        var info1 = this.surface.getObjectInfo(obj1),
            info2 = this.surface.getObjectInfo(obj2),
            source = info1.type === "Port" ? this.surface.getRenderedEndpoint(info1.obj) || info1.el : info1.el,
            target = info2.type === "Port" ? this.surface.getRenderedEndpoint(info2.obj) || info2.el : info2.el;

        if (info1.el && info2.el) {
            _dragConnection(this.surface, source, target, callbacks);
        } else if (info1.el == null) {
            throw new Error(obj1 + " cannot be resolved");
        } else if (info2.el == null) {
            throw new Error(obj2 + " cannot be resolved");
        }
    };

    /**
     * Shortcut to the underlying `load` method of the toolkit.
     * @param options
     * @returns {*}
     */
    jsPlumbToolkitTestHarness.prototype.load = function(options) {
        return this.toolkit.load(options);
    };

    /**
     * Shortcut to the underlying `clear` method of the toolkit.
     * @returns {*}
     */
    jsPlumbToolkitTestHarness.prototype.clear = function() {
        return this.toolkit.clear();
    };

    /**
     * For the given argument, find and return the corresponding DOM element.
     * @param obj A node/group/port id, or node/group/port, or a DOM element.
     * @returns {*}
     */
    jsPlumbToolkitTestHarness.prototype.getRenderedElement = function(obj) {
        var info = this.surface.getObjectInfo(obj);
        return info.el;
    };

    /**
     * For the given argument, find and return the underlying Connection used to render it.
     * @param obj An edge ID, or an Edge.
     * @returns {*}
     */
    jsPlumbToolkitTestHarness.prototype.getRenderedConnection = function(obj) {
        return this.surface.getRenderedConnection(obj);
    };

    /**
     * Drag the given node into the given group.
     * @param node Node id, Node, or DOM element.
     * @param group Group id, Group, or DOM element.
     */
    jsPlumbToolkitTestHarness.prototype.dragNodeIntoGroup = function(node, group) {
        var nodeInfo = this.surface.getObjectInfo(node),
            groupInfo = this.surface.getObjectInfo(group);

        if (nodeInfo.el && groupInfo.el) {
            var dropArea = groupInfo.el.querySelector("[jtk-group-content]") || groupInfo.el,
                dropAreaOffset = this.jsplumb.getOffset(dropArea),
                dropAreaSize = this.jsplumb.getSize(dropArea);

            _dragElementTo(this.surface, nodeInfo.el, dropAreaOffset.left + (dropAreaSize[0] / 2), dropAreaOffset.top + (dropAreaSize[1] / 2));
        }
    };

    /**
     * Gets a Group from the underlying Toolkit.
     * @param obj Group Id, DOM element, or Group.
     * @returns {Group}
     */
    jsPlumbToolkitTestHarness.prototype.getGroup = function(obj) {
        return this.getToolkitObject(obj);
    };

    /**
     * Gets a Node from the underlying Toolkit.
     * @param obj Node Id, DOM element, or Node.
     * @returns {Node}
     */
    jsPlumbToolkitTestHarness.prototype.getNode = function(obj) {
        return this.getToolkitObject(obj);
    };

    /**
     * Find the corresponding Toolkit object for the given input.
     * @param obj A string representing an ID, a DOM element, or an existing Toolkit object.
     * @returns {Node|Port|Group|Edge}
     */
    jsPlumbToolkitTestHarness.prototype.getToolkitObject = function(obj) {
        return this.surface.getObjectInfo(obj).obj;
    };

    /**
     * Drag the given Node to the given [x,y], which are canvas coordinates.
     * @param obj  Node id, node, or DOM element.
     * @param x Location on canvas in X axis to position top left corner of the node.
     * @param y Location on canvas in Y axis to position top left corner of the node.
     */
    jsPlumbToolkitTestHarness.prototype.dragNodeTo = function(obj, x, y) {
        var info = this.surface.getObjectInfo(obj);
        if (info.el) {
            _dragElementTo(this.surface, info.el, x, y);
        } else {
            throw new Error("Cannot drag node: cannot resolve " + obj);
        }
    };

    /**
     * Drag the given Node by the given x/y amounts.
     * @param obj  Node id, node, or DOM element.
     * @param x Amount to move in X axis
     * @param y Amount to move in Y axis
     */
    jsPlumbToolkitTestHarness.prototype.dragNodeBy = function(obj, x, y) {
        var info = this.surface.getObjectInfo(obj);
        if (info.el) {
            _dragElementBy(this.surface, info.el, x, y);
        } else {
            throw new Error("Cannot drag node: cannot resolve " + obj);
        }
    };

    /**
     * Drag the given DOM element by the given x/y amounts.
     * @param obj  DOM element.
     * @param x Amount to move in X axis
     * @param y Amount to move in Y axis
     */
    jsPlumbToolkitTestHarness.prototype.dragElementBy = function(el, x, y) {
        _dragElementBy(this.surface, el, x, y);
    };

    /**
     * Connect the given source and target via a call on the Toolkit, ie. without using the mouse.
     * @param source Node/Port/Group id, node/port/group, or DOM element.
     * @param target Node/Port/Group id, node/port/group, or DOM element.
     * @param data Optional data for the edge.
     * @returns {*}
     */
    jsPlumbToolkitTestHarness.prototype.connect = function(source, target, data) {
        var info1 = this.surface.getObjectInfo(source),
            info2 = this.surface.getObjectInfo(target);

        return this.toolkit.connect({source:info1.obj, target:info2.obj, data:data || {}});
    };

    // there is a chance an obscure Typescript bug will cause this line below to fail: a JS doc on something that's not
    // actually a method. I've seen it before. Currently hopeful that the bug has been fixed.

    /**
     * Drag the given Group to the given [x,y], which are canvas coordinates.
     * @param obj Group id, group, or DOM element.
     * @param x Location on canvas in X axis to position top left corner of the group.
     * @param y Location on canvas in Y axis to position top left corner of the group.
     */
    jsPlumbToolkitTestHarness.prototype.dragGroupTo = jsPlumbToolkitTestHarness.prototype.dragNodeTo;

    /**
     * Trigger the event with the given name on the given object. By default the event will occur in the middle of the DOM element
     * representing the object.
     * @param obj Node/Port/Group id, node/port/group, or DOM element.
     * @param eventName eg 'click', 'mouseover'
     * @param [evt] Optional, an event you previously created via #makeEvent. Sometimes you want to control the specific location
     * of the event.
     */
    jsPlumbToolkitTestHarness.prototype.trigger = function(obj, eventName, evt) {
        var info = this.surface.getObjectInfo(obj);
        if (info.el) {
            evt = evt || _makeEvt(this.surface, info.el);
            this.jsplumb.trigger(info.el, "mousemove", evt);
        } else {
            throw new Error("Trigger: Cannot resolve " + obj);
        }
    };

    /**
     * Synthesize an event for the given object.
     * @param obj Node/Port/Group id, node/port/group, or DOM element.
     * @param [dx] Optional offset from the center of the x axis of the related DOM element to position the event.
     * @param [dy] Optional offset from the center of the y axis of the related DOM element to position the event.
     * @returns {{clientY: *, clientX: *, pageY: *, screenX: *, pageX: *, screenY: *}|void}
     */
    jsPlumbToolkitTestHarness.prototype.makeEvent = function(obj, dx, dy) {
        var info = this.surface.getObjectInfo(obj);
        if (info.el) {
            var e = _makeEvt(this.surface, info.el);
            if (dx || dy) {
                return _nudgeEvent(e, dx == null ? 0 : dx, dy == null ? 0 : dy);
            } else {
                return e;
            }
        } else {
            throw new Error("Trigger: Cannot resolve " + obj);
        }
    };

    /**
     * Gets an Edge.
     * @param obj Edge ID, or Edge object.
     * @returns {*}
     */
    jsPlumbToolkitTestHarness.prototype.getEdge = function(obj) {
        return this.toolkit.getEdge(obj);
    };

    /**
     * Updates an Edge.
     * @param edge Edge, or edge ID.
     * @param data Data to update the edge with.
     */
    jsPlumbToolkitTestHarness.prototype.updateEdge = function(edge, data) {
        this.toolkit.updateEdge(edge, data);
    };

    /**
     * Gets all edges in the underlying Toolkit.
     * @returns {*}
     */
    jsPlumbToolkitTestHarness.prototype.getAllEdges = function() {
        return this.toolkit.getAllEdges();
    };

    /**
     * Gets the Endpoint that was rendered for some port.
     * @param obj Port, or port ID.
     * @returns {*}
     */
    jsPlumbToolkitTestHarness.prototype.getRenderedPort = function(obj) {
        return this.surface.getRenderedPort(obj);
    };

    /**
     * Add a Node to the Toolkit.
     * @param data Data for the Node.
     * @returns {Node}
     */
    jsPlumbToolkitTestHarness.prototype.addNode = function(data) {
        return this.toolkit.addNode(data);
    };

    /**
     * Update a Node in to the Toolkit.
     * @param obj Node, or Node Id.
     * @param data Data for the Node.
     * @returns {Node}
     */
    jsPlumbToolkitTestHarness.prototype.updateNode = function(obj, data) {
        return this.toolkit.updateNode(obj, data);
    };

    /**
     * Clicks on the node with the given ID.
     * @param nodeId ID of the node to click on.
     */
    jsPlumbToolkitTestHarness.prototype.clickOnNode = function(nodeId) {
        _clickOnNode(this, nodeId);
    };

    /**
     * Clicks on an element inside the node with the given ID.
     * @param nodeId ID of the node to click on.
     * @param selector CSS selector identifying the child element to click on.
     */
    jsPlumbToolkitTestHarness.prototype.clickOnElementInsideNode = function(nodeId, selector) {
        _clickOnElementInsideNode(this, nodeId, selector);
    };

    /**
     * Clicks on the given edge
     * @param spec ID of the edge, or the Edge
     */
    jsPlumbToolkitTestHarness.prototype.clickOnEdge = function(spec) {
        _clickOnEdge(this, spec);
    };

    /**
     * Clicks on the overlay with the given ID, on the given Edge.
     * @param edgeSpec ID of the Edge, or the Edge
     * @param overlayId ID of the overlay to click on.
     */
    jsPlumbToolkitTestHarness.prototype.clickOnOverlay = function(edgeSpec, overlayId) {
        _clickOnOverlay(this, edgeSpec, overlayId);
    };

    /**
     * Clicks on the port with the given ID on the node with given node id.
     * @param nodeId ID of the node containing the port
     * @param portId ID of the port to click on.
     */
    jsPlumbToolkitTestHarness.prototype.clickOnPort = function(nodeId, portId) {
        _clickOnPort(this, nodeId, portId);
    };

    /**
     * Returns the count of Edges in the underlying Toolkit.
     * @returns {*}
     */
    jsPlumbToolkitTestHarness.prototype.getEdgeCount = function() {
        return this.toolkit.getEdgeCount();
    };

    /**
     * Create a new Undo manager and attach to our Surface.
     */
    jsPlumbToolkitTestHarness.prototype.configureUndoRedo = function(options) {
        options = jsPlumb.extend(options || {});
        options.surface = this.surface;
        this.undoManager = new jsPlumbToolkitUndoRedo(options);
        return this.undoManager;
    };

    /**
     * Drag the given element onto the canvas, optionally at a specific x,y. Use this when you want to test drag/drop
     * from some palette.
     * @param el Element to drop onto the canvas.
     * @param x Optional, defaults to 250.
     * @param y Optional, defaults to 250.
     */
    jsPlumbToolkitTestHarness.prototype.dragElementToCanvas = function(el, x, y) {
        x = x || 250;
        y = y || 250;

        var acl = this.surface.getApparentCanvasLocation();
        var b = this.jsplumb.getContainer().parentNode.getBoundingClientRect();
        var ox = b.x + acl[0], oy = b.y + acl[1];

        // make a mousedown event, using page coords
        var e = _makeEvt(this.surface, el);
        this.eventManager.trigger(el, DOWN_EVENT, e);
        var s = this.jsplumb.getSize(el);
        var c = this.jsplumb.getContainer().parentNode;

        var br = el.getBoundingClientRect();
        // we move a tiny amount first, because the drop manager gets confused if the first move event is on the canvas.
        this.eventManager.trigger(c, MOVE_EVENT, _evt(br.x + 1, br.y + 1));
        // then we move to the target location.
        this.eventManager.trigger(c, MOVE_EVENT, _evt(x + ox + (s[0] / 2), y + oy + (s[1] / 2)));
        this.eventManager.trigger(c, UP_EVENT);

    };




})();
