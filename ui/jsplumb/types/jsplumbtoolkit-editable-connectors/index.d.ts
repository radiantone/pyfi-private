import { Connection, ConnectorEditor, PointArray, Surface } from "jsplumbtoolkit";
export declare type ConnectionDetachedParameters = {
    connection: Connection;
};
export declare type ConnectionEditParameters = {
    clearOnDrag?: boolean;
    connection: Connection;
};
export declare type BezierConnectorParams = {
    showLoopback?: boolean;
    curviness?: number;
    margin?: number;
    orientation?: string;
    loopbackRadius?: number;
    proximityLimit?: number;
    majorAnchor?: number;
};
export interface Geometry {
    source: any;
    target: any;
}
declare abstract class EditorBase implements ConnectorEditor {
    current: any;
    currentEdge: any;
    currentOverlays: Array<any>;
    sourceDimensions: any;
    targetDimensions: any;
    sourceAnchorPlaceholder: HTMLElement;
    targetAnchorPlaceholder: HTMLElement;
    active: boolean;
    _jsPlumb: any;
    _surface: any;
    eventManager: any;
    update: () => void;
    cleanup: () => void;
    private _katavorio;
    private _katavorioDraggable;
    private _dragHandlers;
    abstract _repaint(args?: any): void;
    constructor(options: any);
    private _attachOverlay;
    private _attachOverlays;
    private _detachOverlays;
    private _attachDeleteButton;
    /**
     * Repaints the current connection, passing some arguments, optionally. These are retrieved inside `refresh`,
     * and are ultimately handed off to the subclass's `repaint` method. Subclasses should call this on things like handle
     * dragging, as the existence (and nature of ) args can subsequently be used by their `repaint` method to decide whether or not
     * to redraw all the handles (such as you would in the event of an external paint event), or just to reposition the existing
     * ones. During a drag, of course, blowing away the current handle would be bad.
     */
    repaintConnection(args?: any): void;
    /**
     * Fires a connection edit event, passing the current connection, and the current
     * connection's exported geometry.
     */
    fireConnectionEditEvent(): void;
    /**
     * Redraw anchor placeholders and editor handles.
     * @param args Optional args to pass to the subclass repaint method.
     */
    refresh(args?: any): void;
    /**
     * Draws, or repositions if they exist already, the anchor placeholders for the current connection.
     * @private
     */
    _drawAnchors(): void;
    /**
     * Removes anchor placeholders.
     * @private
     */
    _cleanupAnchors(): void;
    _clearGeometry(): void;
    reset(): void;
    isActive(): boolean;
    _setElementPosition(el: HTMLElement, x: number, y: number): void;
    /**
     * Activate the editor, with the given Connection. First we
     * call `deactivate`, so there's only ever one edit happening at a time.
     * Then we set the current connection, and override its paint method.
     * @param connection
     */
    activate(surface: Surface, connection: Connection, params?: any): void;
    /**
     * Deactivates the editor, removing all editor handles and anchor placeholders etc.
     * @param e
     */
    deactivate(e?: Event): void;
    protected _addDragHandler(o: any): void;
    abstract _update(): void;
    abstract _clearHandles(): void;
    abstract _activate(surface: Surface, conn: Connection, params?: any): void;
    abstract _elementDragged(p: any): void;
    abstract _elementDragging(p: any): void;
}
/**
 * This is a copy of the Community edition's Flowchart connector, which is not ideal, as any changes there will need
 * to be propagated in here for now, but of course in the long term the aim is to use TS everywhere and have this
 * extend the Community connector. This connector actually overrides the Flowchart registration in the Community edition, so
 * anyone asking for Flowchart connectors gets this.
 */
export interface Connector {
    _compute(paintInfo: any, params: any): void;
    setAnchorOrientation(idx: number, orientation: number[]): void;
}
/**
 * Constructor parameters for a flowchart connector.
 */
export declare type FlowchartConnectorParameters = {
    midpoint?: number;
    alwaysRespectStubs?: boolean;
    cornerRadius?: number;
    stub?: number;
    loopbackRadius?: number;
    trimThreshold?: number;
};
export declare type Orientation = [number, number];
export declare type AxisOrientation = "h" | "v";
export declare type Axis = "x" | "y";
export declare type AnchorOrientation = "opposite" | "orthogonal" | "perpendicular";
export declare type Direction = -1 | 1;
export interface FlowchartGeometry extends Geometry {
    segments: Array<Segment>;
    quadrant?: number;
}
export interface PaintInfo {
    sx: number;
    sy: number;
    tx: number;
    ty: number;
    startStubX: number;
    endStubX: number;
    startStubY: number;
    endStubY: number;
    sourceAxis: Axis;
    anchorOrientation: AnchorOrientation;
    segment: number;
    lw: number;
    stubs: [number, number];
    to: Orientation;
    so: Orientation;
}
export declare type Segment = [number, number, number, number, AxisOrientation, number, number, number, number];
export declare type SegmentContext = {
    segment: Segment;
    prev?: Segment;
    next?: Segment;
    index: number;
    orientation: AxisOrientation;
    left?: [Segment, number];
    right?: [Segment, number];
};
export declare type SegmentMoveResult = {
    ctx: SegmentContext;
    segments: Array<Segment>;
    index: number;
};
export declare type DragInfo = {
    pos: [number, number];
    drag: any;
};
export declare class BezierEditor extends EditorBase {
    private conn;
    private mode;
    private center;
    private cp;
    private cp1;
    private cp2;
    private origin;
    private flipY;
    private sp;
    private tp;
    sourceMidpoints: Array<any>;
    targetMidpoints: Array<any>;
    sourceFace: any;
    targetFace: any;
    sourceCenter: PointArray;
    targetCenter: PointArray;
    sourceEdgeSupported: any;
    targetEdgeSupported: any;
    noEdits: boolean;
    nodeQuadrant: any;
    h1: any;
    h2: any;
    h3: any;
    h4: any;
    l1: any;
    l2: any;
    lockHandles: boolean;
    h1Size: PointArray;
    h2Size: PointArray;
    h3Size: PointArray;
    h4Size: PointArray;
    constructor(params: any);
    private _updateOrigin;
    private _updateConnectorInfo;
    private _updateQuadrants;
    private _updateHandlePositions;
    private _setGeometry;
    private _updateGuidelines;
    private _toBiltongPoint;
    _activate(surface: Surface, conn: Connection, params?: any): void;
    _elementDragged(p: any): void;
    _elementDragging(p: any): void;
    _clearHandles(): void;
    _repaint(args?: any): void;
    _update(): void;
}
export declare class StateMachineEditor extends BezierEditor {
    constructor(params: any);
}
export declare class jsPlumbToolkitEditableConnectors {
}
export {};
