/**
 * A utility for enabling drop of arbitrary elements onto the nodes/groups of a surface.
 */
import { Surface, jsPlumbToolkit, jsPlumbInstance, Node, Group, CanvasLocation, Edge, PointArray } from "jsplumbtoolkit";
export declare type DropFilter<T> = (data: T, target: Node | Group) => boolean;
export declare type CanvasDropFilter<T> = (data: T) => boolean;
export declare type EdgeDropFilter<T> = (data: T, target: Edge) => boolean;
export declare type DragFunction<T> = (data: T, e: Event, position: PointArray, canvasLocation: CanvasLocation) => any;
export declare type DropFunction<T> = (data: T, target: Node | Group, draggedElement?: HTMLElement, e?: Event, position?: PointArray, canvasLocation?: CanvasLocation, targetLocation?: CanvasLocation, locationOnTarget?: CanvasLocation) => void;
export declare type EdgeDropFunction<T> = (data: T, target: Edge, draggedElement?: HTMLElement, e?: Event, position?: PointArray, canvasLocation?: CanvasLocation) => void;
export declare type CanvasDropFunction<T> = (data: T, canvasPosition: CanvasLocation, draggedElement?: HTMLElement, e?: Event, position?: PointArray) => void;
export declare type DataGeneratorFunction<T> = (el: HTMLElement) => T;
export declare type TypeGeneratorFunction<T> = (d: T) => string;
export declare type GroupIdentifierFunction<T> = (d: T, el: HTMLElement) => boolean;
export interface DropManagerOptions<T> {
    surface: Surface;
    source: HTMLElement;
    selector: string;
    scope?: string;
    onDrag?: DragFunction<T>;
    onDrop?: DropFunction<T>;
    onEdgeDrop?: EdgeDropFunction<T>;
    onCanvasDrop?: CanvasDropFunction<T>;
    dropFilter?: DropFilter<T>;
    canvasDropFilter?: CanvasDropFilter<T>;
    edgeDropFilter?: EdgeDropFilter<T>;
    dragActiveClass?: string;
    dragHoverClass?: string;
    dataGenerator: DataGeneratorFunction<T>;
    enabled?: boolean;
    canvasSelector?: string;
}
export declare class jsPlumbToolkitDropManager<T> {
    surface: Surface;
    surfaceCanvas: HTMLElement;
    source: Element;
    selector: string;
    toolkit: jsPlumbToolkit;
    _jsPlumb: jsPlumbInstance;
    elements: Array<Element>;
    dropFilter: DropFilter<T>;
    canvasDropFilter: CanvasDropFilter<T>;
    edgeDropFilter: EdgeDropFilter<T>;
    scope: string;
    onEdgeDrop: EdgeDropFunction<T>;
    onDrop: DropFunction<T>;
    onCanvasDrop: CanvasDropFunction<T>;
    dragActiveClass: string;
    dragHoverClass: string;
    dataGenerator: DataGeneratorFunction<T>;
    onDrag: DragFunction<T>;
    canvasSelector: string;
    private currentNodeList;
    private currentEdgeList;
    private candidateData;
    private candidate;
    private canvasMoveListener;
    private canvasMouseOutListener;
    private isCurrentlyOnCanvasElement;
    private canDropOnCanvas;
    private viewportPosition;
    private enabled;
    private _translateX;
    private _translateY;
    katavorio: any;
    constructor(params: DropManagerOptions<T>);
    /**
     * sets whether or not dragging is currently enabled.
     * @param e
     */
    setEnabled(e: boolean): void;
    setSurface(surface: Surface): void;
    isEffectivelyOnCanvas(e: Event): boolean;
    private getAllNodesAndGroups;
    private _adjustForTransformations;
    /**
     * find all the connectors in the canvas, computing their position in page coords (taking into account the viewport
     * position of the surface and its current zoom). We return [ connection, connector, bounding rect ] for each connector.
     * @returns {Array<EdgeSpec>}
     */
    private getAllConnectors;
    private _cleanupClasses;
}
export interface SurfaceDropManagerOptions<T> {
    surface: Surface;
    source: HTMLElement;
    selector: string;
    dataGenerator?: DataGeneratorFunction<T>;
    typeGenerator?: TypeGeneratorFunction<T>;
    groupIdentifier?: GroupIdentifierFunction<T>;
    magnetize?: boolean;
    allowDropOnEdge?: boolean;
    allowDropOnGroup?: boolean;
    allowDropOnCanvas?: boolean;
    allowNodeDropOnCanvas?: boolean;
    canvasSelector?: string;
}
export declare class SurfaceDropManager<T> {
    surface: Surface;
    dropManager: jsPlumbToolkitDropManager<T>;
    toolkit: jsPlumbToolkit;
    typeGenerator: TypeGeneratorFunction<T>;
    groupIdentifier: GroupIdentifierFunction<T>;
    modelPositionAttributes: [string, string];
    magnetize: boolean;
    allowDropOnEdge: boolean;
    allowDropOnGroup: boolean;
    allowDropOnCanvas: boolean;
    allowNodeDropOnCanvas: boolean;
    private _mapToPositionAttributes;
    constructor(options: SurfaceDropManagerOptions<T>);
    setEnabled(e: boolean): void;
    setSurface(s: Surface): void;
}
