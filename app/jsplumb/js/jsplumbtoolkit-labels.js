(function() {

/*
    much of this stuff is common with both Knockle and the Toolkit now.
 */
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
var root = this;
function getAbsolutePosition(entry) {
    var o = {
        left: parseInt(entry.el.style.left || 0, 10),
        top: parseInt(entry.el.style.top || 0, 10)
    };
    return o;
}
function setAbsolutePosition(entry, p) {
    //  set the absolute position on the connection. it is cleared on a drag.
    var dx = entry.connector.paintExtents.xmin < 0 ? -entry.connector.paintExtents.xmin : 0;
    var dy = entry.connector.paintExtents.ymin < 0 ? -entry.connector.paintExtents.ymin : 0;
    var _x = p.left - entry.connectorOffset.left;
    var _y = p.top - entry.connectorOffset.top;
    var seg = entry.connector.findSegmentForPoint(_x - dx, _y - dy);
    entry.label.loc = seg.connectorLocation;
    return seg.connectorLocation;
}
var jsPlumbToolkitLabelManipulator = /** @class */ (function () {
    function jsPlumbToolkitLabelManipulator(params) {
        var _this = this;
        this.surface = params.surface;
        this.jsPlumb = this.surface.getJsPlumb();
        this.toolkit = this.surface.getToolkit();
        this.getLabel = params.getLabel || function (connection) {
            return connection.getOverlay("label");
        };
        this.toolkit.bind("edgeUpdated", function (p) {
            var connection = _this.surface.getRenderedConnection(p.edge.getId());
            var label = _this.getLabel(connection);
            if (label) {
                var locAtt = _this.surface.getLabelLocationAttribute(p.edge);
                var loc = p.edge.data[locAtt];
                if (loc) {
                    label.loc = loc;
                    connection.repaint();
                }
            }
        });
    }
    jsPlumbToolkitLabelManipulator.prototype.updateEdge = function (edge, label, loc) {
        if (label.id === "label") {
            var locAtt = this.surface.getLabelLocationAttribute(edge);
            var payload = {};
            payload[locAtt] = loc;
            this.toolkit.updateEdge(edge, payload);
        }
    };
    return jsPlumbToolkitLabelManipulator;
}());


var jsPlumbToolkitLabelDragManager = /** @class */ (function (_super) {
    __extends(jsPlumbToolkitLabelDragManager, _super);
    function jsPlumbToolkitLabelDragManager(params) {
        var _this = _super.call(this, params) || this;
        var self = _this;
        var dirty = false;
        _this._dragManager = new Katavorio({
            bind: function () {
                self.jsPlumb.on.apply(self.jsPlumb, arguments);
            }.bind(_this),
            unbind: function () { self.jsPlumb.off.apply(self.jsPlumb, arguments); }.bind(_this),
            getSize: function (elId) {
                return self.jsPlumb.getSize(elId);
            },
            getConstrainingRectangle: function (el) {
                return [el.parentNode.scrollWidth, el.parentNode.scrollHeight];
            },
            getPosition: function (el) {
                return [parseInt(el.style.left || '0', 10), parseInt(el.style.top || '0', 10)];
            },
            setPosition: function (el, xy) {
                el.style.left = xy[0] + 'px';
                el.style.top = xy[1] + 'px';
            },
            addClass: function (el, clazz) { el.classList.add(clazz); },
            removeClass: function (el, clazz) { el.classList.remove(clazz); },
            intersects: Biltong.intersects,
            indexOf: function (l, i) { return l.indexOf(i); }
        });
        _this._dragManager.draggable(_this.surface.getContainer(), {
            selector: ".jtk-overlay",
            start: function (p) {
                if (p.drag.getDragElement()._jsPlumb.id === "label") {
                    dirty = false;
                }
                else {
                    return false;
                }
            },
            drag: function (e) {
                dirty = true;
            },
            stop: function (p) {
                if (dirty) {
                    //    alert("a label was dragged. need to now fix its location on the connector")
                    var conn = p.el._jsPlumb.component.getConnector();
                    var connectorLocation = setAbsolutePosition({
                        connectorOffset: { left: parseInt(conn.canvas.style.left, 10), top: parseInt(conn.canvas.style.top, 10) },
                        label: p.el._jsPlumb,
                        connector: conn
                    }, { left: p.finalPos[0], top: p.finalPos[1] });
                    _this.updateEdge(p.el._jsPlumb.component.edge, p.el._jsPlumb, connectorLocation);
                }
            },
            constrain: function (pos, dragEl, _constrainRect, _size) {
                var connector = dragEl._jsPlumb.component.getConnector(), o = { left: parseInt(connector.canvas.style.left, 10), top: parseInt(connector.canvas.style.top, 10) }, _sx = pos[0] - o.left, _sy = pos[1] - o.top, dx = connector.paintExtents.xmin < 0 ? -connector.paintExtents.xmin : 0, dy = connector.paintExtents.ymin < 0 ? -connector.paintExtents.ymin : 0;
                var closest = connector.findSegmentForPoint(_sx - dx, _sy - dy);
                // const dx = connector.bounds.minX < 0 ? -connector.bounds.minX : 0;
                // const dy = connector.bounds.minY < 0 ? -connector.bounds.minY : 0;
                return [closest.x + o.left + dx, closest.y + o.top + dy];
            }
        });
        return _this;
    }
    return jsPlumbToolkitLabelDragManager;
}(jsPlumbToolkitLabelManipulator));


var jsPlumbToolkitLabelSpacer = /** @class */ (function (_super) {
    __extends(jsPlumbToolkitLabelSpacer, _super);
    function jsPlumbToolkitLabelSpacer(params) {
        var _this = _super.call(this, params) || this;
        _this.padding = params.padding || 5;
        _this.debug = params.debug;
        _this.fireOnNewConnections = params.fireOnNewConnections !== false;
        _this.fireAfterDrag = params.fireAfterDrag !== false;
        _this.cache = new Map();
        _this.dirtyCache = new Map();
        _this.surface.bind("nodeMoveStart", function (p) {
            _this.dirtyCache.set(p.node.id, true);
        });
        _this.surface.bind("nodeMoveEnd", function (p) {
            if (_this.fireAfterDrag) {
                _this.execute();
            }
            _this.dirtyCache.set(p.node.id, false);
        });
        _this.magnetizer = Farahey.getInstance({
            getPosition: getAbsolutePosition,
            setPosition: setAbsolutePosition,
            padding: params.padding,
            getSize: function (entry) { return entry.size; },
            getId: function (entry) { return entry.id; },
            constrain: function (id, current, delta) {
                var entry = _this.cache.get(id), connector = entry.connector, o = entry.connectorOffset, _x = current[0] + delta.left, _y = current[1] + delta.top, _sx = _x - o.left, _sy = _y - o.top;
                // now [_sx,_sy] gives us the value relative to the Connector canvas's origin, so we find the
                // segment closest to that point.
                var closest = connector.findSegmentForPoint(_sx, _sy);
                // [l,t] gives us the point in absolute coordinates relative to the jsPlumb Container.
                var l = o.left + closest.x, t = o.top + closest.y;
                // if (this.debug) {
                //     $("." + id + "-marker").remove();
                //     $("body").append($("<div class='" + id + "-marker' style='z-index:90000;position:absolute;width:5px;height:5px;background-color:red;left:" + l + "px;top:" + t + "px;'></div>"));
                // }
                // the return value is delta allowed, so return difference between [l,t] and the current position.
                return {
                    left: l - current[0],
                    top: t - current[1]
                };
            },
            filter: function (id) {
                // this filters elements that should be magnetized.  we magnetize labels for connections for which
                // one element (source or target) has been dragged and is marked dirty, or for connections whose
                // labels have not been magnetized (either since creation or after a reset)
                return _this.dirtyCache.get(_this.cache.get(id).connection.sourceId) !== false &&
                    _this.dirtyCache.get(_this.cache.get(id).connection.targetId) !== false;
            }
        });
        // if fireOnNewConnections is set, add listener to jsplumb
        if (_this.fireOnNewConnections) {
            _this.jsPlumb.bind("connection", _this.execute.bind(_this));
        }
        return _this;
    }
    jsPlumbToolkitLabelSpacer.prototype.execute = function () {
        var _this = this;
        this.cache.clear();
        var connections = this.jsPlumb.select(), els = [];
        connections.each(function (c) {
            var lbl = _this.getLabel(c);
            if (lbl != null) {
                var lblElement = lbl.getElement(), lblId = _this.jsPlumb.getId(lblElement), size = _this.jsPlumb.getSize(lblElement), conn = c.getConnector(), co = { left: parseInt(conn.canvas.style.left, 10), top: parseInt(conn.canvas.style.top, 10) }, data = {
                    connection: c,
                    edge: c.edge,
                    label: lbl,
                    el: lblElement,
                    size: size,
                    id: lblId,
                    connector: conn,
                    connectorOffset: co
                };
                els.push(data);
                // stash the data, keyed by label element id.
                _this.cache.set(lblId, data);
            }
        });
        this.magnetizer.setElements(els);
        var movedElements = this.magnetizer.executeAtCenter({ padding: [this.padding, this.padding] });
        for (var k in movedElements) {
            var data = this.cache.get(k);
            if (data && data.edge) {
                this.updateEdge(data.edge, data.label, data.label.loc);
            }
        }
        this.jsPlumb.repaintEverything();
    };
    jsPlumbToolkitLabelSpacer.prototype.reset = function () {
        this.dirtyCache.clear();
        this.cache.clear();
        this.jsPlumb.repaintEverything(true);
    };
    return jsPlumbToolkitLabelSpacer;
}(jsPlumbToolkitLabelManipulator));


root.jsPlumbToolkitLabelSpacer = jsPlumbToolkitLabelSpacer;
root.jsPlumbToolkitLabelDragManager = jsPlumbToolkitLabelDragManager;
/// JSPLUMB TOOLKIT
if (typeof exports !== "undefined") {
    exports.jsPlumbToolkitLabelSpacer = jsPlumbToolkitLabelSpacer;
    exports.jsPlumbToolkitLabelDragManager = jsPlumbToolkitLabelDragManager;
}


}).call(typeof window !== 'undefined' ? window : this);