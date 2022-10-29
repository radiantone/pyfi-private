import { Edge, jsPlumbInstance, jsPlumbToolkit, Surface } from "jsplumbtoolkit";
export declare type Offset = {
    left: number;
    top: number;
};
export declare type Entry = {
    el: any;
    connectorOffset: Offset;
    connection: any;
    label: string;
    id: string;
    size: [number, number];
    connector: any;
    edge: Edge;
};
export interface LabelManipulatorParams {
    getLabel?: Function;
    surface: Surface;
}
export interface LabelSpacerParams extends LabelManipulatorParams {
    debug?: boolean;
    fireOnNewConnections?: boolean;
    fireAfterDrag?: boolean;
    padding?: number;
}
export interface LabelDragParams extends LabelManipulatorParams {
}
export declare abstract class jsPlumbToolkitLabelManipulator {
    surface: Surface;
    toolkit: jsPlumbToolkit;
    jsPlumb: jsPlumbInstance;
    getLabel: Function;
    protected constructor(params: LabelManipulatorParams);
    updateEdge(edge: Edge, label: any, loc: number): void;
}
export declare class jsPlumbToolkitLabelDragManager extends jsPlumbToolkitLabelManipulator {
    private _dragManager;
    constructor(params: LabelDragParams);
}
export declare class jsPlumbToolkitLabelSpacer extends jsPlumbToolkitLabelManipulator {
    debug?: boolean;
    cache: Map<string, Entry>;
    dirtyCache: Map<String, boolean>;
    fireOnNewConnections?: boolean;
    fireAfterDrag?: boolean;
    magnetizer: any;
    padding: number;
    constructor(params: LabelSpacerParams);
    execute(): void;
    reset(): void;
}
