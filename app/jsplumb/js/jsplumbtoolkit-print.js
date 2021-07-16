(function() {

/**
 * A collection of utilities that are helpful when printing with the Toolkit.
 */
var root = this;
var CANVAS_ELEMENTS_SELECTOR = ".jtk-overlay,.jtk-node,.jtk-endpoint,.jtk-group,.jtk-connector";
var jsPlumbToolkitPrint = /** @class */ (function () {
    function jsPlumbToolkitPrint() {
    }
    jsPlumbToolkitPrint.convertToPixels = function (values, units) {
        var multiplier = units === jsPlumbToolkitPrint.Units.INCHES ? jsPlumbToolkitPrint.PIXELS_PER_INCH : jsPlumbToolkitPrint.PIXELS_PER_CENTIMETRE;
        return values.map(function (v) { return v * multiplier; });
    };
    jsPlumbToolkitPrint.convertToUnits = function (values, units) {
        var divider = units === jsPlumbToolkitPrint.Units.INCHES ? jsPlumbToolkitPrint.PIXELS_PER_INCH : jsPlumbToolkitPrint.PIXELS_PER_CENTIMETRE;
        return values.map(function (v) { return v / divider; });
    };
    //
    // Instructs the given handler to zoom its content to 1, and then report back how big the page needs to be to
    // render the entire dataset. Note that this method returns an array serialized as a string.
    // @param handlerId ID of the handler to scale.
    // @param [margins] Optional margins to use (in [top,right,bottom,left] format). Values here are expressed in whatever you specify for `units`,
    // which defaults to CENTIMETERS if you leave it empty.
    // @param [units] Optional units, defaults to CENTIMETERS.
    //
    jsPlumbToolkitPrint.scaleToFullPage = function (handlerId, margins, units) {
        if (margins === void 0) { margins = this.EmptyMargins; }
        if (units === void 0) { units = "CENTIMETERS"; }
        if (this.printHandlers[handlerId] != null) {
            return JSON.stringify(this.printHandlers[handlerId].scaleToFullPage(margins, units));
        }
    };
    //
    //  Instructs the given handler to zoom its content so that it would fit into a page of the given size. We currently know about
    //  LETTER, A5, A4, A3, A2, A1, A0 and FULL (which is the same as calling `scaleToFullPage`). Note that this method returns an array serialized as a string.
    //  @param handlerId ID of the handler to scale.
    //  @param size PageSize to fit into.
    //  @param [margins] Optional margins to use (in [top,right,bottom,left] format). Values here are expressed in whatever you specify for `units`,
    //  which defaults to CENTIMETERS if you leave it empty.
    //  @param [units] Optional units, defaults to CENTIMETERS.
    //
    jsPlumbToolkitPrint.scaleToPageSize = function (handlerId, size, margins, units) {
        if (margins === void 0) { margins = this.EmptyMargins; }
        if (units === void 0) { units = "CENTIMETERS"; }
        if (this.printHandlers[handlerId] != null) {
            return JSON.stringify(this.printHandlers[handlerId].scaleToPageSize(size, margins, units));
        }
    };
    //
    //  * Instructs the given handler to zoom its content so that it would fit into a page of the given dimensions. The values are in centimetres,
    //  * unless you specify in the third argument to the method that the dimensions are inches.
    //  * @param handlerId ID of the handler to scale.
    //  * @param dimensions PageDimensions to fit into.
    //  * @param [margins] Optional margins to use (in [top,right,bottom,left] format). Values here are expressed in whatever you specify for `units`,
    //  * which defaults to CENTIMETERS if you leave it empty.
    //  * @param [units] Optional units, defaults to CENTIMETERS.
    //
    jsPlumbToolkitPrint.scaleToPageDimensions = function (handlerId, dimensions, margins, units) {
        if (margins === void 0) { margins = this.EmptyMargins; }
        if (units === void 0) { units = "CENTIMETERS"; }
        if (this.printHandlers[handlerId] != null) {
            return this.printHandlers[handlerId].scaleToPageDimensions(dimensions, margins, units);
        }
    };
    jsPlumbToolkitPrint.findElementBounds = function (el) {
        try {
            if (typeof el.offsetLeft !== "undefined") {
                var l = el.offsetLeft, t = el.offsetTop, w = el.offsetWidth, h = el.offsetHeight;
                // overlays are translated -50% in both axes
                if (el.className.indexOf("jtk-overlay") !== -1) {
                    l -= (w / 2);
                    t -= (h / 2);
                }
                return {
                    l: l,
                    t: t,
                    l1: l + w,
                    t1: t + h
                };
            }
            else {
                var l = parseFloat(el.style.left), t = parseFloat(el.style.top);
                return {
                    l: l,
                    t: t,
                    l1: l + parseFloat(el.getAttribute("width")),
                    t1: t + parseFloat(el.getAttribute("height"))
                };
            }
        }
        catch (e) {
            console.log("Cannot compute bounds for elements " + el);
            return { l: 0, l1: 0, t: 0, t1: 0 };
        }
    };
    //
    // gets the bounds of the content, taking no margins or zoom or anything into account. just the content.
    jsPlumbToolkitPrint.findSurfaceBounds = function (surface) {
        var _this = this;
        surface.relayout(null);
        var xmin = [];
        var xmax = [];
        var ymin = [];
        var ymax = [];
        var els = surface.getJsPlumb().getContainer().querySelectorAll(CANVAS_ELEMENTS_SELECTOR);
        var _p = function (l, list) {
            if (!isNaN(l)) {
                list.push(l);
            }
        };
        els.forEach(function (el) {
            var b = _this.findElementBounds(el);
            _p(b.l, xmin);
            _p(b.t, ymin);
            _p(b.l1, xmax);
            _p(b.t1, ymax);
        });
        var x = Math.min.apply(null, xmin);
        var xm = Math.max.apply(null, xmax);
        var y = Math.min.apply(null, ymin);
        var ym = Math.max.apply(null, ymax);
        return {
            x: x,
            y: y,
            w: xm - x,
            h: ym - y,
            padding: null,
            vw: xm + (x < 0 ? -x : 0),
            vh: ym + (y < 0 ? -y : 0),
            z: null,
            zoom: null
        };
    };
    //
    //  * Instructs the given handler to zoom and pan its content so that it would fit into the given width and height (which
    //  * are pixel values). This is used when printing if we wish to fix to a specific page size like A4.
    //  * @param surface the Surface to scale.
    //  * @param wh Width and height (in pixels) to zoom to
    //  * @param margins Optional margins in [top,right,bottom,left] format. In this method, these values are expressed as pixel values.
    //
    jsPlumbToolkitPrint.scaleToBounds = function (handlerId, wh, margins) {
        if (margins === void 0) { margins = this.EmptyMargins; }
        if (this.printHandlers[handlerId] != null) {
            return this.printHandlers[handlerId].scaleToBounds(wh, margins);
        }
    };
    //
    //  * Register a print handler for the given surface, optionally with the given id. An id will be generated if not
    //  * provided.
    //  * @param surface
    //  * @param id
    //
    jsPlumbToolkitPrint.registerHandler = function (surface, id) {
        var handler = new jsPlumbToolkitPrintHandler(surface, id);
        this.printHandlers[handler.id] = handler;
        return handler;
    };
    //
    // returns whether or not the handler with the given id considers itself ready to print.
    // if no such handler is found we also return false; it is entirely possible that this call could be made
    // before the handler has been instantiated.
    //
    jsPlumbToolkitPrint.isReadyToPrint = function (handlerId) {
        if (this.printHandlers[handlerId] != null) {
            return this.printHandlers[handlerId].isReadyToPrint();
        }
        else {
            return false;
        }
    };
    jsPlumbToolkitPrint.PIXELS_PER_INCH = 96.0;
    jsPlumbToolkitPrint.PIXELS_PER_CENTIMETRE = jsPlumbToolkitPrint.PIXELS_PER_INCH / 2.54;
    jsPlumbToolkitPrint.EmptyMargins = [0, 0, 0, 0];
    jsPlumbToolkitPrint.PAGE_DIMENSIONS = {
        LETTER: [21.59, 27.94],
        A5: [14.8, 21],
        A4: [21.0, 29.7],
        A3: [29.7, 42.0],
        A2: [42.0, 59.4],
        A1: [59.4, 84.1],
        A0: [84.1, 118.9]
    };
    jsPlumbToolkitPrint.printHandlers = {};
    jsPlumbToolkitPrint.Units = { INCHES: "INCHES", CENTIMETERS: "CENTIMETERS" };
    jsPlumbToolkitPrint.PageSizes = { FULL: "FULL", LETTER: "LETTER", A5: "A5", A4: "A4", A3: "A3", A2: "A2", A1: "A1", A0: "A0" };
    return jsPlumbToolkitPrint;
}());


//
// Print handler for a given Surface. Instantiate one of these in your code and provide an id to look it up by later. if you
// dont provide an id, one will be assigned. But remember you need the id to invoke operations on the handler from the global
// context, ie. when printing via dev tools.
//
var jsPlumbToolkitPrintHandler = /** @class */ (function () {
    function jsPlumbToolkitPrintHandler(surface, id) {
        this.surface = surface;
        this.id = id || jsPlumbUtil.uuid();
    }
    jsPlumbToolkitPrintHandler.prototype.scaleToBounds = function (wh, margins) {
        if (margins === void 0) { margins = jsPlumbToolkitPrint.EmptyMargins; }
        //return jsPlumbToolkitPrint.scaleToBounds(this.surface, wh, margins);
        var surfaceBounds = jsPlumbToolkitPrint.findSurfaceBounds(this.surface);
        var width = wh[0] - margins[3] - margins[1];
        var height = wh[1] - margins[0] - margins[2];
        var z = Math.min(width / surfaceBounds.w, height / surfaceBounds.h);
        // get current clamp value and set to false
        var isClamping = this.surface.isClamping();
        this.surface.setClamping(false);
        // adjust zoom
        this.surface.setZoom(z);
        // adjust pan
        this.surface.setPan(-surfaceBounds.x * z, -surfaceBounds.y * z);
        // reset clamping to original value.
        this.surface.setClamping(isClamping);
        return z;
    };
    jsPlumbToolkitPrintHandler.prototype.scaleToPageDimensions = function (dimensions, margins, units) {
        if (margins === void 0) { margins = jsPlumbToolkitPrint.EmptyMargins; }
        if (units === void 0) { units = "CENTIMETERS"; }
        return this.scaleToBounds(jsPlumbToolkitPrint.convertToPixels(dimensions, units), jsPlumbToolkitPrint.convertToPixels(margins, units));
    };
    jsPlumbToolkitPrintHandler.prototype.scaleToPageSize = function (size, margins, units) {
        if (margins === void 0) { margins = jsPlumbToolkitPrint.EmptyMargins; }
        if (units === void 0) { units = "CENTIMETERS"; }
        if (size === "FULL") {
            return this.scaleToFullPage(margins, units);
        }
        var dimensions = jsPlumbToolkitPrint.PAGE_DIMENSIONS[size];
        if (dimensions) {
            // note here we use CENTIMETERS for converting the page dimensions, as that is how we specify them. but we use the user's
            // preference for units for converting the margin.
            var pageBounds = jsPlumbToolkitPrint.convertToPixels(dimensions, jsPlumbToolkitPrint.Units.CENTIMETERS);
            var marginsInPixels = jsPlumbToolkitPrint.convertToPixels(margins, units);
            var zoom = this.scaleToBounds(pageBounds, marginsInPixels);
            return jsPlumbToolkitPrint.convertToUnits(pageBounds, units);
        }
        else {
            throw new Error("Unknown page size " + size);
        }
    };
    jsPlumbToolkitPrintHandler.prototype.scaleToFullPage = function (margins, units) {
        if (margins === void 0) { margins = jsPlumbToolkitPrint.EmptyMargins; }
        if (units === void 0) { units = "CENTIMETERS"; }
        var surfaceBounds = jsPlumbToolkitPrint.findSurfaceBounds(this.surface); // we use the content bounds - pixels - as the page size.
        var pageBounds = [surfaceBounds.w + 5, surfaceBounds.h + 5];
        var marginsInPixels = jsPlumbToolkitPrint.convertToPixels(margins, units);
        var pageDimensions = jsPlumbToolkitPrint.convertToUnits([pageBounds[0] + marginsInPixels[1] + marginsInPixels[3], pageBounds[1] + marginsInPixels[0] + marginsInPixels[2]], units);
        var isClamping = this.surface.isClamping();
        this.surface.setClamping(false);
        // adjust zoom
        this.surface.setZoom(1);
        // adjust pan
        this.surface.setPan(-surfaceBounds.x, -surfaceBounds.y);
        // reset clamping to original value.
        this.surface.setClamping(isClamping);
        return pageDimensions;
    };
    jsPlumbToolkitPrintHandler.prototype.isReadyToPrint = function () {
        var els = this.surface.getJsPlumb().getContainer().querySelectorAll("img");
        for (var i = 0; i < els.length; i++) {
            if (!els[i].complete) {
                return false;
            }
        }
        return true;
    };
    return jsPlumbToolkitPrintHandler;
}());


root.jsPlumbToolkitPrint = jsPlumbToolkitPrint;
if (typeof exports !== "undefined") {
    exports.jsPlumbToolkitPrint = jsPlumbToolkitPrint;
}


}).call(typeof window !== 'undefined' ? window : this);