import { Edge, jsPlumbToolkit, Surface } from "jsplumbtoolkit";
export declare type OnChangeFunction = (undoRedo: jsPlumbToolkitUndoRedo, undoStackSize: number, redoStackSize: number) => void;
export declare type jsPlumbToolkitUndoRedoParams = {
    toolkit?: jsPlumbToolkit;
    maximumSize?: number;
    onChange?: OnChangeFunction;
    compound: boolean;
    surface?: Surface;
};
export declare class jsPlumbToolkitUndoRedo {
    toolkit: jsPlumbToolkit;
    surface: Surface;
    maximumSize: number;
    suspend: boolean;
    onChange: OnChangeFunction;
    compound: boolean;
    private readonly undoStack;
    private readonly redoStack;
    private currentTransaction;
    constructor(params: jsPlumbToolkitUndoRedoParams);
    /**
     * Perhaps compound the given remove action with any prior edge remove actions whose source or target is the focus of the terminus
     * remove. we search down the undo stack looking for EdgeRemoveActions that are for edges connected to the terminus that is being removed,
     * adding them to a list of candidates until we fail to match. If this list of candidates is of non zero length, we compound them all
     * into one action, prepending (this is important - the terminus has to exist before the edges on undo) the terminus remove action. we then
     * splice the undo stack to remove all the candidates we found, and return a compound action, which is added to the top of the undo stack.
     *
     * @param action
     * @returns {UndoRedoAction}
     * @private
     */
    private _possiblyCompound;
    /**
     * Add a terminus remove action - node or group. pulled into a common method since they both do the same thing, but also
     * terminus remove actions are a candidate for "compounding" with any prior edge remove events.
     * @param obj
     * @private
     */
    private _addTerminusRemoveAction;
    private _objectNotEmpty;
    /**
     * Bind listeners to the events in the Toolkit we are interested in.
     * @private
     */
    private _bindListeners;
    /**
     * Fire the on change event, if there's a listener registered.
     * @private
     */
    private _fireUpdate;
    /**
     * add a command to the undo stack, clearing the redo stack.
     * @param action
     */
    private command;
    /**
     * Notification that some edge has been replaced with a copy. This occurs when an edge removed is undone or an edge add is
     * redone. we need to update all references to the previous edge with this new one, as the toolkit no longer knows about
     * the old edge. This is not a method that should be called from outside of the undo manager.
     * @param previousId
     * @param newEdge
     */
    edgeChange(previousId: string, newEdge: Edge): void;
    /**
     * Execute undo on the last command in the undo stack, if it isn't empty.
     */
    undo(): void;
    /**
     * Re-execute the last command in the redo stack, if it isn't empty.
     */
    redo(): void;
    /**
     * Clears both stacks and fires an update event.
     */
    clear(): void;
    /**
     * Run a series of operations as a single transaction in the undo stack, meaning that they will all be undone/redone
     * at once.
     * @param fn
     */
    transaction(fn: (...args: any[]) => any): void;
}
