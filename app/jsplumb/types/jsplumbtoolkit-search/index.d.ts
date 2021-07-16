import { Node, Edge, Group, jsPlumbToolkit, Port } from "jsplumbtoolkit";
export declare type Token = {
    token: string;
    context: string;
};
export declare type Tokenizer = (s: string) => Array<Token>;
export declare type Sorter = (a: HasScore, b: HasScore) => number;
export declare type IdFunction = (doc: any) => string;
export interface HasScore {
    score: number;
}
export interface Hit extends HasScore {
    document: any;
    contexts: Array<string>;
}
export interface jsPlumbToolkitSearchIndexOptions {
    fields?: Array<string>;
    tokenizer?: Tokenizer;
    searchTokenizer?: Tokenizer;
    limit?: number;
    exclusions?: Array<string>;
    caseSensitive?: boolean;
    includeContext?: boolean;
    idFunction?: IdFunction;
    sorter?: Sorter;
}
export interface IndexDocument extends HasScore {
    document: any;
}
export interface IndexEntry {
    index: number;
    children: any;
    documentIds: any;
    key: string;
}
export declare class Index {
    fields: Array<string>;
    root: IndexEntry;
    tokenizer: Tokenizer;
    searchTokenizer: Tokenizer;
    limit: number;
    exclusions: Array<string>;
    caseSensitive: boolean;
    includeContext: boolean;
    idFunction: IdFunction;
    sorter: Sorter;
    private _nodeIdx;
    private _makeNode;
    private _documentMap;
    private _documentList;
    private _documentCount;
    private _nodeMap;
    constructor(options?: jsPlumbToolkitSearchIndexOptions);
    private _storeNodeReferenceForDocument;
    private _addToken;
    private removeExclusions;
    add(doc: any): void;
    addAll(...docs: Array<any>): void;
    reindex(doc: any): void;
    remove(doc: any): void;
    clear(): void;
    getDocumentCount(): number;
    getDocumentList(): Array<IndexDocument>;
    getDocument(id: string): IndexDocument;
    search(q: string, searchLimit?: number): Array<Hit>;
}
export declare type jsPlumbToolkitSearchResults = {
    nodes: Array<Node>;
    groups: Array<Group>;
    edges: Array<Edge>;
    ports: Array<Port>;
};
export declare class jsPlumbToolkitSearch {
    instance: jsPlumbToolkit;
    nodeIndex: Index;
    groupIndex: Index;
    edgeIndex: Index;
    portIndex: Index;
    constructor(instance: jsPlumbToolkit, options?: jsPlumbToolkitSearchIndexOptions);
    private _indexNode;
    private _indexGroup;
    private _indexEdge;
    search(value: string): jsPlumbToolkitSearchResults;
}
