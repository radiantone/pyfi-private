(function() {

var root = this;
function applyCaseSensitivity(token, caseSensitive) {
    if (caseSensitive)
        return token;
    else
        return token.toLowerCase();
}
function fastTrim(s) {
    var str = s.replace(/^\s\s*/, '');
    var ws = /\s/;
    var i = str.length;
    while (ws.test(str.charAt(--i)))
        ;
    return str.slice(0, i + 1);
}
function WhitespaceTokenizer(value) {
    value = "" + value;
    var parts = value.split(/\s/);
    var out = [];
    var counter = 0;
    var queue = [];
    var queueSize = 4;
    for (var i = 0; i < parts.length; i++) {
        // we should track the cursor position here. when we write a token we should be able to say the cursor position at which it
        // started in the original field. these can then be stored as a pair against each document id for a node. So you'll have some
        // node that has a key like 'e', say, which will have a map of document ids, whose values are pairs of [ tokens, cursorPos ].
        // with that information the user can be directed to the correct place when searching.
        //var endCounter = counter + parts[i].length;
        var s = fastTrim(parts[i].replace(/[^\w]*/, ""));
        if (s.length > 0) {
            out.push({ token: s, context: "" });
            queue.unshift(s);
            queue.splice(queueSize - 1);
            if (queue.length > 1) {
                queue.reverse();
                out.push({ token: queue.join(" "), context: "" });
                queue.reverse();
            }
        }
    }
    // there might be values left in queue. we snip the head value one at a time and if there's still more than one value, we write the phrase
    queue.pop();
    while (queue.length > 1) {
        queue.reverse();
        out.push({ token: queue.join(" "), context: "" });
        queue.reverse();
        queue.pop();
    }
    return out;
}
var DefaultTokenizer = WhitespaceTokenizer;
function WhitespaceReplacingTokenizer(value) {
    value = fastTrim(value);
    return [{ token: value.replace(/\s/g, "_"), context: value }];
}
function DefaultSearchTokenizer(value) {
    return [{ token: fastTrim(value), context: value }];
}
function ByScoreSorter(a, b) {
    return (a.score > b.score) ? -1 : 1;
}
var DefaultIdFunction = function (doc) { return doc["id"]; };
// -----------------------------------------
function ListInsert(list, value, compare) {
    if (list.length === 0) {
        list.push(value);
        return;
    }
    var _i = function (start, end) {
        var idx = start + Math.floor((end - start) / 2), val = list[idx], comp = compare(val, value), comp2;
        if (comp === 0) {
            list.splice(idx, 0, value);
            return;
        }
        else if (comp === -1) {
            // list value is less than value to insert.
            // if value is the last value, push to end and return.
            if (idx === list.length - 1) {
                list.push(value);
                return;
            }
            else {
                comp2 = compare(list[idx + 1], value);
                if (comp2 !== comp) {
                    list.splice(idx + 1, 0, value);
                    return;
                }
            }
            _i(idx + 1, end);
        }
        else {
            // list value is greater than value to insert.
            // if idx was zero, push value to head and return
            if (idx === 0) {
                list.unshift(value);
                return;
            }
            else {
                comp2 = compare(list[idx - 1], value);
                if (comp2 !== comp) {
                    list.splice(idx, 0, value);
                    return;
                }
            }
            _i(start, start + Math.floor((end - start) / 2));
        }
    };
    _i(0, list.length - 1);
}
// --------------------------------------------------
var DEFAULT_LIMIT = 10;
var Index = /** @class */ (function () {
    function Index(options) {
        this._nodeIdx = 0;
        this._documentMap = new Map();
        this._documentList = [];
        this._documentCount = 0;
        this._nodeMap = {};
        options = options || {};
        this.fields = options.fields;
        this.root = this._makeNode();
        this.tokenizer = options.tokenizer || DefaultTokenizer;
        this.searchTokenizer = options.searchTokenizer || DefaultSearchTokenizer;
        this.limit = options.limit || DEFAULT_LIMIT;
        this.exclusions = options.exclusions || [];
        this.caseSensitive = options.caseSensitive === true;
        this.includeContext = options.includeContext === true;
        this.idFunction = options.idFunction || DefaultIdFunction;
        this.sorter = options.sorter || ByScoreSorter;
    }
    Index.prototype._makeNode = function (key) {
        return { index: this._nodeIdx++, children: {}, documentIds: {}, key: key };
    };
    Index.prototype._storeNodeReferenceForDocument = function (docId, node, context) {
        var nodes = this._nodeMap[docId];
        if (!nodes) {
            nodes = {};
            this._nodeMap[docId] = nodes;
        }
        nodes[node.index] = node;
    };
    Index.prototype._addToken = function (token, docId, context) {
        var _this = this;
        var _oneLevel = function (node, idx, token, docId) {
            // if at the end of the token, we are done.
            if (idx === token.length)
                return;
            // otherwise, get the char for this index
            var c = token[idx], 
            // see if this node already has a child for that char
            child = node.children[c];
            // if not, create it
            if (!child) {
                child = _this._makeNode(c);
                node.children[c] = child;
            }
            // add this doc id to the list for this node, since we have traversed through it.
            child.documentIds[docId] = child.documentIds[docId] || [];
            child.documentIds[docId].push(token);
            // store a reference to this node in the docId->node map.
            _this._storeNodeReferenceForDocument(docId, child, context);
            _oneLevel(child, idx + 1, token, docId);
        };
        _oneLevel(this.root, 0, token, docId);
    };
    Index.prototype.removeExclusions = function (doc) {
        var out = {};
        for (var k in doc) {
            if (this.exclusions.indexOf(k) === -1) {
                out[k] = doc[k];
            }
        }
        return out;
    };
    Index.prototype.add = function (doc) {
        var _this = this;
        var _a = function (doc) {
            var docToWrite = _this.removeExclusions(doc);
            // add to list
            ListInsert(_this._documentList, { document: docToWrite, score: 1 }, _this.sorter);
            var docId = _this.idFunction(doc), 
            // two ways of looping: if field ids provided, use them. otherwise loop through all fields in document.
            _loopers = {
                "fields": function (f) {
                    for (var i = 0; i < _this.fields.length; i++) {
                        var v = doc[_this.fields[i]];
                        if (jsPlumbUtil.isString(v)) {
                            f(v);
                        }
                    }
                },
                "document": function (f) {
                    for (var i in doc) {
                        if (i !== "id") {
                            var v = doc[i];
                            if (jsPlumbUtil.isString(v)) {
                                f(v);
                            }
                        }
                    }
                }
            };
            _this._documentMap.set(docId, docToWrite);
            // loop through all the fields we need to and index.
            _loopers[_this.fields ? "fields" : "document"](function (v) {
                if (v) {
                    var tokens = _this.tokenizer(v);
                    for (var j = 0; j < tokens.length; j++) {
                        _this._addToken(applyCaseSensitivity(tokens[j].token, _this.caseSensitive), docId, tokens[j].context);
                    }
                }
            });
            _this._documentCount++;
        };
        if (doc.constructor === Array) {
            for (var i = 0; i < doc.length; i++)
                _a(doc[i]);
        }
        else
            _a(doc);
    };
    ;
    Index.prototype.addAll = function () {
        var docs = [];
        for (var _b = 0; _b < arguments.length; _b++) {
            docs[_b] = arguments[_b];
        }
        for (var i = 0; i < docs.length; i++) {
            this.add(docs[i]);
        }
    };
    Index.prototype.reindex = function (doc) {
        this.remove(doc);
        this.add(doc);
    };
    Index.prototype.remove = function (doc) {
        var docId = this.idFunction(doc), nodes = this._nodeMap[docId], i;
        if (nodes) {
            for (i in nodes) {
                delete nodes[i].documentIds[docId];
            }
        }
        var idx = -1;
        for (i = 0; i < this._documentList.length; i++) {
            var id = this.idFunction(this._documentList[i].document);
            if (id === docId) {
                idx = i;
                break;
            }
        }
        if (idx !== -1) {
            this._documentList.splice(idx, 1);
            this._documentCount = this._documentList.length;
        }
        this._documentMap.delete(docId);
    };
    Index.prototype.clear = function () {
        this._documentMap.clear();
        this._nodeMap = {};
        this._nodeIdx = 0;
        this._documentList.length = 0;
        this._documentCount = 0;
        this.root = this._makeNode();
    };
    Index.prototype.getDocumentCount = function () {
        return this._documentCount;
    };
    Index.prototype.getDocumentList = function () {
        return this._documentList;
    };
    Index.prototype.getDocument = function (id) {
        return this._documentMap.get(id);
    };
    Index.prototype.search = function (q, searchLimit) {
        var tokens = this.searchTokenizer(q), idMap = {}, docs = [], scores = {}, hits = {}, hit = function (docId, token, context) {
            var d = idMap[docId];
            if (!d) {
                d = {};
                idMap[docId] = d;
                scores[docId] = 0;
                hits[docId] = [];
            }
            hits[docId].push(context);
            if (!d[token]) {
                d[token] = true;
                scores[docId]++;
            }
        }, _oneToken = function (node, idx, token) {
            if (idx === token.length) {
                for (var i in node.documentIds) {
                    if (node.documentIds.hasOwnProperty(i)) {
                        var contexts = node.documentIds[i];
                        for (var j = 0; j < contexts.length; j++) {
                            hit(i, token, contexts[j]);
                        }
                        //hit(i, token)
                    }
                }
                return;
            }
            var c = token[idx];
            if (node.children[c]) {
                // recurse down a level
                _oneToken(node.children[c], idx + 1, token);
            }
        };
        // process each token
        for (var i = 0; i < tokens.length; i++) {
            _oneToken(this.root, 0, applyCaseSensitivity(tokens[i].token, this.caseSensitive));
        }
        // retrieve the documents.
        for (var j in idMap) {
            docs.unshift({ document: this._documentMap.get(j), score: scores[j], contexts: hits[j] });
        }
        docs.sort(this.sorter);
        return docs.slice(0, searchLimit == null ? this.limit : searchLimit);
    };
    return Index;
}());


var jsPlumbToolkitSearch = /** @class */ (function () {
    function jsPlumbToolkitSearch(instance, options) {
        var _this = this;
        this.instance = instance;
        this.nodeIndex = new Index(options);
        this.groupIndex = new Index(options);
        this.edgeIndex = new Index(options);
        this.portIndex = new Index(options);
        instance.bind("nodeAdded", function (p) {
            _this._indexNode(p.node);
        });
        instance.bind("nodeRemoved", function (params) {
            _this.nodeIndex.remove(params.node.data);
            params.node.getPorts().forEach(function (port) { return _this.portIndex.remove(port.data); });
        });
        instance.bind("nodeUpdated", function (params) {
            _this.nodeIndex.remove(params.node.data);
            _this.nodeIndex.add(params.node.data);
        });
        instance.bind("groupAdded", function (p) {
            _this._indexGroup(p.group);
        });
        instance.bind("groupRemoved", function (params) {
            _this.groupIndex.remove(params.group.data);
        });
        instance.bind("groupUpdated", function (params) {
            _this.groupIndex.remove(params.group.data);
            _this.groupIndex.add(params.group.data);
        });
        instance.bind("edgeAdded", function (params) {
            _this._indexEdge(params.edge);
        });
        instance.bind("edgeRemoved", function (params) {
            _this.edgeIndex.remove({ id: params.edge.getId() });
        });
        instance.bind("edgeUpdated", function (params) {
            var d = jsPlumb.extend(params.originalData || {}, { id: params.edge.getId() });
            _this.edgeIndex.remove(d);
            var d2 = jsPlumb.extend(params.edge.data || {}, { id: params.edge.getId() });
            _this.edgeIndex.add(d2);
        });
        instance.bind("portAdded", function (params) {
            _this.portIndex.add(params.port.data);
        });
        instance.bind("portRemoved", function (params) {
            _this.portIndex.remove(params.port.data);
        });
        instance.bind("portUpdated", function (params) {
            _this.portIndex.remove(params.port.data);
            _this.portIndex.add(params.port.data);
        });
        instance.bind("graphCleared", function () {
            _this.nodeIndex.clear();
            _this.groupIndex.clear();
            _this.edgeIndex.clear();
            _this.portIndex.clear();
        });
        this.instance.eachNode(function (idx, node) {
            _this._indexNode(node);
        });
        this.instance.eachGroup(function (idx, group) {
            _this._indexGroup(group);
        });
        this.instance.eachEdge(function (idx, edge) {
            _this._indexEdge(edge);
        });
    }
    jsPlumbToolkitSearch.prototype._indexNode = function (node) {
        var _this = this;
        this.nodeIndex.add(node.data);
        node.getPorts().forEach(function (port) { return _this.portIndex.add(port.data); });
    };
    jsPlumbToolkitSearch.prototype._indexGroup = function (group) {
        this.groupIndex.add(group.data);
    };
    jsPlumbToolkitSearch.prototype._indexEdge = function (edge) {
        var d = jsPlumb.extend(edge.data || {}, { id: edge.getId() });
        this.edgeIndex.add(edge.data);
    };
    jsPlumbToolkitSearch.prototype.search = function (value) {
        var _this = this;
        var nodeResults = this.nodeIndex.search(value).map(function (sr) { return _this.instance.getNode(sr.document.id); });
        var portResults = this.portIndex.search(value).map(function (sr) { return _this.instance.getPort(sr.document.id); });
        var groupResults = this.groupIndex.search(value).map(function (sr) { return _this.instance.getGroup(sr.document.id); });
        var edgeResults = this.edgeIndex.search(value).map(function (sr) { return _this.instance.getEdge(sr.document.id); });
        return {
            nodes: nodeResults,
            groups: groupResults,
            edges: edgeResults,
            ports: portResults
        };
    };
    return jsPlumbToolkitSearch;
}());


root.jsPlumbToolkitSearch = jsPlumbToolkitSearch;
/// JSPLUMB TOOLKIT
if (typeof exports !== "undefined") {
    exports.jsPlumbToolkitSearch = jsPlumbToolkitSearch;
}


}).call(typeof window !== 'undefined' ? window : this);