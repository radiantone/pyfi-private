(function() {

var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var CLASS_CONNECTION_EDIT = "jtk-connection-edit";
var CLASS_BEZIER_GUIDELINE = "jtk-bezier-guideline";
var CLASS_ANCHOR_PLACEHOLDER = "jtk-anchor-placeholder";
var CLASS_ANCHOR_CANDIDATE = "jtk-anchor-candidate";
var CLASS_BEZIER_HANDLE = "jtk-bezier-handle";
var CLASS_BEZIER_HANDLE_CONTROL_POINT = "jtk-bezier-handle-control-point";
var CLASS_BEZIER_HANDLE_CONTROL_POINT_1 = "jtk-bezier-handle-control-point-1";
var CLASS_BEZIER_HANDLE_CONTROL_POINT_2 = "jtk-bezier-handle-control-point-2";
var CLASS_BEZIER_SECONDARY_HANDLE = "jtk-bezier-handle-secondary";
var CLASS_BEZIER_SECONDARY_SOURCE_HANDLE = "jtk-bezier-handle-secondary-source";
var CLASS_BEZIER_SECONDARY_TARGET_HANDLE = "jtk-bezier-handle-secondary-target";
var CLASS_EDGE_DELETE_BUTTON = "jtk-edge-delete";
var ATTR_ANCHOR_FACE = "jtk-anchor-face";
var NONE = "none";
var BLOCK = "block";
var LEFT = "left";
var TOP = "top";
var RIGHT = "right";
var BOTTOM = "bottom";
var PX = "px";
var ABSOLUTE = "absolute";
var DUAL = "dual";
var SINGLE = "single";
var EVT_CLEAR_CONNECTION_EDITS = "clearConnectionEdits";
var EVT_START_CONNECTION_EDIT = "startConnectionEdit";
var EVT_STOP_CONNECTION_EDIT = "stopConnectionEdit";
var EVT_CONNECTION_EDIT = "connectionEdit";
var EVT_CLICK = "click";
var EVT_INTERNAL_CONNECTION_DETACHED = "internal.connectionDetached";
var EVT_ZOOM = "zoom";
var EVT_NODE_MOVE_END = "nodeMoveEnd";
var EVT_NODE_MOVE = "nodeMove";
var root = this;
var _jp = root.jsPlumb;
var _jpi = root.jsPlumbInstance;
var _ju = root.jsPlumbUtil;
var _jtk = root.jsPlumbToolkit;
function dot(cls) { return "." + cls; }
var ANCHOR_PLACEHOLDER_SELECTOR = dot(CLASS_ANCHOR_PLACEHOLDER);
function _makeElement(x, y, clazz) {
    var h = document.createElement("div");
    h.className = clazz ? clazz : "";
    h.style.position = ABSOLUTE;
    h.style.left = x + PX;
    h.style.top = y + PX;
    return h;
}
function _makeElementAt(_jsPlumb, parent, x, y, clazz) {
    var parentSize = _jsPlumb.getSize(parent);
    var _x = parentSize[0] * x, _y = parentSize[1] * y;
    var el = _makeElement(_x, _y, clazz);
    parent.appendChild(el);
    var s = _jsPlumb.getSize(el);
    el.style.left = (_x - (s[0] / 2)) + PX;
    el.style.top = (_y - (s[1] / 2)) + PX;
    return el;
}
var EditorBase = /** @class */ (function () {
    function EditorBase(options) {
        var _this = this;
        this.currentOverlays = [];
        this._dragHandlers = {};
        this.active = false;
        this._jsPlumb = options.jsPlumb;
        this._surface = options.surface;
        this._surface.getToolkit().bind("graphClearStart", function () {
            _this.deactivate();
        });
        /**
         * on detach event, deactivate the editor.
         */
        this._jsPlumb.bind(EVT_INTERNAL_CONNECTION_DETACHED, function (params) {
            var conn = params.connection;
            if (conn === _this.current) {
                _this.deactivate();
            }
        });
        this.eventManager = new Mottle();
        this._katavorio = new Katavorio({
            bind: function (el, evt, fn) { return _this.eventManager.on(el, evt, fn); },
            unbind: function (el, evt, fn) { return _this.eventManager.off(el, evt, fn); },
            getSize: function (el) { return [parseInt(el.offsetWidth, 10), parseInt(el.offsetHeight, 10)]; },
            getPosition: function (el) {
                return [parseInt(el.style.left, 10), parseInt(el.style.top, 10)];
            },
            setPosition: function (el, xy) {
                el.style.left = xy[0] + PX;
                el.style.top = xy[1] + PX;
            },
            addClass: this._jsPlumb.addClass.bind(this._jsPlumb),
            removeClass: this._jsPlumb.removeClass.bind(this._jsPlumb),
            intersects: Biltong.intersects,
            indexOf: function (l, i) {
                return l.indexOf(i);
            },
            scope: "connector-editor",
            css: {
                noSelect: this._jsPlumb.dragSelectClass,
                delegatedDraggable: "jtk-delegated-draggable",
                droppable: "jtk-droppable",
                draggable: "jtk-draggable",
                drag: "jtk-drag",
                selected: "jtk-drag-selected",
                active: "jtk-drag-active",
                hover: "jtk-drag-hover",
                ghostProxy: "jtk-ghost-proxy"
            },
            zoom: this._jsPlumb.getZoom()
        });
        // register a draggable handler for the container. we'll attach delegated handlers to this. it may be better in a future release
        // to use jsplumb's own drag handler (from 4.x onwards)
        this._katavorioDraggable = this._katavorio.draggable(this._jsPlumb.getContainer(), {})[0];
        // todo respond to container changes and re-register the drag handler
        // this is the drag handler for relocating anchors. it is common to all connector editors.
        this._katavorioDraggable.addSelector({
            selector: ANCHOR_PLACEHOLDER_SELECTOR,
            constrain: function (pos, dragEl, constrainRect, elementSize) {
                var a = dragEl._jsPlumbAnchor.anchor;
                var ep = dragEl._jsPlumbAnchor.endpoint;
                var idx = dragEl._jsPlumbAnchor.idx;
                if (a.isContinuous) {
                    pos = relocateContinuousAnchor(a, ep, pos, dragEl, constrainRect, elementSize, idx, _this.current.getConnector(), _this._jsPlumb);
                }
                else if (a.isDynamic) {
                    pos = relocateDynamicAnchor(a, ep, pos, dragEl, constrainRect, elementSize, idx, _this.current.getConnector(), _this._jsPlumb);
                }
                else {
                    pos = relocateAnchor(a, ep, pos, dragEl, constrainRect, elementSize, idx, _this.current.getConnector(), _this._jsPlumb);
                }
                _this._jsPlumb.revalidate(dragEl.parentNode);
                // we used to allow the placeholder to drag anywhere
                // return pos;
                // now we constrain it to the parent element.
                var s = [
                    dragEl.offsetWidth,
                    dragEl.offsetHeight
                ], b = {
                    xmin: -s[0] / 2,
                    xmax: constrainRect.w - (s[0] / 2),
                    ymin: -s[1] / 2,
                    ymax: constrainRect.h - (s[1] / 2)
                };
                return [
                    pos[0] < b.xmin ? b.xmin : pos[0] > b.xmax ? b.xmax : pos[0],
                    pos[1] < b.ymin ? b.ymin : pos[1] > b.ymax ? b.ymax : pos[1]
                ];
            },
            start: function (params) {
                // drag
                //e
                //el
                //pos
                var dragEl = params.drag.getDragElement();
                var a = dragEl._jsPlumbAnchor.anchor;
                var ep = dragEl._jsPlumbAnchor.endpoint;
                if (a.isContinuous) {
                    // highlight current face
                    dragEl.parentNode.setAttribute(ATTR_ANCHOR_FACE, a.getCurrentFace());
                }
                else if (a.isDynamic) {
                    var locs = a.getAnchors().map(function (_a) { return [_a.x, _a.y, _a.orientation[0], _a.orientation[1]]; });
                    locs.forEach(function (loc) {
                        _makeElementAt(_this._jsPlumb, ep.element, loc[0], loc[1], CLASS_ANCHOR_CANDIDATE);
                    });
                }
                else {
                    var locs = [
                        [a.x, a.y, a.orientation[0], a.orientation[1]],
                        [a.y, 1 - a.x, a.orientation[1], -1 * a.orientation[0]],
                        [1 - a.x, 1 - a.y, -1 * a.orientation[0], -1 * a.orientation[1]],
                        [1 - a.y, a.x, -1 * a.orientation[1], a.orientation[0]]
                    ];
                    locs.forEach(function (loc) {
                        _makeElementAt(_this._jsPlumb, ep.element, loc[0], loc[1], CLASS_ANCHOR_CANDIDATE);
                    });
                }
            },
            stop: function (params) {
                var parent = params.el.parentNode;
                var dragEl = params.drag.getDragElement();
                var a = dragEl._jsPlumbAnchor.anchor;
                var idx = dragEl._jsPlumbAnchor.idx;
                var ep = dragEl._jsPlumbAnchor.endpoint;
                if (a.isContinuous) {
                    // stop highlighting current face
                    parent.removeAttribute(ATTR_ANCHOR_FACE);
                }
                else if (a.isDynamic) {
                    // drag stopped on dynamic anchor. no action.
                }
                else {
                    // drag stopped on fixed anchor. no action.
                }
                var candidates = ep.element.querySelectorAll(dot(CLASS_ANCHOR_CANDIDATE));
                candidates.forEach(function (c) { return c.parentNode.removeChild(c); });
                _this._drawAnchors();
                _this._update();
                _this.fireConnectionEditEvent();
            }
        });
        this._surface.bind(EVT_NODE_MOVE_END, function (p) {
            // check if the moved node is connected to a connection we are editing.
            if (_this.active && _this.currentEdge && (p.node === _this.currentEdge.source || p.node === _this.currentEdge.target)) {
                _this._elementDragged(p);
                _this.fireConnectionEditEvent();
            }
        });
        this._surface.bind(EVT_NODE_MOVE, function (p) {
            // check if the moving node is connected to a connection we are editing.
            if (_this.active && _this.currentEdge && (p.node === _this.currentEdge.source || p.node === _this.currentEdge.target)) {
                _this._elementDragging(p);
            }
        });
        this._jsPlumb.bind(EVT_ZOOM, function (z) {
            _this._katavorio.setZoom(z);
        });
    }
    EditorBase.prototype._attachOverlay = function (surface, connection, overlaySpec) {
        var os = [overlaySpec[0], surface.getJsPlumb().extend({}, overlaySpec[1])];
        os[1].id = jsPlumbUtil.uuid();
        this.currentOverlays.push(connection.addOverlay(os));
    };
    EditorBase.prototype._attachOverlays = function (surface, connection, overlaySpecs) {
        var _this = this;
        this._detachOverlays();
        overlaySpecs.forEach(function (overlaySpec) {
            _this._attachOverlay(surface, connection, overlaySpec);
        });
    };
    EditorBase.prototype._detachOverlays = function () {
        var _this = this;
        this.currentOverlays.forEach(function (o) {
            _this.current.removeOverlay(o.id);
        });
    };
    EditorBase.prototype._attachDeleteButton = function (surface, params) {
        var _this = this;
        var cls = params.deleteButtonClass || CLASS_EDGE_DELETE_BUTTON;
        var loc = params.deleteButtonLocation || 0.1;
        var doRemove = function () { return surface.getToolkit().removeEdge(_this.currentEdge); };
        var deleteHandler = function () {
            if (params.onMaybeDelete) {
                params.onMaybeDelete(_this.currentEdge, _this.current, doRemove);
            }
            else {
                doRemove();
            }
        };
        if (!Array.isArray(loc)) {
            loc = [loc];
        }
        loc.forEach(function (l) {
            _this._attachOverlay(surface, _this.current, ["Label", {
                    location: l,
                    cssClass: cls,
                    events: {
                        click: deleteHandler
                    }
                }]);
        });
    };
    /**
     * Repaints the current connection, passing some arguments, optionally. These are retrieved inside `refresh`,
     * and are ultimately handed off to the subclass's `repaint` method. Subclasses should call this on things like handle
     * dragging, as the existence (and nature of ) args can subsequently be used by their `repaint` method to decide whether or not
     * to redraw all the handles (such as you would in the event of an external paint event), or just to reposition the existing
     * ones. During a drag, of course, blowing away the current handle would be bad.
     */
    EditorBase.prototype.repaintConnection = function (args) {
        if (this.current) {
            this.current.repaint({ args: args });
        }
    };
    /**
     * Fires a connection edit event, passing the current connection, and the current
     * connection's exported geometry.
     */
    EditorBase.prototype.fireConnectionEditEvent = function () {
        this._jsPlumb.fire(EVT_CONNECTION_EDIT, {
            connection: this.current,
            geometry: this.current.connector.exportGeometry()
        });
    };
    /**
     * Redraw anchor placeholders and editor handles.
     * @param args Optional args to pass to the subclass repaint method.
     */
    EditorBase.prototype.refresh = function (args) {
        if (this.current) {
            // reposition the anchor placeholders.
            this._drawAnchors();
            // instruct the subclass to repaint (and pass it the args, if they are present)
            this._repaint && this._repaint(args);
        }
    };
    /**
     * Draws, or repositions if they exist already, the anchor placeholders for the current connection.
     * @private
     */
    EditorBase.prototype._drawAnchors = function () {
        var _this = this;
        var _b, _c;
        if (this.current) {
            var _one = function (idx, existingPlaceholder) {
                var ep = _this.current.endpoints[idx];
                var a = ep.anchor;
                if (a.isDynamic || a.isContinuous) {
                    var sa = a.getCurrentLocation({ element: ep }).slice();
                    // if element rotated, `sa` has the rotated values
                    var d = _this._jsPlumb.getOffset(ep.element);
                    var r = _this._jsPlumb.getRotation(ep.elementId);
                    // this is the travel in each axis from the origin of the element, in pixels. for an unrotated element,
                    // with an anchor as [0.5,0], for instance, x here would 0.5 of the element width and y would be 0.
                    //
                    // these values are used to locate the anchor placeholder - it is a child of the element to which it belongs.
                    //
                    // when an element is rotated, [x,y] should be calculated by first rotating the value of `sa` back, as
                    // the anchor placeholder will be subject to the rotation of the parent.
                    if (r !== 0) {
                        var s = _this._jsPlumb.getSize(ep.element), c = [d.left + (s[0] / 2), d.top + (s[1] / 2)], rax = jsPlumbUtil.rotatePoint(sa, c, -r);
                        sa[0] = rax[0];
                        sa[1] = rax[1];
                    }
                    var _b = [sa[0] - d.left, sa[1] - d.top], x = _b[0], y = _b[1];
                    var p = void 0;
                    if (existingPlaceholder != null) {
                        p = existingPlaceholder;
                    }
                    else {
                        p = _makeElement(x, y, CLASS_ANCHOR_PLACEHOLDER);
                        ep.element.appendChild(p);
                        _this._setElementPosition(p, x, y);
                        p._jsPlumbAnchor = {
                            anchor: a,
                            endpoint: ep,
                            idx: idx
                        };
                    }
                    var ps = _this._jsPlumb.getSize(p);
                    p.style.left = (x - (ps[0] / 2)) + PX;
                    p.style.top = (y - (ps[1] / 2)) + PX;
                    return [d, p];
                }
                else {
                    return [[0, 0], null];
                }
            };
            _b = _one(0, this.sourceAnchorPlaceholder), this.sourceDimensions = _b[0], this.sourceAnchorPlaceholder = _b[1];
            _c = _one(1, this.targetAnchorPlaceholder), this.targetDimensions = _c[0], this.targetAnchorPlaceholder = _c[1];
        }
    };
    /**
     * Removes anchor placeholders.
     * @private
     */
    EditorBase.prototype._cleanupAnchors = function () {
        if (this.current) {
            if (this.sourceAnchorPlaceholder) {
                this.sourceAnchorPlaceholder.parentNode.removeChild(this.sourceAnchorPlaceholder);
                delete this.sourceAnchorPlaceholder._jsPlumbAnchor;
            }
            if (this.targetAnchorPlaceholder) {
                this.targetAnchorPlaceholder.parentNode.removeChild(this.targetAnchorPlaceholder);
                delete this.targetAnchorPlaceholder._jsPlumbAnchor;
            }
        }
        this.sourceAnchorPlaceholder = null;
        this.targetAnchorPlaceholder = null;
        this.sourceDimensions = null;
        this.targetDimensions = null;
    };
    EditorBase.prototype._clearGeometry = function () {
        if (this.current) {
            this.current.getConnector().setGeometry(null, true);
            this.current.getConnector().setEditing(false);
        }
    };
    EditorBase.prototype.reset = function () {
        this.deactivate();
        this._clearGeometry();
        this._clearHandles();
        this._jsPlumb.revalidate(this.current.source);
        this._jsPlumb.revalidate(this.current.target);
        this._jsPlumb.fire(EVT_CLEAR_CONNECTION_EDITS, this.current);
    };
    EditorBase.prototype.isActive = function () {
        return this.active;
    };
    EditorBase.prototype._setElementPosition = function (el, x, y) {
        var s = this._jsPlumb.getSize(el), _x = (x - (s[0] / 2)), _y = (y - (s[1] / 2));
        el.style.left = _x + PX;
        el.style.top = _y + PX;
    };
    /**
     * Activate the editor, with the given Connection. First we
     * call `deactivate`, so there's only ever one edit happening at a time.
     * Then we set the current connection, and override its paint method.
     * @param connection
     */
    EditorBase.prototype.activate = function (surface, connection, params) {
        var _this = this;
        this.deactivate();
        this.current = connection;
        this.currentEdge = this.current.edge;
        this._katavorio.setZoom(this._jsPlumb.getZoom());
        // if current connection has been cleaned up, return.
        if (this.current._jsPlumb == null) {
            this.current = null;
            this.currentEdge = null;
            return;
        }
        // override the paint method
        this.current._paint = this.current.paint;
        this.current.paint = function (params) {
            _this.current._paint.apply(_this.current, [params]);
            params = params || {};
            _this.refresh(params.args);
        };
        if (params.overlays) {
            this._attachOverlays(surface, connection, params.overlays);
        }
        if (params.deleteButton === true) {
            this._attachDeleteButton(surface, params);
        }
        // tell the subclass to activate
        this._activate(surface, connection, params);
        var sourceEndpoint = this.current.endpoints[0];
        var sourceAnchor = sourceEndpoint.anchor;
        var targetEndpoint = this.current.endpoints[1];
        var targetAnchor = targetEndpoint.anchor;
        sourceAnchor.locked = true;
        targetAnchor.locked = true;
        this._drawAnchors();
        this.current.addClass(CLASS_CONNECTION_EDIT);
        // -------------------------- TODO: 1.x and 2.x only.  4.x uses delegated drag and so this _katavorioDrag member will not be present. Instead, the exclusion will need to be added to the
        //                              element drag handler.
        if (connection.source._katavorioDrag) {
            connection.source._katavorioDrag.addFilter(ANCHOR_PLACEHOLDER_SELECTOR);
        }
        if (connection.target._katavorioDrag) {
            connection.target._katavorioDrag.addFilter(ANCHOR_PLACEHOLDER_SELECTOR);
        }
        // ----------------------------------------------- / TODO -------------------------------------------------
        this.active = true;
        this._jsPlumb.fire(EVT_START_CONNECTION_EDIT, this.current);
    };
    /**
     * Deactivates the editor, removing all editor handles and anchor placeholders etc.
     * @param e
     */
    EditorBase.prototype.deactivate = function (e) {
        if (this.current != null && this.current._jsPlumb != null) {
            this._detachOverlays();
            this.current.paint = this.current._paint;
            this.current._paint = null;
            // -------------------------- TODO: 1.x and 2.x only.  4.x uses delegated drag and so this _katavorioDrag member will not be present. Instead, the exclusion will need to be added to the
            //                              element drag handler.
            if (this.current.source._katavorioDrag) {
                this.current.source._katavorioDrag.removeFilter(ANCHOR_PLACEHOLDER_SELECTOR);
            }
            if (this.current.target._katavorioDrag) {
                this.current.target._katavorioDrag.removeFilter(ANCHOR_PLACEHOLDER_SELECTOR);
            }
            // ----------------------------------------------- / TODO -------------------------------------------------
            var sourceAnchor = this.current.endpoints[0].anchor;
            var targetAnchor = this.current.endpoints[1].anchor;
            // TODO can 'revert' be folded into the 'unlock' ? is revert needed? etc
            // sourceAnchor.revert && sourceAnchor.revert();
            // targetAnchor.revert && targetAnchor.revert();
            // TODO only do this if no edits occurred.
            //sourceAnchor.unlock();
            //targetAnchor.unlock();
            this.current.removeClass(CLASS_CONNECTION_EDIT);
            this._cleanupAnchors();
        }
        this._clearHandles();
        if (this.current != null) {
            this._jsPlumb.fire(EVT_STOP_CONNECTION_EDIT, this.current);
        }
        this.active = false;
        this.current = null;
        this.currentEdge = null;
    };
    //
    // for subclasses to use. we keep a record of it so we can unsubscribe all handlers at once.
    EditorBase.prototype._addDragHandler = function (o) {
        this._katavorioDraggable.addSelector(o);
        this._dragHandlers[o.selector] = o;
    };
    return EditorBase;
}());
/**
 * relocate the given continuous anchor according to the given proximity of `pos` to each of the anchor's supported faces. the face is changed
 * on the anchor itself (and the anchor is locked), and in this case we simply return the current value of `pos`, meaning the user sees the drag proxy
 * under the mouse cursor, which is probably not where the anchor is now positioned, but it makes for a better UX. on drag stop, for all anchor types,
 * the anchor proxy is relocated to the current value.
 * @param anchor
 * @param ep
 * @param pos
 * @param dragEl
 * @param constrainRect
 * @param elementSize
 * @returns {number[]}
 */
function relocateContinuousAnchor(anchor, ep, pos, dragEl, constrainRect, elementSize, idx, connector, instance) {
    var supportedFaces = anchor.getSupportedFaces();
    var parent = dragEl.parentNode;
    var l = [
        ["left", pos[0]],
        ["right", constrainRect.w - pos[0]],
        ["top", pos[1]],
        ["bottom", constrainRect.h - pos[1]]
    ];
    var orientations = new Map([
        ["top", [0, -1]],
        ["bottom", [0, 1]],
        ["left", [-1, 0]],
        ["right", [1, 0]]
    ]);
    l.sort(function (a, b) {
        if (a[1] < b[1]) {
            return -1;
        }
        else {
            return 1;
        }
    });
    var face = null;
    for (var i = 0; i < l.length; i++) {
        if (supportedFaces.indexOf(l[i][0]) != -1) {
            face = l[i][0];
            break;
        }
    }
    if (face != null) {
        parent.setAttribute(ATTR_ANCHOR_FACE, face);
        anchor.setCurrentFace(face);
        anchor.lock(); // override lock when setting the current face.
        var orientation_1 = orientations.get(face).slice();
        //const r =
        // if r != 0, rotate the orientation
        var r = instance.getRotation(ep.elementId);
        if (r != 0) {
            orientation_1 = jsPlumbUtil.rotateAnchorOrientation(orientation_1, r);
        }
        connector.setAnchorOrientation(idx, orientation_1);
    }
    return pos;
}
/**
 * relocate the given dynamic anchor according to the given proximity of `pos` to each of the anchor's supported locations. the face is changed
 * on the anchor itself (and the anchor is locked), and in this case we simply return the current value of `pos`, meaning the user sees the drag proxy
 * under the mouse cursor, which is probably not where the anchor is now positioned, but it makes for a better UX. on drag stop, for all anchor types,
 * the anchor proxy is relocated to the current value.
 * @param anchor
 * @param pos
 * @param dragEl
 * @param constrainRect
 * @param elementSize
 * @returns {number[]}
 */
function relocateDynamicAnchor(anchor, ep, pos, dragEl, constrainRect, elementSize, idx, connector, instance) {
    var availableLocations = anchor.getAnchors().map(function (_a) { return [_a.x, _a.y, _a.orientation[0], _a.orientation[1], _a]; });
    var distances = availableLocations.map(function (loc, idx) {
        var _b = [constrainRect.w * loc[0], constrainRect.h * loc[1]], px = _b[0], py = _b[1], d = Math.sqrt(Math.pow(pos[0] - px, 2) + Math.pow(pos[1] - py, 2));
        return [idx, d, loc];
    });
    distances.sort(function (a, b) {
        if (a[1] < b[1]) {
            return -1;
        }
        else {
            return 1;
        }
    });
    var newPos = distances[0][2];
    anchor.setAnchor(newPos[4]);
    var newOrientation = newPos.slice(2);
    connector.setAnchorOrientation(idx, newOrientation);
    return pos;
}
function relocateAnchor(anchor, ep, pos, dragEl, constrainRect, elementSize, idx, connector, instance) {
    // for a given position [a,b], the allowed anchor positions are:
    //
    // [ b, 1-a, oy, -ox ]
    // [ 1-a, 1-b, -ox, -oy ]
    // [ 1-b, a, -oy, ox ]
    // these are in anticlockwise order
    // that is unless the Anchor was created with snapOnRelocate:false, in which case the anchor can be anywhere on
    // its parent (even outside the parent bounds)
    //
    // also if relocatable:false is set on the anchor, then it cannot be moved. this is true of all anchors.
    var availableLocations = [
        [anchor.x, anchor.y, anchor.orientation[0], anchor.orientation[1]],
        [anchor.y, 1 - anchor.x, anchor.orientation[1], -1 * anchor.orientation[0]],
        [1 - anchor.x, 1 - anchor.y, -1 * anchor.orientation[0], -1 * anchor.orientation[1]],
        [1 - anchor.y, anchor.x, -1 * anchor.orientation[1], anchor.orientation[0]]
    ];
    var distances = availableLocations.map(function (loc, idx) {
        var _b = [constrainRect.w * loc[0], constrainRect.h * loc[1]], px = _b[0], py = _b[1], d = Math.sqrt(Math.pow(pos[0] - px, 2) + Math.pow(pos[1] - py, 2));
        return [idx, d, loc];
    });
    distances.sort(function (a, b) {
        if (a[1] < b[1]) {
            return -1;
        }
        else {
            return 1;
        }
    });
    var newPos = distances[0][2];
    anchor.x = newPos[0];
    anchor.y = newPos[1];
    anchor.orientation = newPos.slice(2);
    anchor.lastReturnValue = null;
    connector.setAnchorOrientation(idx, newPos.slice(2));
    return pos;
}
// -------------- editable connector superclass ------------------------------------
var AbstractEditableConnector = /** @class */ (function () {
    function AbstractEditableConnector() {
    }
    AbstractEditableConnector.prototype._setAnchorLocation = function (loc, connection, endpointIndex) {
        var a = connection.endpoints[endpointIndex].anchor;
        // we do different things depending on the anchor type.
        // continuous -> convert anchor loc into a face, try to set it, fallback to next available etc.
        // dynamic -> set the anchor point, assuming it is supported.
        // fixed -> set the anchor point
        if (a.isContinuous) {
            var face = TOP;
            if (loc[2] === 0) {
                face = LEFT;
            }
            else if (loc[2] === 1) {
                face = RIGHT;
            }
            else if (loc[3] === 1) {
                face = BOTTOM;
            }
            a.setCurrentFace(face);
            a.lock();
        }
        else if (a.isDynamic) {
            a.setAnchorCoordinates(loc.slice(2));
            a.lastReturnValue = null;
        }
        else {
            a.x = loc[2];
            a.y = loc[3];
            a.orientation = loc.slice(4);
            a.lastReturnValue = null;
        }
        a.locked = true;
    };
    AbstractEditableConnector.prototype.importGeometry = function (geometry, connection) {
        if (this._importGeometry) {
            if (this._importGeometry(geometry)) {
                this._setAnchorLocation(geometry.source, connection, 0);
                this._setAnchorLocation(geometry.target, connection, 1);
                // in all cases we want to fire the same event we fire when the user drags an anchor, as if
                // the chosen anchor location has caused a re-route of the connector we want to keep track
                // of it.
                return true;
            }
            else {
                // the geometry was not set.
                return false;
            }
        }
        else {
            return false;
        }
    };
    AbstractEditableConnector.prototype.clearEdits = function () {
        if (this._clearEdits) {
            this._clearEdits();
            //this.edited = false;
            // anchors?
        }
    };
    return AbstractEditableConnector;
}());
_jp.Connectors.AbstractEditableConnector = AbstractEditableConnector;
_ju.extend(AbstractEditableConnector, _jp.Connectors.AbstractConnector);
// -------------- / editable connector superclass ------------------------------------
if (_jtk != null) {
    //
    // resolve an Edge or Connection or Edge ID into a Connection.
    //
    _jtk.Renderers.Surface.prototype._resolveConnection = function (edgeOrConnection) {
        return edgeOrConnection == null ? null :
            typeof edgeOrConnection === "string" ? this.getRenderedConnection(edgeOrConnection) :
                edgeOrConnection.constructor == _jp.Connection ? edgeOrConnection :
                    this.getRenderedConnection(edgeOrConnection.getId());
    };
    //
    // ensure the editors have been included. throw a TypeError if not.
    //
    _jtk.Renderers.Surface.prototype._ensureCanEdit = function () {
        if (!this.startEditing) {
            throw new Error("Connection editors not available.");
        }
    };
    /**
     * Starts editing of the given Edge, Connection, or Edge ID.
     * @method startEditing
     * @param {String|Edge|Connection} edgeOrConnection Either an Edge, or a Connection, or an Edge ID.
     * @param {Object} [params] Optional params for the start edit call.
     */
    _jtk.Renderers.Surface.prototype.startEditing = function (edgeOrConnection, params) {
        this._ensureCanEdit();
        var conn = this._resolveConnection(edgeOrConnection);
        if (conn != null) {
            var _jsPlumb = this.getJsPlumb();
            var connector = conn.getConnector();
            params = _jp.extend({}, params || {});
            var connectorType = conn.getConnector().type;
            if (!_jp.ConnectorEditors) {
                throw new Error("Connector editors not found. Have you imported jsPlumbToolkitEditableConnectors ?");
            }
            if (!_jp.ConnectorEditors[connectorType]) {
                throw new Error("No editor available for connector type [" + connectorType + "]");
            }
            else {
                if (_jsPlumb._connectorEditors == null) {
                    _jsPlumb._connectorEditors = {};
                }
                if (_jsPlumb._connectorEditors[connectorType] == null) {
                    var p = _jsPlumb.extend({}, params);
                    p.jsPlumb = _jsPlumb;
                    p.surface = this;
                    _jsPlumb._connectorEditors[connectorType] = new _jp.ConnectorEditors[connectorType](p);
                }
                _jsPlumb._connectorEditors[connectorType].activate(this, conn, params);
            }
        }
    };
    /**
     * Stops editing, if editing is happening right now. Otherwise does nothing.
     * @method stopEditing
     */
    _jtk.Renderers.Surface.prototype.stopEditing = function () {
        this._ensureCanEdit();
        var _jsPlumb = this.getJsPlumb();
        //this.getJsPlumb().stopEditing();
        for (var i in _jsPlumb._connectorEditors) {
            _jsPlumb._connectorEditors[i].deactivate();
        }
    };
    /**
     * Clears edits for the given Edge, Connection, or Edge ID.
     * @param {String|Edge|Connection} edgeOrConnection Either an Edge, or a Connection, or an Edge ID.
     */
    _jtk.Renderers.Surface.prototype.clearEdits = function (edgeOrConnection) {
        this._ensureCanEdit();
        var conn = this._resolveConnection(edgeOrConnection);
        if (conn != null) {
            var connector = conn.getConnector();
            if (connector.clearEdits) {
                connector.clearEdits();
                conn.repaint();
                return true;
            }
            else {
                return false;
            }
        }
    };
}
var VERTICAL = "v";
var HORIZONTAL = "h";
var NEGATIVE = -1;
var FLOWCHART_TYPE_DESCRIPTOR = "EditableFlowchart";
var STRAIGHT = "Straight";
var ARC = "Arc";
function sgn(n) {
    return n < 0 ? -1 : n === 0 ? 0 : 1;
}
function segLength(s) {
    if (s == null)
        debugger;
    return Math.sqrt(Math.pow(s[7] - s[5], 2) + Math.pow(s[8] - s[6], 2));
}
function segmentDirections(segment) {
    return [
        sgn(segment[2] - segment[0]),
        sgn(segment[3] - segment[1])
    ];
}
function _cloneSegment(a) {
    var _a = [];
    _a.push.apply(_a, a);
    return _a;
}
function positionEquals(p1, p2) {
    return p1[0] === p2[0] && p1[1] === p2[1];
}
function addSegment(connector, x, y, paintInfo, dx, dy) {
    if (connector.lastx === x && connector.lasty === y) {
        return;
    }
    var lx = connector.lastx == null ? paintInfo.sx : connector.lastx, ly = connector.lasty == null ? paintInfo.sy : connector.lasty, o = lx === x ? VERTICAL : HORIZONTAL;
    connector.lastx = x;
    connector.lasty = y;
    // we store the x,y relative to the canvas origin as well as the absolute location
    connector.segments.push([lx, ly, x, y, o, lx + dx, ly + dy, x + dx, y + dy]);
}
function commonStubCalculator(paintInfo, alwaysRespectStubs) {
    return [paintInfo.startStubX, paintInfo.startStubY, paintInfo.endStubX, paintInfo.endStubY];
}
/**
 * for the given set of segments, use the absolute coordinates to figure out the origin of the
 * connector, then translate to coords relative to this origin. also populate the orientation value.
 * @param segments
 */
function transformFromAbsolute(segments) {
    var sx = segments[0][5], sy = segments[0][6], tx = segments[segments.length - 1][7], ty = segments[segments.length - 1][8], dx = tx >= sx ? sx : tx, dy = ty >= sy ? sy : ty;
    segments.forEach(function (segment) {
        segment[0] = segment[5] - dx;
        segment[1] = segment[6] - dy;
        segment[2] = segment[7] - dx;
        segment[3] = segment[8] - dy;
        if (segment[4] == null || segment[4].length === 0) {
            segment[4] = segment[5] === segment[7] ? VERTICAL : HORIZONTAL;
        }
    });
    return segments;
}
function findSegment(segments, dir, axis, segment) {
    var candidate = null, start;
    if (segment != null) {
        start = segments.indexOf(segment);
        // if segment not found, return null
        if (start === -1) {
            return null;
        }
        else {
            // otherwise shift one in the appropriate direction to find the first segment to test
            start += dir;
        }
    }
    else {
        start = dir === NEGATIVE ? segments.length - 2 : 1;
    }
    for (var i = start; i > 0 && i < segments.length - 1; i += dir) {
        if (segments[i][4] === axis) {
            candidate = [segments[i], i];
            break;
        }
    }
    return candidate;
}
/**
 * Flowchart connector, editable.
 */
var EditableFlowchart = /** @class */ (function () {
    function EditableFlowchart(params) {
        params = params || {};
        params.stub = params.stub == null ? 30 : params.stub;
        this.type = FLOWCHART_TYPE_DESCRIPTOR;
        this._super = _jp.Connectors.AbstractConnector.apply(this, arguments);
        this.midpoint = params.midpoint == null ? 0.5 : params.midpoint;
        this.alwaysRespectStubs = params.alwaysRespectStubs === true;
        this.lastx = null;
        this.lasty = null;
        this.lastOrientation = null;
        this.cornerRadius = params.cornerRadius != null ? params.cornerRadius : 0;
        this.trimThreshold = params.trimThreshold == null ? 5 : params.trimThreshold;
        this.loopbackRadius = params.loopbackRadius || 25;
        this.isLoopbackCurrently = false;
    }
    // TODO refactor to a single method? setGeometry is used by the original paint code. setGeometryNew is used by
    // the edit code. the original paint code should probably work in absolute coordinates and then this method could
    // always run the transform (or vice versa?)
    EditableFlowchart.prototype.setGeometry = function (g, internal) {
        this.geometry = g;
        this.edited = g != null && !internal;
    };
    EditableFlowchart.prototype.setAndTransformGeometry = function (g) {
        g.segments = transformFromAbsolute(g.segments);
        this.setGeometry(g, false);
    };
    EditableFlowchart.prototype.setAndTransformSegments = function (s) {
        if (this.geometry != null) {
            this.geometry.segments = transformFromAbsolute(s);
        }
    };
    /**
     * export the current geometry in a format that _importGeometry can handle. this connector exports
     * the source/target points as `source` and `target` respectively, as well as an array labelled
     * `segments`, which is the list of corner points.  There are, therefore, n+1 segments in a geometry
     * whose segments array contains n entries.
     * @returns {any}
     */
    EditableFlowchart.prototype.exportGeometry = function () {
        if (this.geometry == null) {
            return null;
        }
        else {
            var l = this.geometry.segments.length, lp = this.geometry.segments[l - 1], target = [lp[7], lp[8]];
            var segs = this.geometry.segments.slice(1).map(function (seg) { return [seg[5], seg[6]]; });
            return {
                segments: segs,
                source: this.geometry.source,
                target: this.geometry.target
            };
        }
    };
    EditableFlowchart.prototype._importGeometry = function (geometry) {
        if (geometry != null && geometry.segments != null && geometry.source != null && geometry.target != null) {
            var segments = geometry.segments;
            if (segments != null && segments.length >= 3) {
                var s = [], cx = geometry.source[0], cy = geometry.source[1];
                for (var i = 0; i < segments.length; i++) {
                    // if not in X or Y axis, abort.
                    if (segments[i][0] - cx === 0 || segments[i][1] - cy === 0) {
                        s.push([0, 0, 0, 0, null, cx, cy, segments[i][0], segments[i][1]]);
                        cx = segments[i][0];
                        cy = segments[i][1];
                    }
                    else {
                        console.log("Invalid path segment", cx, cy, segments[i][0], segments[i][1], "not in X or Y axis");
                        return;
                    }
                }
                s.push([0, 0, 0, 0, null, cx, cy, geometry.target[0], geometry.target[1]]);
                this.setAndTransformGeometry({ segments: s, source: geometry.source, target: geometry.target });
                return true;
            }
        }
        return false;
    };
    EditableFlowchart.prototype._clearEdits = function () {
        this.geometry = null;
        this.edited = false;
    };
    EditableFlowchart.prototype.isEdited = function () {
        return this.edited;
    };
    EditableFlowchart.prototype.isEditable = function () { return true; };
    EditableFlowchart.prototype.writeSegments = function (conn, segments, paintInfo) {
        this.paintInfo = paintInfo;
        var current = null, next, currentDirection, nextDirection;
        for (var i = 0; i < segments.length - 1; i++) {
            current = current || _cloneSegment(segments[i]);
            next = _cloneSegment(segments[i + 1]);
            currentDirection = segmentDirections(current);
            nextDirection = segmentDirections(next);
            if (this.cornerRadius > 0 && current[4] !== next[4]) {
                var minSegLength = Math.min(segLength(current), segLength(next));
                var radiusToUse = Math.min(this.cornerRadius, minSegLength / 2);
                current[2] -= currentDirection[0] * radiusToUse;
                current[3] -= currentDirection[1] * radiusToUse;
                next[0] += nextDirection[0] * radiusToUse;
                next[1] += nextDirection[1] * radiusToUse;
                var ac = (currentDirection[1] === nextDirection[0] && nextDirection[0] === 1) ||
                    ((currentDirection[1] === nextDirection[0] && nextDirection[0] === 0) && currentDirection[0] !== nextDirection[1]) ||
                    (currentDirection[1] === nextDirection[0] && nextDirection[0] === -1), sgny = next[1] > current[3] ? 1 : -1, sgnx = next[0] > current[2] ? 1 : -1, sgnEqual = sgny === sgnx, cx = (sgnEqual && ac || (!sgnEqual && !ac)) ? next[0] : current[2], cy = (sgnEqual && ac || (!sgnEqual && !ac)) ? current[3] : next[1];
                this._super.addSegment(conn, STRAIGHT, {
                    x1: current[0], y1: current[1], x2: current[2], y2: current[3]
                });
                this._super.addSegment(conn, ARC, {
                    r: radiusToUse,
                    x1: current[2],
                    y1: current[3],
                    x2: next[0],
                    y2: next[1],
                    cx: cx,
                    cy: cy,
                    ac: ac
                });
            }
            else {
                // dx + dy are used to adjust for line width.
                var dx = (current[2] === current[0]) ? 0 : (current[2] > current[0]) ? (paintInfo.lw / 2) : -(paintInfo.lw / 2), dy = (current[3] === current[1]) ? 0 : (current[3] > current[1]) ? (paintInfo.lw / 2) : -(paintInfo.lw / 2);
                this._super.addSegment(conn, STRAIGHT, {
                    x1: current[0] - dx, y1: current[1] - dy, x2: current[2] + dx, y2: current[3] + dy
                });
            }
            current = next;
        }
        if (next != null) {
            // last segment
            this._super.addSegment(conn, STRAIGHT, {
                x1: next[0], y1: next[1], x2: next[2], y2: next[3]
            });
        }
    };
    ;
    EditableFlowchart.prototype._compute = function (paintInfo, params) {
        var _this = this;
        this.segments = [];
        this.lastx = null;
        this.lasty = null;
        this.lastOrientation = null;
        var sp = params.sourcePos, tp = params.targetPos;
        var geometry = this.geometry;
        if (this.isEdited() && geometry != null && geometry.segments != null && geometry.segments.length > 0) {
            this.segments = geometry.segments;
            var sourceMoved = !positionEquals(params.sourcePos, geometry.source), targetMoved = !positionEquals(params.targetPos, geometry.target);
            if (targetMoved) {
                var ls = this.segments[this.segments.length - 1];
                var lastTargetVertical = findSegment(this.segments, -1, VERTICAL);
                var lastTargetHorizontal = findSegment(this.segments, -1, HORIZONTAL);
                ls[5] = (params.targetPos[0] + (paintInfo.stubs[1] * paintInfo.to[0]));
                ls[6] = (params.targetPos[1] + (paintInfo.stubs[1] * paintInfo.to[1]));
                ls[7] = params.targetPos[0];
                ls[8] = params.targetPos[1];
                // TODO we need to ensure that orientation will always be clamped to [0,1] to be certain that this is correct.
                ls[4] = params.targetOrientation[1] === 0 ? "h" : "v";
                //*
                if (lastTargetVertical != null && lastTargetHorizontal != null) {
                    if (lastTargetVertical[1] > lastTargetHorizontal[1]) {
                        // if the vertical segment came after the horizontal, set its X values to the end of the horizontal and dont move the horizontal
                        lastTargetVertical[0][5] = ls[5];
                        lastTargetVertical[0][7] = ls[5];
                        lastTargetVertical[0][8] = ls[6];
                        lastTargetHorizontal[0][7] = ls[5];
                    }
                    else {
                        // otherwise set the horizontal's vertical values
                        lastTargetHorizontal[0][6] = ls[6];
                        lastTargetHorizontal[0][8] = ls[6];
                        lastTargetHorizontal[0][7] = ls[5];
                        lastTargetVertical[0][8] = ls[6];
                    }
                }
                this.segments = transformFromAbsolute(this.segments);
            }
            if (sourceMoved) {
                var ls2 = this.segments[0];
                var firstSourceVertical = findSegment(this.segments, 1, VERTICAL);
                var firstSourceHorizontal = findSegment(this.segments, 1, HORIZONTAL);
                ls2[5] = params.sourcePos[0];
                ls2[6] = params.sourcePos[1];
                ls2[7] = (params.sourcePos[0] + (paintInfo.stubs[0] * paintInfo.so[0]));
                ls2[8] = (params.sourcePos[1] + (paintInfo.stubs[0] * paintInfo.so[1]));
                // TODO we need to ensure that orientation will always be clamped to [0,1] to be certain that this is correct.
                ls2[4] = params.sourceOrientation[1] === 0 ? "h" : "v";
                if (firstSourceVertical != null && firstSourceHorizontal != null) {
                    if (firstSourceVertical[1] > firstSourceHorizontal[1]) {
                        firstSourceHorizontal[0][6] = ls2[8];
                        firstSourceHorizontal[0][8] = ls2[8];
                        firstSourceHorizontal[0][5] = ls2[7];
                        firstSourceVertical[0][6] = ls2[8];
                    }
                    else {
                        firstSourceVertical[0][5] = ls2[7];
                        firstSourceVertical[0][7] = ls2[7];
                        firstSourceVertical[0][6] = ls2[8];
                        firstSourceHorizontal[0][5] = ls2[7];
                    }
                }
                this.segments = transformFromAbsolute(this.segments);
            }
            this.setGeometry({
                segments: this.segments,
                source: params.sourcePos.concat(params.sourceOrientation),
                target: params.targetPos.concat(params.targetOrientation),
                quadrant: paintInfo.segment
            }, false);
        }
        else {
            var dx = tp[0] >= sp[0] ? sp[0] : tp[0], dy = tp[1] >= sp[1] ? sp[1] : tp[1];
            var stubCalculators = new Map([
                ["perpendicular", commonStubCalculator],
                ["orthogonal", commonStubCalculator],
                ["opposite", function (paintInfo, alwaysRespectStubs) {
                        var pi = paintInfo, idx = pi.sourceAxis === "x" ? 0 : 1, areInProximity = {
                            "x": function () {
                                return ((pi.so[idx] === 1 && (((pi.startStubX > pi.endStubX) && (pi.tx > pi.startStubX)) ||
                                    ((pi.sx > pi.endStubX) && (pi.tx > pi.sx))))) ||
                                    ((pi.so[idx] === -1 && (((pi.startStubX < pi.endStubX) && (pi.tx < pi.startStubX)) ||
                                        ((pi.sx < pi.endStubX) && (pi.tx < pi.sx)))));
                            },
                            "y": function () {
                                return ((pi.so[idx] === 1 && (((pi.startStubY > pi.endStubY) && (pi.ty > pi.startStubY)) ||
                                    ((pi.sy > pi.endStubY) && (pi.ty > pi.sy))))) ||
                                    ((pi.so[idx] === -1 && (((pi.startStubY < pi.endStubY) && (pi.ty < pi.startStubY)) ||
                                        ((pi.sy < pi.endStubY) && (pi.ty < pi.sy)))));
                            }
                        };
                        if (!alwaysRespectStubs && areInProximity[pi.sourceAxis]()) {
                            return {
                                "x": [(paintInfo.sx + paintInfo.tx) / 2, paintInfo.startStubY, (paintInfo.sx + paintInfo.tx) / 2, paintInfo.endStubY],
                                "y": [paintInfo.startStubX, (paintInfo.sy + paintInfo.ty) / 2, paintInfo.endStubX, (paintInfo.sy + paintInfo.ty) / 2]
                            }[pi.sourceAxis];
                        }
                        else {
                            return [paintInfo.startStubX, paintInfo.startStubY, paintInfo.endStubX, paintInfo.endStubY];
                        }
                    }]
            ]);
            // calculate Stubs.
            var stubs = stubCalculators.get(paintInfo.anchorOrientation)(paintInfo, this.alwaysRespectStubs), idx_1 = paintInfo.sourceAxis === "x" ? 0 : 1, oidx = paintInfo.sourceAxis === "x" ? 1 : 0, ss = stubs[idx_1], oss = stubs[oidx], es = stubs[idx_1 + 2], oes = stubs[oidx + 2];
            // add the start stub segment. use stubs for loopback as it will look better, with the loop spaced
            // away from the element.
            addSegment(this, stubs[0], stubs[1], paintInfo, dx, dy);
            // if its a loopback and we should treat it differently.
            // if (false &&params.sourcePos[0] === params.targetPos[0] && params.sourcePos[1] === params.targetPos[1]) {
            //
            //     // we use loopbackRadius here, as statemachine connectors do.
            //     // so we go radius to the left from stubs[0], then upwards by 2*radius, to the right by 2*radius,
            //     // down by 2*radius, left by radius.
            //     addSegment(this, stubs[0] - this.loopbackRadius, stubs[1], paintInfo);
            //     addSegment(this, stubs[0] - this.loopbackRadius, stubs[1] - (2 * this.loopbackRadius), paintInfo);
            //     addSegment(this, stubs[0] + this.loopbackRadius, stubs[1] - (2 * this.loopbackRadius), paintInfo);
            //     addSegment(this, stubs[0] + this.loopbackRadius, stubs[1], paintInfo);
            //     addSegment(this, stubs[0], stubs[1], paintInfo);
            //
            // }
            // else {
            var midx_1 = paintInfo.startStubX + ((paintInfo.endStubX - paintInfo.startStubX) * this.midpoint), midy_1 = paintInfo.startStubY + ((paintInfo.endStubY - paintInfo.startStubY) * this.midpoint);
            var orientations_1 = { x: [0, 1], y: [1, 0] }, lineCalculators = {
                "perpendicular": function (pi, axis) {
                    var //pi = paintInfo,
                    sis = {
                        x: [
                            [[1, 2, 3, 4], null, [2, 1, 4, 3]],
                            null,
                            [[4, 3, 2, 1], null, [3, 4, 1, 2]]
                        ],
                        y: [
                            [[3, 2, 1, 4], null, [2, 3, 4, 1]],
                            null,
                            [[4, 1, 2, 3], null, [1, 4, 3, 2]]
                        ]
                    }, stubs = {
                        x: [[pi.startStubX, pi.endStubX], null, [pi.endStubX, pi.startStubX]],
                        y: [[pi.startStubY, pi.endStubY], null, [pi.endStubY, pi.startStubY]]
                    }, midLines = {
                        x: [[midx_1, pi.startStubY], [midx_1, pi.endStubY]],
                        y: [[pi.startStubX, midy_1], [pi.endStubX, midy_1]]
                    }, linesToEnd = {
                        x: [[pi.endStubX, pi.startStubY]],
                        y: [[pi.startStubX, pi.endStubY]]
                    }, startToEnd = {
                        x: [[pi.startStubX, pi.endStubY], [pi.endStubX, pi.endStubY]],
                        y: [[pi.endStubX, pi.startStubY], [pi.endStubX, pi.endStubY]]
                    }, startToMidToEnd = {
                        x: [[pi.startStubX, midy_1], [pi.endStubX, midy_1], [pi.endStubX, pi.endStubY]],
                        y: [[midx_1, pi.startStubY], [midx_1, pi.endStubY], [pi.endStubX, pi.endStubY]]
                    }, otherStubs = {
                        x: [pi.startStubY, pi.endStubY],
                        y: [pi.startStubX, pi.endStubX]
                    }, soIdx = orientations_1[axis][0], toIdx = orientations_1[axis][1], _so = pi.so[soIdx] + 1, _to = pi.to[toIdx] + 1, otherFlipped = (pi.to[toIdx] === -1 && (otherStubs[axis][1] < otherStubs[axis][0])) || (pi.to[toIdx] === 1 && (otherStubs[axis][1] > otherStubs[axis][0])), stub1 = stubs[axis][_so][0], stub2 = stubs[axis][_so][1], segmentIndexes = sis[axis][_so][_to];
                    if (pi.segment === segmentIndexes[3] || (pi.segment === segmentIndexes[2] && otherFlipped)) {
                        return midLines[axis];
                    }
                    else if (pi.segment === segmentIndexes[2] && stub2 < stub1) {
                        return linesToEnd[axis];
                    }
                    else if ((pi.segment === segmentIndexes[2] && stub2 >= stub1) || (pi.segment === segmentIndexes[1] && !otherFlipped)) {
                        return startToMidToEnd[axis];
                    }
                    else if (pi.segment === segmentIndexes[0] || (pi.segment === segmentIndexes[1] && otherFlipped)) {
                        return startToEnd[axis];
                    }
                },
                "orthogonal": function (pi, axis, startStub, otherStartStub, endStub, otherEndStub) {
                    var //pi = paintInfo,
                    extent = {
                        "x": pi.so[0] === -1 ? Math.min(startStub, endStub) : Math.max(startStub, endStub),
                        "y": pi.so[1] === -1 ? Math.min(startStub, endStub) : Math.max(startStub, endStub)
                    }[axis];
                    return {
                        "x": [
                            [extent, otherStartStub],
                            [extent, otherEndStub],
                            [endStub, otherEndStub]
                        ],
                        "y": [
                            [otherStartStub, extent],
                            [otherEndStub, extent],
                            [otherEndStub, endStub]
                        ]
                    }[axis];
                },
                "opposite": function (pi, axis, ss, oss, es) {
                    var //pi = paintInfo,
                    otherAxis = { "x": "y", "y": "x" }[axis], dim = { "x": "height", "y": "width" }[axis], comparator = pi["is" + axis.toUpperCase() + "GreaterThanStubTimes2"];
                    if (params.sourceEndpoint.elementId === params.targetEndpoint.elementId) {
                        var _val = oss + ((1 - params.sourceEndpoint.anchor[otherAxis]) * params.sourceInfo[dim]) + _this.maxStub;
                        return {
                            "x": [
                                [ss, _val],
                                [es, _val]
                            ],
                            "y": [
                                [_val, ss],
                                [_val, es]
                            ]
                        }[axis];
                    }
                    else if (!comparator || (pi.so[idx_1] === 1 && ss > es) || (pi.so[idx_1] === -1 && ss < es)) {
                        return {
                            "x": [
                                [ss, midy_1],
                                [es, midy_1]
                            ],
                            "y": [
                                [midx_1, ss],
                                [midx_1, es]
                            ]
                        }[axis];
                    }
                    else if ((pi.so[idx_1] === 1 && ss < es) || (pi.so[idx_1] === -1 && ss > es)) {
                        return {
                            "x": [
                                [midx_1, pi.sy],
                                [midx_1, pi.ty]
                            ],
                            "y": [
                                [pi.sx, midy_1],
                                [pi.tx, midy_1]
                            ]
                        }[axis];
                    }
                }
            };
            // compute the rest of the line
            var p = lineCalculators[paintInfo.anchorOrientation](paintInfo, paintInfo.sourceAxis, ss, oss, es, oes);
            if (p) {
                for (var i = 0; i < p.length; i++) {
                    addSegment(this, p[i][0], p[i][1], paintInfo, dx, dy);
                }
            }
            // line to end stub
            addSegment(this, stubs[2], stubs[3], paintInfo, dx, dy);
            //}
            // end stub to end (common)
            addSegment(this, paintInfo.tx, paintInfo.ty, paintInfo, dx, dy);
            this.setGeometry({
                segments: this.segments,
                source: params.sourcePos.concat(params.sourceOrientation),
                target: params.targetPos.concat(params.targetOrientation),
                quadrant: paintInfo.segment
            }, true);
        }
        // write out the segments.
        this.writeSegments(this, this.segments, paintInfo);
    };
    /**
     * For a given segment, find it - and its index - inside our current list.
     * @param {Segment} segment The segment to locate
     * @param {boolean} [findRelatives] If true, look also for segments with the same orientation in both forwards and backwards directions. These latter are used when
     * trying to decide of a segment can be deleted.
     * @returns {SegmentContext} If found, a context object containing the segment, its index, its previous/next segments (if defined),
     * and optionally (if requested) segments with the same orientation in both forwards and backwards directions. These latter are used when
     * trying to decide of a segment can be deleted.
     * @private
     */
    EditableFlowchart.prototype._locateSegment = function (segment, findRelatives) {
        var idx = this.segments.findIndex(function (g) { return g[5] === segment[5] && g[6] === segment[6] && g[7] === segment[7] && g[8] === segment[8]; });
        if (idx > -1) {
            var o = this.segments[idx][4], s = this.segments[idx];
            return {
                segment: s,
                index: idx,
                orientation: o,
                prev: idx > 1 ? this.segments[idx - 1] : null,
                next: idx < this.segments.length - 2 ? this.segments[idx + 1] : null,
                left: findRelatives ? findSegment(this.segments, -1, o, s) : null,
                right: findRelatives ? findSegment(this.segments, 1, o, s) : null
            };
        }
        else {
            return null;
        }
    };
    EditableFlowchart.prototype.setSegmentPosition = function (segment, pos) {
        var ctx = this._locateSegment(segment);
        if (ctx != null) {
            if (ctx.orientation === VERTICAL) {
                ctx.segment[5] = ctx.segment[7] = pos[0];
            }
            else {
                ctx.segment[6] = ctx.segment[8] = pos[1];
            }
            var currentVertical = ctx.orientation === VERTICAL;
            var idx = ctx.index;
            var originalIndex = ctx.index;
            // go back through the segment list to the first segment, adjusting end positions as we go, starting at the
            // segment before this one. we ignore the stubs. if, when adjusting a previous segment, it is discovered to now be
            // of length 0, it is removed.
            var previous = idx > 1 ? this.segments[idx - 1] : null, current = ctx.segment;
            while (previous != null) {
                if (previous[4] === current[4]) {
                    previous[currentVertical ? 5 : 6] = current[currentVertical ? 5 : 6];
                    previous[currentVertical ? 7 : 8] = current[currentVertical ? 7 : 8];
                }
                else {
                    previous[7] = current[5];
                    previous[8] = current[6];
                }
                current = previous;
                idx--;
                previous = idx > 1 ? this.segments[idx - 1] : null;
            }
            if (current[5] !== this.segments[0][7]) {
                var newSegment = [null, null, null, null, HORIZONTAL, this.segments[0][7], this.segments[0][8], current[5], current[6]];
                this.segments.splice(1, 0, newSegment);
                originalIndex++;
            }
            else if (current[6] !== this.segments[0][8]) {
                var newSegment = [null, null, null, null, VERTICAL, this.segments[0][7], this.segments[0][8], current[5], current[6]];
                this.segments.splice(1, 0, newSegment);
                originalIndex++;
            }
            current = ctx.segment;
            idx = ctx.index;
            var next = idx < this.segments.length - 2 ? this.segments[idx + 1] : null;
            while (next != null) {
                if (next[4] === current[4]) {
                    next[currentVertical ? 5 : 6] = current[currentVertical ? 5 : 6];
                    next[currentVertical ? 7 : 8] = current[currentVertical ? 7 : 8];
                }
                else {
                    next[5] = current[7];
                    next[6] = current[8];
                }
                current = next;
                idx++;
                next = idx < this.segments.length - 2 ? this.segments[idx + 1] : null;
            }
            var endStub = this.segments[this.segments.length - 1];
            if (current[7] !== endStub[5]) {
                var newSegment = [null, null, null, null, HORIZONTAL, current[7], current[8], endStub[5], endStub[6]];
                this.segments.splice(this.segments.length - 1, 0, newSegment);
            }
            else if (current[8] !== endStub[6]) {
                var newSegment = [null, null, null, null, VERTICAL, current[7], current[8], endStub[5], endStub[6]];
                this.segments.splice(this.segments.length - 1, 0, newSegment);
            }
            this.segments = transformFromAbsolute(this.segments);
            this.edited = true;
            return {
                ctx: ctx,
                segments: this.segments,
                index: originalIndex
            };
        }
        else {
            return null;
        }
    };
    EditableFlowchart.prototype.trim = function () {
        // attempt #3: keep the first and last segments and filter anything in between
        var out = [jsPlumbUtil.clone(this.segments[0])];
        var final = jsPlumbUtil.clone(this.segments[this.segments.length - 1]);
        var s2 = this.segments.slice(1, this.segments.length - 1).filter(function (s) { return segLength(s) > 0; }).map(jsPlumbUtil.clone);
        var prev = null;
        var prevOrientation = null;
        for (var i = 0; i < s2.length; i++) {
            if (prev == null || prevOrientation == null) {
                prev = s2[i];
                prevOrientation = s2[i][4];
            }
            else {
                if (s2[i][4] === prevOrientation) {
                    prev[3] = s2[i][3];
                    prev[2] = s2[i][2];
                    prev[8] = s2[i][8];
                    prev[7] = s2[i][7];
                }
                else {
                    out.push(prev);
                    prev = s2[i];
                    prevOrientation = s2[i][4];
                }
            }
        }
        out.push(prev);
        out.push(final);
        // if only 3 segments, put placeholder empty segments in, to preserve the stubs.
        if (out.length === 3) {
            var midSegment = out[1], mido = midSegment[4];
            var ns1 = jsPlumbUtil.clone(midSegment), ns2 = jsPlumbUtil.clone(midSegment), ns3 = jsPlumbUtil.clone(midSegment);
            ns2[4] = mido === "h" ? "v" : "h";
            ns2[0] = ns1[0];
            ns2[1] = ns1[1];
            ns2[2] = ns1[0];
            ns2[3] = ns1[1];
            ns2[5] = ns1[5];
            ns2[6] = ns1[6];
            ns2[7] = ns1[5];
            ns2[8] = ns1[6];
            ns3[4] = mido === "h" ? "v" : "h";
            ns3[0] = ns1[2];
            ns3[1] = ns1[3];
            ns3[2] = ns1[2];
            ns3[3] = ns1[3];
            ns3[5] = ns1[7];
            ns3[6] = ns1[8];
            ns3[7] = ns1[7];
            ns3[8] = ns1[8];
            out = [out[0], ns2, ns1, ns3, out[2]];
        }
        this.setAndTransformSegments(out);
    };
    EditableFlowchart.prototype.setAnchorOrientation = function (idx, orientation) {
        if (this.segments.length >= 2) {
            var segment = idx === 0 ? this.segments[0] : this.segments[this.segments.length - 1];
            var o = orientation[0] === 0 ? VERTICAL : HORIZONTAL;
            segment[4] = o;
        }
    };
    return EditableFlowchart;
}());
_jp.Connectors[FLOWCHART_TYPE_DESCRIPTOR] = EditableFlowchart;
_ju.extend(EditableFlowchart, _jp.Connectors.AbstractEditableConnector);
var FLOWCHART_HANDLE_CLASS = "jtk-flowchart-handle";
var SEGMENT_DRAG_HANDLE = "jtk-flowchart-segment-drag";
var SEGMENT_DRAG_HANDLE_VERTICAL_CLASS = "jtk-flowchart-segment-drag-ns";
var SEGMENT_DRAG_HANDLE_HORIZONTAL_CLASS = "jtk-flowchart-segment-drag-ew";
function _makeHandle(x, y, clazz, visible) {
    var h = document.createElement("div");
    h.className = clazz;
    h.style.position = ABSOLUTE;
    h.style.left = x + PX;
    h.style.top = y + PX;
    if (!visible) {
        h.style.display = NONE;
    }
    return h;
}
function _makeAndAppendHandle(x, y, _jsPlumb, clazz, visible) {
    var h = _makeHandle(x, y, clazz, visible);
    _jsPlumb.appendElement(h);
    var s = _jsPlumb.getSize(h);
    h.style.left = (x - (s[0] / 2)) + "px";
    h.style.top = (y - (s[1] / 2)) + "px";
    return h;
}
function _updateGuideline(handle, anchor, line, x, y) {
    x = x + (handle.offsetWidth / 2);
    y = y + (handle.offsetHeight / 2);
    var w = Math.max(5, Math.abs(x - anchor.left)), h = Math.max(5, Math.abs(y - anchor.top));
    jsPlumbUtil.svg.attr(line, { width: w, height: h });
    line.style.left = (Math.min(anchor.left, x)) + PX;
    line.style.top = (Math.min(anchor.top, y)) + PX;
    var path = "M " + (x > anchor.left ? w : "0") + " " + (y > anchor.top ? h : "0") + " L " +
        (x > anchor.left ? "0" : w) + " " + (y > anchor.top ? "0" : h);
    jsPlumbUtil.svg.attr(line.childNodes[0], { d: path });
}
function _makeGuideline(handle, anchor, x2, y2) {
    var w = Math.abs(x2 - anchor.left), h = Math.abs(y2 - anchor.top), s = _ju.svg.node("svg", { width: w, height: h }), l = _ju.svg.node("path", { d: "M " + 0 + " " + 0 + " L " + w + " " + h });
    s.appendChild(l);
    _jp.addClass(s, CLASS_BEZIER_GUIDELINE);
    _updateGuideline(handle, anchor, s, x2, y2);
    return s;
}
var FlowchartEditor = /** @class */ (function (_super_1) {
    __extends(FlowchartEditor, _super_1);
    // repaintConnection:(args?:any)=>void;
    // _setElementPosition:(handle:HTMLElement, x:number, y:number)=>void;
    // fireConnectionEditEvent:()=>void;
    function FlowchartEditor(params) {
        var _this = _super_1.call(this, params) || this;
        _this.segments = [];
        _this.segmentHandles = [];
        //this.self = this;
        /**
         * Attaches a delegated drag listener for segment handles. When dragged,
         * a handle is constrained to move in the perpendicular axis to that of the segment,
         * and each time it moves the underlying editable flowchart connector is informed.
         * It is the connector itself that decides what happens to the path; it returns the
         * new full list of segments from the `setSegmentPosition` method. This drag handler
         * then stores the new geometry for the segment being dragged, and calls
         * `repaintConnection`, which is a method on the superclass. We pass in the current
         * segment to this method, which itself calls `repaint` on the Connection, passing in
         * any parameters we gave it.
         *
         * This method - or at least the behaviour of this method - is
         * specific to the flowchart editor. the bezier editor also
         * support handle dragging, but it does different stuff.
         */
        _this._addDragHandler({
            selector: dot(SEGMENT_DRAG_HANDLE),
            drag: function (dp) {
                var segmentInfo = dp.drag.getDragElement()._jsPlumbDragHandle;
                var s = _this._jsPlumb.getSize(segmentInfo.el);
                var p = [Math.floor(dp.pos[0] + (s[0] / 2)), Math.floor(dp.pos[1] + (s[1] / 2))];
                var moveResult = _this.current.connector.setSegmentPosition(segmentInfo.geometry, p);
                if (moveResult != null) {
                    // the move result contains the new set of segments, plus the index of the segment that was moved; this index
                    // might have changed because of a segment being added or deleted. so we stash the new list of segments,
                    // and we also update the geometry of the current moving segment with the updated value from the connector.
                    _this.segments.length = 0;
                    _this.geometry.segments = moveResult.segments;
                    Array.prototype.push.apply(_this.segments, _this.geometry.segments);
                    segmentInfo.geometry = _this.geometry.segments[moveResult.index];
                    // now we need to redraw everything except the current segment.
                    _this.repaintConnection({ segmentInfo: segmentInfo, segmentIndex: moveResult.index });
                }
            },
            constrain: function (desiredLoc, dragEl, dim, dragElSize) {
                var segmentInfo = dragEl._jsPlumbDragHandle;
                var vertical = segmentInfo.geometry[5] === segmentInfo.geometry[7];
                if (vertical) {
                    return [
                        desiredLoc[0],
                        ((segmentInfo.geometry[6] + segmentInfo.geometry[8]) / 2) - (dragElSize[1] / 2)
                    ];
                }
                else {
                    return [
                        ((segmentInfo.geometry[5] + segmentInfo.geometry[7]) / 2) - (dragElSize[0] / 2),
                        desiredLoc[1]
                    ];
                }
            },
            stop: function () {
                _this._trimConnection();
                _this.fireConnectionEditEvent();
            }
        });
        return _this;
    }
    FlowchartEditor.prototype._setHandlePosition = function (segmentInfo, mid) {
        segmentInfo.el.style.visibility = "visible";
        this._setElementPosition(segmentInfo.el, mid[0], mid[1]);
    };
    /**
     * Repaint the editor. This may or may not have come
     * about as the result of a call by this class to `repaintConnection` - if
     * `internalEditorRepaint` and/or `args` is set, then that is the case.
     * @override
     * @protected
     * @param args
     * @private
     */
    FlowchartEditor.prototype._repaint = function (args) {
        // update the connector info. args may optionally contain
        // a segment to exclude from the update, if this method
        // was called via repaintConnection in a handle drag.
        this._update(args);
        // update segment handles on screen and also their underlying geometry.
        for (var i = 0; i < this.segmentHandles.length; i++) {
            this.segmentHandles[i].geometry = this.geometry.segments[i + 1]; // NOTE here the +1 - we ignore the source stub segment.
            if (segLength(this.segmentHandles[i].geometry) > 0) {
                var mid = [(this.segmentHandles[i].geometry[5] + this.segmentHandles[i].geometry[7]) / 2, (this.segmentHandles[i].geometry[6] + this.segmentHandles[i].geometry[8]) / 2];
                this._setHandlePosition(this.segmentHandles[i], mid);
            }
            else {
                this.segmentHandles[i].el.style.visibility = "hidden";
            }
        }
    };
    /**
     * clear all handles, except, optionally, the one provided.
     * @param excludeHandle
     * @protected
     * @override
     */
    FlowchartEditor.prototype._clearHandles = function (excludeHandle) {
        for (var i = 0; i < this.segmentHandles.length; i++) {
            if (this.segmentHandles[i].el !== excludeHandle) {
                this._jsPlumb.remove(this.segmentHandles[i].el, true);
            }
        }
    };
    /**
     * Activates the editor, on the given connection.
     * @override
     * @param conn
     * @private
     */
    FlowchartEditor.prototype._activate = function (surface, conn) {
        this._update();
    };
    FlowchartEditor.prototype._elementDragged = function (p) {
        this._trimConnection();
    };
    FlowchartEditor.prototype._elementDragging = function (p) { };
    /**
     * updates the current origin of the connector's SVG element (the location of its to left corner wrt
     * the origin of the jsplumb instance's container). Then updates the offset of the source and target points
     * from the origin of the SVG element. Finally, extracts the control point information from the connection,
     * either as geometry (if previously edited or set) or from the computed control points.
     * @override
     * @protected
     */
    FlowchartEditor.prototype._update = function (args) {
        args = args || {};
        var excludeSegment = args.segmentInfo, excludeIndex = args.segmentIndex;
        this.geometry = this.current.getConnector().geometry;
        if (this.geometry && this.geometry.segments) {
            this._clearHandles(excludeSegment ? excludeSegment.el : null);
            this.segmentHandles.length = 0;
            this.segments.length = 0;
            Array.prototype.push.apply(this.segments, this.geometry.segments);
            for (var i = 1; i < this.segments.length - 1; i++) {
                if (excludeSegment == null || i !== excludeIndex) {
                    var mid = [(this.segments[i][5] + this.segments[i][7]) / 2, (this.segments[i][6] + this.segments[i][8]) / 2], handleLeft = mid[0], handleTop = mid[1], vertical = this.segments[i][4] === VERTICAL, handle = _makeAndAppendHandle(handleLeft, handleTop, this._jsPlumb, [FLOWCHART_HANDLE_CLASS, SEGMENT_DRAG_HANDLE, (vertical ? SEGMENT_DRAG_HANDLE_HORIZONTAL_CLASS : SEGMENT_DRAG_HANDLE_VERTICAL_CLASS)].join(" "), true);
                    var segmentInfo = {
                        left: handleLeft,
                        top: handleTop,
                        el: handle,
                        geometry: this.segments[i],
                        vertical: vertical
                    };
                    handle._jsPlumbDragHandle = segmentInfo;
                    this.segmentHandles.push(segmentInfo);
                    this._setHandlePosition(segmentInfo, mid);
                }
                else if (i === excludeIndex) {
                    this.segmentHandles.push(excludeSegment);
                }
            }
        }
    };
    /**
     * Trims any segments that are now of length zero, then
     * concatenates subsequent segments that are in the same axis.
     * then instructs the superclass to repaint (which will
     * result in this class redrawing all its handles)
     * @private
     */
    FlowchartEditor.prototype._trimConnection = function () {
        if (this.current) {
            this.current.getConnector().trim();
            this.repaintConnection();
        }
    };
    return FlowchartEditor;
}(EditorBase));
// ----------------------------------- / FLOWCHART EDITOR -----------------
var AbstractBezierConnector = /** @class */ (function () {
    function AbstractBezierConnector(params) {
        params = params || {};
        this._super = _jp.Connectors.AbstractConnector.apply(this, arguments);
        this.showLoopback = params.showLoopback !== false;
        this.curviness = params.curviness || 10;
        this.margin = params.margin || 5;
        this.proximityLimit = params.proximityLimit || 80;
        this.clockwise = params.orientation && params.orientation === "clockwise";
        this.loopbackRadius = params.loopbackRadius || 25;
        this.isLoopbackCurrently = false;
    }
    // --------------- common with flowchart (and all connectors -------------
    AbstractBezierConnector.prototype.setGeometry = function (g, internal) {
        this.geometry = g;
        this.edited = g != null && !internal;
    };
    AbstractBezierConnector.prototype.getGeometry = function () {
        return this.geometry;
    };
    AbstractBezierConnector.prototype.exportGeometry = function () {
        if (this.geometry == null) {
            return null;
        }
        else {
            var s = [], t = [], cp1 = [], cp2 = [];
            Array.prototype.push.apply(s, this.geometry.source);
            Array.prototype.push.apply(t, this.geometry.target);
            Array.prototype.push.apply(cp1, this.geometry.controlPoints[0]);
            Array.prototype.push.apply(cp2, this.geometry.controlPoints[1]);
            return {
                source: s,
                target: t,
                controlPoints: [cp1, cp2]
            };
        }
    };
    AbstractBezierConnector.prototype._importGeometry = function (geometry) {
        if (geometry != null) {
            if (geometry.controlPoints == null || geometry.controlPoints.length != 2) {
                console.log("EditableBezier: cannot import geometry; controlPoints missing or does not have length 2");
                this.setGeometry(null, true);
                return false;
            }
            if (geometry.controlPoints[0].length != 2 || geometry.controlPoints[1].length != 2) {
                console.log("EditableBezier: cannot import geometry; controlPoints malformed");
                this.setGeometry(null, true);
                return false;
            }
            if (geometry.source == null || geometry.source.length != 4) {
                console.log("EditableBezier: cannot import geometry; source missing or malformed");
                this.setGeometry(null, true);
                return false;
            }
            if (geometry.target == null || geometry.target.length != 4) {
                console.log("EditableBezier: cannot import geometry; target missing or malformed");
                this.setGeometry(null, true);
                return false;
            }
            this.setGeometry(geometry, false);
            return true;
        }
        else {
            return false;
        }
    };
    AbstractBezierConnector.prototype._clearEdits = function () {
        this.geometry = null;
        this.edited = false;
    };
    AbstractBezierConnector.prototype.isEdited = function () {
        return this.edited;
    };
    AbstractBezierConnector.prototype.isEditable = function () { return true; };
    // -------------------------------------
    AbstractBezierConnector.prototype._compute = function (paintInfo, p) {
        var sp = p.sourcePos, tp = p.targetPos, _w = Math.abs(sp[0] - tp[0]), _h = Math.abs(sp[1] - tp[1]);
        if (!this.showLoopback || (p.sourceEndpoint.elementId !== p.targetEndpoint.elementId)) {
            this.isLoopbackCurrently = false;
            this._computeBezier(paintInfo, p, sp, tp, _w, _h);
        }
        else {
            this.isLoopbackCurrently = true;
            // a loopback connector.  draw an arc from one anchor to the other.
            var x1 = p.sourcePos[0], y1 = p.sourcePos[1] - this.margin, cx = x1, cy = y1 - this.loopbackRadius, 
            // canvas sizing stuff, to ensure the whole painted area is visible.
            _x = cx - this.loopbackRadius, _y = cy - this.loopbackRadius;
            _w = 2 * this.loopbackRadius;
            _h = 2 * this.loopbackRadius;
            paintInfo.points[0] = _x;
            paintInfo.points[1] = _y;
            paintInfo.points[2] = _w;
            paintInfo.points[3] = _h;
            // ADD AN ARC SEGMENT.
            this._super.addSegment(this, "Arc", {
                loopback: true,
                x1: (x1 - _x) + 4,
                y1: y1 - _y,
                startAngle: 0,
                endAngle: 2 * Math.PI,
                r: this.loopbackRadius,
                ac: !this.clockwise,
                x2: (x1 - _x) - 4,
                y2: y1 - _y,
                cx: cx - _x,
                cy: cy - _y
            });
        }
    };
    AbstractBezierConnector.prototype.setAnchorOrientation = function (idx, orientation) { };
    return AbstractBezierConnector;
}());
var Bezier = /** @class */ (function (_super_1) {
    __extends(Bezier, _super_1);
    function Bezier(params) {
        var _this = _super_1.call(this, params) || this;
        params = params || {};
        _this.type = "EditableBezier";
        _this.majorAnchor = params.curviness || 150;
        _this.minorAnchor = 10;
        return _this;
    }
    Bezier.prototype.getCurviness = function () {
        return this.majorAnchor;
    };
    ;
    Bezier.prototype._findControlPoint = function (point, sourceAnchorPosition, targetAnchorPosition, sourceEndpoint, targetEndpoint, soo, too) {
        // determine if the two anchors are perpendicular to each other in their orientation.  we swap the control
        // points around if so (code could be tightened up)
        var perpendicular = soo[0] !== too[0] || soo[1] === too[1], p = [];
        if (!perpendicular) {
            if (soo[0] === 0) {
                p.push(sourceAnchorPosition[0] < targetAnchorPosition[0] ? point[0] + this.minorAnchor : point[0] - this.minorAnchor);
            }
            else {
                p.push(point[0] - (this.majorAnchor * soo[0]));
            }
            if (soo[1] === 0) {
                p.push(sourceAnchorPosition[1] < targetAnchorPosition[1] ? point[1] + this.minorAnchor : point[1] - this.minorAnchor);
            }
            else {
                p.push(point[1] + (this.majorAnchor * too[1]));
            }
        }
        else {
            if (too[0] === 0) {
                p.push(targetAnchorPosition[0] < sourceAnchorPosition[0] ? point[0] + this.minorAnchor : point[0] - this.minorAnchor);
            }
            else {
                p.push(point[0] + (this.majorAnchor * too[0]));
            }
            if (too[1] === 0) {
                p.push(targetAnchorPosition[1] < sourceAnchorPosition[1] ? point[1] + this.minorAnchor : point[1] - this.minorAnchor);
            }
            else {
                p.push(point[1] + (this.majorAnchor * soo[1]));
            }
        }
        return p;
    };
    ;
    Bezier.prototype._computeBezier = function (paintInfo, p, sp, tp, _w, _h) {
        var _CP, _CP2, _sx = sp[0] < tp[0] ? _w : 0, _sy = sp[1] < tp[1] ? _h : 0, _tx = sp[0] < tp[0] ? 0 : _w, _ty = sp[1] < tp[1] ? 0 : _h;
        if (this.edited !== true) {
            _CP = this._findControlPoint([_sx, _sy], sp, tp, p.sourceEndpoint, p.targetEndpoint, paintInfo.so, paintInfo.to);
            _CP2 = this._findControlPoint([_tx, _ty], tp, sp, p.targetEndpoint, p.sourceEndpoint, paintInfo.to, paintInfo.so);
        }
        else {
            _CP = this.geometry.controlPoints[0];
            _CP2 = this.geometry.controlPoints[1];
        }
        this.geometry = {
            controlPoints: [_CP, _CP2],
            source: p.sourcePos,
            target: p.targetPos
        };
        this._super.addSegment(this, "Bezier", {
            x1: _sx, y1: _sy, x2: _tx, y2: _ty,
            cp1x: _CP[0], cp1y: _CP[1], cp2x: _CP2[0], cp2y: _CP2[1]
        });
    };
    ;
    return Bezier;
}(AbstractBezierConnector));
_jp.Connectors.EditableBezier = Bezier;
_ju.extend(Bezier, _jp.Connectors.AbstractEditableConnector);
var StateMachine = /** @class */ (function (_super_1) {
    __extends(StateMachine, _super_1);
    function StateMachine(params) {
        var _this = _super_1.call(this, params) || this;
        _this.type = "EditableStateMachine";
        return _this;
    }
    StateMachine.prototype._computeBezier = function (paintInfo, params, sp, tp, w, h) {
        var _sx = params.sourcePos[0] < params.targetPos[0] ? 0 : w, _sy = params.sourcePos[1] < params.targetPos[1] ? 0 : h, _tx = params.sourcePos[0] < params.targetPos[0] ? w : 0, _ty = params.sourcePos[1] < params.targetPos[1] ? h : 0;
        // now adjust for the margin
        if (params.sourcePos[2] === 0) {
            _sx -= this.margin;
        }
        if (params.sourcePos[2] === 1) {
            _sx += this.margin;
        }
        if (params.sourcePos[3] === 0) {
            _sy -= this.margin;
        }
        if (params.sourcePos[3] === 1) {
            _sy += this.margin;
        }
        if (params.targetPos[2] === 0) {
            _tx -= this.margin;
        }
        if (params.targetPos[2] === 1) {
            _tx += this.margin;
        }
        if (params.targetPos[3] === 0) {
            _ty -= this.margin;
        }
        if (params.targetPos[3] === 1) {
            _ty += this.margin;
        }
        if (this.edited !== true) {
            //
            // these connectors are quadratic bezier curves, having a single control point. if both anchors
            // are located at 0.5 on their respective faces, the control point is set to the midpoint and you
            // get a straight line.  this is also the case if the two anchors are within 'proximityLimit', since
            // it seems to make good aesthetic sense to do that. outside of that, the control point is positioned
            // at 'curviness' pixels away along the normal to the straight line connecting the two anchors.
            //
            // there may be two improvements to this.  firstly, we might actually support the notion of avoiding nodes
            // in the UI, or at least making a good effort at doing so.  if a connection would pass underneath some node,
            // for example, we might increase the distance the control point is away from the midpoint in a bid to
            // steer it around that node.  this will work within limits, but i think those limits would also be the likely
            // limits for, once again, aesthetic good sense in the layout of a chart using these connectors.
            //
            // the second possible change is actually two possible changes: firstly, it is possible we should gradually
            // decrease the 'curviness' as the distance between the anchors decreases; start tailing it off to 0 at some
            // point (which should be configurable).  secondly, we might slightly increase the 'curviness' for connectors
            // with respect to how far their anchor is from the center of its respective face. this could either look cool,
            // or stupid, and may indeed work only in a way that is so subtle as to have been a waste of time.
            //
            var _midx = (_sx + _tx) / 2, _midy = (_sy + _ty) / 2, segment = this._segment(_sx, _sy, _tx, _ty), distance = Math.sqrt(Math.pow(_tx - _sx, 2) + Math.pow(_ty - _sy, 2));
            // calculate the control point.  this code will be where we'll put in a rudimentary element avoidance scheme; it
            // will work by extending the control point to force the curve to be, um, curvier.
            this._controlPoint = this._findControlPoint(_midx, _midy, segment, params.sourcePos, params.targetPos, this.curviness, this.curviness, distance, this.proximityLimit);
        }
        else {
            // todo only writing both right now because of old editor. new editor
            // should expect this one to have single 'controlPoint' in geometry.
            this._controlPoint = this.geometry.controlPoints[0];
        }
        var cp1x, cp2x, cp1y, cp2y;
        cp1x = this._controlPoint[0];
        cp2x = this._controlPoint[0];
        cp1y = this._controlPoint[1];
        cp2y = this._controlPoint[1];
        // todo only writing both right now because of old editor. new editor
        // should expect this one to have single 'controlPoint' in geometry.
        this.geometry = {
            controlPoints: [this._controlPoint, this._controlPoint],
            source: params.sourcePos,
            target: params.targetPos
        };
        this._super.addSegment(this, "Bezier", {
            x1: _tx, y1: _ty, x2: _sx, y2: _sy,
            cp1x: cp1x, cp1y: cp1y,
            cp2x: cp2x, cp2y: cp2y
        });
    };
    StateMachine.prototype._segment = function (x1, y1, x2, y2) {
        if (x1 <= x2 && y2 <= y1) {
            return 1;
        }
        else if (x1 <= x2 && y1 <= y2) {
            return 2;
        }
        else if (x2 <= x1 && y2 >= y1) {
            return 3;
        }
        return 4;
    };
    StateMachine.prototype._findControlPoint = function (midx, midy, segment, sourceEdge, targetEdge, dx, dy, distance, proximityLimit) {
        // TODO (maybe)
        // - if anchor pos is 0.5, make the control point take into account the relative position of the elements.
        if (distance <= proximityLimit) {
            return [midx, midy];
        }
        if (segment === 1) {
            if (sourceEdge[3] <= 0 && targetEdge[3] >= 1) {
                return [midx + (sourceEdge[2] < 0.5 ? -1 * dx : dx), midy];
            }
            else if (sourceEdge[2] >= 1 && targetEdge[2] <= 0) {
                return [midx, midy + (sourceEdge[3] < 0.5 ? -1 * dy : dy)];
            }
            else {
                return [midx + (-1 * dx), midy + (-1 * dy)];
            }
        }
        else if (segment === 2) {
            if (sourceEdge[3] >= 1 && targetEdge[3] <= 0) {
                return [midx + (sourceEdge[2] < 0.5 ? -1 * dx : dx), midy];
            }
            else if (sourceEdge[2] >= 1 && targetEdge[2] <= 0) {
                return [midx, midy + (sourceEdge[3] < 0.5 ? -1 * dy : dy)];
            }
            else {
                return [midx + dx, midy + (-1 * dy)];
            }
        }
        else if (segment === 3) {
            if (sourceEdge[3] >= 1 && targetEdge[3] <= 0) {
                return [midx + (sourceEdge[2] < 0.5 ? -1 * dx : dx), midy];
            }
            else if (sourceEdge[2] <= 0 && targetEdge[2] >= 1) {
                return [midx, midy + (sourceEdge[3] < 0.5 ? -1 * dy : dy)];
            }
            else {
                return [midx + (-1 * dx), midy + (-1 * dy)];
            }
        }
        else if (segment === 4) {
            if (sourceEdge[3] <= 0 && targetEdge[3] >= 1) {
                return [midx + (sourceEdge[2] < 0.5 ? -1 * dx : dx), midy];
            }
            else if (sourceEdge[2] <= 0 && targetEdge[2] >= 1) {
                return [midx, midy + (sourceEdge[3] < 0.5 ? -1 * dy : dy)];
            }
            else {
                return [midx + dx, midy + (-1 * dy)];
            }
        }
    };
    return StateMachine;
}(AbstractBezierConnector));
_jp.Connectors.EditableStateMachine = StateMachine;
_ju.extend(StateMachine, _jp.Connectors.AbstractEditableConnector);
// --------------------------------------------- BEZIER EDITOR -----------------
var BezierEditor = /** @class */ (function (_super_1) {
    __extends(BezierEditor, _super_1);
    function BezierEditor(params) {
        var _this = _super_1.call(this, params) || this;
        _this.cp1 = [0, 0];
        _this.cp2 = [0, 0];
        _this.flipY = false;
        _this.noEdits = true;
        // this.cp = [ this.cp1, this.cp2 ];
        _this._addDragHandler({
            selector: dot(CLASS_BEZIER_HANDLE),
            drag: function (dp) {
                if (_this.noEdits) {
                    _this._setGeometry();
                    _this.noEdits = false;
                }
                var dragEl = dp.drag.getDragElement();
                var cp = dragEl._jsPlumbControlPoint;
                var l = dp.pos[0] - _this.origin[0], t = dp.pos[1] - _this.origin[1];
                if (!_this.lockHandles) {
                    cp[0] = l;
                    cp[1] = t;
                }
                else {
                    if (_this.mode === DUAL) {
                        // get radius and then get a line that is a tangent to the circle, whose length is 1.5 times
                        // the radius. This has the effect of making the curve more bulbous as you drag it out.
                        var radius = Biltong.lineLength(_this.center, dp.pos);
                        var cpLine = Biltong.perpendicularLineTo(_this._toBiltongPoint(_this.center), _this._toBiltongPoint(dp.pos), radius * 1.5);
                        // ensure the line has the correct direction; it must match the direction implied by nodeQuadrant:
                        // if nodeQuadrant is 2 or 3, then the second point's Y must be less than the first point's Y.
                        var cminy = Math.min(cpLine[0].y, cpLine[1].y), cminx = Math.min(cpLine[0].x, cpLine[1].x);
                        var cmaxy = Math.max(cpLine[0].y, cpLine[1].y), cmaxx = Math.max(cpLine[0].x, cpLine[1].x);
                        cpLine = ([
                            null,
                            [{ x: cmaxx, y: cminy }, { x: cminx, y: cmaxy }],
                            [{ x: cmaxx, y: cmaxy }, { x: cminx, y: cminy }],
                            [{ x: cminx, y: cmaxy }, { x: cmaxx, y: cminy }],
                            [{ x: cminx, y: cminy }, { x: cmaxx, y: cmaxy }] // q4, y >, x >
                        ])[_this.nodeQuadrant];
                        // swap the two control points if in segment 4 or 2.
                        //var quadrant = Biltong.quadrant(center, dp.pos);
                        /*var idx1 = quadrant == 1 || quadrant == 3 ? 0 : 1,
                         idx2 = quadrant == 1 || quadrant == 3 ? 1 : 0;



                         // flip control points if source below target
                         (flipY ? cp2 : cp1)[0] = cpLine[idx1].x - origin[0];
                         (flipY ? cp2 : cp1)[1] = cpLine[idx1].y - origin[1];
                         (flipY ? cp1 : cp2)[0] = cpLine[idx2].x - origin[0];
                         (flipY ? cp1 : cp2)[1] = cpLine[idx2].y - origin[1];*/
                        /*console.log("nodeQuadrant", nodeQuadrant, "center", center)
                         console.log("sourceCenter", sourceCenter, "targetCenter", targetCenter)
                         console.log("dp", dp.pos)
                         console.log("cpLine", cpLine[0], cpLine[1])

                         console.log("quadrant is ", quadrant);
                         console.log("flipY is", flipY);
                         console.log("  ");*/
                        _this.cp1[0] = cpLine[0].x - _this.origin[0];
                        _this.cp1[1] = cpLine[0].y - _this.origin[1];
                        _this.cp2[0] = cpLine[1].x - _this.origin[0];
                        _this.cp2[1] = cpLine[1].y - _this.origin[1];
                        _this.h3.style.left = (_this.origin[0] + _this.cp1[0]) + PX;
                        _this.h3.style.top = (_this.origin[1] + _this.cp1[1]) + PX;
                        _this.h4.style.left = (_this.origin[0] + _this.cp2[0]) + PX;
                        _this.h4.style.top = (_this.origin[1] + _this.cp2[1]) + PX;
                    }
                    else {
                        _this.cp1[0] = l;
                        _this.cp1[1] = t;
                        _this.cp2[0] = l;
                        _this.cp2[1] = t;
                    }
                }
                _this._updateQuadrants();
                _this._setGeometry();
                _this._updateGuidelines();
            },
            stop: function () {
                if (!_this.noEdits) {
                    _this.fireConnectionEditEvent();
                }
                _this.noEdits = true;
            }
        });
        return _this;
    }
    BezierEditor.prototype._updateOrigin = function () {
        this.sp = this._jsPlumb.getOffset(this.current.endpoints[0].canvas);
        this.tp = this._jsPlumb.getOffset(this.current.endpoints[1].canvas);
        this.origin = [Math.min(this.sp.left, this.tp.left), Math.min(this.sp.top, this.tp.top)];
        this.center = [(this.sp.left + this.tp.left) / 2, (this.sp.top + this.tp.top) / 2];
        this.nodeQuadrant = Biltong.quadrant([this.sp.left, this.sp.top], [this.tp.left, this.tp.top]);
    };
    ;
    //
    // updates the current origin of the connector's SVG element (the location of its to left corner wrt
    // the origin of the jsplumb instance's container). Then updates the offset of the source and target points
    // from the origin of the SVG element. Finally, extracts the control point information from the connection,
    // either as geometry (if previously edited or set) or from the computed control points.
    //
    // The offset of the source and target points is of interest because control points are treated as being
    // with respect to the source point.  When you drag a handle, you get an offset for it wrt the the jsplumb
    // instance's container. You can then adjust this
    BezierEditor.prototype._updateConnectorInfo = function () {
        this._updateOrigin();
        var geom = this.current.getConnector().geometry;
        if (geom && geom.controlPoints) {
            this.cp = geom.controlPoints;
            this.cp1[0] = geom.controlPoints[0][0];
            this.cp1[1] = geom.controlPoints[0][1];
            this.cp2[0] = geom.controlPoints[1][0];
            this.cp2[1] = geom.controlPoints[1][1];
        }
    };
    ;
    BezierEditor.prototype._updateQuadrants = function () {
        var sp = [this.origin[0] + this.cp2[0], this.origin[1] + this.cp2[1]], tp = [this.origin[0] + this.cp1[0], this.origin[1] + this.cp1[1]];
        this.sourceMidpoints.sort(function (a, b) {
            return Biltong.lineLength(a, sp) < Biltong.lineLength(b, sp) ? -1 : 1;
        });
        this.sourceFace = this.sourceMidpoints[0][2];
        this.targetMidpoints.sort(function (a, b) {
            return Biltong.lineLength(a, tp) < Biltong.lineLength(b, tp) ? -1 : 1;
        });
        this.targetFace = this.targetMidpoints[0][2];
    };
    ;
    BezierEditor.prototype._updateHandlePositions = function () {
        if (this.mode === DUAL) {
            this.h1.style.left = this.origin[0] + ((this.cp1[0] + this.cp2[0]) / 2) + PX;
            this.h1.style.top = this.origin[1] + ((this.cp1[1] + this.cp2[1]) / 2) + PX;
            // h1.style.left = (origin[0] + cp1[0]) + PX;
            // h1.style.top = (origin[1] + cp1[1]) + PX;
            //console.log("update dual")
            this.h3.style.left = (this.origin[0] + this.cp1[0]) + PX;
            this.h3.style.top = (this.origin[1] + this.cp1[1]) + PX;
            this.h4.style.left = (this.origin[0] + this.cp2[0]) + PX;
            this.h4.style.top = (this.origin[1] + this.cp2[1]) + PX;
        }
        else {
            this.h1.style.left = (this.origin[0] + this.cp1[0]) + PX;
            this.h1.style.top = (this.origin[1] + this.cp1[1]) + PX;
            var _cp2 = this.lockHandles ? this.cp1 : this.cp2;
            this.h2.style.left = (this.origin[0] + _cp2[0]) + PX;
            this.h2.style.top = (this.origin[1] + _cp2[1]) + PX;
        }
        this._updateQuadrants();
    };
    BezierEditor.prototype._setGeometry = function () {
        this.current.getConnector().setGeometry({
            controlPoints: [this.cp1, this.cp2]
        });
        this._jsPlumb.repaint(this.current.endpoints[0].elementId);
        if (this.current.endpoints[0].elementId !== this.current.endpoints[1].elementId) {
            this._jsPlumb.repaint(this.current.endpoints[1].elementId);
        }
    };
    BezierEditor.prototype._updateGuidelines = function () {
        _updateGuideline(this.h1, this.tp, this.l1, this.origin[0] + this.cp1[0], this.origin[1] + this.cp1[1]);
        var _cp2 = this.lockHandles ? this.cp1 : this.cp2;
        _updateGuideline(this.lockHandles ? this.h1 : this.h2, this.sp, this.l2, this.origin[0] + _cp2[0], this.origin[1] + _cp2[1]);
    };
    BezierEditor.prototype._toBiltongPoint = function (xy) { return { x: xy[0], y: xy[1] }; };
    BezierEditor.prototype._activate = function (surface, conn, params) {
        if (this.current._jsPlumb == null) {
            return;
        }
        this.cp1 = [0, 0];
        this.cp2 = [0, 0];
        this.cp = [this.cp1, this.cp2];
        params = params || {};
        this.mode = params.mode || SINGLE;
        this._updateConnectorInfo();
        this.h1 = _makeHandle(this.sp.left + this.cp[0][0], this.sp.top + this.cp[0][1], [CLASS_BEZIER_HANDLE, CLASS_BEZIER_HANDLE_CONTROL_POINT, CLASS_BEZIER_HANDLE_CONTROL_POINT_1].join(" "));
        this.h2 = _makeHandle(this.sp.left + this.cp[1][0], this.sp.top + this.cp[1][1], [CLASS_BEZIER_HANDLE, CLASS_BEZIER_HANDLE_CONTROL_POINT, CLASS_BEZIER_HANDLE_CONTROL_POINT_2].join(" "));
        this.h1._jsPlumbControlPoint = this.cp1;
        this.h2._jsPlumbControlPoint = this.cp2;
        this.h3 = _makeHandle(this.origin[0] + this.cp[0][0], this.origin[1] + this.cp[0][1], [CLASS_BEZIER_SECONDARY_HANDLE, CLASS_BEZIER_SECONDARY_SOURCE_HANDLE].join(" "));
        this.h4 = _makeHandle(this.origin[0] + this.cp[0][0], this.origin[1] + this.cp[0][1], [CLASS_BEZIER_SECONDARY_HANDLE, CLASS_BEZIER_SECONDARY_TARGET_HANDLE].join(" "));
        if (this.mode === DUAL) {
            this.h3.style.display = BLOCK;
            this.h4.style.display = BLOCK;
            this._jsPlumb.appendElement(this.h3);
            this._jsPlumb.appendElement(this.h4);
            this.flipY = this.tp.top < this.sp.top;
        }
        this._jsPlumb.appendElement(this.h1);
        this._jsPlumb.appendElement(this.h2);
        this.h1Size = [this.h1.offsetWidth, this.h1.offsetHeight];
        this.h1.style.display = BLOCK;
        if (!this.lockHandles) {
            this.h2.style.display = BLOCK;
            this.h2Size = [this.h2.offsetWidth, this.h2.offsetHeight];
        }
        if (this.mode === DUAL) {
            this.h3.style.display = BLOCK;
            this.h4.style.display = BLOCK;
            this.h3Size = [this.h3.offsetWidth, this.h3.offsetHeight];
            this.h4Size = [this.h4.offsetWidth, this.h4.offsetHeight];
        }
        this.l1 = _makeGuideline(this.h1, this.tp, this.origin[0] + this.cp[0][0], this.origin[1] + this.cp[0][1]);
        this.l2 = _makeGuideline(this.lockHandles ? this.h1 : this.h2, this.sp, this.origin[0] + this.cp[1][0], this.origin[1] + this.cp[1][1]);
        this._jsPlumb.appendElement(this.l1);
        this._jsPlumb.appendElement(this.l2);
        // get center point of source and target elements
        var ss = this._jsPlumb.getSize(this.current.source), so = this._jsPlumb.getOffset(this.current.source), ts = this._jsPlumb.getSize(this.current.target), to = this._jsPlumb.getOffset(this.current.target);
        this.sourceCenter = [so.left + (ss[0] / 2), so.top + (ss[1] / 2)];
        this.targetCenter = [to.left + (ts[0] / 2), to.top + (ts[1] / 2)];
        this.sourceMidpoints = [
            [so.left, this.sourceCenter[1], LEFT],
            [this.sourceCenter[0], so.top, TOP],
            [so.left + ss[0], this.sourceCenter[1], RIGHT],
            [this.sourceCenter[0], so.top + ss[1], BOTTOM]
        ];
        this.targetMidpoints = [
            [to.left, this.targetCenter[1], LEFT],
            [this.targetCenter[0], to.top, TOP],
            [to.left + ts[0], this.targetCenter[1], RIGHT],
            [this.targetCenter[0], to.top + ts[1], BOTTOM]
        ];
        this._updateHandlePositions();
        var showGuidelines = params.guidelines !== false;
        this.l1.style.display = showGuidelines ? BLOCK : NONE;
        this.l2.style.display = showGuidelines ? BLOCK : NONE;
        this.sp = this._jsPlumb.getOffset(this.current.endpoints[0].canvas);
        this.tp = this._jsPlumb.getOffset(this.current.endpoints[1].canvas);
        this._updateGuidelines();
        this.current.addClass(CLASS_CONNECTION_EDIT);
        this._setGeometry();
    };
    ;
    BezierEditor.prototype._elementDragged = function (p) {
        this._updateOrigin();
        this._updateHandlePositions();
        this._updateGuidelines();
    };
    BezierEditor.prototype._elementDragging = function (p) {
        this.sp = this._jsPlumb.getOffset(this.current.endpoints[0].canvas);
        this.tp = this._jsPlumb.getOffset(this.current.endpoints[1].canvas);
        this._updateGuidelines();
    };
    BezierEditor.prototype._clearHandles = function () {
        (function (els) {
            for (var i = 0; i < els.length; i++) {
                if (els[i] != null && els[i].parentNode) {
                    els[i].parentNode.removeChild(els[i]);
                }
            }
        })([this.h1, this.h2, this.h3, this.h4, this.l1, this.l2]);
    };
    BezierEditor.prototype._repaint = function (args) { };
    BezierEditor.prototype._update = function () {
        this._updateOrigin();
        this._updateConnectorInfo();
        this._updateHandlePositions();
        this._updateGuidelines();
    };
    return BezierEditor;
}(EditorBase));


var StateMachineEditor = /** @class */ (function (_super_1) {
    __extends(StateMachineEditor, _super_1);
    function StateMachineEditor(params) {
        var _this = _super_1.call(this, params) || this;
        _this.lockHandles = true;
        return _this;
    }
    return StateMachineEditor;
}(BezierEditor));


var jsPlumbToolkitEditableConnectors = /** @class */ (function () {
    function jsPlumbToolkitEditableConnectors() {
    }
    return jsPlumbToolkitEditableConnectors;
}());


root.jsPlumbToolkitEditableConnectors = jsPlumbToolkitEditableConnectors;
root.jsPlumb.ConnectorEditors = {
    EditableFlowchart: FlowchartEditor,
    EditableBezier: BezierEditor,
    EditableStateMachine: StateMachineEditor
};
/// JSPLUMB TOOLKIT
if (typeof exports != 'undefined') {
    exports.jsPlumbToolkitEditableConnectors = jsPlumbToolkitEditableConnectors;
}


}).call(typeof window !== 'undefined' ? window : this);