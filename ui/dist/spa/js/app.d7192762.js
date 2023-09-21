/******/ (function(modules) { // webpackBootstrap
/******/ 	// install a JSONP callback for chunk loading
/******/ 	function webpackJsonpCallback(data) {
/******/ 		var chunkIds = data[0];
/******/ 		var moreModules = data[1];
/******/ 		var executeModules = data[2];
/******/
/******/ 		// add "moreModules" to the modules object,
/******/ 		// then flag all "chunkIds" as loaded and fire callback
/******/ 		var moduleId, chunkId, i = 0, resolves = [];
/******/ 		for(;i < chunkIds.length; i++) {
/******/ 			chunkId = chunkIds[i];
/******/ 			if(Object.prototype.hasOwnProperty.call(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 				resolves.push(installedChunks[chunkId][0]);
/******/ 			}
/******/ 			installedChunks[chunkId] = 0;
/******/ 		}
/******/ 		for(moduleId in moreModules) {
/******/ 			if(Object.prototype.hasOwnProperty.call(moreModules, moduleId)) {
/******/ 				modules[moduleId] = moreModules[moduleId];
/******/ 			}
/******/ 		}
/******/ 		if(parentJsonpFunction) parentJsonpFunction(data);
/******/
/******/ 		while(resolves.length) {
/******/ 			resolves.shift()();
/******/ 		}
/******/
/******/ 		// add entry modules from loaded chunk to deferred list
/******/ 		deferredModules.push.apply(deferredModules, executeModules || []);
/******/
/******/ 		// run deferred modules when all chunks ready
/******/ 		return checkDeferredModules();
/******/ 	};
/******/ 	function checkDeferredModules() {
/******/ 		var result;
/******/ 		for(var i = 0; i < deferredModules.length; i++) {
/******/ 			var deferredModule = deferredModules[i];
/******/ 			var fulfilled = true;
/******/ 			for(var j = 1; j < deferredModule.length; j++) {
/******/ 				var depId = deferredModule[j];
/******/ 				if(installedChunks[depId] !== 0) fulfilled = false;
/******/ 			}
/******/ 			if(fulfilled) {
/******/ 				deferredModules.splice(i--, 1);
/******/ 				result = __webpack_require__(__webpack_require__.s = deferredModule[0]);
/******/ 			}
/******/ 		}
/******/
/******/ 		return result;
/******/ 	}
/******/
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// object to store loaded CSS chunks
/******/ 	var installedCssChunks = {
/******/ 		2: 0
/******/ 	};
/******/
/******/ 	// object to store loaded and loading chunks
/******/ 	// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 	// Promise = chunk loading, 0 = chunk loaded
/******/ 	var installedChunks = {
/******/ 		2: 0
/******/ 	};
/******/
/******/ 	var deferredModules = [];
/******/
/******/ 	// script path function
/******/ 	function jsonpScriptSrc(chunkId) {
/******/ 		return __webpack_require__.p + "js/" + ({"1":"chunk-common"}[chunkId]||chunkId) + "." + {"1":"7a2cfc38","3":"4d0c1ef9","4":"2bbb949b","5":"085e73d0","6":"5062560d","7":"a864a240","8":"4ff8cc71"}[chunkId] + ".js"
/******/ 	}
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/ 	// This file contains only the entry chunk.
/******/ 	// The chunk loading function for additional chunks
/******/ 	__webpack_require__.e = function requireEnsure(chunkId) {
/******/ 		var promises = [];
/******/
/******/
/******/ 		// mini-css-extract-plugin CSS loading
/******/ 		var cssChunks = {"1":1,"3":1,"4":1,"5":1,"6":1};
/******/ 		if(installedCssChunks[chunkId]) promises.push(installedCssChunks[chunkId]);
/******/ 		else if(installedCssChunks[chunkId] !== 0 && cssChunks[chunkId]) {
/******/ 			promises.push(installedCssChunks[chunkId] = new Promise(function(resolve, reject) {
/******/ 				var href = "css/" + ({"1":"chunk-common"}[chunkId]||chunkId) + "." + {"1":"c1205e73","3":"c1205e73","4":"aa36d997","5":"20fe3735","6":"3c67bf93","7":"31d6cfe0","8":"31d6cfe0"}[chunkId] + ".css";
/******/ 				var fullhref = __webpack_require__.p + href;
/******/ 				var existingLinkTags = document.getElementsByTagName("link");
/******/ 				for(var i = 0; i < existingLinkTags.length; i++) {
/******/ 					var tag = existingLinkTags[i];
/******/ 					var dataHref = tag.getAttribute("data-href") || tag.getAttribute("href");
/******/ 					if(tag.rel === "stylesheet" && (dataHref === href || dataHref === fullhref)) return resolve();
/******/ 				}
/******/ 				var existingStyleTags = document.getElementsByTagName("style");
/******/ 				for(var i = 0; i < existingStyleTags.length; i++) {
/******/ 					var tag = existingStyleTags[i];
/******/ 					var dataHref = tag.getAttribute("data-href");
/******/ 					if(dataHref === href || dataHref === fullhref) return resolve();
/******/ 				}
/******/ 				var linkTag = document.createElement("link");
/******/ 				linkTag.rel = "stylesheet";
/******/ 				linkTag.type = "text/css";
/******/ 				linkTag.onload = resolve;
/******/ 				linkTag.onerror = function(event) {
/******/ 					var request = event && event.target && event.target.src || fullhref;
/******/ 					var err = new Error("Loading CSS chunk " + chunkId + " failed.\n(" + request + ")");
/******/ 					err.code = "CSS_CHUNK_LOAD_FAILED";
/******/ 					err.request = request;
/******/ 					delete installedCssChunks[chunkId]
/******/ 					linkTag.parentNode.removeChild(linkTag)
/******/ 					reject(err);
/******/ 				};
/******/ 				linkTag.href = fullhref;
/******/
/******/ 				var head = document.getElementsByTagName("head")[0];
/******/ 				head.appendChild(linkTag);
/******/ 			}).then(function() {
/******/ 				installedCssChunks[chunkId] = 0;
/******/ 			}));
/******/ 		}
/******/
/******/ 		// JSONP chunk loading for javascript
/******/
/******/ 		var installedChunkData = installedChunks[chunkId];
/******/ 		if(installedChunkData !== 0) { // 0 means "already installed".
/******/
/******/ 			// a Promise means "currently loading".
/******/ 			if(installedChunkData) {
/******/ 				promises.push(installedChunkData[2]);
/******/ 			} else {
/******/ 				// setup Promise in chunk cache
/******/ 				var promise = new Promise(function(resolve, reject) {
/******/ 					installedChunkData = installedChunks[chunkId] = [resolve, reject];
/******/ 				});
/******/ 				promises.push(installedChunkData[2] = promise);
/******/
/******/ 				// start chunk loading
/******/ 				var script = document.createElement('script');
/******/ 				var onScriptComplete;
/******/
/******/ 				script.charset = 'utf-8';
/******/ 				script.timeout = 120;
/******/ 				if (__webpack_require__.nc) {
/******/ 					script.setAttribute("nonce", __webpack_require__.nc);
/******/ 				}
/******/ 				script.src = jsonpScriptSrc(chunkId);
/******/
/******/ 				// create error before stack unwound to get useful stacktrace later
/******/ 				var error = new Error();
/******/ 				onScriptComplete = function (event) {
/******/ 					// avoid mem leaks in IE.
/******/ 					script.onerror = script.onload = null;
/******/ 					clearTimeout(timeout);
/******/ 					var chunk = installedChunks[chunkId];
/******/ 					if(chunk !== 0) {
/******/ 						if(chunk) {
/******/ 							var errorType = event && (event.type === 'load' ? 'missing' : event.type);
/******/ 							var realSrc = event && event.target && event.target.src;
/******/ 							error.message = 'Loading chunk ' + chunkId + ' failed.\n(' + errorType + ': ' + realSrc + ')';
/******/ 							error.name = 'ChunkLoadError';
/******/ 							error.type = errorType;
/******/ 							error.request = realSrc;
/******/ 							chunk[1](error);
/******/ 						}
/******/ 						installedChunks[chunkId] = undefined;
/******/ 					}
/******/ 				};
/******/ 				var timeout = setTimeout(function(){
/******/ 					onScriptComplete({ type: 'timeout', target: script });
/******/ 				}, 120000);
/******/ 				script.onerror = script.onload = onScriptComplete;
/******/ 				document.head.appendChild(script);
/******/ 			}
/******/ 		}
/******/ 		return Promise.all(promises);
/******/ 	};
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// on error function for async loading
/******/ 	__webpack_require__.oe = function(err) { console.error(err); throw err; };
/******/
/******/ 	var jsonpArray = window["webpackJsonp"] = window["webpackJsonp"] || [];
/******/ 	var oldJsonpFunction = jsonpArray.push.bind(jsonpArray);
/******/ 	jsonpArray.push = webpackJsonpCallback;
/******/ 	jsonpArray = jsonpArray.slice();
/******/ 	for(var i = 0; i < jsonpArray.length; i++) webpackJsonpCallback(jsonpArray[i]);
/******/ 	var parentJsonpFunction = oldJsonpFunction;
/******/
/******/
/******/ 	// add entry module to deferred list
/******/ 	deferredModules.push([0,0]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ 0:
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__("2f39");


/***/ }),

/***/ "0047":
/***/ (function(module, exports, __webpack_require__) {

// extracted by mini-css-extract-plugin

/***/ }),

/***/ "2f39":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXTERNAL MODULE: ./node_modules/@babel/runtime/helpers/asyncToGenerator.js
var asyncToGenerator = __webpack_require__("c973");
var asyncToGenerator_default = /*#__PURE__*/__webpack_require__.n(asyncToGenerator);

// EXTERNAL MODULE: ./node_modules/regenerator-runtime/runtime.js
var runtime = __webpack_require__("96cf");

// EXTERNAL MODULE: ./node_modules/core-js/modules/es.regexp.exec.js
var es_regexp_exec = __webpack_require__("ac1f");

// EXTERNAL MODULE: ./node_modules/core-js/modules/es.string.replace.js
var es_string_replace = __webpack_require__("5319");

// EXTERNAL MODULE: ./node_modules/quasar/dist/quasar.ie.polyfills.js
var quasar_ie_polyfills = __webpack_require__("5c7d");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/ionicons-v4/ionicons-v4.css
var ionicons_v4 = __webpack_require__("35fc");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/mdi-v5/mdi-v5.css
var mdi_v5 = __webpack_require__("9f29");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/fontawesome-v5/fontawesome-v5.css
var fontawesome_v5 = __webpack_require__("573e");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/eva-icons/eva-icons.css
var eva_icons = __webpack_require__("43b9");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/line-awesome/line-awesome.css
var line_awesome = __webpack_require__("81a9");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/roboto-font/roboto-font.css
var roboto_font = __webpack_require__("7d6e");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/material-icons/material-icons.css
var material_icons = __webpack_require__("e54f");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/bounce.css
var bounce = __webpack_require__("4439");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/flash.css
var flash = __webpack_require__("4605");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/flip.css
var flip = __webpack_require__("f580");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/headShake.css
var headShake = __webpack_require__("5b2b");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/heartBeat.css
var heartBeat = __webpack_require__("8753");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/hinge.css
var hinge = __webpack_require__("2967");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/jello.css
var jello = __webpack_require__("7e67");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/pulse.css
var pulse = __webpack_require__("d770");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/rubberBand.css
var rubberBand = __webpack_require__("dd82");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/shake.css
var shake = __webpack_require__("922cc");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/shakeX.css
var shakeX = __webpack_require__("d7fb");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/shakeY.css
var shakeY = __webpack_require__("a533");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/swing.css
var swing = __webpack_require__("c32e");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/tada.css
var tada = __webpack_require__("a151");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/wobble.css
var wobble = __webpack_require__("8bc7");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/backInDown.css
var backInDown = __webpack_require__("e80f");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/backInLeft.css
var backInLeft = __webpack_require__("5fec");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/backInRight.css
var backInRight = __webpack_require__("e42f");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/backInUp.css
var backInUp = __webpack_require__("57fc");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/bounceIn.css
var bounceIn = __webpack_require__("d67f");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/bounceInDown.css
var bounceInDown = __webpack_require__("880e");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/bounceInLeft.css
var bounceInLeft = __webpack_require__("1c10");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/bounceInRight.css
var bounceInRight = __webpack_require__("9482");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/bounceInUp.css
var bounceInUp = __webpack_require__("e797");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeIn.css
var fadeIn = __webpack_require__("4848");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeInBottomLeft.css
var fadeInBottomLeft = __webpack_require__("53d0");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeInBottomRight.css
var fadeInBottomRight = __webpack_require__("63b1");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeInDown.css
var fadeInDown = __webpack_require__("e9fd");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeInDownBig.css
var fadeInDownBig = __webpack_require__("195c");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeInLeft.css
var fadeInLeft = __webpack_require__("64e9");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeInLeftBig.css
var fadeInLeftBig = __webpack_require__("33c5");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeInRight.css
var fadeInRight = __webpack_require__("4f62");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeInRightBig.css
var fadeInRightBig = __webpack_require__("0dbc");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeInTopLeft.css
var fadeInTopLeft = __webpack_require__("7c38");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeInTopRight.css
var fadeInTopRight = __webpack_require__("0756");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeInUp.css
var fadeInUp = __webpack_require__("4953");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeInUpBig.css
var fadeInUpBig = __webpack_require__("81db");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/flipInX.css
var flipInX = __webpack_require__("2e52");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/flipInY.css
var flipInY = __webpack_require__("2248");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/jackInTheBox.css
var jackInTheBox = __webpack_require__("7797");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/lightSpeedInLeft.css
var lightSpeedInLeft = __webpack_require__("12a1");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/lightSpeedInRight.css
var lightSpeedInRight = __webpack_require__("ce96");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/rollIn.css
var rollIn = __webpack_require__("70ca");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/rotateIn.css
var rotateIn = __webpack_require__("2318");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/rotateInDownLeft.css
var rotateInDownLeft = __webpack_require__("24bd");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/rotateInDownRight.css
var rotateInDownRight = __webpack_require__("8f27");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/rotateInUpLeft.css
var rotateInUpLeft = __webpack_require__("3064");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/rotateInUpRight.css
var rotateInUpRight = __webpack_require__("c9a2");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/slideInDown.css
var slideInDown = __webpack_require__("8767");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/slideInLeft.css
var slideInLeft = __webpack_require__("4a8e");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/slideInRight.css
var slideInRight = __webpack_require__("b828");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/slideInUp.css
var slideInUp = __webpack_require__("3c1c");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/zoomIn.css
var zoomIn = __webpack_require__("21cb");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/zoomInDown.css
var zoomInDown = __webpack_require__("c00e");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/zoomInLeft.css
var zoomInLeft = __webpack_require__("e4a8");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/zoomInRight.css
var zoomInRight = __webpack_require__("e4d3");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/zoomInUp.css
var zoomInUp = __webpack_require__("f4d9");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/backOutDown.css
var backOutDown = __webpack_require__("fffd");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/backOutLeft.css
var backOutLeft = __webpack_require__("f645");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/backOutRight.css
var backOutRight = __webpack_require__("639e");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/backOutUp.css
var backOutUp = __webpack_require__("34ee");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/bounceOut.css
var bounceOut = __webpack_require__("b794");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/bounceOutDown.css
var bounceOutDown = __webpack_require__("af24");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/bounceOutLeft.css
var bounceOutLeft = __webpack_require__("7c9c");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/bounceOutRight.css
var bounceOutRight = __webpack_require__("7bb2");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/bounceOutUp.css
var bounceOutUp = __webpack_require__("64f7");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeOut.css
var fadeOut = __webpack_require__("c382");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeOutBottomLeft.css
var fadeOutBottomLeft = __webpack_require__("053c");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeOutBottomRight.css
var fadeOutBottomRight = __webpack_require__("c48f");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeOutDown.css
var fadeOutDown = __webpack_require__("f5d1");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeOutDownBig.css
var fadeOutDownBig = __webpack_require__("3cec");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeOutLeft.css
var fadeOutLeft = __webpack_require__("c00ee");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeOutLeftBig.css
var fadeOutLeftBig = __webpack_require__("d450");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeOutRight.css
var fadeOutRight = __webpack_require__("ca07");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeOutRightBig.css
var fadeOutRightBig = __webpack_require__("14e3");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeOutTopLeft.css
var fadeOutTopLeft = __webpack_require__("9393");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeOutTopRight.css
var fadeOutTopRight = __webpack_require__("9227");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeOutUp.css
var fadeOutUp = __webpack_require__("1dba");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/fadeOutUpBig.css
var fadeOutUpBig = __webpack_require__("674a");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/flipOutX.css
var flipOutX = __webpack_require__("de26");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/flipOutY.css
var flipOutY = __webpack_require__("6721");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/lightSpeedOutLeft.css
var lightSpeedOutLeft = __webpack_require__("9cb5");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/lightSpeedOutRight.css
var lightSpeedOutRight = __webpack_require__("ed9b");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/rollOut.css
var rollOut = __webpack_require__("fc83");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/rotateOut.css
var rotateOut = __webpack_require__("98e5");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/rotateOutDownLeft.css
var rotateOutDownLeft = __webpack_require__("605a");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/rotateOutDownRight.css
var rotateOutDownRight = __webpack_require__("ba60");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/rotateOutUpLeft.css
var rotateOutUpLeft = __webpack_require__("df07");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/rotateOutUpRight.css
var rotateOutUpRight = __webpack_require__("7903");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/slideOutDown.css
var slideOutDown = __webpack_require__("e046");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/slideOutLeft.css
var slideOutLeft = __webpack_require__("58af");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/slideOutRight.css
var slideOutRight = __webpack_require__("7713");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/slideOutUp.css
var slideOutUp = __webpack_require__("0571");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/zoomOut.css
var zoomOut = __webpack_require__("3e27");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/zoomOutDown.css
var zoomOutDown = __webpack_require__("6837");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/zoomOutLeft.css
var zoomOutLeft = __webpack_require__("3fc9");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/zoomOutRight.css
var zoomOutRight = __webpack_require__("0693");

// EXTERNAL MODULE: ./node_modules/@quasar/extras/animate/zoomOutUp.css
var zoomOutUp = __webpack_require__("bf41");

// EXTERNAL MODULE: ./node_modules/quasar/dist/quasar.sass
var quasar = __webpack_require__("985d");

// EXTERNAL MODULE: ./src/css/app.sass
var css_app = __webpack_require__("0047");

// EXTERNAL MODULE: ./node_modules/@quasar/quasar-ui-qmarkdown/src/index.sass
var src = __webpack_require__("a1e8");

// EXTERNAL MODULE: ./node_modules/vue/dist/vue.runtime.esm.js
var vue_runtime_esm = __webpack_require__("2b0e");

// EXTERNAL MODULE: ./node_modules/quasar/lang/en-us.js
var en_us = __webpack_require__("1f91");

// EXTERNAL MODULE: ./node_modules/quasar/icon-set/material-icons.js
var icon_set_material_icons = __webpack_require__("42d2");

// EXTERNAL MODULE: ./node_modules/quasar/src/vue-plugin.js + 1 modules
var vue_plugin = __webpack_require__("b05d");

// EXTERNAL MODULE: ./node_modules/quasar/src/plugins/Cookies.js
var Cookies = __webpack_require__("515f");

// EXTERNAL MODULE: ./node_modules/quasar/src/plugins/AppFullscreen.js
var AppFullscreen = __webpack_require__("b12a");

// EXTERNAL MODULE: ./node_modules/quasar/src/plugins/Loading.js
var Loading = __webpack_require__("f508");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/breadcrumbs/QBreadcrumbsEl.js
var QBreadcrumbsEl = __webpack_require__("079e");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/breadcrumbs/QBreadcrumbs.js
var QBreadcrumbs = __webpack_require__("ead5");

// EXTERNAL MODULE: ./node_modules/quasar/src/plugins/Dialog.js + 5 modules
var Dialog = __webpack_require__("436b");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/drawer/QDrawer.js
var QDrawer = __webpack_require__("9404");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/tree/QTree.js
var QTree = __webpack_require__("7f41");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/btn-toggle/QBtnToggle.js
var QBtnToggle = __webpack_require__("6a67");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/spinner/QSpinnerOval.js
var QSpinnerOval = __webpack_require__("1b41");

// EXTERNAL MODULE: ./node_modules/quasar/src/plugins/Notify.js
var Notify = __webpack_require__("2a19");

// CONCATENATED MODULE: ./.quasar/import-quasar.js
/**
 * THIS FILE IS GENERATED AUTOMATICALLY.
 * DO NOT EDIT.
 *
 * You are probably looking on adding startup/initialization code.
 * Use "quasar new boot <name>" and add it there.
 * One boot file per concern. Then reference the file(s) in quasar.conf.js > boot:
 * boot: ['file', ...] // do not add ".js" extension to it.
 *
 * Boot files are your "main.js"
 **/



;
vue_runtime_esm["default"].use(vue_plugin["a" /* default */], {
  config: {
    "loadingBar": {}
  },
  lang: en_us["a" /* default */],
  iconSet: icon_set_material_icons["a" /* default */],
  plugins: {
    Cookies: Cookies["a" /* default */],
    AppFullscreen: AppFullscreen["a" /* default */],
    Loading: Loading["a" /* default */],
    QBreadcrumbsEl: QBreadcrumbsEl["a" /* default */],
    QBreadcrumbs: QBreadcrumbs["a" /* default */],
    Dialog: Dialog["a" /* default */],
    QDrawer: QDrawer["a" /* default */],
    QTree: QTree["a" /* default */],
    QBtnToggle: QBtnToggle["a" /* default */],
    QSpinnerOval: QSpinnerOval["a" /* default */],
    Notify: Notify["a" /* default */]
  }
});
// CONCATENATED MODULE: ./node_modules/@quasar/app/lib/webpack/loader.transform-quasar-imports.js!./node_modules/babel-loader/lib??ref--2-0!./node_modules/vue-loader/lib/loaders/templateLoader.js??ref--7!./node_modules/@quasar/app/lib/webpack/loader.auto-import-client.js?kebab!./node_modules/vue-loader/lib??vue-loader-options!./src/App.vue?vue&type=template&id=3930a7c2&
var Appvue_type_template_id_3930a7c2_render = function render() {
  var _vm = this,
      _c = _vm._self._c,
      _setup = _vm._self._setupProxy;

  return _c('div', {
    attrs: {
      "id": "q-app"
    }
  }, [_c('keep-alive', [_c('router-view')], 1)], 1);
};

var staticRenderFns = [];

// CONCATENATED MODULE: ./src/App.vue?vue&type=template&id=3930a7c2&

// EXTERNAL MODULE: ./node_modules/quasar/src/plugins/LoadingBar.js + 1 modules
var LoadingBar = __webpack_require__("1b3f");

// EXTERNAL MODULE: ./node_modules/vue-router/dist/vue-router.esm.js
var vue_router_esm = __webpack_require__("8c4f");

// EXTERNAL MODULE: ./node_modules/core-js/modules/es.object.assign.js
var es_object_assign = __webpack_require__("cca6");

// CONCATENATED MODULE: ./src/security/index.js


var instance;
/** Returns the current instance of the SDK */

var getInstance = function getInstance() {
  return instance;
};
/** Creates an instance of the Auth0 SDK. If one has already been created, it returns that instance */

var security_Security = function Security(_ref) {
  var options = Object.assign({}, _ref);
  if (instance) return instance; // The 'instance' is simply a Vue object

  instance = new vue_runtime_esm["default"]({
    data: function data() {
      return {
        level: 'LEVEL 1',
        auth: this.$auth,
        token: function token() {
          // return this.$auth.getTokenSilently({ audience: 'https://api.elasticcode.ai/' })
          return this.$auth.getTokenSilently();
        },
        user: function user() {
          return this.$auth.user;
        }
      };
    },
    methods: {}
  });
  return instance;
};
var SecurityPlugin = {
  install: function install(Vue, options) {
    Vue.prototype.security = security_Security(options);
    console.log('SECURITY INJECTION COMPLETE ', Vue.prototype.security);
  }
};
// EXTERNAL MODULE: ./node_modules/msw/lib/index.js
var lib = __webpack_require__("9525");

// EXTERNAL MODULE: ./node_modules/jsplumbtoolkit-vue2/jsplumbtoolkit-vue2.js + 2 modules
var jsplumbtoolkit_vue2 = __webpack_require__("88c0");

// EXTERNAL MODULE: ./src/plugins/stream-plugin.ts
var stream_plugin = __webpack_require__("51a7");

// EXTERNAL MODULE: ./auth_config.json
var auth_config = __webpack_require__("8160");

// EXTERNAL MODULE: ./node_modules/@babel/runtime/helpers/objectSpread2.js
var objectSpread2 = __webpack_require__("ded3");
var objectSpread2_default = /*#__PURE__*/__webpack_require__.n(objectSpread2);

// EXTERNAL MODULE: ./node_modules/@babel/runtime/helpers/objectWithoutProperties.js
var objectWithoutProperties = __webpack_require__("4082");
var objectWithoutProperties_default = /*#__PURE__*/__webpack_require__.n(objectWithoutProperties);

// EXTERNAL MODULE: ./node_modules/core-js/modules/es.array.includes.js
var es_array_includes = __webpack_require__("caad");

// EXTERNAL MODULE: ./node_modules/core-js/modules/es.string.includes.js
var es_string_includes = __webpack_require__("2532");

// EXTERNAL MODULE: ./node_modules/core-js/modules/es.string.search.js
var es_string_search = __webpack_require__("841c");

// EXTERNAL MODULE: ./node_modules/@auth0/auth0-spa-js/dist/auth0-spa-js.production.esm.js
var auth0_spa_js_production_esm = __webpack_require__("9767");

// CONCATENATED MODULE: ./src/auth/index.js










/** Define a default action to perform after authentication */

var DEFAULT_REDIRECT_CALLBACK = function DEFAULT_REDIRECT_CALLBACK() {
  return window.history.replaceState({}, document.title, window.location.pathname);
};

var auth_instance;
/** Returns the current instance of the SDK */

var auth_getInstance = function getInstance() {
  return auth_instance;
};
/** Creates an instance of the Auth0 SDK. If one has already been created, it returns that instance */

var auth_useAuth0 = function useAuth0(_ref) {
  var _ref$onRedirectCallba = _ref.onRedirectCallback,
      onRedirectCallback = _ref$onRedirectCallba === void 0 ? DEFAULT_REDIRECT_CALLBACK : _ref$onRedirectCallba,
      _ref$redirectUri = _ref.redirectUri,
      redirectUri = _ref$redirectUri === void 0 ? window.location.origin : _ref$redirectUri,
      options = objectWithoutProperties_default()(_ref, ["onRedirectCallback", "redirectUri"]);

  if (auth_instance) return auth_instance; // The 'instance' is simply a Vue object

  auth_instance = new vue_runtime_esm["default"]({
    data: function data() {
      return {
        loading: true,
        isAuthenticated: false,
        user: {},
        auth0Client: null,
        popupOpen: false,
        error: null
      };
    },
    methods: {
      /** Authenticates the user using a popup window */
      loginWithPopup: function loginWithPopup(callback, options, config) {
        var _this = this;

        return asyncToGenerator_default()( /*#__PURE__*/regeneratorRuntime.mark(function _callee() {
          var user;
          return regeneratorRuntime.wrap(function _callee$(_context) {
            while (1) {
              switch (_context.prev = _context.next) {
                case 0:
                  _this.popupOpen = true;
                  _context.prev = 1;
                  _context.next = 4;
                  return _this.auth0Client.loginWithPopup(options, config);

                case 4:
                  _context.next = 6;
                  return _this.auth0Client.getUser();

                case 6:
                  _this.user = _context.sent;
                  _context.next = 9;
                  return _this.auth0Client.isAuthenticated();

                case 9:
                  _this.isAuthenticated = _context.sent;
                  _this.error = null;
                  _context.next = 17;
                  break;

                case 13:
                  _context.prev = 13;
                  _context.t0 = _context["catch"](1);
                  _this.error = _context.t0; // eslint-disable-next-line

                  console.error(_context.t0);

                case 17:
                  _context.prev = 17;
                  _this.popupOpen = false;
                  return _context.finish(17);

                case 20:
                  _context.next = 22;
                  return _this.auth0Client.getUser();

                case 22:
                  user = _context.sent;
                  _this.user = user;
                  _this.isAuthenticated = user !== undefined;
                  callback(_this.user);

                case 26:
                case "end":
                  return _context.stop();
              }
            }
          }, _callee, null, [[1, 13, 17, 20]]);
        }))();
      },

      /** Handles the callback when logging in using a redirect */
      handleRedirectCallback: function handleRedirectCallback() {
        var _this2 = this;

        return asyncToGenerator_default()( /*#__PURE__*/regeneratorRuntime.mark(function _callee2() {
          return regeneratorRuntime.wrap(function _callee2$(_context2) {
            while (1) {
              switch (_context2.prev = _context2.next) {
                case 0:
                  _this2.loading = true;
                  _context2.prev = 1;
                  _context2.next = 4;
                  return _this2.auth0Client.handleRedirectCallback();

                case 4:
                  _context2.next = 6;
                  return _this2.auth0Client.getUser();

                case 6:
                  _this2.user = _context2.sent;
                  _this2.isAuthenticated = true;
                  _this2.error = null;
                  _context2.next = 14;
                  break;

                case 11:
                  _context2.prev = 11;
                  _context2.t0 = _context2["catch"](1);
                  _this2.error = _context2.t0;

                case 14:
                  _context2.prev = 14;
                  _this2.loading = false;
                  return _context2.finish(14);

                case 17:
                case "end":
                  return _context2.stop();
              }
            }
          }, _callee2, null, [[1, 11, 14, 17]]);
        }))();
      },

      /** Authenticates the user using the redirect method */
      loginWithRedirect: function loginWithRedirect(o) {
        return this.auth0Client.loginWithRedirect(o);
      },

      /** Returns all the claims present in the ID token */
      getIdTokenClaims: function getIdTokenClaims(o) {
        return this.auth0Client.getIdTokenClaims(o);
      },

      /** Returns the access token. If the token is invalid or missing, a new one is retrieved */
      getTokenSilently: function getTokenSilently(o) {
        return this.auth0Client.getTokenSilently(o);
      },

      /** Gets the access token using a popup window */
      getTokenWithPopup: function getTokenWithPopup(o) {
        return this.auth0Client.getTokenWithPopup(o);
      },

      /** Logs the user out and removes their session on the authorization server */
      logout: function logout(o) {
        return this.auth0Client.logout(o);
      }
    },

    /** Use this lifecycle method to instantiate the SDK client */
    created: function created() {
      var _this3 = this;

      return asyncToGenerator_default()( /*#__PURE__*/regeneratorRuntime.mark(function _callee3() {
        var _yield$_this3$auth0Cl, appState;

        return regeneratorRuntime.wrap(function _callee3$(_context3) {
          while (1) {
            switch (_context3.prev = _context3.next) {
              case 0:
                _context3.next = 2;
                return Object(auth0_spa_js_production_esm["a" /* createAuth0Client */])(objectSpread2_default()(objectSpread2_default()({}, options), {}, {
                  authorizationParams: {
                    redirect_uri: redirectUri
                  }
                }));

              case 2:
                _this3.auth0Client = _context3.sent;
                _context3.prev = 3;

                if (!(window.location.search.includes('code=') && window.location.search.includes('state='))) {
                  _context3.next = 11;
                  break;
                }

                _context3.next = 7;
                return _this3.auth0Client.handleRedirectCallback();

              case 7:
                _yield$_this3$auth0Cl = _context3.sent;
                appState = _yield$_this3$auth0Cl.appState;
                _this3.error = null; // Notify subscribers that the redirect callback has happened, passing the appState
                // (useful for retrieving any pre-authentication state)

                onRedirectCallback(appState);

              case 11:
                _context3.next = 16;
                break;

              case 13:
                _context3.prev = 13;
                _context3.t0 = _context3["catch"](3);
                _this3.error = _context3.t0;

              case 16:
                _context3.prev = 16;
                _context3.next = 19;
                return _this3.auth0Client.isAuthenticated();

              case 19:
                _this3.isAuthenticated = _context3.sent;
                _context3.next = 22;
                return _this3.auth0Client.getUser();

              case 22:
                _this3.user = _context3.sent;
                _this3.loading = false;
                return _context3.finish(16);

              case 25:
              case "end":
                return _context3.stop();
            }
          }
        }, _callee3, null, [[3, 13, 16, 25]]);
      }))();
    }
  });
  return auth_instance;
}; // Create a simple Vue plugin to expose the wrapper object throughout the application

var Auth0Plugin = {
  install: function install(Vue, options) {
    Vue.prototype.$auth = auth_useAuth0(options);
  }
};
// CONCATENATED MODULE: ./src/router/routes.ts
// import { LoginCallback } from '@okta/okta-vue'
const routes = [
    {
        path: '/',
        component: () => Promise.all(/* import() */[__webpack_require__.e(0), __webpack_require__.e(1), __webpack_require__.e(4)]).then(__webpack_require__.bind(null, "713b")),
        children: [{ path: '', component: () => Promise.all(/* import() */[__webpack_require__.e(0), __webpack_require__.e(3)]).then(__webpack_require__.bind(null, "5bda")) }]
    },
    {
        path: '/app',
        component: () => Promise.all(/* import() */[__webpack_require__.e(0), __webpack_require__.e(1), __webpack_require__.e(5)]).then(__webpack_require__.bind(null, "dead"))
    },
    {
        path: '/block',
        name: 'block',
        component: () => Promise.all(/* import() */[__webpack_require__.e(0), __webpack_require__.e(7)]).then(__webpack_require__.bind(null, "7df3"))
    },
    // Always leave this as last one,
    // but you can also remove it
    {
        path: '*',
        component: () => Promise.all(/* import() */[__webpack_require__.e(0), __webpack_require__.e(8)]).then(__webpack_require__.bind(null, "e51e"))
    },
    // { path: '/login/callback', component: LoginCallback }
    /*
    {
      path: '/profile',
      name: 'profile',
      component: () => import('components/Profile.vue')
    }, */
    {
        path: '/logout',
        name: 'logout',
        component: () => __webpack_require__.e(/* import() */ 6).then(__webpack_require__.bind(null, "4ab3"))
    }
];
/* harmony default export */ var router_routes = (routes);

// CONCATENATED MODULE: ./src/router/index.ts


const Router = new vue_router_esm["a" /* default */]({
    scrollBehavior: () => ({ x: 0, y: 0 }),
    routes: router_routes,
    // Leave these as is and change from quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    mode: "hash",
    base: ""
});
/* harmony default export */ var src_router = (Router);

// EXTERNAL MODULE: ./node_modules/@quasar/quasar-ui-qmarkdown/dist/index.css
var dist = __webpack_require__("0247");

// CONCATENATED MODULE: ./node_modules/@quasar/app/lib/webpack/loader.transform-quasar-imports.js!./node_modules/ts-loader??ref--3-0!./node_modules/@quasar/app/lib/webpack/loader.auto-import-client.js?kebab!./node_modules/vue-loader/lib??vue-loader-options!./src/App.vue?vue&type=script&lang=ts&
;




const handlers = [
    // TODO: Implement flow block dispatcher here
    // It will be up to the app to load the flows first
    // e.g. let flow = ElasticCode.loadFlow("/Home/Database Example")
    // let result = flow.block("Service").run({"some":"data"})
    lib["rest"].get('/apitest/', (req, res, ctx) => {
        return res(ctx.status(200), ctx.json({
            username: 'admin'
        }));
    })
];
const worker = Object(lib["setupWorker"])(...handlers);
worker.start({ onUnhandledRequest: 'bypass' });
vue_runtime_esm["default"].use(vue_router_esm["a" /* default */]);






vue_runtime_esm["default"].use(SecurityPlugin);
// eslint-disable-next-line @typescript-eslint/no-unsafe-assignment,@typescript-eslint/no-var-requires
const VueTypedJs = __webpack_require__("8cb8");
vue_runtime_esm["default"].use(Auth0Plugin, {
    domain: auth_config["b" /* domain */],
    clientId: auth_config["a" /* clientId */],
    onRedirectCallback: (appState) => {
        src_router.push(appState && appState.targetUrl
            ? appState.targetUrl
            : window.location.pathname);
    }
});
vue_runtime_esm["default"].use(VueTypedJs);
vue_runtime_esm["default"].use(stream_plugin["a" /* default */]);
vue_runtime_esm["default"].use(jsplumbtoolkit_vue2["c" /* JsPlumbToolkitVue2Plugin */]);
vue_runtime_esm["default"].config.silent = true;
LoadingBar["a" /* default */].setDefaults({
    color: 'dark',
    size: '3px',
    position: 'top'
});
/* harmony default export */ var Appvue_type_script_lang_ts_ = (vue_runtime_esm["default"].extend({
    components: {},
    created() {
        console.log('Q', this.$q);
        console.log('VERSION', this.$store.state.designer.version);
        console.log('DEV', false);
        console.log('CLIENT', true);
        console.log('SERVER', false);
        console.log('NODE_ENV', "production");
    },
    mounted() {
    },
    data() {
        return {
            incrementStr: 3
        };
    },
    computed: {
        wrapper() {
            return { increment: +this.incrementStr };
        }
    }
}));

// CONCATENATED MODULE: ./src/App.vue?vue&type=script&lang=ts&
 /* harmony default export */ var src_Appvue_type_script_lang_ts_ = (Appvue_type_script_lang_ts_); 
// EXTERNAL MODULE: ./node_modules/vue-loader/lib/runtime/componentNormalizer.js
var componentNormalizer = __webpack_require__("2877");

// CONCATENATED MODULE: ./src/App.vue





/* normalize component */

var component = Object(componentNormalizer["a" /* default */])(
  src_Appvue_type_script_lang_ts_,
  Appvue_type_template_id_3930a7c2_render,
  staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* harmony default export */ var App = (component.exports);
// EXTERNAL MODULE: ./node_modules/quasar/wrappers/index.js
var wrappers = __webpack_require__("4bde");

// EXTERNAL MODULE: ./node_modules/vuex/dist/vuex.esm.js
var vuex_esm = __webpack_require__("2f62");

// CONCATENATED MODULE: ./src/store/client/state.ts
function state() {
    return {
        logged_in: false
    };
}
/* harmony default export */ var client_state = (state);

// CONCATENATED MODULE: ./src/store/client/actions.ts
const actions = {
    someAction( /* context */) {
        // your code
    }
};
/* harmony default export */ var client_actions = (actions);

// CONCATENATED MODULE: ./src/store/client/getters.ts
const getters = {
    getLoggedIn() {
        console.log('getLoggedIn ', this.logged_in);
        return this.logged_in;
    }
};
/* harmony default export */ var client_getters = (getters);

// CONCATENATED MODULE: ./src/store/client/mutations.ts
const mutation = {
    updateLoggedIn(state, val) {
        console.log('updatedLoggedIn:', val);
        state.logged_in = val;
        console.log('updatedLoggedIn:', this.logged_in);
    }
};
/* harmony default export */ var mutations = (mutation);

// CONCATENATED MODULE: ./src/store/client/index.ts




const exampleModule = {
    namespaced: true,
    actions: client_actions,
    getters: client_getters,
    mutations: mutations,
    state: client_state
};
/* harmony default export */ var client = (exampleModule);

// EXTERNAL MODULE: ./src/store/CountStore.ts
var CountStore = __webpack_require__("6dee");

// CONCATENATED MODULE: ./src/store/DesignerStore.ts


const STORE_NAME = 'designer';
const SET_MESSAGE = 'setMessage';
const SET_STREAMING = 'setStreaming';
const SET_CONNECTED = 'setConnected';
const SET_TOKEN = 'setToken';
const SET_SUBSCRIPTION = 'setSubscription';
const SET_PYTHON = 'setPython';
const DesignerStore_getters = {
    getMessage(state) {
        return state.message;
    },
    getStreaming(state) {
        return state.streaming;
    },
    getConnected(state) {
        return state.connected;
    },
    getPython(state) {
        return state.python;
    },
    getVersion(state) {
        return state.version;
    },
    getToken(state) {
        return state.token;
    },
    getSubscription(state) {
        return state.subscription;
    }
};
const DesignerStore_actions = {
    async setMessage({ commit }, { message }) {
        await new Promise(resolve => {
            commit(SET_MESSAGE, message);
            resolve();
        });
    },
    async setStreaming({ commit }, { streaming }) {
        await new Promise(resolve => {
            commit(SET_STREAMING, streaming);
            resolve();
        });
    },
    async setConnected({ commit }, { connected }) {
        await new Promise(resolve => {
            commit(SET_CONNECTED, connected);
            resolve();
        });
    },
    async setPython({ commit }, { python }) {
        await new Promise(resolve => {
            commit(SET_PYTHON, python);
            resolve();
        });
    },
    async setToken({ commit }, { token }) {
        await new Promise(resolve => {
            commit(SET_TOKEN, token);
            resolve();
        });
    },
    async setSubscription({ commit }, { subscription }) {
        await new Promise(resolve => {
            commit(SET_SUBSCRIPTION, subscription);
            resolve();
        });
    }
};
const DesignerStore = {
    namespaced: true,
    state: {
        message: 'Ready',
        streaming: false,
        connected: false,
        python: false,
        version: "v1.0.0 Free Version",
        token: 'none',
        subscription: 'none'
    },
    getters: DesignerStore_getters,
    mutations: {
        setMessage(state, message) {
            state.message = message;
        },
        setStreaming(state, streaming) {
            state.streaming = streaming;
        },
        setConnected(state, connected) {
            state.connected = connected;
        },
        setPython(state, python) {
            state.python = python;
        },
        setToken(state, token) {
            state.token = token;
        },
        setSubscription(state, subscription) {
            state.subscription = subscription;
        }
    },
    actions: DesignerStore_actions
};
const mappedStatusState = Object(vuex_esm["d" /* mapState */])(STORE_NAME, [
    'message', 'streaming', 'connected', 'python', 'version', 'token', 'subscription'
]);
const mappedStatusGetters = Object(vuex_esm["c" /* mapGetters */])(STORE_NAME, [
    'getMessage', 'getStreaming', 'getConnected', 'getPython', 'getVersion', 'getToken', 'getSubscription'
]);
const mappedStatusActions = Object(vuex_esm["b" /* mapActions */])(STORE_NAME, [
    'setMessage', 'setStreaming', 'setConnected', 'setPython', 'setVersion', 'setToken', 'setSubscription'
]);
const DesignerComponentBase = vue_runtime_esm["default"].extend({
    computed: {
        ...mappedStatusState,
        ...mappedStatusGetters
    },
    methods: {
        ...mappedStatusActions
    }
});
// This class will implement a variety of interfaces for each type of state used by the designer app
class DesignerStore_DesignerComponentBaseClass extends vue_runtime_esm["default"] {
}

// CONCATENATED MODULE: ./src/store/index.ts





const count = CountStore["b" /* CountStore */];
const designer = DesignerStore;
/* harmony default export */ var src_store = (Object(wrappers["store"])(({ Vue }) => {
    Vue.use(vuex_esm["a" /* default */]);
    const Store = new vuex_esm["a" /* default */].Store({
        modules: {
            client: client,
            count,
            designer
        },
        // enable strict mode (adds overhead!)
        // for dev mode only
        strict: !!true
    });
    return Store;
}));

// CONCATENATED MODULE: ./.quasar/app.js



/**
 * THIS FILE IS GENERATED AUTOMATICALLY.
 * DO NOT EDIT.
 *
 * You are probably looking on adding startup/initialization code.
 * Use "quasar new boot <name>" and add it there.
 * One boot file per concern. Then reference the file(s) in quasar.conf.js > boot:
 * boot: ['file', ...] // do not add ".js" extension to it.
 *
 * Boot files are your "main.js"
 **/





/* harmony default export */ var _quasar_app = (function () {
  return app_ref.apply(this, arguments);
});

function app_ref() {
  app_ref = asyncToGenerator_default()( /*#__PURE__*/regeneratorRuntime.mark(function _callee() {
    var store, router, app;
    return regeneratorRuntime.wrap(function _callee$(_context) {
      while (1) {
        switch (_context.prev = _context.next) {
          case 0:
            if (!(typeof src_store === 'function')) {
              _context.next = 6;
              break;
            }

            _context.next = 3;
            return src_store({
              Vue: vue_runtime_esm["default"]
            });

          case 3:
            _context.t0 = _context.sent;
            _context.next = 7;
            break;

          case 6:
            _context.t0 = src_store;

          case 7:
            store = _context.t0;

            if (!(typeof src_router === 'function')) {
              _context.next = 14;
              break;
            }

            _context.next = 11;
            return src_router({
              Vue: vue_runtime_esm["default"],
              store: store
            });

          case 11:
            _context.t1 = _context.sent;
            _context.next = 15;
            break;

          case 14:
            _context.t1 = src_router;

          case 15:
            router = _context.t1;
            // make router instance available in store
            store.$router = router; // Create the app instantiation Object.
            // Here we inject the router, store to all child components,
            // making them available everywhere as `this.$router` and `this.$store`.

            app = {
              router: router,
              store: store,
              render: function render(h) {
                return h(App);
              }
            };
            app.el = '#q-app'; // expose the app, the router and the store.
            // note we are not mounting the app here, since bootstrapping will be
            // different depending on whether we are in a browser or on the server.

            return _context.abrupt("return", {
              app: app,
              store: store,
              router: router
            });

          case 20:
          case "end":
            return _context.stop();
        }
      }
    }, _callee);
  }));
  return app_ref.apply(this, arguments);
}
// EXTERNAL MODULE: ./node_modules/@vue/composition-api/dist/vue-composition-api.umd.js
var vue_composition_api_umd = __webpack_require__("e4fd");
var vue_composition_api_umd_default = /*#__PURE__*/__webpack_require__.n(vue_composition_api_umd);

// CONCATENATED MODULE: ./src/boot/composition-api.ts


/* harmony default export */ var composition_api = (Object(wrappers["boot"])(({ Vue }) => {
    Vue.use(vue_composition_api_umd_default.a);
}));

// CONCATENATED MODULE: ./src/i18n/en-us/index.ts
// This is just an example,
// so you can safely delete all default props below
/* harmony default export */ var i18n_en_us = ({
    failed: 'Action failed',
    success: 'Action was successful'
});

// CONCATENATED MODULE: ./src/i18n/index.ts

/* harmony default export */ var i18n = ({
    'en-us': i18n_en_us
});

// EXTERNAL MODULE: ./node_modules/vue-i18n/dist/vue-i18n.esm.js
var vue_i18n_esm = __webpack_require__("a925");

// CONCATENATED MODULE: ./src/boot/i18n.ts




vue_runtime_esm["default"].use(vue_i18n_esm["a" /* default */]);
const i18n_i18n = new vue_i18n_esm["a" /* default */]({
    locale: 'en-us',
    fallbackLocale: 'en-us',
    messages: i18n
});
/* harmony default export */ var boot_i18n = (Object(wrappers["boot"])(({ app }) => {
    // Set i18n instance on app
    app.i18n = i18n_i18n;
}));

// EXTERNAL MODULE: ./node_modules/axios/index.js
var axios = __webpack_require__("bc3a");
var axios_default = /*#__PURE__*/__webpack_require__.n(axios);

// CONCATENATED MODULE: ./src/boot/axios.ts


/* harmony default export */ var boot_axios = (Object(wrappers["boot"])(({ Vue }) => {
    // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
    Vue.prototype.$axios = axios_default.a;
}));

// EXTERNAL MODULE: ./node_modules/vue-apexcharts/dist/vue-apexcharts.js
var vue_apexcharts = __webpack_require__("1321");
var vue_apexcharts_default = /*#__PURE__*/__webpack_require__.n(vue_apexcharts);

// CONCATENATED MODULE: ./src/boot/charts.ts


/* harmony default export */ var charts = (Object(wrappers["boot"])(({ Vue }) => {
    Vue.use(vue_apexcharts_default.a);
    Vue.component('Apexchart', vue_apexcharts_default.a);
}));

// EXTERNAL MODULE: ./node_modules/@quasar/quasar-app-extension-qmarkdown/src/boot/register.js + 14 modules
var register = __webpack_require__("4b46");

// CONCATENATED MODULE: ./.quasar/client-entry.js





/**
 * THIS FILE IS GENERATED AUTOMATICALLY.
 * DO NOT EDIT.
 *
 * You are probably looking on adding startup/initialization code.
 * Use "quasar new boot <name>" and add it there.
 * One boot file per concern. Then reference the file(s) in quasar.conf.js > boot:
 * boot: ['file', ...] // do not add ".js" extension to it.
 *
 * Boot files are your "main.js"
 **/









































































































 // We load Quasar stylesheet file











vue_runtime_esm["default"].config.devtools = true;
vue_runtime_esm["default"].config.productionTip = false;
var publicPath = "";

function start() {
  return _start.apply(this, arguments);
}

function _start() {
  _start = asyncToGenerator_default()( /*#__PURE__*/regeneratorRuntime.mark(function _callee() {
    var _yield$createApp, app, store, router, hasRedirected, redirect, urlPath, bootFiles, i;

    return regeneratorRuntime.wrap(function _callee$(_context) {
      while (1) {
        switch (_context.prev = _context.next) {
          case 0:
            _context.next = 2;
            return _quasar_app();

          case 2:
            _yield$createApp = _context.sent;
            app = _yield$createApp.app;
            store = _yield$createApp.store;
            router = _yield$createApp.router;
            hasRedirected = false;

            redirect = function redirect(url) {
              hasRedirected = true;
              var normalized = Object(url) === url ? router.resolve(url).route.fullPath : url;
              window.location.href = normalized;
            };

            urlPath = window.location.href.replace(window.location.origin, '');
            bootFiles = [composition_api, boot_i18n, boot_axios, charts, register["default"]];
            i = 0;

          case 11:
            if (!(hasRedirected === false && i < bootFiles.length)) {
              _context.next = 29;
              break;
            }

            if (!(typeof bootFiles[i] !== 'function')) {
              _context.next = 14;
              break;
            }

            return _context.abrupt("continue", 26);

          case 14:
            _context.prev = 14;
            _context.next = 17;
            return bootFiles[i]({
              app: app,
              router: router,
              store: store,
              Vue: vue_runtime_esm["default"],
              ssrContext: null,
              redirect: redirect,
              urlPath: urlPath,
              publicPath: publicPath
            });

          case 17:
            _context.next = 26;
            break;

          case 19:
            _context.prev = 19;
            _context.t0 = _context["catch"](14);

            if (!(_context.t0 && _context.t0.url)) {
              _context.next = 24;
              break;
            }

            window.location.href = _context.t0.url;
            return _context.abrupt("return");

          case 24:
            console.error('[Quasar] boot error:', _context.t0);
            return _context.abrupt("return");

          case 26:
            i++;
            _context.next = 11;
            break;

          case 29:
            if (!(hasRedirected === true)) {
              _context.next = 31;
              break;
            }

            return _context.abrupt("return");

          case 31:
            new vue_runtime_esm["default"](app);

          case 32:
          case "end":
            return _context.stop();
        }
      }
    }, _callee, null, [[14, 19]]);
  }));
  return _start.apply(this, arguments);
}

start();

/***/ }),

/***/ "51a7":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(process) {/* harmony import */ var socket_io_client__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__("daa8");

/* harmony default export */ __webpack_exports__["a"] = ({
    // called by Vue.use(FirstPlugin)
    install(Vue, options) {
        // create a mixin
        const socket = Object(socket_io_client__WEBPACK_IMPORTED_MODULE_0__[/* io */ "a"])(process.env.SOCKETIO);
        socket.on('basicEmit', (a, b, c) => {
            // console.log("STREAM PLUGIN: SERVER EMIT", a, b, c)
        });
        Vue.mixin({
            created() {
                // console.log("FIRST PLUGIN",Vue);
            }
        });
    }
});

/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__("4362")))

/***/ }),

/***/ "6dee":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "b", function() { return CountStore; });
/* unused harmony export mappedCountState */
/* unused harmony export mappedCountGetters */
/* unused harmony export mappedCountActions */
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return CountComponentBase; });
/* unused harmony export CountComponentBaseClass */
/* harmony import */ var vuex__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__("2f62");
/* harmony import */ var vue__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__("2b0e");


// import { STORE_NAME as META_STORE_NAME, NEW_MUTATION } from './MetaStore';
const STORE_NAME = 'count';
const INCREMENT = 'increment';
const getters = {
    isEven(state) {
        return !(state.count % 2);
    }
};
const actions = {
    async performAsyncIncrement({ commit /* state, rootState */ }, { increment, delayMs }) {
        await new Promise(resolve => {
            setTimeout(() => {
                // commit(`${META_STORE_NAME}/${NEW_MUTATION}`, null, { root: true });
                commit(INCREMENT, increment);
                resolve();
            }, delayMs);
        });
    }
};
const CountStore = {
    namespaced: true,
    state: {
        count: 0
    },
    getters,
    mutations: {
        [INCREMENT](state, increment = 1) {
            state.count += increment;
        }
    },
    actions
};
const mappedCountState = Object(vuex__WEBPACK_IMPORTED_MODULE_0__[/* mapState */ "d"])(STORE_NAME, [
    'count'
]);
const mappedCountGetters = Object(vuex__WEBPACK_IMPORTED_MODULE_0__[/* mapGetters */ "c"])(STORE_NAME, [
    'isEven'
]);
const mappedCountActions = Object(vuex__WEBPACK_IMPORTED_MODULE_0__[/* mapActions */ "b"])(STORE_NAME, [
    'performAsyncIncrement'
]);
const CountComponentBase = vue__WEBPACK_IMPORTED_MODULE_1__["default"].extend({
    computed: {
        ...mappedCountState,
        ...mappedCountGetters
    },
    methods: {
        ...mappedCountActions
    }
});
class CountComponentBaseClass extends vue__WEBPACK_IMPORTED_MODULE_1__["default"] {
}


/***/ }),

/***/ "8160":
/***/ (function(module) {

module.exports = JSON.parse("{\"b\":\"elasticcode.us.auth0.com\",\"a\":\"LpGArknVfsb05jUVVLklp2xSvnFDlRiQ\"}");

/***/ })

/******/ });
//# sourceMappingURL=app.d7192762.js.map