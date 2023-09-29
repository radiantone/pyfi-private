(window["webpackJsonp"] = window["webpackJsonp"] || []).push([[4],{

/***/ "1a0a":
/***/ (function(module, exports, __webpack_require__) {

// extracted by mini-css-extract-plugin

/***/ }),

/***/ "2793":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _node_modules_mini_css_extract_plugin_dist_loader_js_ref_7_oneOf_2_0_node_modules_css_loader_dist_cjs_js_ref_7_oneOf_2_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_src_index_js_ref_7_oneOf_2_2_node_modules_quasar_app_lib_webpack_loader_auto_import_client_js_kebab_node_modules_vue_loader_lib_index_js_vue_loader_options_ToolPalette_vue_vue_type_style_index_0_id_1993a0da_prod_scoped_true_lang_css___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__("3723");
/* harmony import */ var _node_modules_mini_css_extract_plugin_dist_loader_js_ref_7_oneOf_2_0_node_modules_css_loader_dist_cjs_js_ref_7_oneOf_2_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_src_index_js_ref_7_oneOf_2_2_node_modules_quasar_app_lib_webpack_loader_auto_import_client_js_kebab_node_modules_vue_loader_lib_index_js_vue_loader_options_ToolPalette_vue_vue_type_style_index_0_id_1993a0da_prod_scoped_true_lang_css___WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_mini_css_extract_plugin_dist_loader_js_ref_7_oneOf_2_0_node_modules_css_loader_dist_cjs_js_ref_7_oneOf_2_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_src_index_js_ref_7_oneOf_2_2_node_modules_quasar_app_lib_webpack_loader_auto_import_client_js_kebab_node_modules_vue_loader_lib_index_js_vue_loader_options_ToolPalette_vue_vue_type_style_index_0_id_1993a0da_prod_scoped_true_lang_css___WEBPACK_IMPORTED_MODULE_0__);
/* unused harmony reexport * */


/***/ }),

/***/ "28e7":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";

// EXTERNAL MODULE: ./node_modules/core-js/modules/es.function.name.js
var es_function_name = __webpack_require__("b0c0");

// CONCATENATED MODULE: ./node_modules/@quasar/app/lib/webpack/loader.transform-quasar-imports.js!./node_modules/babel-loader/lib??ref--2-0!./node_modules/vue-loader/lib/loaders/templateLoader.js??ref--7!./node_modules/@quasar/app/lib/webpack/loader.auto-import-client.js?kebab!./node_modules/vue-loader/lib??vue-loader-options!./src/components/ToolPalette.vue?vue&type=template&id=1993a0da&scoped=true&


var render = function render() {
  var _vm = this,
      _c = _vm._self._c;

  return _c('div', [_c('q-toolbar', {
    staticClass: "sidebar node-palette",
    staticStyle: {
      "padding": "0px"
    }
  }, [_c('img', {
    staticStyle: {
      "padding-left": "15px",
      "height": "55px",
      "padding-right": "10px"
    },
    attrs: {
      "src": __webpack_require__("4676")
    }
  }), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "min-height": "56px",
      "cursor": "grabbing",
      "font-size": "1.5em"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "icon": "las la-file-alt",
      "aria-label": "Data",
      "size": "large",
      "id": "data"
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        Data\n      ")])], 1), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "icon": _vm.braces,
      "aria-label": "Schema",
      "size": "large",
      "id": "schema"
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        Schema\n      ")])], 1), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "icon": _vm.border,
      "aria-label": "Border",
      "size": "large",
      "id": "border"
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        Border\n      ")])], 1), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "icon": "las la-scroll",
      "aria-label": "Script",
      "size": "xl",
      "id": "script"
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        Script\n      ")])], 1), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "icon": "icon-processor",
      "aria-label": "Processor",
      "size": "large",
      "id": "processor",
      "disabled": !_vm.hasHosted,
      "title": "Upgrade to Hosted Plan"
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        Processor\n      ")])], 1), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "icon": "las la-cloud-upload-alt",
      "aria-label": "API",
      "size": "xl",
      "id": "api"
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        API\n      ")])], 1), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "icon": "las la-sign-in-alt",
      "aria-label": "Label",
      "size": "xl",
      "id": "queue",
      "disabled": !_vm.hasPro
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        Queue\n      ")])], 1), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "icon": "las la-redo-alt",
      "aria-label": "Loop",
      "size": "xl",
      "id": "loop"
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        Loop\n      ")])], 1), _c('q-btn', {
    staticClass: "text-dark text-bold sidebar-item",
    staticStyle: {
      "display": "none",
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "icon": "icon-group",
      "aria-label": "Group",
      "size": "large",
      "data-node-icon": "far fa-object-group",
      "data-node-type": "group",
      "data-node-name": "Group",
      "data-node-label": "Group",
      "data-node-description": "A processor group description",
      "data-node-package": "my.python.package",
      "data-node-id": "group",
      "jtk-is-group": "true",
      "id": "processorgroup"
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        Process Group\n      ")])], 1), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "icon": "las la-table",
      "aria-label": "spreadsheet",
      "size": "xl",
      "id": "spreadsheet"
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        Spreadsheet\n      ")])], 1), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "icon": "las la-database",
      "aria-label": "Database",
      "size": "xl",
      "id": "database",
      "disabled": !_vm.hasHosted,
      "title": "Upgrade to Hosted Plan"
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        Database\n      ")])], 1), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "icon": "icon-label",
      "aria-label": "Label",
      "size": "large",
      "id": "label"
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        Label\n      ")])], 1), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "display": "none",
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "icon": _vm.markdown,
      "aria-label": "Label",
      "size": "xl",
      "id": "markdown"
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        Markdown\n      ")])], 1), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "display": "none",
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "icon": "las la-robot",
      "aria-label": "Label",
      "size": "xl",
      "id": "chatgpt"
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        ChatGPT\n      ")])], 1), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "display": "none",
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "icon": "las la-code",
      "aria-label": "Label",
      "size": "xl",
      "id": "lambda"
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        Lambda Function\n      ")]), _c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        Lambda\n      ")])], 1), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "icon": "las la-brain",
      "aria-label": "Label",
      "size": "xl",
      "id": "inference",
      "disabled": !_vm.hasPro
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        Inference\n      ")])], 1), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "icon": "las la-window-maximize",
      "aria-label": "App",
      "size": "xl"
    },
    on: {
      "click": function click($event) {
        return _vm.$router.push('/app');
      }
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        App\n      ")])], 1), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "icon": "las la-book",
      "aria-label": "App",
      "size": "xl",
      "id": "library",
      "disabled": !_vm.hasPro,
      "title": "Upgrade to PRO Plan"
    },
    on: {
      "click": _vm.openLibrary
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        Library\n      ")])], 1), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "aria-label": "AI Buddy",
      "size": "xl",
      "id": "chat",
      "title": "Python Tools"
    },
    on: {
      "click": _vm.openChat
    }
  }, [_c('img', {
    staticStyle: {
      "width": "40px",
      "min-width": "40px"
    },
    attrs: {
      "src": __webpack_require__("68b1")
    }
  }), _c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        Python Tools\n      ")])], 1), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "icon": "las la-ellipsis-h",
      "aria-label": "Elipsis",
      "size": "large",
      "id": "openblocks"
    },
    on: {
      "click": _vm.openBlocks
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n        More Blocks\n      ")])], 1), _c('q-item-label', {
    staticClass: "text-secondary"
  }, [_vm._v("\n      BETA SOFTWARE\n    ")]), _c('q-space'), _vm.$auth.isAuthenticated && _vm.hasHosted ? _c('q-toolbar', [_c('q-space'), _c('q-item-label', {
    staticClass: "text-secondary",
    staticStyle: {
      "margin-top": "40px",
      "margin-right": "20px"
    }
  }, [_c('a', {
    staticClass: "link-hover",
    attrs: {
      "href": "#"
    },
    on: {
      "click": function click($event) {
        return _vm.showStats('Nodes', _vm.nodeStatsColumns, 'nodes');
      }
    }
  }, [_vm._v("Nodes:")]), _c('span', {
    staticClass: "text-dark"
  }, [_vm._v(_vm._s(_vm.nodes))])]), _c('q-item-label', {
    staticClass: "text-secondary",
    staticStyle: {
      "margin-top": "40px",
      "margin-right": "20px"
    },
    attrs: {
      "disabled": false
    }
  }, [_c('a', {
    staticClass: "link-hover",
    attrs: {
      "href": "#"
    },
    on: {
      "click": function click($event) {
        return _vm.showStats('Agents', _vm.agentStatsColumns, 'agents');
      }
    }
  }, [_vm._v("Agents:")]), _c('span', {
    staticClass: "text-dark"
  }, [_vm._v(_vm._s(_vm.agents))])]), _c('q-item-label', {
    staticClass: "text-secondary",
    staticStyle: {
      "margin-top": "40px",
      "margin-right": "20px"
    }
  }, [_c('a', {
    staticClass: "link-hover",
    attrs: {
      "href": "#"
    },
    on: {
      "click": function click($event) {
        return _vm.showStats('Queues', _vm.queueStatsColumns, 'queues');
      }
    }
  }, [_vm._v("Queues:")]), _c('span', {
    staticClass: "text-dark"
  }, [_vm._v(_vm._s(_vm.queues))])]), _c('q-item-label', {
    staticClass: "text-secondary",
    staticStyle: {
      "margin-top": "40px",
      "margin-right": "20px"
    }
  }, [_c('a', {
    staticClass: "link-hover",
    attrs: {
      "href": "#"
    },
    on: {
      "click": function click($event) {
        return _vm.showStats('Processors', _vm.procStatsColumns, 'processors');
      }
    }
  }, [_vm._v("Processors:")]), _c('span', {
    staticClass: "text-dark"
  }, [_vm._v(_vm._s(_vm.processors))])]), _c('q-item-label', {
    staticClass: "text-secondary",
    staticStyle: {
      "margin-top": "40px",
      "margin-right": "20px"
    }
  }, [_c('a', {
    staticClass: "link-hover",
    attrs: {
      "href": "#"
    },
    on: {
      "click": function click($event) {
        return _vm.showStats('Deployments', _vm.deployStatsColumns, 'deployments');
      }
    }
  }, [_vm._v("Deployments:")]), _c('span', {
    staticClass: "text-dark"
  }, [_vm._v(_vm._s(_vm.deployments))])]), _c('q-item-label', {
    staticClass: "text-secondary",
    staticStyle: {
      "margin-top": "40px",
      "margin-right": "20px"
    }
  }, [_c('a', {
    staticClass: "link-hover",
    attrs: {
      "href": "#"
    },
    on: {
      "click": function click($event) {
        return _vm.showStats('CPUs', _vm.workerStatsColumns, 'workers');
      }
    }
  }, [_vm._v("CPUS:")]), _c('span', {
    staticClass: "text-dark"
  }, [_vm._v(_vm._s(_vm.cpus_running) + "/" + _vm._s(_vm.cpus_total))])]), _c('q-item-label', {
    staticClass: "text-secondary",
    staticStyle: {
      "margin-top": "40px",
      "margin-right": "20px"
    }
  }, [_c('a', {
    staticClass: "link-hover",
    attrs: {
      "href": "#"
    },
    on: {
      "click": function click($event) {
        return _vm.showStats('Tasks', _vm.taskStatsColumns, 'tasks');
      }
    }
  }, [_vm._v("Tasks:")]), _c('span', {
    staticClass: "text-dark"
  }, [_vm._v(_vm._s(_vm.tasks))])])], 1) : _vm._e(), _vm.$auth.isAuthenticated && _vm.hasHosted ? _c('q-item-label', {
    staticClass: "text-secondary",
    staticStyle: {
      "margin-top": "40px",
      "white-space": "nowrap"
    }
  }, [_vm._v("\n      System Usage:\n    ")]) : _vm._e(), _vm.$auth.isAuthenticated && _vm.hasHosted ? _c('apexchart', {
    staticStyle: {
      "margin-right": "280px"
    },
    attrs: {
      "type": "bar",
      "height": "50",
      "width": "100",
      "options": _vm.chartOptions,
      "series": _vm.series
    }
  }) : _vm._e(), _c('q-item-label', {
    staticClass: "text-accent",
    staticStyle: {
      "white-space": "nowrap",
      "margin-top": "40px",
      "margin-right": "-190px"
    }
  }, [_vm._v("\n      " + _vm._s(this.subscriptions[this.$store.state.designer.subscription]) + "\n    ")]), _c('q-item-label', {
    staticClass: "text-dark",
    staticStyle: {
      "white-space": "nowrap"
    }
  }, [!_vm.$auth.loading ? _c('div', [!_vm.$auth.isAuthenticated ? _c('button', {
    on: {
      "click": _vm.login
    }
  }, [_vm._v("\n          Log in\n        ")]) : _vm._e(), _vm.$auth.isAuthenticated ? _c('button', {
    on: {
      "click": _vm.logout
    }
  }, [_vm._v("\n          Log out " + _vm._s(_vm.$auth.user.name) + "\n        ")]) : _vm._e()]) : _vm._e()]), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "aria-label": "Menu",
      "icon": "menu",
      "size": "large"
    }
  }, [_c('q-menu', [_c('q-list', {
    attrs: {
      "dense": ""
    }
  }, [_c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": ""
    },
    on: {
      "click": _vm.newFlow
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fas fa-plus"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n              New Flow\n            ")])], 1), _c('q-separator'), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": "",
      "disabled": ""
    },
    on: {
      "click": _vm.newQueue
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fas fa-sign-in-alt"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n              New Queue\n            ")])], 1), _c('q-separator'), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": "",
      "disabled": ""
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fab fa-docker"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n              Containers\n            ")])], 1), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": "",
      "disabled": !this.$auth.isAuthenticated
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fas fa-cog"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n              Configure\n            ")])], 1), _c('q-separator'), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": "",
      "disabled": ""
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fas fa-users"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n              Manage Groups\n            ")])], 1), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": "",
      "disabled": ""
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fas fa-user"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n              Manage Users\n            ")])], 1), _c('q-separator'), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": "",
      "disabled": ""
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fa fa-area-chart"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n              Server History\n            ")])], 1), _c('q-separator'), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": "",
      "disabled": !this.$auth.isAuthenticated
    },
    on: {
      "click": _vm.showProfile
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fas fa-user"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n              Profile\n            ")])], 1), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": ""
    },
    on: {
      "click": _vm.manage
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "far fa-envelope"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n              Manage Plan\n            ")])], 1), _c('q-separator'), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": ""
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fas fa-question-circle"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n              Help\n            ")])], 1), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": ""
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fas fa-info-circle"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    },
    on: {
      "click": function click($event) {
        _vm.showAboutDialog = true;
      }
    }
  }, [_vm._v("\n              About\n            ")])], 1)], 1)], 1)], 1)], 1), _c('q-dialog', {
    attrs: {
      "persistent": ""
    },
    model: {
      value: _vm.viewStatsDialog,
      callback: function callback($$v) {
        _vm.viewStatsDialog = $$v;
      },
      expression: "viewStatsDialog"
    }
  }, [_c('q-card', {
    staticStyle: {
      "padding": "10px",
      "padding-top": "30px",
      "min-width": "40vw",
      "height": "50%"
    }
  }, [_c('q-card-section', {
    staticClass: "bg-secondary",
    staticStyle: {
      "position": "absolute",
      "left": "0px",
      "top": "0px",
      "width": "100%",
      "height": "40px"
    }
  }, [_c('div', {
    staticStyle: {
      "font-weight": "bold",
      "font-size": "18px",
      "margin-left": "10px",
      "margin-top": "-5px",
      "margin-right": "5px",
      "color": "#fff"
    }
  }, [_c('q-toolbar', [_c('q-item-label', [_vm._v(_vm._s(_vm.statname))]), _c('q-space'), _c('q-icon', {
    staticClass: "text-primary",
    staticStyle: {
      "z-index": "10",
      "cursor": "pointer"
    },
    attrs: {
      "name": "fas fa-close"
    },
    on: {
      "click": function click($event) {
        _vm.viewStatsDialog = false;
      }
    }
  })], 1)], 1)]), _c('q-card-section', {
    staticClass: "row items-center",
    staticStyle: {
      "height": "120px",
      "width": "100%"
    }
  }, [_c('q-table', {
    staticStyle: {
      "width": "100%",
      "margin-top": "20px",
      "border-top-radius": "0px",
      "border-bottom-radius": "0px"
    },
    attrs: {
      "dense": "",
      "columns": _vm.viewStatsColumns,
      "data": _vm.viewStatsData,
      "row-key": "name",
      "flat": ""
    }
  })], 1), _c('q-card-actions', {
    attrs: {
      "align": "right"
    }
  }, [_c('q-btn', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    staticClass: "bg-secondary text-white",
    staticStyle: {
      "position": "absolute",
      "bottom": "0px",
      "right": "0px",
      "width": "100px"
    },
    attrs: {
      "flat": "",
      "label": "Close",
      "color": "primary"
    }
  })], 1), _c('q-inner-loading', {
    staticStyle: {
      "z-index": "9999999"
    },
    attrs: {
      "showing": _vm.viewStatsLoader
    }
  }, [_c('q-spinner-gears', {
    attrs: {
      "size": "50px",
      "color": "primary"
    }
  })], 1)], 1)], 1), _c('q-dialog', {
    attrs: {
      "persistent": ""
    },
    model: {
      value: _vm.showAboutDialog,
      callback: function callback($$v) {
        _vm.showAboutDialog = $$v;
      },
      expression: "showAboutDialog"
    }
  }, [_c('q-card', {
    staticStyle: {
      "width": "800px",
      "height": "500px",
      "padding": "10px",
      "padding-top": "30px"
    }
  }, [_c('q-card-section', {
    staticClass: "bg-secondary",
    staticStyle: {
      "position": "absolute",
      "left": "0px",
      "top": "0px",
      "width": "100%",
      "height": "40px"
    }
  }, [_c('div', {
    staticStyle: {
      "font-weight": "bold",
      "font-size": "18px",
      "margin-left": "10px",
      "margin-top": "-5px",
      "margin-right": "5px",
      "color": "#fff"
    }
  }, [_c('q-toolbar', [_c('q-item-label', [_c('i', {
    staticClass: "fas fa-info",
    staticStyle: {
      "margin-right": "20px"
    }
  }), _vm._v("About ElasticCode\n            ")]), _c('q-space'), _c('q-btn', {
    staticClass: "text-primary",
    staticStyle: {
      "z-index": "10"
    },
    attrs: {
      "flat": "",
      "dense": "",
      "round": "",
      "size": "sm",
      "icon": "fas fa-close"
    },
    on: {
      "click": function click($event) {
        _vm.showAboutDialog = false;
      }
    }
  })], 1)], 1)]), _c('q-card-section', {
    staticClass: "row items-center",
    staticStyle: {
      "margin-top": "30px"
    }
  }, [_c('b', [_vm._v("Build ID")]), _vm._v(": "), _c('a', {
    attrs: {
      "href": _vm.buildUrl,
      "target": "build"
    }
  }, [_vm._v(_vm._s(_vm.commit.substring(0, 7)))])]), _c('q-card-section', {
    staticClass: "row items-center"
  }, [_c('b', [_vm._v("Build Date")]), _vm._v(": " + _vm._s(_vm.buildDate) + "\n      ")]), _c('q-card-actions', {
    attrs: {
      "align": "right"
    }
  }, [_c('q-btn', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    staticClass: "bg-secondary text-white",
    staticStyle: {
      "position": "absolute",
      "bottom": "0px",
      "right": "0px",
      "width": "100px"
    },
    attrs: {
      "flat": "",
      "label": "Ok",
      "color": "primary"
    }
  })], 1)], 1)], 1), _c('q-dialog', {
    attrs: {
      "persistent": ""
    },
    model: {
      value: _vm.showProfileDialog,
      callback: function callback($$v) {
        _vm.showProfileDialog = $$v;
      },
      expression: "showProfileDialog"
    }
  }, [_c('q-card', {
    staticStyle: {
      "width": "800px",
      "height": "500px",
      "padding": "10px",
      "padding-top": "30px"
    }
  }, [_c('q-card-section', {
    staticClass: "bg-secondary",
    staticStyle: {
      "position": "absolute",
      "left": "0px",
      "top": "0px",
      "width": "100%",
      "height": "40px"
    }
  }, [_c('div', {
    staticStyle: {
      "font-weight": "bold",
      "font-size": "18px",
      "margin-left": "10px",
      "margin-top": "-5px",
      "margin-right": "5px",
      "color": "#fff"
    }
  }, [_c('q-toolbar', [_c('q-item-label', [_c('i', {
    staticClass: "fas fa-user",
    staticStyle: {
      "margin-right": "20px"
    }
  }), _vm._v("Your Profile\n            ")]), _c('q-space'), _c('q-btn', {
    staticClass: "text-primary",
    staticStyle: {
      "z-index": "10"
    },
    attrs: {
      "flat": "",
      "dense": "",
      "round": "",
      "size": "sm",
      "icon": "fas fa-close"
    },
    on: {
      "click": function click($event) {
        _vm.showProfileDialog = false;
      }
    }
  })], 1)], 1)]), _c('q-card-section', {
    staticClass: "row items-center",
    staticStyle: {
      "height": "120px",
      "margin-top": "20px"
    }
  }, [_c('q-icon', {
    staticStyle: {
      "font-size": "5em"
    },
    attrs: {
      "name": "fas fa-user",
      "color": "primary"
    }
  })], 1), _c('q-card-section', {
    staticClass: "row items-center"
  }, [_c('span', {
    staticStyle: {
      "font-size": "2em"
    }
  }, [_vm._v(_vm._s(_vm.$auth.user ? _vm.$auth.user.nickname : ''))])]), _c('q-card-section', {
    staticClass: "row items-center"
  }, [_c('span', [_c('b', [_vm._v("Name")]), _vm._v(": " + _vm._s(_vm.$auth.user ? _vm.$auth.user.name : ''))])]), _c('q-card-section', {
    staticClass: "row items-center"
  }, [_c('span', [_c('b', [_vm._v("Email")]), _vm._v(": " + _vm._s(_vm.$auth.user ? _vm.$auth.user.email : ''))])]), _c('q-card-section', {
    staticClass: "row items-center"
  }, [_c('span', [_c('b', [_vm._v("Verified")]), _vm._v(": " + _vm._s(_vm.$auth.user ? _vm.$auth.user.email_verified : ''))])]), _c('q-card-section', {
    staticClass: "row items-center"
  }, [_c('span', [_c('b', [_vm._v("Last Updated")]), _vm._v(": " + _vm._s(_vm.$auth.user ? _vm.$auth.user.updated_at : ''))])]), _c('q-card-actions', {
    attrs: {
      "align": "right"
    }
  }, [_c('q-btn', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    staticClass: "bg-secondary text-white",
    staticStyle: {
      "position": "absolute",
      "bottom": "0px",
      "right": "0px",
      "width": "100px"
    },
    attrs: {
      "flat": "",
      "label": "Ok",
      "color": "primary"
    },
    on: {
      "click": function click($event) {
        _vm.showProfileDialog = false;
      }
    }
  })], 1)], 1)], 1)], 1);
};

var staticRenderFns = [];

// CONCATENATED MODULE: ./src/components/ToolPalette.vue?vue&type=template&id=1993a0da&scoped=true&

// EXTERNAL MODULE: ./node_modules/@mdi/js/mdi.js
var mdi = __webpack_require__("94ed");

// EXTERNAL MODULE: ./src/components/util/DataService.ts
var DataService = __webpack_require__("7c43");

// CONCATENATED MODULE: ./node_modules/@quasar/app/lib/webpack/loader.transform-quasar-imports.js!./node_modules/babel-loader/lib??ref--2-0!./node_modules/@quasar/app/lib/webpack/loader.auto-import-client.js?kebab!./node_modules/vue-loader/lib??vue-loader-options!./src/components/ToolPalette.vue?vue&type=script&lang=js&


/* eslint-disable @typescript-eslint/no-this-alias */





/* harmony default export */ var ToolPalettevue_type_script_lang_js_ = ({
  name: 'ToolPalette',
  props: ['nodes', 'agents', 'queues', 'processors', 'tasks', 'deployments', 'cpus_total', 'cpus_running'],
  created: function created() {
    this.braces = mdi["f" /* mdiCodeBraces */];
    this.border = mdi["d" /* mdiBorderNoneVariant */];
    this.python = mdi["o" /* mdiLanguagePython */];
    this.markdown = mdi["n" /* mdiLanguageMarkdownOutline */];
  },
  mounted: function mounted() {
    var me = this;
    window.$router = this.$router;
    console.log('TOOLPALETTE STORE', this.$store);
    this.$root.$on('show.objects', function (objects) {
      console.log('show.objects ', objects); // eslint-disable-next-line @typescript-eslint/no-unsafe-call

      me.showStats(objects.name, objects.columns, objects.objects);
    });
  },
  computed: {
    hasHosted: function hasHosted() {
      if (this.$auth.isAuthenticated && this.$store.state.designer.subscription) {
        return this.sublevel[this.$store.state.designer.subscription] >= this.HOSTED;
      } else {
        return false;
      }
    },
    hasPro: function hasPro() {
      if (this.$auth.isAuthenticated && this.$store.state.designer.subscription) {
        return this.sublevel[this.$store.state.designer.subscription] >= this.PRO;
      } else {
        return false;
      }
    }
  },
  watch: {
    '$store.state.designer.subscription': function $storeStateDesignerSubscription(sub) {}
  },
  methods: {
    setCommit: function setCommit(commit, buildDate, buildUrl, repoUrl) {
      this.commit = commit;
      this.buildDate = buildDate;
      this.buildUrl = buildUrl;
      this.repoUrl = repoUrl;
    },
    hasEnterprise: function hasEnterprise() {
      if (this.$auth.isAuthenticated && this.$store.state.designer.subscription) {
        return this.sublevel[this.$store.state.designer.subscription] === this.ENTERPRISE;
      } else {
        return false;
      }
    },
    showProfile: function showProfile() {
      console.log(this.$auth.user);
      this.showProfileDialog = this.$auth.isAuthenticated;
    },
    logout: function logout() {
      DataService["a" /* default */].logout(this.$store.state.designer.token).then(this.$auth.logout({
        returnTo: '/logout'
      }));
    },
    login: function login() {
      this.$root.$emit('login');
    },
    showStats: function showStats(name, columns, objects) {
      var me = this;

      if (this.false) {
        return;
      }

      this.statname = name;
      this.viewStatsColumns = columns;
      this.viewStatsLoader = true;
      this.viewStatsDialog = true;
      me.viewStatsData = [];
      DataService["a" /* default */].getObjects(objects, this.$store.state.designer.token).then(function (response) {
        me.viewStatsData = response.data;
        console.log(name + ' STATS:', response.data);
        me.viewStatsLoader = false;
      }).catch(function (error) {
        me.notifyMessage('dark', 'error', 'Something went wrong');
        me.viewStatsLoader = false;
      });
    },
    notifyMessage: function notifyMessage(color, icon, message) {
      this.$q.notify({
        color: color,
        timeout: 2000,
        position: 'top',
        message: message,
        icon: icon
      });
    },
    loadPython: function loadPython() {
      var head = document.getElementById('head');
      var script = document.createElement('script');
      var style = document.createElement('link');
      style.setAttribute('href', 'https://pyscript.net/latest/pyscript.css');
      style.setAttribute('rel', 'stylesheet');
      script.setAttribute('src', 'https://pyscript.net/latest/pyscript.js');
      script.setAttribute('type', 'application/javascript');
      head.appendChild(style);
      head.appendChild(script);
    },
    openBlocks: function openBlocks() {
      this.$root.$emit('open.blocks');
    },
    openChat: function openChat() {
      this.$root.$emit('open.chat');
    },
    openLibrary: function openLibrary() {
      this.$root.$emit('open.library');
    },
    newFlow: function newFlow() {
      this.$root.$emit('new.flow');
    },
    newQueue: function newQueue() {
      this.$root.$emit('new.queue');
    },
    checkout: function checkout() {
      this.$root.$emit('checkout');
    },
    manage: function manage() {
      this.$root.$emit('manage.subscription');
    },
    upgrade: function upgrade() {
      this.$root.$emit('upgrade.subscription');
    }
  },
  data: function data() {
    return {
      GUEST: 0,
      FREE: 1,
      DEVELOPER: 2,
      PRO: 3,
      HOSTED: 4,
      ENTERPRISE: 5,
      subscriptions: {
        'ec_developer-USD-Monthly': 'Developer',
        'ec_hosted-USD-Yearly': 'Hosted'
      },
      buildDate: 'N/A',
      sublevel: {
        guest: 0,
        free: 1,
        'ec_developer-USD-Monthly': 2,
        'ec_pro-USD-Monthly': 3,
        'ec_hosted-USD-Yearly': 4
      },
      showProfileDialog: false,
      showAboutDialog: false,
      viewStatsLoader: false,
      commit: '',
      deployStatsColumns: [{
        name: 'name',
        label: 'Name',
        field: 'name',
        align: 'left'
      }, {
        name: 'owner',
        label: 'Owner',
        field: 'owner',
        align: 'left'
      }, {
        name: 'created',
        label: 'Created On',
        field: 'created',
        align: 'left'
      }, {
        name: 'lastupdated',
        label: 'Last Updated',
        field: 'lastupdated',
        align: 'left'
      }, {
        name: 'hostname',
        label: 'Host',
        field: 'hostname',
        align: 'left'
      }, {
        name: 'cpus',
        label: 'CPUS',
        field: 'cpus',
        align: 'left'
      }, {
        name: 'status',
        label: 'Status',
        field: 'status',
        align: 'left'
      }],
      taskStatsColumns: [{
        name: 'name',
        label: 'Function',
        field: 'name',
        align: 'left'
      }, {
        name: 'owner',
        label: 'Owner',
        field: 'owner',
        align: 'left'
      }, {
        name: 'created',
        label: 'Created On',
        field: 'created',
        align: 'left'
      }, {
        name: 'lastupdated',
        label: 'Last Updated',
        field: 'lastupdated',
        align: 'left'
      }, {
        name: 'module',
        label: 'Module',
        field: 'module',
        align: 'left'
      }, {
        name: 'deployments',
        label: 'Deployments',
        field: 'deployments',
        align: 'left'
      }],
      nodeStatsColumns: [{
        name: 'name',
        label: 'Name',
        field: 'name',
        align: 'left'
      }, {
        name: 'owner',
        label: 'Owner',
        field: 'owner',
        align: 'left'
      }, {
        name: 'created',
        label: 'Created On',
        field: 'created',
        align: 'left'
      }, {
        name: 'lastupdated',
        label: 'Last Updated',
        field: 'lastupdated',
        align: 'left'
      }, {
        name: 'hostname',
        label: 'Host',
        field: 'hostname',
        align: 'left'
      }, {
        name: 'cpus',
        label: 'CPUS',
        field: 'cpus',
        align: 'left'
      }, {
        name: 'status',
        label: 'Status',
        field: 'status',
        align: 'left'
      }],
      agentStatsColumns: [{
        name: 'name',
        label: 'Name',
        field: 'name',
        align: 'left'
      }, {
        name: 'owner',
        label: 'Owner',
        field: 'owner',
        align: 'left'
      }, {
        name: 'created',
        label: 'Created On',
        field: 'created',
        align: 'left'
      }, {
        name: 'lastupdated',
        label: 'Last Updated',
        field: 'lastupdated',
        align: 'left'
      }, {
        name: 'hostname',
        label: 'Host',
        field: 'hostname',
        align: 'left'
      }, {
        name: 'cpus',
        label: 'CPUS',
        field: 'cpus',
        align: 'left'
      }, {
        name: 'status',
        label: 'Status',
        field: 'status',
        align: 'left'
      }],
      queueStatsColumns: [{
        name: 'name',
        label: 'Name',
        field: 'name',
        align: 'left'
      }, {
        name: 'owner',
        label: 'Owner',
        field: 'owner',
        align: 'left'
      }, {
        name: 'id',
        label: 'ID',
        field: 'id',
        align: 'left'
      }, {
        name: 'type',
        label: 'Type',
        field: 'type',
        align: 'left'
      }, {
        name: 'created',
        label: 'Created On',
        field: 'created',
        align: 'left'
      }, {
        name: 'lastupdated',
        label: 'Last Updated',
        field: 'lastupdated',
        align: 'left'
      }, {
        name: 'status',
        label: 'Status',
        field: 'status',
        align: 'left'
      }],
      procStatsColumns: [{
        name: 'name',
        label: 'Name',
        field: 'name',
        align: 'left'
      }, {
        name: 'owner',
        label: 'Owner',
        field: 'owner',
        align: 'left'
      }, {
        name: 'id',
        label: 'ID',
        field: 'id',
        align: 'left'
      }, {
        name: 'concurrency',
        label: 'Concurrency',
        field: 'concurrency',
        align: 'left'
      }, {
        name: 'created',
        label: 'Created On',
        field: 'created',
        align: 'left'
      }, {
        name: 'lastupdated',
        label: 'Last Updated',
        field: 'lastupdated',
        align: 'left'
      }, {
        name: 'status',
        label: 'Status',
        field: 'status',
        align: 'left'
      }],
      workerStatsColumns: [{
        name: 'name',
        label: 'Name',
        field: 'name',
        align: 'left'
      }, {
        name: 'owner',
        label: 'Owner',
        field: 'owner',
        align: 'left'
      }, {
        name: 'id',
        label: 'ID',
        field: 'id',
        align: 'left'
      }, {
        name: 'concurrency',
        label: 'Concurrency',
        field: 'concurrency',
        align: 'left'
      }, {
        name: 'created',
        label: 'Created On',
        field: 'created',
        align: 'left'
      }, {
        name: 'lastupdated',
        label: 'Last Updated',
        field: 'lastupdated',
        align: 'left'
      }, {
        name: 'status',
        label: 'Status',
        field: 'status',
        align: 'left'
      }],
      viewStatsColumns: [],
      viewStatsData: [],
      viewStatsDialog: false,
      statcolumns: [],
      statname: '',
      statdata: [],
      variablecolumns: [{
        name: 'name',
        label: 'Name',
        field: 'name',
        align: 'left'
      }, {
        name: 'value',
        label: 'Value',
        field: 'value',
        align: 'left'
      }, {
        name: 'scope',
        label: 'Scope',
        field: 'scope',
        align: 'left'
      }],
      variabledata: [],
      mode: 'code',
      series: [{
        data: [12, 14, 2, 47, 42, 15, 47, 75, 65, 19, 14]
      }],
      chartOptions: {
        colors: ['#e3e8ec', '#054848'],
        chart: {
          type: 'bar',
          width: 100,
          height: 35,
          sparkline: {
            enabled: true
          }
        },
        plotOptions: {
          bar: {
            columnWidth: '50%'
          }
        },
        labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        xaxis: {
          crosshairs: {
            width: 1
          }
        },
        tooltip: {
          fixed: {
            enabled: false
          },
          x: {
            show: false
          },
          theme: 'dark',
          y: {
            title: {
              formatter: function formatter(seriesName) {
                return 'Tasks';
              }
            }
          },
          marker: {
            show: false
          }
        }
      }
    };
  }
});
// CONCATENATED MODULE: ./src/components/ToolPalette.vue?vue&type=script&lang=js&
 /* harmony default export */ var components_ToolPalettevue_type_script_lang_js_ = (ToolPalettevue_type_script_lang_js_); 
// EXTERNAL MODULE: ./src/components/ToolPalette.vue?vue&type=style&index=0&id=1993a0da&prod&scoped=true&lang=css&
var ToolPalettevue_type_style_index_0_id_1993a0da_prod_scoped_true_lang_css_ = __webpack_require__("2793");

// EXTERNAL MODULE: ./node_modules/vue-loader/lib/runtime/componentNormalizer.js
var componentNormalizer = __webpack_require__("2877");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/toolbar/QToolbar.js
var QToolbar = __webpack_require__("65c6");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/btn/QBtn.js
var QBtn = __webpack_require__("9c40");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/tooltip/QTooltip.js
var QTooltip = __webpack_require__("05c0");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/item/QItemLabel.js
var QItemLabel = __webpack_require__("0170");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/space/QSpace.js
var QSpace = __webpack_require__("2c91");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/menu/QMenu.js + 2 modules
var QMenu = __webpack_require__("4e73");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/item/QList.js
var QList = __webpack_require__("1c1c");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/item/QItem.js
var QItem = __webpack_require__("66e5");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/item/QItemSection.js
var QItemSection = __webpack_require__("4074");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/icon/QIcon.js
var QIcon = __webpack_require__("0016");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/separator/QSeparator.js
var QSeparator = __webpack_require__("eb85");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/dialog/QDialog.js
var QDialog = __webpack_require__("24e8");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/card/QCard.js
var QCard = __webpack_require__("f09f");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/card/QCardSection.js
var QCardSection = __webpack_require__("a370");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/table/QTable.js + 18 modules
var QTable = __webpack_require__("eaac");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/card/QCardActions.js
var QCardActions = __webpack_require__("4b7e");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/inner-loading/QInnerLoading.js
var QInnerLoading = __webpack_require__("74f7");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/spinner/QSpinnerGears.js
var QSpinnerGears = __webpack_require__("cf57");

// EXTERNAL MODULE: ./node_modules/quasar/src/directives/ClosePopup.js
var ClosePopup = __webpack_require__("7f67");

// EXTERNAL MODULE: ./node_modules/@quasar/app/lib/webpack/runtime.auto-import.js
var runtime_auto_import = __webpack_require__("eebe");
var runtime_auto_import_default = /*#__PURE__*/__webpack_require__.n(runtime_auto_import);

// CONCATENATED MODULE: ./src/components/ToolPalette.vue






/* normalize component */

var component = Object(componentNormalizer["a" /* default */])(
  components_ToolPalettevue_type_script_lang_js_,
  render,
  staticRenderFns,
  false,
  null,
  "1993a0da",
  null
  
)

/* harmony default export */ var ToolPalette = __webpack_exports__["a"] = (component.exports);



















runtime_auto_import_default()(component, 'components', {QToolbar: QToolbar["a" /* default */],QBtn: QBtn["a" /* default */],QTooltip: QTooltip["a" /* default */],QItemLabel: QItemLabel["a" /* default */],QSpace: QSpace["a" /* default */],QMenu: QMenu["a" /* default */],QList: QList["a" /* default */],QItem: QItem["a" /* default */],QItemSection: QItemSection["a" /* default */],QIcon: QIcon["a" /* default */],QSeparator: QSeparator["a" /* default */],QDialog: QDialog["a" /* default */],QCard: QCard["a" /* default */],QCardSection: QCardSection["a" /* default */],QTable: QTable["a" /* default */],QCardActions: QCardActions["a" /* default */],QInnerLoading: QInnerLoading["a" /* default */],QSpinnerGears: QSpinnerGears["a" /* default */]});runtime_auto_import_default()(component, 'directives', {ClosePopup: ClosePopup["a" /* default */]});


/***/ }),

/***/ "3723":
/***/ (function(module, exports, __webpack_require__) {

// extracted by mini-css-extract-plugin

/***/ }),

/***/ "3792":
/***/ (function(module, exports, __webpack_require__) {

// extracted by mini-css-extract-plugin

/***/ }),

/***/ "3cff":
/***/ (function(module, exports, __webpack_require__) {

// extracted by mini-css-extract-plugin

/***/ }),

/***/ 4:
/***/ (function(module, exports) {

/* (ignored) */

/***/ }),

/***/ "4676":
/***/ (function(module, exports) {

module.exports = "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjwhLS0gQ3JlYXRlZCB3aXRoIElua3NjYXBlIChodHRwOi8vd3d3Lmlua3NjYXBlLm9yZy8pIC0tPgoKPHN2ZwogICB3aWR0aD0iMjAwIgogICBoZWlnaHQ9IjEwMCIKICAgdmlld0JveD0iMCAwIDUyLjkxNjY2MyAyNi40NTgzMzQiCiAgIHZlcnNpb249IjEuMSIKICAgaWQ9InN2ZzUiCiAgIGlua3NjYXBlOnZlcnNpb249IjEuMi4xICg5YzZkNDFlNDEwLCAyMDIyLTA3LTE0KSIKICAgc29kaXBvZGk6ZG9jbmFtZT0iZWxhc3RpY2NvZGUuc3ZnIgogICB4bWxuczppbmtzY2FwZT0iaHR0cDovL3d3dy5pbmtzY2FwZS5vcmcvbmFtZXNwYWNlcy9pbmtzY2FwZSIKICAgeG1sbnM6c29kaXBvZGk9Imh0dHA6Ly9zb2RpcG9kaS5zb3VyY2Vmb3JnZS5uZXQvRFREL3NvZGlwb2RpLTAuZHRkIgogICB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciCiAgIHhtbG5zOnN2Zz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgogIDxzb2RpcG9kaTpuYW1lZHZpZXcKICAgICBpZD0ibmFtZWR2aWV3NyIKICAgICBwYWdlY29sb3I9IiNmZmZmZmYiCiAgICAgYm9yZGVyY29sb3I9IiM2NjY2NjYiCiAgICAgYm9yZGVyb3BhY2l0eT0iMS4wIgogICAgIGlua3NjYXBlOnBhZ2VzaGFkb3c9IjIiCiAgICAgaW5rc2NhcGU6cGFnZW9wYWNpdHk9IjAuMCIKICAgICBpbmtzY2FwZTpwYWdlY2hlY2tlcmJvYXJkPSIwIgogICAgIGlua3NjYXBlOmRvY3VtZW50LXVuaXRzPSJtbSIKICAgICBzaG93Z3JpZD0iZmFsc2UiCiAgICAgaW5rc2NhcGU6em9vbT0iMi4xMjY2Mzc1IgogICAgIGlua3NjYXBlOmN4PSItNzEuNzA5NDQ3IgogICAgIGlua3NjYXBlOmN5PSI4Mi45OTQ4NjkiCiAgICAgaW5rc2NhcGU6d2luZG93LXdpZHRoPSIxOTYyIgogICAgIGlua3NjYXBlOndpbmRvdy1oZWlnaHQ9IjEwODIiCiAgICAgaW5rc2NhcGU6d2luZG93LXg9IjIyODYiCiAgICAgaW5rc2NhcGU6d2luZG93LXk9IjE1NSIKICAgICBpbmtzY2FwZTp3aW5kb3ctbWF4aW1pemVkPSIwIgogICAgIGlua3NjYXBlOmN1cnJlbnQtbGF5ZXI9ImxheWVyMSIKICAgICB1bml0cz0icHgiCiAgICAgaW5rc2NhcGU6c2hvd3BhZ2VzaGFkb3c9IjIiCiAgICAgaW5rc2NhcGU6ZGVza2NvbG9yPSIjZDFkMWQxIiAvPgogIDxkZWZzCiAgICAgaWQ9ImRlZnMyIiAvPgogIDxnCiAgICAgaW5rc2NhcGU6bGFiZWw9IkxheWVyIDEiCiAgICAgaW5rc2NhcGU6Z3JvdXBtb2RlPSJsYXllciIKICAgICBpZD0ibGF5ZXIxIj4KICAgIDxwYXRoCiAgICAgICBzdHlsZT0iZmlsbDojMDAwMDAwO3N0cm9rZS13aWR0aDowLjE0NDMzOSIKICAgICAgIGlkPSJwYXRoMTI4NyIKICAgICAgIGQ9IiIgLz4KICAgIDxwYXRoCiAgICAgICBzdHlsZT0iZmlsbDojMDAwMDAwO3N0cm9rZS13aWR0aDowLjE0NDMzOSIKICAgICAgIGlkPSJwYXRoMTI2NyIKICAgICAgIGQ9IiIgLz4KICAgIDxwYXRoCiAgICAgICBzdHlsZT0iZmlsbDojMDAwMDAwO3N0cm9rZS13aWR0aDowLjE0NDMzOSIKICAgICAgIGlkPSJwYXRoMTI0NyIKICAgICAgIGQ9IiIgLz4KICAgIDxwYXRoCiAgICAgICBzdHlsZT0iZmlsbDojMDAwMDAwO3N0cm9rZS13aWR0aDowLjE0NDMzOSIKICAgICAgIGlkPSJwYXRoMTIyNyIKICAgICAgIGQ9IiIgLz4KICAgIDxwYXRoCiAgICAgICBzdHlsZT0iZmlsbDojMDAwMDAwO3N0cm9rZS13aWR0aDowLjE0NDMzOSIKICAgICAgIGlkPSJwYXRoMTIwNyIKICAgICAgIGQ9IiIgLz4KICAgIDxwYXRoCiAgICAgICBzdHlsZT0iZmlsbDojMDAwMDAwO3N0cm9rZS13aWR0aDowLjE0NDMzOSIKICAgICAgIGlkPSJwYXRoMTEzMSIKICAgICAgIGQ9IiIgLz4KICAgIDxwYXRoCiAgICAgICBzdHlsZT0iZmlsbDojMDAwMDAwO3N0cm9rZS13aWR0aDowLjI2NDU4MyIKICAgICAgIGlkPSJwYXRoMTA3MSIKICAgICAgIGQ9IiIgLz4KICAgIDxwYXRoCiAgICAgICBzdHlsZT0iZmlsbDojMDAwMDAwO3N0cm9rZS13aWR0aDowLjI2NDU4MyIKICAgICAgIGlkPSJwYXRoMTA1MSIKICAgICAgIGQ9IiIgLz4KICAgIDx0ZXh0CiAgICAgICB4bWw6c3BhY2U9InByZXNlcnZlIgogICAgICAgc3R5bGU9ImZvbnQtc2l6ZTozOC4xNTI2cHg7bGluZS1oZWlnaHQ6MS4yNTtmb250LWZhbWlseTpzYW5zLXNlcmlmO2xldHRlci1zcGFjaW5nOjBweDt3b3JkLXNwYWNpbmc6MHB4O2ZpbGw6I2QwZDlkYztmaWxsLW9wYWNpdHk6MTtzdHJva2Utd2lkdGg6MC4xOTkwMjtzdHJva2UtbWl0ZXJsaW1pdDo0O3N0cm9rZS1kYXNoYXJyYXk6bm9uZSIKICAgICAgIHg9IjE5LjcyNjQ3OSIKICAgICAgIHk9IjIwLjk1MDI1NCIKICAgICAgIGlkPSJ0ZXh0NTM2MyIKICAgICAgIHRyYW5zZm9ybT0ic2NhbGUoMC45NDUwMDcyOCwxLjA1ODE5MjkpIj48dHNwYW4KICAgICAgICAgc29kaXBvZGk6cm9sZT0ibGluZSIKICAgICAgICAgaWQ9InRzcGFuNTM2MSIKICAgICAgICAgc3R5bGU9ImZvbnQtc3R5bGU6bm9ybWFsO2ZvbnQtdmFyaWFudDpub3JtYWw7Zm9udC13ZWlnaHQ6bm9ybWFsO2ZvbnQtc3RyZXRjaDpub3JtYWw7Zm9udC1zaXplOjE2Ljk1NjZweDtmb250LWZhbWlseTpBbnRvbjstaW5rc2NhcGUtZm9udC1zcGVjaWZpY2F0aW9uOidBbnRvbiwgTm9ybWFsJztmb250LXZhcmlhbnQtbGlnYXR1cmVzOm5vcm1hbDtmb250LXZhcmlhbnQtY2Fwczpub3JtYWw7Zm9udC12YXJpYW50LW51bWVyaWM6bm9ybWFsO2ZvbnQtdmFyaWFudC1lYXN0LWFzaWFuOm5vcm1hbDtmaWxsOiNkMGQ5ZGM7ZmlsbC1vcGFjaXR5OjE7c3Ryb2tlLXdpZHRoOjAuMTk5MDI7c3Ryb2tlLW1pdGVybGltaXQ6NDtzdHJva2UtZGFzaGFycmF5Om5vbmUiCiAgICAgICAgIHg9IjE5LjcyNjQ3OSIKICAgICAgICAgeT0iMjAuOTUwMjU0Ij5jb2RlPC90c3Bhbj48L3RleHQ+CiAgICA8dGV4dAogICAgICAgeG1sOnNwYWNlPSJwcmVzZXJ2ZSIKICAgICAgIHN0eWxlPSJmb250LXNpemU6NzguODEwMXB4O2xpbmUtaGVpZ2h0OjEuMjU7Zm9udC1mYW1pbHk6c2Fucy1zZXJpZjtsZXR0ZXItc3BhY2luZzowcHg7d29yZC1zcGFjaW5nOjBweDtmaWxsOiM2Yjg3OTE7ZmlsbC1vcGFjaXR5OjE7c3Ryb2tlLXdpZHRoOjAuNDEwNDY5IgogICAgICAgeD0iMjIuNjYzMzYxIgogICAgICAgeT0iNi4zNzkzNzAyIgogICAgICAgaWQ9InRleHQzNzU2IgogICAgICAgdHJhbnNmb3JtPSJzY2FsZSgwLjg3NjcxNTkzLDEuMTQwNjIwMykiPjx0c3BhbgogICAgICAgICBzb2RpcG9kaTpyb2xlPSJsaW5lIgogICAgICAgICBpZD0idHNwYW4zNzU0IgogICAgICAgICBzdHlsZT0iZm9udC1zdHlsZTpub3JtYWw7Zm9udC12YXJpYW50Om5vcm1hbDtmb250LXdlaWdodDpib2xkO2ZvbnQtc3RyZXRjaDpub3JtYWw7Zm9udC1zaXplOjYuNTY3NXB4O2ZvbnQtZmFtaWx5OidOaW1idXMgU2Fucyc7LWlua3NjYXBlLWZvbnQtc3BlY2lmaWNhdGlvbjonTmltYnVzIFNhbnMsIEJvbGQnO2ZvbnQtdmFyaWFudC1saWdhdHVyZXM6bm9ybWFsO2ZvbnQtdmFyaWFudC1jYXBzOm5vcm1hbDtmb250LXZhcmlhbnQtbnVtZXJpYzpub3JtYWw7Zm9udC12YXJpYW50LWVhc3QtYXNpYW46bm9ybWFsO2ZpbGw6IzZiODc5MTtmaWxsLW9wYWNpdHk6MTtzdHJva2Utd2lkdGg6MC40MTA0NjkiCiAgICAgICAgIHg9IjIyLjY2MzM2MSIKICAgICAgICAgeT0iNi4zNzkzNzAyIj5lbGFzdGljPC90c3Bhbj48L3RleHQ+CiAgICA8cGF0aAogICAgICAgc3R5bGU9ImZpbGw6IzZiODc5MTtmaWxsLW9wYWNpdHk6MTtzdHJva2Utd2lkdGg6MC4yNzc5MjgiCiAgICAgICBkPSJtIDguOTU4MzUxNCwxOS4yNTA2MTYgdiAtMS42Njc1NzMgaCAxLjY2NzU2ODYgMS42Njc1NjggdiAxLjY2NzU3MyAxLjY2NzU2OCBIIDEwLjYyNTkyIDguOTU4MzUxNCBaIG0gNi4zOTIzNDM2LDAuNTcyNjM3IGMgMCwtMS4xMjQ4NzYgMC4wMDM1LC0xLjEyODQ5MSAxLjA3NTAyOSwtMS4xMjg0OTEgMS4wNjI4LDAgMS4wNzQ2NTQsMC4wMTE5IDEuMDQyMjMsMS4wNDIyMjEgLTAuMDMxMzcsMC45OTY4OSAtMC4wNzgxNSwxLjA0NTk5IC0xLjA3NTAyOCwxLjEyODUwMSBsIC0xLjA0MjIzMSwwLjA4NjIzIHogbSAtMi41MDEzNTEsLTUuMDQyMTY3IHYgLTIuNDc4NjY4IGwgMi4yOTI5MDYsLTguM2UtNSAyLjI5MjkwNiwtNy40ZS01IC0wLjAzMTMsMi40MzE5NTEgLTAuMDMxMywyLjQzMTk0NSAtMi4yNjE2MDMsMC4wNDY4NyAtMi4yNjE2MDQsMC4wNDY4OCB6IE0gMy4zOTk3OTI1LDE0LjI0NzkwNyB2IC0xLjk0NTQ4OSBoIDEuOTQ1NDk1MyAxLjk0NTQ5NTMgdiAxLjk0NTQ4OSAxLjk0NTUwNSBIIDUuMzQ1Mjg3OCAzLjM5OTc5MjUgWiBNIDEuMDczNjEzNSwxMS4zOTkxNDkgQyAwLjc1ODA1NDI4LDEwLjIyMTY0OCAwLjg1OTI1NTA3LDEwLjA3ODk5IDIuMDEwMTUyLDEwLjA3ODk5IGMgMS4wODUyNDIyLDAgMS4xMTE3MTA5LDAuMDIzMjggMS4xMTE3MTA5LDAuOTcyNzQ1IDAsMC45MjAwNTEgLTAuMDUwOTQ5LDAuOTcyNzYxIC0wLjk0MDMzMjksMC45NzI3NjEgLTAuNzQwMjE5NSwwIC0wLjk3NTk5NTYsLTAuMTMzMDg2IC0xLjEwNzkxNjUsLTAuNjI1MzQ3IHogTSA3LjU2ODcxMTcsOS42NjIxMDQxIFYgNy4yOTk3MTQ3IEggOS45MzEwOTk1IDEyLjI5MzQ4OCBWIDkuNjYyMTA0MSAxMi4wMjQ0OTYgSCA5LjkzMTA5OTUgNy41Njg3MTE3IFogTSAxNC4yMzg5ODQsOC44MTM3ODk1IFYgNy4yNzA2NzExIGwgMS40NTkxMjMsMC4wODQwMzIgMS40NTkxMjIsMC4wODQwMzIgMC4wODQsMS40NTkxMTc5IDAuMDg0LDEuNDU5MTE3IEggMTUuNzgyMTEzIDE0LjIzODk4NCBaIE0gMy4xMjE4NjI5LDcuODM1MTkwMyBjIDAsLTAuMzg3MTcwMiAwLjE1MDk2NjYsLTAuNTQ2NzQ3NiAwLjQ2MDExNywtMC40ODYzNjcxIDAuNjY5ODYxMywwLjEzMDgxNzQgMC43MzIyNDg1LDEuMDYyNTk0MiAwLjA3MTE0OSwxLjA2MjU5NDIgLTAuMzUyMjQxOSwwIC0wLjUzMTI2NDgsLTAuMTk0MTY0NyAtMC41MzEyNjQ4LC0wLjU3NjIyNzEgeiBNIDQuNTExNTAzNCw1LjYzMjE0NzIgViA0LjI0MjQ5OTMgSCA1LjkwMTE0MzYgNy4yOTA3ODMxIFYgNS42MzIxNDcyIDcuMDIxNzg2OSBIIDUuOTAxMTQzNiA0LjUxMTUwMzQgWiBtIDcuNTA0MDU2NiwwLjAyOTQ0NSBjIDAsLTAuNjgzMzUwMiAwLjEwNDUxOCwtMC43OTgzNDk4IDAuNjk0NjI0LC0wLjc2NDI5NDcgMC41NjI3MTUsMC4wMzI0NzggMC42OTQ2NjIsMC4xODUyMDY0IDAuNjk0ODE5LDAuODA0Mzc0NyAxLjYyZS00LDAuNjMwMDIzOSAtMC4xMjE4NzYsMC43NjQzMDUgLTAuNjk0NjIyLDAuNzY0MzA1IC0wLjU4MTA5NCwwIC0wLjY5NDgyMSwtMC4xMzE2NTk4IC0wLjY5NDgyMSwtMC44MDQzODUgeiIKICAgICAgIGlkPSJwYXRoODM2IiAvPgogIDwvZz4KPC9zdmc+Cg=="

/***/ }),

/***/ "49d7":
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__.p + "fonts/fontawesome-webfont.20fd1704.woff2";

/***/ }),

/***/ "49de":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* WEBPACK VAR INJECTION */(function(process) {/* harmony import */ var _home_darren_PycharmProjects_pyfi_ui_node_modules_babel_runtime_helpers_asyncToGenerator__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__("c973");
/* harmony import */ var _home_darren_PycharmProjects_pyfi_ui_node_modules_babel_runtime_helpers_asyncToGenerator__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_home_darren_PycharmProjects_pyfi_ui_node_modules_babel_runtime_helpers_asyncToGenerator__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var regenerator_runtime_runtime_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__("96cf");
/* harmony import */ var regenerator_runtime_runtime_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(regenerator_runtime_runtime_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var core_js_modules_web_dom_collections_for_each_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__("159b");
/* harmony import */ var core_js_modules_web_dom_collections_for_each_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_web_dom_collections_for_each_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var core_js_modules_es_function_name_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__("b0c0");
/* harmony import */ var core_js_modules_es_function_name_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es_function_name_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var core_js_modules_es_array_slice_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__("fb6a");
/* harmony import */ var core_js_modules_es_array_slice_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es_array_slice_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var core_js_modules_es_number_to_fixed_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__("b680");
/* harmony import */ var core_js_modules_es_number_to_fixed_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es_number_to_fixed_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var core_js_modules_es_symbol_js__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__("a4d3");
/* harmony import */ var core_js_modules_es_symbol_js__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es_symbol_js__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var core_js_modules_es_symbol_description_js__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__("e01a");
/* harmony import */ var core_js_modules_es_symbol_description_js__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es_symbol_description_js__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var core_js_modules_es_regexp_exec_js__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__("ac1f");
/* harmony import */ var core_js_modules_es_regexp_exec_js__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es_regexp_exec_js__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var core_js_modules_es_string_split_js__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__("1276");
/* harmony import */ var core_js_modules_es_string_split_js__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es_string_split_js__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var core_js_modules_es_array_filter_js__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__("4de4");
/* harmony import */ var core_js_modules_es_array_filter_js__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(core_js_modules_es_array_filter_js__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _vue_composition_api__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__("e4fd");
/* harmony import */ var _vue_composition_api__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_vue_composition_api__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var src_pages_Designer_vue__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__("5bda");
/* harmony import */ var src_components_ToolPalette_vue__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__("28e7");
/* harmony import */ var src_components_ModelToolPalette_vue__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__("61d3");
/* harmony import */ var src_components_Console__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__("e013");
/* harmony import */ var _mdi_js__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__("94ed");
/* harmony import */ var src_components_Library_vue__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__("d9c5");
/* harmony import */ var components_Processors_vue__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__("8bbe");
/* harmony import */ var components_util_DataService__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__("7c43");
/* harmony import */ var auth0_lock__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__("65b6");
/* harmony import */ var auth0_lock__WEBPACK_IMPORTED_MODULE_20___default = /*#__PURE__*/__webpack_require__.n(auth0_lock__WEBPACK_IMPORTED_MODULE_20__);
/* harmony import */ var src_store_Store__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__("eaff");
/* harmony import */ var assets_css_font_awesome_min_css__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__("1a0a");
/* harmony import */ var assets_css_font_awesome_min_css__WEBPACK_IMPORTED_MODULE_22___default = /*#__PURE__*/__webpack_require__.n(assets_css_font_awesome_min_css__WEBPACK_IMPORTED_MODULE_22__);
/* harmony import */ var assets_css_flowfont_css__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__("c37e");
/* harmony import */ var assets_css_flowfont_css__WEBPACK_IMPORTED_MODULE_23___default = /*#__PURE__*/__webpack_require__.n(assets_css_flowfont_css__WEBPACK_IMPORTED_MODULE_23__);
/* harmony import */ var assets_fonts_fontawesome_webfont_eot__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__("ecb4");
/* harmony import */ var assets_fonts_fontawesome_webfont_eot__WEBPACK_IMPORTED_MODULE_24___default = /*#__PURE__*/__webpack_require__.n(assets_fonts_fontawesome_webfont_eot__WEBPACK_IMPORTED_MODULE_24__);
/* harmony import */ var assets_fonts_fontawesome_webfont_svg__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__("b213");
/* harmony import */ var assets_fonts_fontawesome_webfont_svg__WEBPACK_IMPORTED_MODULE_25___default = /*#__PURE__*/__webpack_require__.n(assets_fonts_fontawesome_webfont_svg__WEBPACK_IMPORTED_MODULE_25__);
/* harmony import */ var assets_fonts_fontawesome_webfont_woff2__WEBPACK_IMPORTED_MODULE_26__ = __webpack_require__("49d7");
/* harmony import */ var assets_fonts_fontawesome_webfont_woff2__WEBPACK_IMPORTED_MODULE_26___default = /*#__PURE__*/__webpack_require__.n(assets_fonts_fontawesome_webfont_woff2__WEBPACK_IMPORTED_MODULE_26__);
/* harmony import */ var assets_fonts_fontawesome_webfont_woff__WEBPACK_IMPORTED_MODULE_27__ = __webpack_require__("c37a");
/* harmony import */ var assets_fonts_fontawesome_webfont_woff__WEBPACK_IMPORTED_MODULE_27___default = /*#__PURE__*/__webpack_require__.n(assets_fonts_fontawesome_webfont_woff__WEBPACK_IMPORTED_MODULE_27__);
/* harmony import */ var assets_fonts_flowfont2_woff2__WEBPACK_IMPORTED_MODULE_28__ = __webpack_require__("e44f");
/* harmony import */ var assets_fonts_flowfont2_woff2__WEBPACK_IMPORTED_MODULE_28___default = /*#__PURE__*/__webpack_require__.n(assets_fonts_flowfont2_woff2__WEBPACK_IMPORTED_MODULE_28__);
/* harmony import */ var socket_io_client__WEBPACK_IMPORTED_MODULE_29__ = __webpack_require__("daa8");












var _require = __webpack_require__("e144"),
    uuidv4 = _require.v4;

var dd = __webpack_require__("4d3a"); // import { rest, setupWorker } from 'msw'













var chargebee = __webpack_require__("85db");
/*
export const handlers = [

  rest.get('/api1/', (req, res, ctx) => {

    return res(
      ctx.status(200),
      ctx.json({
        username: 'admin'
      })
    )
  })
]
 */


chargebee.configure({
  site: 'elasticcode-test',
  api_key: 'test_cd3cu6vRcuyFScdCW8W8Y3QU1HmrVZ7AaXEm'
});

var filesize = __webpack_require__("4f10");

var size = filesize.partial({
  base: 2,
  standard: 'jedec'
});









/* harmony default export */ __webpack_exports__["a"] = (Object(_vue_composition_api__WEBPACK_IMPORTED_MODULE_11__["defineComponent"])({
  name: 'MainLayout',
  components: {
    editor: __webpack_require__("7c9e"),
    Designer: src_pages_Designer_vue__WEBPACK_IMPORTED_MODULE_12__["default"],
    ToolPalette: src_components_ToolPalette_vue__WEBPACK_IMPORTED_MODULE_13__[/* default */ "a"],
    Console: src_components_Console__WEBPACK_IMPORTED_MODULE_15__[/* default */ "a"],
    ModelToolPalette: src_components_ModelToolPalette_vue__WEBPACK_IMPORTED_MODULE_14__[/* default */ "a"],
    Processors: components_Processors_vue__WEBPACK_IMPORTED_MODULE_18__[/* default */ "a"],
    Library: src_components_Library_vue__WEBPACK_IMPORTED_MODULE_17__[/* default */ "a"]
  },
  created: function created() {
    this.mdiEmailAlert = _mdi_js__WEBPACK_IMPORTED_MODULE_16__[/* mdiEmailAlert */ "h"];
    this.mdiEmailFast = _mdi_js__WEBPACK_IMPORTED_MODULE_16__[/* mdiEmailFast */ "j"];
    this.mdiEmailCheck = _mdi_js__WEBPACK_IMPORTED_MODULE_16__[/* mdiEmailCheck */ "i"];
    this.mdiWavesArrowRight = _mdi_js__WEBPACK_IMPORTED_MODULE_16__[/* mdiWavesArrowRight */ "q"];
    this.mdiFlashOutline = _mdi_js__WEBPACK_IMPORTED_MODULE_16__[/* mdiFlashOutline */ "l"];
    this.mdiFlash = _mdi_js__WEBPACK_IMPORTED_MODULE_16__[/* mdiFlash */ "k"];
    this.borderIcon = _mdi_js__WEBPACK_IMPORTED_MODULE_16__[/* mdiBorderNoneVariant */ "d"];
    this.designers = []; // this.worker = setupWorker(...handlers)
    // Reset connection status to disconnected

    this.$store.commit('designer/setConnected', false);
    this.$store.commit('designer/setStreaming', false);
    var n = this.$q.notify;

    this.$q.notify = function (opts) {
      n(opts);
      opts.message = new Date().toLocaleDateString('en-us', {
        hour: '2-digit',
        minute: '2-digit'
      }) + ' ' + opts.message;
      me.$root.$emit('log.message', opts.message);
    };

    this.schemaIcon = _mdi_js__WEBPACK_IMPORTED_MODULE_16__[/* mdiCodeBraces */ "f"];
    var me = this;
    this.tab = 'flow' + this.flows[0].id;
    window.layout = this;
    this.listenGlobal(); // this.worker.start({ onUnhandledRequest: 'bypass'})
  },
  watch: {
    '$auth.isAuthenticated': function $authIsAuthenticated(val) {
      console.log('$auth.isAuthenticated', val);
      var me = this;

      if (val) {
        this.security.token().then(function (token) {
          console.log('SET TOKEN', token);
          me.$store.commit('designer/setToken', token);
          me.updateSubscription();
        });
      }
    },
    connected: function connected(newv, oldv) {
      console.log('CONNECTED', oldv, newv);

      if (newv) {// This means that changes to the flow are committed back
        // to the database as they happen
      }
    },
    streaming: function streaming(newv, oldv) {
      console.log('STREAMING', oldv, newv);

      if (newv) {
        // This means the flow is receiving streaming messages in real-time
        console.log('Turning on messages'); // TODO: Only enable this if Streaming is on

        var socket = Object(socket_io_client__WEBPACK_IMPORTED_MODULE_29__[/* io */ "a"])(process.env.SOCKETIO);
        window.socket = socket;
        this.listenGlobal();
      } else {
        console.log('Turning off messages');
        window.socket.off('global'); // if (window.socket.connected) {
        //  window.socket.close()
        // }
      }
    },
    viewQueueDialog: function viewQueueDialog(val) {
      var _this = this;

      if (val) {
        this.queueloading = true;
        components_util_DataService__WEBPACK_IMPORTED_MODULE_19__[/* default */ "a"].getMessages(this.queuename, this.$store.state.designer.token).then(function (messages) {
          _this.queueloading = false;
          _this.queuedata = messages.data;

          _this.updateQueuedTasks();
        }).catch(function (err) {
          _this.queueloading = false; // show error message
        });
      }
    },
    text: function text(val) {
      if (this.text.length > 0) {
        this.searchdrawer = true;
      } else {
        this.searchdrawer = false;
      }
    }
  },
  computed: {
    modeModel: {
      get: function get() {
        return this.mode;
      },
      set: function set(val) {
        var me = this;
        this.mode = val;

        if (val === 'disconnected') {
          me.$store.commit('designer/setConnected', false);
          me.$store.commit('designer/setStreaming', false);
        }

        if (val === 'connected') {
          me.$store.commit('designer/setConnected', true);
          me.$store.commit('designer/setStreaming', false);
        }

        if (val === 'streaming') {
          me.$store.commit('designer/setConnected', true);
          me.$store.commit('designer/setStreaming', true);
        }

        console.log('setMode', this.mode);
      }
    },
    connected: function connected() {
      return this.$store.state.designer.connected;
    },
    streaming: function streaming() {
      return this.$store.state.designer.streaming;
    },
    status: function status() {
      return this.$store.state.designer.message;
    },
    getSurfaceId: function getSurfaceId() {
      return window.toolkit.surfaceId;
    },
    hasHosted: function hasHosted() {
      console.log('hasHosted', this.$auth.isAuthenticated, this.$store.state.designer.subscription);

      if (!this.$auth.isAuthenticated) {
        return false;
      }

      if (this.$auth.isAuthenticated && this.$store.state.designer.subscription) {
        return this.sublevel[this.$store.state.designer.subscription] >= this.HOSTED;
      } else {
        return false;
      }
    }
  },
  methods: {
    addNewFlow: function addNewFlow() {
      this.$root.$emit('new.flow');
    },
    updateBlocks: function updateBlocks() {
      var _this2 = this;

      setTimeout(function () {
        _this2.blocks.forEach(function (el) {
          var _el = document.querySelector('#block' + el.data.id);

          console.log('updateBlock: checkPlan ', el.data.enabled);

          if (el.data.enabled && _this2.checkPlan(el.data.enabled)) {
            var data = el.data;
            var draghandle = dd.drag(_el, {
              image: true // default drag image

            });
            draghandle.on('start', function (setData, e) {
              setData('object', JSON.stringify(data));
            });
            _el.disabled = false;
            el.disabled = false;
          } else {
            _el.disabled = true;
            el.disabled = true;
            console.log('updateBlock: disable block ', _el);
          }
        });
      });
    },
    isProPlan: function isProPlan() {
      if (this.$auth.isAuthenticated && this.$store.state.designer.subscription) {
        return this.sublevel[this.$store.state.designer.subscription] >= this.PRO;
      } else {
        return false;
      }
    },
    allPlan: function allPlan() {
      return true;
    },
    hasHostedPlan: function hasHostedPlan() {
      console.log('hasHosted', this.$auth.isAuthenticated, this.$store.state.designer.subscription);

      if (!this.$auth.isAuthenticated) {
        return false;
      }

      if (this.$auth.isAuthenticated && this.$store.state.designer.subscription) {
        return this.sublevel[this.$store.state.designer.subscription] >= this.HOSTED;
      } else {
        return false;
      }
    },
    checkPlan: function checkPlan(plan) {
      if (plan && this[plan]) {
        var cp = this[plan]();
        console.log('CHECKPLAN', plan, cp);
        return cp;
      }
    },
    showBlock: function showBlock(block) {
      this.blockshown = block;
      this.blockdrawer = true;
    },
    checkResolution: function checkResolution() {
      var x = window.screen.width * window.devicePixelRatio;
      var y = window.screen.height * window.devicePixelRatio;

      if (x < 2460 || y < 1440) {// this.resolutiondialog = true
      }
    },
    hasEnterprise: function hasEnterprise() {
      if (this.$store.state.designer.subscription) {
        return this.sublevel[this.$store.state.designer.subscription] === this.ENTERPRISE;
      } else {
        return false;
      }
    },
    updateSubscription: function updateSubscription() {
      var me = this;
      components_util_DataService__WEBPACK_IMPORTED_MODULE_19__[/* default */ "a"].getSubscriptions(this.$auth.user.name, this.$store.state.designer.token).then(function (subscriptions) {
        if (subscriptions.error && subscription.subscription === false) {
          me.$store.commit('designer/setSubscription', 'Registered');
        }

        if (subscriptions.data && subscriptions.data.subscription.status !== 'cancelled') {
          subscriptions.data.subscription.subscription_items.forEach(function (subscription) {
            console.log('SUBSCRIPTION', subscription);
            me.$store.commit('designer/setSubscription', subscription.item_price_id);
          });
        } else {
          me.$store.commit('designer/setSubscription', 'cancelled');
        }

        me.updateBlocks();
      }).catch(function (error) {
        me.notifyMessage('dark', 'error', 'There was an error retrieving your subscription.');
      });
    },
    info: function info(title) {
      this.infotitle = title;
      this.infodialog = true;
    },
    notifyMessage: function notifyMessage(color, icon, message) {
      this.$q.notify({
        color: color,
        timeout: 2000,
        position: 'top',
        message: message,
        icon: icon
      });
    },
    sendChat: function sendChat() {
      var me = this;
      this.loadingchat = true;
      components_util_DataService__WEBPACK_IMPORTED_MODULE_19__[/* default */ "a"].askChat(this.question, this.$store.state.designer.token).then(function (answer) {
        me.answer = answer.data;
        console.log(me.answer);
        me.loadingchat = false;
      }).catch(function (error) {});
    },
    getToken: function getToken() {
      var accessToken = this.security.token();
      accessToken.then(function (result) {
        // here you can use the result of promiseB
        console.log('accessToken: ', result);
      });
    },
    checkout: function checkout() {
      var cbInstance = Chargebee.getInstance();
      var cart = cbInstance.getCart();
      var planPriceId = 'ec_developer-USD-Monthly'; // Plan price point ID is used to identify the product

      var planPriceQuantity = 1;
      var product = cbInstance.initializeProduct(planPriceId, planPriceQuantity);
      cart.replaceProduct(product);
      cart.proceedToCheckout();
    },
    upgrade: function upgrade(plan) {
      this.upgradeDialog = false;
      var me = this;
      var cbInstance = Chargebee.getInstance();
      var cart = cbInstance.getCart();
      cart.setCustomer({
        email: this.$auth.user.name
      });
      cbInstance.setCheckoutCallbacks(function (cart) {
        return {
          loaded: function loaded() {
            console.log('checkout opened');
          },
          close: function close() {
            console.log('checkout closed');
          },
          success: function success(hostedPageId) {
            console.log('CART', JSON.parse(JSON.stringify(cart)));
            me.updateSubscription();
          },
          step: function step(value) {
            // value -> which step in checkout
            console.log(value);
          }
        };
      });
      var product = cbInstance.initializeProduct(plan, 1); // product.addAddon({ id: 'worldmap' })
      // product.addAddon({ id: 'storyboard' })

      cart.replaceProduct(product);
      this.cart = cart;
      this.cart.proceedToCheckout();
    },
    manage: function manage() {
      var cbInstance = Chargebee.getInstance();
      var cbPortal = cbInstance.createChargebeePortal();
      console.log('Subscriptions opened');
      cbInstance.setCheckoutCallbacks(function (cart) {
        return {
          loaded: function loaded() {
            console.log('checkout opened');
          },
          close: function close() {
            console.log('checkout closed');
            window.location.reload();
          },
          success: function success(hostedPageId) {
            console.log('checkout success');
            me.updateSubscription();
          },
          step: function step(value) {
            console.log('checkout step'); // value -> which step in checkout

            console.log(value);
          }
        };
      });
      cbPortal.open({
        subscriptionCancelled: function subscriptionCancelled(data) {
          console.log('subscription cancelled'); // TODO: Show warning dialog about reload

          me.updateSubscription();
        },
        subscriptionReactivated: function subscriptionReactivated(data) {
          console.log('subscription reactivated');
          me.updateSubscription();
        },
        subscriptionChanged: function subscriptionChanged(data) {
          console.log('subscription changed');
          me.updateSubscription();
        },
        close: function close() {
          console.log('Portal closed');
        }
      });
    },
    login: function login() {
      var dualScreenLeft = window.screenLeft !== undefined ? window.screenLeft : window.screenX;
      var dualScreenTop = window.screenTop !== undefined ? window.screenTop : window.screenY;
      var width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width;
      var height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height;
      var systemZoom = width / window.screen.availWidth;
      var left = (width - 500) / 2 / systemZoom + dualScreenLeft;
      var top = (height - 715) / 2 / systemZoom + dualScreenTop;
      var popup = window.open('', 'auth0:authorize:popup', 'left=' + left + ',top=' + top + ',width=500,height=715,scrollbars=no,resizable=no');
      this.$auth.loginWithPopup(this.getToken, {
        popup: popup
      });
    },
    showPurgeConfirm: function showPurgeConfirm(name) {
      this.purgeQueueName = name;
      this.confirmQueuePurge = true;
    },
    showStats: function showStats(name, objects) {
      console.log('showStats', objects);
      this.$root.$emit('show.objects', {
        name: name,
        objects: objects,
        columns: this.objectcolumns[objects]
      });
    },
    purgeQueue: function purgeQueue(name) {
      var _this3 = this;

      components_util_DataService__WEBPACK_IMPORTED_MODULE_19__[/* default */ "a"].purgeQueue(name, this.$store.state.designer.token).then(function (res) {
        _this3.$q.notify({
          color: 'secondary',
          timeout: 2000,
          position: 'top',
          message: 'Purging Queue ' + name + '...',
          icon: 'fas fa-exclamation'
        });
      }).catch(function (res) {
        _this3.$q.notify({
          color: 'secondary',
          timeout: 2000,
          position: 'top',
          message: 'Error Purging Queue ' + name,
          icon: 'fas fa-exclamation'
        });
      });
    },
    queueDetailEditorInit: function queueDetailEditorInit() {
      var me = this;

      __webpack_require__("2099"); // language extension prerequsite...


      __webpack_require__("be9d");

      __webpack_require__("8882"); // language


      __webpack_require__("0329");

      __webpack_require__("95b81");

      __webpack_require__("6a21"); // snippet


      var editor = this.$refs.queueDetailEditor.editor;
      editor.setAutoScrollEditorIntoView(true);
    },
    showQueueDetail: function showQueueDetail(name) {
      var _this4 = this;

      this.queueDetailData = this.queueDetails[name]; // const editor = this.$refs.queueDetailEditor.editor;

      this.detailedqueues.forEach(function (queue) {
        if (queue.name === name) {
          // editor.session.setValue(JSON.stringify(queue, null, "\t"));
          _this4.queueDetailContent = JSON.stringify(queue, null, '\t');
        }
      });
    },
    listenGlobal: function listenGlobal() {
      var _this5 = this;

      var me = this;
      var socket = window.socket;

      if (socket) {
        socket.on('global', function (msg) {
          // console.log('MAINLAYOUT', msg)
          if (msg.type && msg.type === 'DeploymentModel') {
            console.log('DEPLOYMENT WAS UPDATED ', msg);
            window.root.$emit('message.received', msg);
          }

          if (msg.type && msg.type === 'ProcessorModel') {
            // console.log('PROCESSOR WAS UPDATED ', msg)
            window.root.$emit('message.received', msg);
          }

          if (msg.channel === 'task') {
            me.msglogs.unshift(msg);
            me.msglogs = me.msglogs.slice(0, 200);
            window.root.$emit('message.count', 1);
            var bytes = JSON.stringify(msg).length;
            window.root.$emit('message.size', bytes);
          } else if (msg.type && msg.type === 'stats') {
            me.stats = msg;
          } else {
            var qs = [];

            if (msg.type && msg.type === 'queues') {
              var queued_tasks = 0;
              me.detailedqueues = msg.queues;
              msg.queues.forEach(function (queue) {
                if (queue.name.indexOf('celery') === -1) {
                  var ack_rate = 0;
                  var deliver_rate = 0;
                  var properties = [];

                  if ('message_stats' in queue) {
                    ack_rate = queue.message_stats && queue.message_stats.ack_details ? queue.message_stats.ack_details.rate : 0;
                    deliver_rate = queue.message_stats && queue.message_stats.deliver_get_details ? queue.message_stats.deliver_get_details.rate : 0;
                  }

                  qs.push({
                    name: queue.name,
                    messages: queue.messages,
                    ready: queue.messages_ready,
                    acked_rate: ack_rate,
                    deliver_rate: deliver_rate,
                    unacked: queue.messages_unacknowledged,
                    ready_rate: queue.messages_ready_details,
                    unacked_rate: queue.messages_unacknowledged_details,
                    bytes: queue.message_bytes,
                    action: ''
                  });
                  properties.push({
                    name: 'Messages Ready',
                    value: queue.messages_ready
                  });
                  properties.push({
                    name: 'Messages Ackd',
                    value: queue.messages_ready
                  });
                  properties.push({
                    name: 'Avg Ack Ingress Rate',
                    value: parseFloat(queue.backing_queue_status.avg_ack_ingress_rate).toFixed(2)
                  });
                  properties.push({
                    name: 'Avg Ingress Rate',
                    value: parseFloat(queue.backing_queue_status.avg_ingress_rate).toFixed(2)
                  });
                  properties.push({
                    name: 'Avg Engress Rate',
                    value: parseFloat(queue.backing_queue_status.avg_egress_rate).toFixed(2)
                  });
                  properties.push({
                    name: 'Memory',
                    value: queue.memory
                  });
                  properties.push({
                    name: 'Message Bytes',
                    value: queue.message_bytes
                  });
                  properties.push({
                    name: 'Message Bytes Persistent',
                    value: queue.message_bytes_persistent
                  });
                  properties.push({
                    name: 'Message Bytes Ram',
                    value: queue.message_bytes_ram
                  });
                  properties.push({
                    name: 'Message Bytes Ready',
                    value: queue.message_bytes_ready
                  });
                  properties.push({
                    name: 'Message Bytes UnAckd',
                    value: queue.message_bytes_unacknowledged
                  });
                  properties.push({
                    name: 'Messages',
                    value: queue.messages
                  });
                  properties.push({
                    name: 'Messages Persistent',
                    value: queue.messages_persistent
                  });
                  properties.push({
                    name: 'Messages Ram',
                    value: queue.messages_ram
                  });
                  properties.push({
                    name: 'Messages Ready',
                    value: queue.messages_ready
                  });
                  properties.push({
                    name: 'Messages Ready Rate',
                    value: parseFloat(queue.messages_ready_details.rate).toFixed(2)
                  });
                  properties.push({
                    name: 'Messages UnAckd Rate',
                    value: parseFloat(queue.messages_unacknowledged_details.rate).toFixed(2)
                  });
                  properties.push({
                    name: 'Messages Ready Ram',
                    value: queue.messages_ready_ram
                  });
                  properties.push({
                    name: 'Node',
                    value: queue.node
                  });
                  _this5.queueDetails[queue.name] = properties;
                  queued_tasks += parseInt(queue.messages);
                  _this5.queuedTasks = queued_tasks;
                }
              });
              me.queues = qs;
              window.root.$emit('update.queues', qs);
            }
          }
        });
      }
    },
    showMessagePayload: function showMessagePayload(payload) {
      var editor = this.$refs.resultEditor.editor;
      editor.session.setValue(payload);
    },
    resultEditorInit: function resultEditorInit() {
      var me = this;

      __webpack_require__("2099"); // language extension prerequsite...


      __webpack_require__("be9d");

      __webpack_require__("8882"); // language


      __webpack_require__("0329");

      __webpack_require__("95b81");

      __webpack_require__("6a21"); // snippet


      var editor = this.$refs.resultEditor.editor;
      editor.setAutoScrollEditorIntoView(true);
      editor.on('change', function () {});
    },
    centerNode: function centerNode(id) {
      window.toolkit.surface.centerOn(id, {
        doNotAnimate: true,
        onComplete: function onComplete() {
          window.toolkit.surface.pan(0, -200);
        }
      });
    },
    searchString: function searchString() {
      var _this6 = this;

      console.log('Searching for', this.text);
      this.items = [];
      this.graph.nodes.forEach(function (node) {
        console.log('Searching node ', node);

        if (node.name && (node.name.indexOf(_this6.text) > -1 || node.description.indexOf(_this6.text) > -1)) {
          _this6.items.push(node);
        }
      });
    },
    transmitted: function transmitted() {
      var _this7 = this;

      var me = this;
      setTimeout(function () {
        me.transmittedSize = size(_this7.messageSize);
        me.transmitted();
      }, 3000);
    },
    updateStats: function updateStats() {
      console.log('UPDATE STATS');
      var running = 0;
      var stopped = 0;

      if (window.toolkit) {
        var objs = window.toolkit.getGraph().serialize();
        console.log('OBJS', objs);
        objs.nodes.forEach(function (node) {
          console.log('NODE', node);

          if (node.status === 'running') {
            running += 1;
          }

          if (node.status === 'stopped') {
            stopped += 1;
          }
        });
      } // this.stopped = stopped;
      // this.running = running;
      // this.groups = objs['groups'].length;

    },
    getUuid: function getUuid() {
      return 'key_' + uuidv4();
    },
    updateQueuedTasks: function updateQueuedTasks() {
      var queued_tasks = 0;
      this.queuedata.forEach(function (queue) {
        console.log('QUEUE', queue);
        queued_tasks += parseInt(queue.messages);
      });
      console.log('QUEUED TASKS', queued_tasks);
      this.queuedTasks = queued_tasks;
    },
    refreshQueues: function refreshQueues() {
      var _this8 = this;

      this.queueloading = true;
      console.log('QUEUES REFRESHING');
      components_util_DataService__WEBPACK_IMPORTED_MODULE_19__[/* default */ "a"].getMessages(this.queuename, this.$store.state.designer.token).then(function (messages) {
        _this8.queueloading = false;
        _this8.queuedata = messages.data;

        _this8.updateQueuedTasks();
      }).catch(function (err) {
        _this8.queueloading = false; // show error message
      });
    },
    toggleSplitter: function toggleSplitter() {
      this.librarydrawer = false;

      if (this.splitterModel < 100) {
        this.splitterSave = this.splitterModel;
        this.splitterModel = 100;
      } else {
        this.splitterModel = this.splitterSave;
      }
    },
    toggleChat: function toggleChat() {
      this.chatdrawer = !this.chatdrawer;
    },
    updateFlow: function updateFlow(name) {
      this.flow.filename = name;
    },
    tabChanged: function tabChanged(tab) {
      var me = this;
      console.log('REFS:', this.$refs);
      console.log('TAB:', tab, this.$refs[tab]);

      for (var i = 0; i < this.flows.length; i++) {
        var flow = this.flows[i];

        if (tab === 'flow' + flow.id) {
          this.flow = flow;
        }
      }

      console.log('GRAPH', this.graph);

      if (this.$refs[tab + 'designer']) {
        window.toolkit = this.$refs[tab + 'designer'][0].toolkit;
        window.toolkit.$q = this.$q;
        this.graph = window.toolkit.getGraph().serialize();
        window.renderer = window.toolkit.renderer;
        console.log('Refreshing designer');
        setTimeout(function () {
          me.$refs[tab + 'designer'][0].redraw();
        });
      }
    }
  },
  mounted: function mounted() {
    var _this9 = this;

    var me = this;
    this.checkResolution();

    function load() {
      return _load.apply(this, arguments);
    }

    function _load() {
      _load = _home_darren_PycharmProjects_pyfi_ui_node_modules_babel_runtime_helpers_asyncToGenerator__WEBPACK_IMPORTED_MODULE_0___default()( /*#__PURE__*/regeneratorRuntime.mark(function _callee() {
        var micropip;
        return regeneratorRuntime.wrap(function _callee$(_context) {
          while (1) {
            switch (_context.prev = _context.next) {
              case 0:
                _context.next = 2;
                return pyodide.loadPackage('micropip');

              case 2:
                micropip = pyodide.pyimport('micropip');
                _context.next = 5;
                return micropip.install('durable-rules');

              case 5:
              case "end":
                return _context.stop();
            }
          }
        }, _callee);
      }));
      return _load.apply(this, arguments);
    }

    components_util_DataService__WEBPACK_IMPORTED_MODULE_19__[/* default */ "a"].getCommit().then(function (response) {
      console.log('COMMIT', response);
      var hash = response.data.split('|')[0];
      var buildDate = response.data.split('|')[1];
      var buildUrl = response.data.split('|')[2];
      var repoUrl = response.data.split('|')[3];

      _this9.$refs.toolPalette.setCommit(hash, buildDate, buildUrl, repoUrl);
    }); // console.log('MAINLAYOUT MESSAGE', this.$store.state.designer.message);
    // console.log('MAINLAYOUT STORE', this.$store);

    window.designer.$root.$on('toolkit.dirty', function () {
      _this9.updateStats();
    });
    console.log('STATUS: CONNECTED', this.connected);

    if (this.$auth.isAuthenticated) {
      this.security.token().then(function (token) {
        console.log('SET TOKEN', token);
        me.$store.commit('designer/setToken', token);
        components_util_DataService__WEBPACK_IMPORTED_MODULE_19__[/* default */ "a"].getQueues(token).then(function (queues) {
          me.queues = queues.data;
          window.root.$emit('update.queues', queues.data);
        });
        me.updateSubscription();
      });
    }

    this.transmitted();
    window.root.$off('console.message');
    window.root.$on('console.message', function (date, obj, msg) {
      me.consolelog.push({
        name: obj.name,
        date: date,
        msg: msg
      });
    });

    if (me.consolelog.length >= 1000) {
      me.consolelog = [];
    }

    window.root.$on('message.count', function (count) {
      me.messageCount += count;
    });
    window.root.$on('message.size', function (size) {
      me.messageSize += size;
    });
    this.$root.$on('flow.uuid', function (flowid, flowuuid) {
      for (var i = 0; i < me.flows.length; i++) {
        var flow = me.flows[i];

        if (flow.id === flowid) {
          flow._id = flowuuid;
          console.log('Updated flow', flow, ' with uuid', flowuuid);
        }
      }
    });
    window.root.$on('edge.clicked', function (edge) {
      _this9.viewEdgeDialog = true;
    });
    window.root.$on('view.queue', function (queue) {
      _this9.queuename = queue;
      _this9.viewQueueDialog = true;
    });
    this.$root.$on('login', this.login);
    this.$root.$on('manage.subscription', this.manage);
    this.$root.$on('upgrade.subscription', this.upgrade);
    this.$root.$on('checkout', this.checkout);
    this.$root.$on('open.blocks', function () {
      _this9.blocksdrawer = !_this9.blocksdrawer;
    });
    this.$root.$on('open.chat', function () {
      _this9.chatdrawer = !_this9.chatdrawer;
    });
    this.$root.$on('open.library', function () {
      console.log('open.library');
      _this9.librarydrawer = !_this9.librarydrawer;
    });
    this.$root.$on('new.queue', function () {
      console.log('NEW.QUEUE');
      _this9.newQueueDialog = true;
    });
    this.$root.$on('close.flow', function (flowid) {
      console.log('DELETING FLOWID', flowid);
      console.log('BEFORE DELETE', me.flows);
      var index = -1;

      for (var i = 0; i < me.flows.length; i++) {
        var flow = me.flows[i];

        if (flow.id === flowid) {
          index = i;
          break;
        }
      }

      me.flows = me.flows.filter(function (value, index, arr) {
        console.log(value.id, flowid);
        return value.id !== flowid;
      });
      _this9.tab = 'flow' + me.flows[index - 1].id;

      _this9.$refs[_this9.tab + 'designer'][0].refresh();

      console.log('AFTER DELETE', me.flows);
    });
    this.$root.$on('new.flow', function () {
      var id = me.flows.length + 1;
      me.flows.push({
        filename: 'New Flow',
        id: id,
        code: null
      });

      for (var i = 0; i < me.flows.length; i++) {
        var flow = me.flows[i];

        if (flow.id === id) {
          me.flow = flow;
        }
      }

      me.tab = 'flow' + id;
      setTimeout(function () {
        me.tabChanged(me.tab);
      });
    });
    this.$root.$on('loading.flow', function () {
      me.flowloading = true;
    });
    this.$root.$on('load.flow', function (flow) {
      console.log('load.flow', flow);
      me.flowloading = false;
      var id = me.flows.length + 1;
      flow._id = flow._id;
      flow.id = id;
      me.flows.push(flow);
      me.tab = 'flow' + id;
      setTimeout(function () {
        me.tabChanged(me.tab);
      });
    });
    console.log('Mounting....');
    console.log('REFS', this.$refs);
    window.toolkit = this.$refs.flow1designer[0].toolkit;
    window.layout = this;
    window.toolkit.$q = this.$q;
    window.renderer = window.toolkit.renderer;
    window.toolkit.load({
      type: 'json',
      url: '/scratch.json',
      onload: function onload() {
        // called after the data has loaded.
        window.toolkit.surface.setZoom(1.0);
        window.toolkit.surface.zoomToFit({
          fill: 0.75
        });
        window.toolkit.surface.setPan(0, 0, false);
        window.toolkit.surface.setPan(0, 0, false);
        window.toolkit.surface.setPan(0, 0, false);
        me.graph = window.toolkit.getGraph().serialize();
      }
    });
    setTimeout(function () {
      var script = document.querySelector('#script');
      script.data = {
        id: 1,
        enabled: 'allPlan',
        node: {
          icon: 'las la-scroll',
          style: '',
          type: 'script',
          name: 'Script',
          label: 'Script',
          description: 'A script description',
          package: 'my.python.package',
          version: '1.0.0',
          disabled: false,
          columns: [],
          properties: []
        }
      };
      var api = document.querySelector('#api');
      api.data = {
        id: 2,
        enabled: 'allPlan',
        node: {
          icon: 'las la-cloud-upload-alt',
          style: '',
          type: 'api',
          name: 'API',
          label: 'API',
          description: 'A web API',
          package: 'my.python.package',
          version: '1.0.0',
          disabled: false,
          columns: [],
          properties: []
        }
      };
      var border = document.querySelector('#border');
      border.data = {
        id: 3,
        enabled: 'allPlan',
        node: {
          style: '',
          icon: _this9.borderIcon,
          version: '1.0.0',
          type: 'border',
          name: 'Border',
          label: 'Border'
        }
      };
      var processor = document.querySelector('#processor');
      processor.data = {
        id: 4,
        enabled: 'hasHostedPlan',
        node: {
          icon: 'icon-processor',
          style: '',
          type: 'processor',
          name: 'Processor',
          label: 'Script',
          description: 'A script processor description',
          version: '1.0.0',
          package: 'my.python.package',
          disabled: false,
          columns: [],
          properties: []
        }
      };
      var markdown = document.querySelector('#markdown');
      markdown.data = {
        id: 5,
        enabled: 'allPlan',
        node: {
          icon: 'lab la-markdown',
          style: '',
          type: 'markdown',
          name: 'Markdown',
          label: 'Markdown',
          description: 'A markdown block',
          version: '1.0.0',
          disabled: false,
          columns: [],
          properties: []
        }
      };
      var group = document.querySelector('#processorgroup');
      group.data = {
        id: 8,
        enabled: 'allPlan',
        node: {
          icon: 'far fa-object-group',
          style: 'size:50px',
          type: 'group',
          name: 'Group',
          label: 'Group',
          description: 'A processor group description',
          version: '1.0.0',
          package: 'my.python.package',
          disabled: false,
          group: true,
          columns: [],
          properties: []
        }
      };
      /*
      var parallel = document.querySelector('#parallel')
      parallel.data = {
        node: {
          icon: 'fas fa-list',
          style: 'size:50px',
          type: 'parallel',
          name: 'Parallel',
          label: 'Parallel',
          description: 'A parallel tool description',
          package: 'my.python.package',
          disabled: false,
          columns: [],
          properties: []
        }
      }
       var pipeline = document.querySelector('#pipeline')
      pipeline.data = {
        node: {
          icon: 'fas fa-long-arrow-alt-right',
          style: 'size:50px',
          type: 'pipeline',
          name: 'Pipeline',
          label: 'Pipeline',
          description: 'A pipeline tool description',
          package: 'my.python.package',
          disabled: false,
          columns: [],
          properties: []
        }
      }
       var segment = document.querySelector('#segment')
      segment.data = {
        node: {
          icon: 'grid_view',
          style: 'size:50px',
          type: 'segment',
          name: 'Segment',
          label: 'Segment',
          description: 'A segment tool description',
          package: 'my.python.package',
          disabled: false,
          columns: [],
          properties: []
        }
      }
       var chord = document.querySelector('#chord')
      chord.data = {
        node: {
          icon: 'low_priority',
          style: 'size:50px',
          type: 'chord',
          name: 'Chord',
          label: 'Chord',
          description: 'A chord tool description',
          package: 'my.python.package',
          disabled: false,
          columns: [],
          properties: []
        }
      }
      */

      var label = document.querySelector('#label');
      label.data = {
        id: 9,
        enabled: 'allPlan',
        node: {
          icon: 'icon-label',
          style: 'size:50px',
          type: 'note',
          name: 'Label',
          description: 'A description',
          package: 'ec.blocks.general',
          label: 'Label',
          version: '1.0.0',
          disabled: false,
          columns: [],
          properties: []
        }
      };
      var data = document.querySelector('#data');
      data.data = {
        id: 10,
        enabled: 'allPlan',
        node: {
          icon: 'las la-file-alt',
          style: 'size:50px',
          type: 'data',
          name: 'Data',
          description: 'A description',
          package: 'ec.blocks.general',
          version: '1.0.0',
          label: 'Data',
          disabled: false,
          columns: [],
          properties: []
        }
      };
      var lambda = document.querySelector('#lambda');
      lambda.data = {
        id: 19,
        enabled: 'allPlan',
        node: {
          icon: 'las la-code',
          style: 'size:50px',
          type: 'lambda',
          name: 'Lambda',
          description: 'A description',
          package: 'ec.blocks.general',
          version: '1.0.0',
          label: 'Lambda',
          disabled: false,
          columns: [],
          properties: []
        }
      };
      var schema = document.querySelector('#schema');
      schema.data = {
        id: 11,
        enabled: 'hasHostedPlan',
        node: {
          icon: _this9.schemaIcon,
          style: 'size:50px',
          type: 'schema',
          name: 'Schema',
          description: 'A description',
          package: 'ec.blocks.general',
          label: 'Schema',
          version: '1.0.0',
          disabled: false,
          columns: [],
          properties: []
        }
      };
      var chatgpt = document.querySelector('#chatgpt');
      chatgpt.data = {
        id: 13,
        enabled: 'hasHostedPlan',
        node: {
          icon: 'las la-robot',
          style: 'size:50px',
          type: 'chatgpt',
          name: 'ChatGPT',
          description: 'A description',
          package: 'ec.blocks.general',
          label: 'ChatGPT',
          version: '1.0.0',
          disabled: false,
          columns: [],
          properties: []
        }
      };
      var inference = document.querySelector('#inference');
      inference.data = {
        id: 14,
        enabled: 'hasHostedPlan',
        node: {
          icon: 'las la-brain',
          style: 'size:50px',
          type: 'inference',
          description: 'A description',
          package: 'ec.blocks.ai',
          name: 'Inference',
          label: 'Inference',
          version: '1.0.0',
          disabled: false,
          columns: [],
          properties: []
        }
      };
      var queue = document.querySelector('#queue');
      queue.data = {
        id: 15,
        enabled: 'allPlan',
        node: {
          icon: 'input',
          style: 'size:50px',
          type: 'queue',
          name: 'Queue',
          description: 'A description',
          package: 'ec.blocks.general',
          label: 'Queue',
          version: '1.0.0',
          disabled: false,
          columns: [],
          properties: []
        }
      };
      var database = document.querySelector('#database');
      database.data = {
        id: 16,
        enabled: 'hasHostedPlan',
        node: {
          icon: 'fas fa-database',
          style: 'size:50px',
          type: 'database',
          name: 'Database',
          description: 'A description',
          package: 'ec.blocks.data',
          label: 'Database',
          version: '1.0.0',
          disabled: false,
          columns: [],
          properties: []
        }
      };
      var loop = document.querySelector('#loop');
      loop.data = {
        id: 17,
        enabled: 'free',
        node: {
          icon: 'las la-redo-alt',
          style: 'size:50px',
          type: 'loop',
          name: 'Loop',
          description: 'A description',
          package: 'ec.blocks.data',
          label: 'Loop',
          version: '1.0.0',
          disabled: false,
          columns: [],
          properties: []
        }
      };
      var spreadsheet = document.querySelector('#spreadsheet');
      spreadsheet.data = {
        id: 18,
        enabled: 'free',
        node: {
          icon: 'las la-table',
          style: 'size:50px',
          type: 'spreadsheet',
          name: 'Spreadsheet',
          description: 'A description',
          package: 'ec.blocks.data',
          label: 'Spreadsheet',
          version: '1.0.0',
          disabled: false,
          columns: [],
          properties: []
        }
      };
      var els = [script, api, processor, markdown, group, label, data, schema, border, chatgpt, lambda, inference, queue, database, loop, spreadsheet];
      _this9.blocks = els;
      els.forEach(function (el) {
        var data = el.data; // data.id = uuidv4()

        var draghandle = dd.drag(el, {
          image: true // default drag image

        });
        draghandle.on('start', function (setData, e) {
          setData('object', JSON.stringify(data));
        });
      });
    });
    var me = this;
    this.$root.$on('update.tab', function () {
      me.tabChanged(me.tab);
    });
    window.designer.$root.$on('node.added', function (node) {
      me.tabChanged(me.tab);
    });
  },
  data: function data() {
    return {
      blockdrawer: false,
      sublevel: {
        guest: 0,
        free: 1,
        'ec_developer-USD-Monthly': 2,
        'ec_pro-USD-Monthly': 3,
        'ec_hosted-USD-Yearly': 4
      },
      GUEST: 0,
      FREE: 1,
      DEVELOPER: 2,
      PRO: 3,
      HOSTED: 4,
      ENTERPRISE: 5,
      blockshown: {},
      blocks: [],
      blockstabs: 'blocksregistry',
      loadingchat: false,
      answer: '',
      infodialog: false,
      infotitle: '',
      consolelog: [],
      separator: Object(_vue_composition_api__WEBPACK_IMPORTED_MODULE_11__["ref"])('vertical'),
      chooseplan: false,
      flowloading: false,
      purgeQueueName: null,
      confirmQueuePurge: false,
      queueDetailContent: '',
      queueDetailColumns: [{
        name: 'name',
        label: 'Property',
        field: 'name',
        align: 'left'
      }, {
        name: 'value',
        label: 'Value',
        field: 'value',
        align: 'left'
      }],
      queueDetailData: [],
      queuedetailtab: 'stats',
      objectcolumns: {
        runningprocessors: [{
          name: 'name',
          label: 'Name',
          field: 'name',
          align: 'left'
        }, {
          name: 'owner',
          label: 'Owner',
          field: 'owner',
          align: 'left'
        }, {
          name: 'id',
          label: 'ID',
          field: 'id',
          align: 'left'
        }, {
          name: 'concurrency',
          label: 'Concurrency',
          field: 'concurrency',
          align: 'left'
        }, {
          name: 'created',
          label: 'Created On',
          field: 'created',
          align: 'left'
        }, {
          name: 'lastupdated',
          label: 'Last Updated',
          field: 'lastupdated',
          align: 'left'
        }, {
          name: 'status',
          label: 'Status',
          field: 'status',
          align: 'left'
        }]
      },
      queueTableSplitter: 40,
      detailedqueues: [],
      queuedTasks: 0,
      mode: 'disconnected',
      messageContent: '',
      graph: {},
      items: [],
      messageCount: 0,
      messageSize: 0,
      transmittedSize: 0,
      stats: {
        nodes: 0,
        agents: 0,
        queues: 0,
        processors: 0,
        cpus_total: 0,
        deployments: 0,
        cpus_running: 0,
        processors_starting: 0,
        processors_running: 0,
        processors_errored: 0,
        tasks: 0
      },
      running: 0,
      stopped: 0,
      groups: 0,
      librarydrawer: false,
      chatdrawer: false,
      blocksdrawer: false,
      newQueueDialog: false,
      pythontabs: 'pythonconsole',
      messagedrawer: false,
      queueloading: false,
      queueSplitter: 50,
      messageSplitter: 70,
      queuecolumns: [{
        name: 'task',
        label: 'Task',
        field: 'task',
        align: 'left'
      }, {
        name: 'tracking',
        label: 'Tracking',
        field: 'tracking',
        align: 'left'
      }, {
        name: 'id',
        label: 'ID',
        field: 'id',
        align: 'left'
      }, {
        name: 'time',
        label: 'Time',
        field: 'time',
        align: 'left'
      }, {
        name: 'parent',
        label: 'Parent',
        field: 'parent',
        align: 'left'
      }, {
        name: 'routing_key',
        label: 'Routing Key',
        field: 'routing_key',
        align: 'left'
      }],
      queuedata: [],
      queueDetails: {},
      initialPagination: {
        sortBy: 'desc',
        descending: false,
        page: 1,
        rowsPerPage: 50 // rowsNumber: xx if getting data from a server

      },
      queuePagination: {
        sortBy: 'desc',
        descending: false,
        page: 1,
        rowsPerPage: 20 // rowsNumber: xx if getting data from a server

      },
      viewQueueDialog: false,
      viewEdgeDialog: false,
      betanoticedialog: true,
      chatModel: 40,
      splitterModel: 100,
      splitterSave: 73,
      messageColumns: [{
        name: 'date',
        label: 'Date',
        field: 'date',
        align: 'left'
      }, {
        name: 'channel',
        label: 'Channel',
        field: 'channel',
        align: 'left'
      }, {
        name: 'module',
        label: 'Module',
        field: 'module',
        align: 'left'
      }, {
        name: 'task',
        label: 'Task',
        field: 'task',
        align: 'left'
      }, {
        name: 'room',
        label: 'Room',
        field: 'room',
        align: 'left'
      }, {
        name: 'state',
        label: 'State',
        field: 'state',
        align: 'left'
      }, {
        name: 'duration',
        label: 'Duration',
        field: 'duration',
        align: 'left'
      }],
      columns: [{
        name: 'name',
        label: 'Name',
        field: 'name',
        align: 'left'
      }, {
        name: 'messages',
        align: 'center',
        label: 'Messages',
        field: 'messages'
      }, {
        name: 'ready',
        align: 'center',
        label: 'Ready',
        field: 'ready'
      }, {
        name: 'unacked',
        align: 'center',
        label: 'Not Acked',
        field: 'unacked'
      },
      /*        {
      name: "incoming",
      align: "center",
      label: "Incoming/sec",
      field: "incoming",
      },
      {
      name: "delivered",
      align: "center",
      label: "Delivered/sec",
      field: "delivered",
      },
      {
      name: "acked",
      align: "center",
      label: "Acked/sec",
      field: "acked",
      }, */
      {
        name: 'bytes',
        align: 'right',
        classes: 'text-secondary',
        label: 'Bytes',
        field: 'bytes'
      }, {
        name: 'actions',
        align: 'center',
        style: 'min-width:150px',
        classes: 'text-secondary',
        label: 'Actions'
      }],
      queues: [],
      variablecolumns: [{
        name: 'name',
        label: 'Name',
        field: 'name',
        align: 'left'
      }, {
        name: 'value',
        label: 'Value',
        field: 'value',
        align: 'left'
      }, {
        name: 'scope',
        label: 'Scope',
        field: 'scope',
        align: 'left'
      }],
      variabledata: [],
      jsondata: {},
      msglogs: [],
      searchdrawer: false,
      flows: [{
        filename: 'Scratch Flow',
        id: 1
      }],
      drawertab: 'console',
      drawer: true,
      tab: 'flow1',
      tools: 'code',
      question: '',
      text: ''
    };
  }
}));
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__("4362")))

/***/ }),

/***/ "5d52":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _node_modules_mini_css_extract_plugin_dist_loader_js_ref_7_oneOf_2_0_node_modules_css_loader_dist_cjs_js_ref_7_oneOf_2_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_src_index_js_ref_7_oneOf_2_2_node_modules_quasar_app_lib_webpack_loader_auto_import_client_js_kebab_node_modules_vue_loader_lib_index_js_vue_loader_options_Library_vue_vue_type_style_index_0_id_3e6a54f4_prod_lang_css___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__("3cff");
/* harmony import */ var _node_modules_mini_css_extract_plugin_dist_loader_js_ref_7_oneOf_2_0_node_modules_css_loader_dist_cjs_js_ref_7_oneOf_2_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_src_index_js_ref_7_oneOf_2_2_node_modules_quasar_app_lib_webpack_loader_auto_import_client_js_kebab_node_modules_vue_loader_lib_index_js_vue_loader_options_Library_vue_vue_type_style_index_0_id_3e6a54f4_prod_lang_css___WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_mini_css_extract_plugin_dist_loader_js_ref_7_oneOf_2_0_node_modules_css_loader_dist_cjs_js_ref_7_oneOf_2_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_src_index_js_ref_7_oneOf_2_2_node_modules_quasar_app_lib_webpack_loader_auto_import_client_js_kebab_node_modules_vue_loader_lib_index_js_vue_loader_options_Library_vue_vue_type_style_index_0_id_3e6a54f4_prod_lang_css___WEBPACK_IMPORTED_MODULE_0__);
/* unused harmony reexport * */


/***/ }),

/***/ "61d3":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";

// CONCATENATED MODULE: ./node_modules/@quasar/app/lib/webpack/loader.transform-quasar-imports.js!./node_modules/babel-loader/lib??ref--2-0!./node_modules/vue-loader/lib/loaders/templateLoader.js??ref--7!./node_modules/@quasar/app/lib/webpack/loader.auto-import-client.js?kebab!./node_modules/vue-loader/lib??vue-loader-options!./src/components/ModelToolPalette.vue?vue&type=template&id=9e3a0e0a&scoped=true&
var render = function render() {
  var _vm = this,
      _c = _vm._self._c;

  return _c('q-toolbar', {
    staticClass: "sidebar node-palette"
  }, [_c('img', {
    staticStyle: {
      "padding-left": "15px",
      "height": "55px",
      "padding-right": "10px"
    },
    attrs: {
      "src": __webpack_require__("4676")
    }
  }), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "align": "left",
      "icon": "format_list_bulleted",
      "aria-label": "Processor",
      "size": "large",
      "id": "class"
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n      Class\n    ")])], 1), _c('q-space'), _c('q-item-label', {
    staticClass: "text-secondary",
    staticStyle: {
      "margin-top": "40px",
      "margin-right": "20px"
    }
  }, [_vm._v("\n    Active Hosts:\n    "), _c('span', {
    staticClass: "text-dark"
  }, [_vm._v("17")])]), _c('q-item-label', {
    staticClass: "text-secondary",
    staticStyle: {
      "margin-top": "40px",
      "margin-right": "20px"
    }
  }, [_vm._v("\n    Active Queues:\n    "), _c('span', {
    staticClass: "text-dark"
  }, [_vm._v("20")])]), _c('q-item-label', {
    staticClass: "text-secondary",
    staticStyle: {
      "margin-top": "40px",
      "margin-right": "20px"
    }
  }, [_vm._v("\n    Active Processors:\n    "), _c('span', {
    staticClass: "text-dark"
  }, [_vm._v("125")])]), _c('q-item-label', {
    staticClass: "text-secondary",
    staticStyle: {
      "margin-top": "40px"
    }
  }, [_vm._v("\n    System Usage:\n  ")]), _c('apexchart', {
    staticStyle: {
      "margin-right": "200px"
    },
    attrs: {
      "type": "bar",
      "height": "50",
      "width": "100",
      "options": _vm.chartOptions,
      "series": _vm.series
    }
  }), _c('q-item-label', {
    staticClass: "text-dark"
  }, [_c('a', {
    attrs: {
      "href": "#"
    },
    on: {
      "click": _vm.login
    }
  }, [_vm._v("Login")])]), _c('q-btn', {
    staticClass: "text-dark text-bold",
    staticStyle: {
      "min-height": "56px",
      "cursor": "grabbing"
    },
    attrs: {
      "flat": "",
      "aria-label": "Menu",
      "icon": "menu",
      "size": "large"
    }
  }, [_c('q-menu', [_c('q-list', {
    attrs: {
      "dense": ""
    }
  }, [_c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": ""
    },
    on: {
      "click": _vm.newFlow
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fas fa-plus"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n            New Flow\n          ")])], 1), _c('q-separator'), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": ""
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fas fa-table"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n            Summary\n          ")])], 1), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": ""
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fas fa-calculator"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n            Counters\n          ")])], 1), _c('q-separator'), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": ""
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "far fa-sticky-note"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n            Bulletin Board\n          ")])], 1), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": ""
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fas fa-database"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n            Data Provenance\n          ")])], 1), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": ""
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fas fa-wrench"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n            Controller Settings\n          ")])], 1), _c('q-separator'), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": ""
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fas fa-list-alt"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n            Parameter Contexts\n          ")])], 1), _c('q-separator'), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": ""
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fa fa-history"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n            Flow Configuration History\n          ")])], 1), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": ""
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fa fa-area-chart"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n            Node Status History\n          ")])], 1), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": ""
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fas fa-project-diagram"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n            Templates\n          ")])], 1), _c('q-separator'), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": ""
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fas fa-user"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n            Profile\n          ")])], 1), _c('q-separator'), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": ""
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fas fa-question-circle"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n            Help\n          ")])], 1), _c('q-item', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    attrs: {
      "clickable": ""
    }
  }, [_c('q-item-section', {
    attrs: {
      "side": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "fas fa-info-circle"
    }
  })], 1), _c('q-item-section', {
    staticClass: "text-blue-grey-8",
    attrs: {
      "side": ""
    }
  }, [_vm._v("\n            About\n          ")])], 1)], 1)], 1)], 1)], 1);
};

var staticRenderFns = [];

// CONCATENATED MODULE: ./src/components/ModelToolPalette.vue?vue&type=template&id=9e3a0e0a&scoped=true&

// CONCATENATED MODULE: ./node_modules/@quasar/app/lib/webpack/loader.transform-quasar-imports.js!./node_modules/babel-loader/lib??ref--2-0!./node_modules/@quasar/app/lib/webpack/loader.auto-import-client.js?kebab!./node_modules/vue-loader/lib??vue-loader-options!./src/components/ModelToolPalette.vue?vue&type=script&lang=js&
/* harmony default export */ var ModelToolPalettevue_type_script_lang_js_ = ({
  name: 'ModelToolPalette',
  created: function created() {},
  mounted: function mounted() {
    console.log('TOOLPALETTE STORE', this.$store);
  },
  methods: {
    logout: function logout() {
      this.$auth0.logout({
        returnTo: window.location.origin
      });
    },
    login: function login() {
      this.$auth0.loginWithRedirect();
    },
    newFlow: function newFlow() {
      this.$root.$emit('new.flow');
    }
  },
  data: function data() {
    return {
      mode: 'code',
      series: [{
        data: [12, 14, 2, 47, 42, 15, 47, 75, 65, 19, 14]
      }],
      chartOptions: {
        colors: ['#e3e8ec', '#054848'],
        chart: {
          type: 'bar',
          width: 100,
          height: 35,
          sparkline: {
            enabled: true
          }
        },
        plotOptions: {
          bar: {
            columnWidth: '50%'
          }
        },
        labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        xaxis: {
          crosshairs: {
            width: 1
          }
        },
        tooltip: {
          fixed: {
            enabled: false
          },
          x: {
            show: false
          },
          y: {
            title: {
              formatter: function formatter(seriesName) {
                return 'Value';
              }
            }
          },
          marker: {
            show: false
          }
        }
      }
    };
  }
});
// CONCATENATED MODULE: ./src/components/ModelToolPalette.vue?vue&type=script&lang=js&
 /* harmony default export */ var components_ModelToolPalettevue_type_script_lang_js_ = (ModelToolPalettevue_type_script_lang_js_); 
// EXTERNAL MODULE: ./src/components/ModelToolPalette.vue?vue&type=style&index=0&id=9e3a0e0a&prod&scoped=true&lang=css&
var ModelToolPalettevue_type_style_index_0_id_9e3a0e0a_prod_scoped_true_lang_css_ = __webpack_require__("ce28");

// EXTERNAL MODULE: ./node_modules/vue-loader/lib/runtime/componentNormalizer.js
var componentNormalizer = __webpack_require__("2877");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/toolbar/QToolbar.js
var QToolbar = __webpack_require__("65c6");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/btn/QBtn.js
var QBtn = __webpack_require__("9c40");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/tooltip/QTooltip.js
var QTooltip = __webpack_require__("05c0");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/space/QSpace.js
var QSpace = __webpack_require__("2c91");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/item/QItemLabel.js
var QItemLabel = __webpack_require__("0170");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/menu/QMenu.js + 2 modules
var QMenu = __webpack_require__("4e73");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/item/QList.js
var QList = __webpack_require__("1c1c");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/item/QItem.js
var QItem = __webpack_require__("66e5");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/item/QItemSection.js
var QItemSection = __webpack_require__("4074");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/icon/QIcon.js
var QIcon = __webpack_require__("0016");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/separator/QSeparator.js
var QSeparator = __webpack_require__("eb85");

// EXTERNAL MODULE: ./node_modules/quasar/src/directives/ClosePopup.js
var ClosePopup = __webpack_require__("7f67");

// EXTERNAL MODULE: ./node_modules/@quasar/app/lib/webpack/runtime.auto-import.js
var runtime_auto_import = __webpack_require__("eebe");
var runtime_auto_import_default = /*#__PURE__*/__webpack_require__.n(runtime_auto_import);

// CONCATENATED MODULE: ./src/components/ModelToolPalette.vue






/* normalize component */

var component = Object(componentNormalizer["a" /* default */])(
  components_ModelToolPalettevue_type_script_lang_js_,
  render,
  staticRenderFns,
  false,
  null,
  "9e3a0e0a",
  null
  
)

/* harmony default export */ var ModelToolPalette = __webpack_exports__["a"] = (component.exports);












runtime_auto_import_default()(component, 'components', {QToolbar: QToolbar["a" /* default */],QBtn: QBtn["a" /* default */],QTooltip: QTooltip["a" /* default */],QSpace: QSpace["a" /* default */],QItemLabel: QItemLabel["a" /* default */],QMenu: QMenu["a" /* default */],QList: QList["a" /* default */],QItem: QItem["a" /* default */],QItemSection: QItemSection["a" /* default */],QIcon: QIcon["a" /* default */],QSeparator: QSeparator["a" /* default */]});runtime_auto_import_default()(component, 'directives', {ClosePopup: ClosePopup["a" /* default */]});


/***/ }),

/***/ "68b1":
/***/ (function(module, exports) {

module.exports = "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiIHN0YW5kYWxvbmU9Im5vIj8+CjwhLS0gQ3JlYXRlZCB3aXRoIElua3NjYXBlIChodHRwOi8vd3d3Lmlua3NjYXBlLm9yZy8pIC0tPgoKPHN2ZwogICB3aWR0aD0iNDVtbSIKICAgaGVpZ2h0PSI0NW1tIgogICB2aWV3Qm94PSIwIDAgNDUgNDUiCiAgIHZlcnNpb249IjEuMSIKICAgaWQ9InN2ZzUiCiAgIHhtbDpzcGFjZT0icHJlc2VydmUiCiAgIGlua3NjYXBlOnZlcnNpb249IjEuMi4xICg5YzZkNDFlNDEwLCAyMDIyLTA3LTE0KSIKICAgc29kaXBvZGk6ZG9jbmFtZT0icHl0aG9uLnN2ZyIKICAgeG1sbnM6aW5rc2NhcGU9Imh0dHA6Ly93d3cuaW5rc2NhcGUub3JnL25hbWVzcGFjZXMvaW5rc2NhcGUiCiAgIHhtbG5zOnNvZGlwb2RpPSJodHRwOi8vc29kaXBvZGkuc291cmNlZm9yZ2UubmV0L0RURC9zb2RpcG9kaS0wLmR0ZCIKICAgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIgogICB4bWxuczpzdmc9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48c29kaXBvZGk6bmFtZWR2aWV3CiAgICAgaWQ9Im5hbWVkdmlldzciCiAgICAgcGFnZWNvbG9yPSIjZmZmZmZmIgogICAgIGJvcmRlcmNvbG9yPSIjMDAwMDAwIgogICAgIGJvcmRlcm9wYWNpdHk9IjAuMjUiCiAgICAgaW5rc2NhcGU6c2hvd3BhZ2VzaGFkb3c9IjIiCiAgICAgaW5rc2NhcGU6cGFnZW9wYWNpdHk9IjAuMCIKICAgICBpbmtzY2FwZTpwYWdlY2hlY2tlcmJvYXJkPSIwIgogICAgIGlua3NjYXBlOmRlc2tjb2xvcj0iI2QxZDFkMSIKICAgICBpbmtzY2FwZTpkb2N1bWVudC11bml0cz0ibW0iCiAgICAgc2hvd2dyaWQ9ImZhbHNlIgogICAgIGlua3NjYXBlOnpvb209IjAuODkyNjM0NjgiCiAgICAgaW5rc2NhcGU6Y3g9IjM1NC4wMDgyIgogICAgIGlua3NjYXBlOmN5PSIyOTIuMzkyODUiCiAgICAgaW5rc2NhcGU6d2luZG93LXdpZHRoPSIyNTYwIgogICAgIGlua3NjYXBlOndpbmRvdy1oZWlnaHQ9IjEyODUiCiAgICAgaW5rc2NhcGU6d2luZG93LXg9IjE5MjAiCiAgICAgaW5rc2NhcGU6d2luZG93LXk9IjMyIgogICAgIGlua3NjYXBlOndpbmRvdy1tYXhpbWl6ZWQ9IjEiCiAgICAgaW5rc2NhcGU6Y3VycmVudC1sYXllcj0ibGF5ZXIxIiAvPjxkZWZzCiAgICAgaWQ9ImRlZnMyIiAvPjxnCiAgICAgaW5rc2NhcGU6bGFiZWw9IkxheWVyIDEiCiAgICAgaW5rc2NhcGU6Z3JvdXBtb2RlPSJsYXllciIKICAgICBpZD0ibGF5ZXIxIj48cGF0aAogICAgICAgc3R5bGU9ImZpbGw6IzA1NDg0ODtzdHJva2Utd2lkdGg6MC4wODMyNTg4O2ZpbGwtb3BhY2l0eToxIgogICAgICAgZD0ibSAxOS40NTEwNjYsNDMuOTAzNjY3IGMgLTEuODU3NDI0LC0wLjQwOTU4OCAtMy4yNzUyMjcsLTEuNTUyODU2IC00LjA1MzAwOCwtMy4yNjgyMTMgLTAuNDc0NjYzLC0xLjA0Njg1MSAtMC40ODE1ODMsLTEuMTQ4MjE1IC0wLjQ4MzE2MSwtNy4wNzgyMSBsIC0wLjAwMTUsLTUuNDMyNjQ2IEggMTAuNzA1MzEgYyAtNC43NDkwODc1LDAgLTUuMDAyNzAxNCwtMC4wMjQwNSAtNi4xNTc2NTQxLC0wLjU4MzM1NyBDIDMuMTM3ODQyNSwyNi44NTg0NTggMi4xMjk1MzM0LDI1LjcwMTMyMSAxLjYwOTg5MTMsMjQuMTY5Nzk0IEwgMS4zODM4OTQ5LDIzLjUwMzcyMiBWIDIwLjU0ODAzIDE3LjU5MjMzNSBsIDAuMjI1OTk2NCwtMC42NjYwNzMgYyAwLjUxOTY0MjEsLTEuNTMxNTI3IDEuNTI3OTUxMiwtMi42ODg2NjQgMi45Mzc4MTYyLC0zLjM3MTQ0MyAxLjE1NDk1MjcsLTAuNTU5MzMgMS40MDg1NjY1LC0wLjU4MzM1NyA2LjE1NzY1NDUsLTAuNTgzMzU3IGggNC4yMDgwOSBsIDAuMDAxNSwtMy4yNjc5MTU3IGMgMC4wMDE2LC0zLjY5NzU3NjEgMC4wMzM3NiwtMy45ODIwODQyIDAuNTc0NTA0LC01LjA4ODkyNTggMC43MTY3ODYsLTEuNDY3MTc1MiAxLjkxNTE2NCwtMi40ODY1NTQ4IDMuNTAzNzM4LC0yLjk4MDQwMzUgMC42MDMxNiwtMC4xODc1MDgyIDAuNzIyMzM1LC0wLjE5NDEyMjggMy40OTY4OCwtMC4xOTQxMjI4IDIuNTUzMjQ0LDAgMi45Mjc5NDYsMC4wMTcwMjQgMy4zNzE5ODcsMC4xNTMyNjc4IDEuNTI1NzExLDAuNDY4MTAxOSAyLjg3ODc4NywxLjU3NTQ1MzMgMy41MjcyOTUsMi44ODY3MTcxIDAuNjUzNDI2LDEuMzIxMjA3OCAwLjYyMjkwOCwxLjAwMDY2MjUgMC42NTU4NjIsNi44ODg2NDc5IGwgMC4wMjk0OSw1LjI2NjEyOSBoIDQuMTAyMDA2IGMgMi41ODU2NCwwIDQuMjg0NjI0LDAuMDMzMzQgNC41OTYwMzEsMC4wOTAyIDEuNzIyMTAxLDAuMzE0NDI1IDMuMjE2NjAzLDEuNDQ3NTAyIDMuOTk5MTYsMy4wMzIwMDggMC41NzIzOTksMS4xNTg5ODMgMC42MTMyOTksMS40NzgyNDIgMC42MTMyOTksNC43ODczOTQgMCwzLjIwOTMwMiAtMC4wNDY0NCwzLjYxNjg1NiAtMC41MjYyMDUsNC42MTg0ODUgLTAuNjA2MzE1LDEuMjY1ODE0IC0xLjQzNjI5MiwyLjEwNTMyMyAtMi42NzYzNzUsMi43MDcxMDMgLTEuMTQ5MjEsMC41NTc2ODUgLTEuNDIwOTQ2LDAuNTg0MDE0IC02LjAyNzAwNywwLjU4NDAxNCBoIC00LjA3NzQ0MiBsIC0wLjAzMzIzLDMuNDM0NDMzIGMgLTAuMDM3MDIsMy44MjU5MzcgLTAuMDMzNjQsMy43OTkzNzIgLTAuNjM5NjA4LDUuMDI0NzM2IC0wLjc2NjM0MywxLjU0OTY3MSAtMi4zODcwMDMsMi43NDkzNzQgLTQuMDg2NTc4LDMuMDI1MTE1IC0wLjc5NDA5LDAuMTI4ODM3IC01LjI0NTQwOCwwLjEwMjUyMSAtNS44Njc2MjQsLTAuMDM0NjggeiBtIDUuOTQyODIzLC0yLjY4NzE5NSBjIDAuOTA2NzA0LC0wLjM2MjEwMiAxLjQ1Njg0NiwtMC44OTUxNTkgMS44MTAwMDQsLTEuNzUzODAxIDAuMTkyMzAxLC0wLjQ2NzU0MSAwLjE5NDQ3NiwtMC41MDg5NTkgMC4xOTY0MzEsLTMuNzQwNjkxIGwgMC4wMDE5LC0zLjI2NzkxNyAtMi4xNDM5MTgsLTEuNjdlLTQgYyAtMS44NzY1NzYsLTguMmUtNSAtMi4xNzk1MTgsLTAuMDE4MjggLTIuNDI5NDA2LC0wLjE0NTcwMyAtMC40MjkyOTgsLTAuMjE4OTAzIC0wLjYxNDgyNywtMC41MjczMTEgLTAuNjUwMzcyLC0xLjA4MTExOSAtMC4wMzQ3MywtMC41NDA5MTkgMC4xMjg2NzUsLTAuODk3NDIyIDAuNTMyNjY0LC0xLjE2MjIxOCAwLjIxNTU0MywtMC4xNDEyNzkgMC42ODgyNDUsLTAuMTUyNzA4IDcuOTM0MzkyLC0wLjE5MTg1NyBsIDcuNzA1MiwtMC4wNDE2MyAwLjQ3ODQ2MiwtMC4xOTMyMTMgYyAwLjU4Nzc0NSwtMC4yMzczNDEgMS4zMzY0NDQsLTAuOTA0Mjg5IDEuNjAwODM4LC0xLjQyNjA0NCAwLjEwNzQ3OCwtMC4yMTIxMSAwLjIzNjI0MywtMC42MDY0NjMgMC4yODYxMzIsLTAuODc2MzM5IDAuMTE4ODAyLC0wLjY0MjYyOSAwLjExODgwMiwtNC45NDAwNzQgMCwtNS41ODI3MDQgLTAuMTg2MTUxLC0xLjAwNjk0MyAtMC43OTI0NjgsLTEuNzg2MzI5IC0xLjc0MDk5LC0yLjIzNzkwNiBsIC0wLjU0MTE4NCwtMC4yNTc2NDggLTQuMTc5MTQxLC0wLjAyNTA4IC00LjE3OTE0MiwtMC4wMjUwNSAtMC4wMjU0MywxLjc4ODQ1OSBjIC0wLjAyNzkxLDEuOTYxODk2IC0wLjAzNzQyLDIuMDAwMzg3IC0wLjU5ODY0NCwyLjQxOTQ3MiAtMC4yMjYzOTIsMC4xNjkwNTggLTAuMzE4ODYyLDAuMTcyMDA0IC02LjA5NjA2MSwwLjE5NDEyMyBsIC01Ljg2NjE4MSwwLjAyMjQ3IDAuMDIzMzEsNy42Nzg5OTkgMC4wMjMyOSw3LjY3ODk5NSAwLjE5MzIxLDAuNDc4NDYgYyAwLjM4MzA2MywwLjk0ODYwNSAxLjM3NDE2NywxLjc0MzUzOSAyLjM2NDgzNywxLjg5Njc2MyAwLjI0MTYwMiwwLjAzNzM3IDEuNDMyMTM5LDAuMDU5NDQgMi42NDU2NDEsMC4wNDkwNiAyLjAzNzE0OCwtMC4wMTc0NCAyLjI0MDY5OSwtMC4wMzI2IDIuNjU0MDksLTAuMTk3Njk4IHogbSAtMC45NjI2NjUsLTQuNDM4ODM3IGMgLTAuNTY3ODA1LC0wLjE2OTgzMiAtMS4wMjIwMywtMC45MTc2NzUgLTAuODkyMTQsLTEuNDY4ODMyIDAuMTM0MzczLC0wLjU3MDE3OSAwLjU2OTM2LC0wLjk4NjQwNiAxLjA3NDA0LC0xLjAyNzcxIDAuNTc4NzA1LC0wLjA0NzM2IDAuNzI3ODIsMC4wMDI4IDEuMDkzMzIzLDAuMzY4Mzc3IDAuMzY1NSwwLjM2NTUwMyAwLjQxNTc0MywwLjUxNDYxNyAwLjM2ODM3NiwxLjA5MzMyMyAtMC4wNTk5OSwwLjczMzA2OCAtMC44OTQ5NDYsMS4yNTg3NjkgLTEuNjQzNTk5LDEuMDM0ODQyIHogbSAtOS41MTY0MDIsLTEzLjAwMzMyIGMgMC4wMDEzLC0xLjY3NzI2OCAwLjAxMTAyLC0xLjc4NjExOSAwLjE4NzMzMiwtMi4wOTM2MjMgMC4zODE5NDgsLTAuNjY2MjE5IDAuMDQwMjksLTAuNjMzMTA4IDYuNTMzMTYzLC0wLjYzMzEwOCBIIDI3LjQwMjMgTCAyNy40MDA0LDEzLjc0MTYwNiAyNy4zOTg1LDYuNDM1NjMwOCAyNy4yMDQwNDcsNS45NjI4NTI5IEMgMjYuODUwNzUxLDUuMTAzODQzNSAyNi4yOTk3MDksNC41NzAxMDI3IDI1LjM5NDA1OCw0LjIwOTY3MTggMjQuOTg5NjQ1LDQuMDQ4NzI1OCAyNC43NDg5ODcsNC4wMjgyMjc0IDIyLjkwNjQ4NSwzLjk5NzgwNDIgYyAtMi4zMjU2MjksLTAuMDM4NCAtMy4wNjEzOTksMC4wMzQzOTUgLTMuNzIxMDc4LDAuMzY4MTYyNyAtMC41ODUwODEsMC4yOTYwMjU0IC0xLjIwODkxNCwwLjk3ODUxNTMgLTEuNDU0NDQ1LDEuNTkxMjAyOSAtMC4xODY4NSwwLjQ2NjI2MDggLTAuMTkyNDQzLDAuNTYxODAwNyAtMC4yMTkyNjMsMy43NDYzNzY1IGwgLTAuMDI3NTIsMy4yNjc5MTU3IDIuMjMyNDE2LDEuNjRlLTQgYyAxLjk2MDgzMSw4LjVlLTUgMi4yNjcxNDYsMC4wMTc4NCAyLjUxNzkwNiwwLjE0NTcwNiAwLjQyOTI5NSwwLjIxODkwMSAwLjYxNDgyNywwLjUyNzMxMyAwLjY1MDM3MiwxLjA4MTExNiAwLjAzNTk2LDAuNTYwMzY0IC0wLjEzOTI3NiwwLjkxODUzNSAtMC41ODEyNSwxLjE4ODAxIC0wLjI2NTQzMiwwLjE2MTgzOCAtMC40MzQ4MTIsMC4xNjU0NjIgLTcuNzY0NjYzLDAuMTY2MjQgLTQuNDYwNzYxLDYuMjllLTQgLTcuNjkzNjEzMiwwLjAzMzYgLTcuOTg4MjUzNSwwLjA4MTg1IC0wLjk3OTk1NjUsMC4xNjA0NzQgLTEuODYxODkzMiwwLjgxMTM0NCAtMi4yODM4NTI5LDEuNjg1NDkzIC0wLjI5MjUxNTQsMC42MDU5ODQgLTAuMzYyOTE0NywxLjQwNzEwOSAtMC4zMjM5MDU3LDMuNjg1OTU3IDAuMDMyNjc5LDEuOTA5MDczIDAuMDUxMDc0LDIuMTIxMTAzIDAuMjIyMDg2MiwyLjU1OTkzNyAwLjM2NDU2MjYsMC45MzU0OTUgMS4zMzA2NDU2LDEuNzI1OTU4IDIuMzEwMzMzNiwxLjg5MDM0NCAwLjIyMjA3MSwwLjAzNzI2IDIuMjExNTI2MywwLjA3MjE2IDQuNDIxMDExMywwLjA3NzU0IGwgNC4wMTcyNDcsMC4wMDk4IDAuMDAxMywtMS43NjkyNTEgeiBNIDE5LjY1NTIxNCwxMS4xMTg2NjcgQyAxOS4wNzc0NTYsMTAuNzI5MzE0IDE4Ljg4MjQ4OSw5Ljk1MjMzMiAxOS4yMTY0OSw5LjM3MDI2NCBjIDAuMjE1MzY3LC0wLjM3NTMyNDcgMC44MDA0MjMsLTAuNjY2MTU3OSAxLjI0Njg5NSwtMC42MTk4NDAzIDAuOTkzNjI0LDAuMTAzMDgyNyAxLjUxMzY2MSwxLjMxNDk2MzMgMC44ODQ5MTYsMi4wNjIxODIzIC0wLjQ0MDgxMiwwLjUyMzg3MyAtMS4xNzMzNjgsMC42NTYzIC0xLjY5MzA4NywwLjMwNjA2MSB6IgogICAgICAgaWQ9InBhdGg4NTYiIC8+PC9nPjwvc3ZnPgo="

/***/ }),

/***/ "713b":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXTERNAL MODULE: ./node_modules/core-js/modules/es.function.name.js
var es_function_name = __webpack_require__("b0c0");

// EXTERNAL MODULE: ./node_modules/core-js/modules/es.symbol.js
var es_symbol = __webpack_require__("a4d3");

// EXTERNAL MODULE: ./node_modules/core-js/modules/es.symbol.description.js
var es_symbol_description = __webpack_require__("e01a");

// CONCATENATED MODULE: ./node_modules/@quasar/app/lib/webpack/loader.transform-quasar-imports.js!./node_modules/babel-loader/lib??ref--2-0!./node_modules/vue-loader/lib/loaders/templateLoader.js??ref--7!./node_modules/@quasar/app/lib/webpack/loader.auto-import-client.js?kebab!./node_modules/vue-loader/lib??vue-loader-options!./src/layouts/MainLayout.vue?vue&type=template&id=47e28f36&




var render = function render() {
  var _vm = this,
      _c = _vm._self._c,
      _setup = _vm._self._setupProxy;

  return _c('q-layout', {
    attrs: {
      "view": "lHh Lpr lFf"
    }
  }, [_c('q-inner-loading', {
    staticStyle: {
      "z-index": "9999999"
    },
    attrs: {
      "showing": _vm.flowloading
    }
  }, [_c('q-spinner-gears', {
    attrs: {
      "size": "50px",
      "color": "primary"
    }
  })], 1), _c('q-header', {
    attrs: {
      "elevated": ""
    }
  }, [_vm.tools === 'code' ? _c('ToolPalette', {
    ref: "toolPalette",
    attrs: {
      "surface-id": "flow1",
      "selector": "[data-node-type]",
      "nodes": this.stats.nodes,
      "agents": this.stats.agents,
      "queues": this.stats.queues,
      "processors": this.stats.processors,
      "tasks": this.stats.tasks,
      "cpus_total": this.stats.cpus_total,
      "deployments": this.stats.deployments,
      "cpus_running": this.stats.cpus_running
    }
  }) : _vm._e(), _vm.tools === 'model' ? _c('ModelToolPalette', {
    attrs: {
      "surface-id": "flow1",
      "selector": "[data-node-type]"
    }
  }) : _vm._e(), _c('q-toolbar', {
    staticClass: "bg-accent",
    staticStyle: {
      "min-height": "40px",
      "padding": "0px"
    }
  }, [_c('q-btn', {
    staticClass: "text-dark",
    staticStyle: {
      "padding": "0px",
      "height": "40px"
    },
    attrs: {
      "color": "secondary",
      "flat": "",
      "size": "sm",
      "icon": "fa fa-list",
      "label": "0",
      "disable": !_vm.hasHosted
    },
    on: {
      "click": function click($event) {
        return _vm.showStats('Statistics Table', 'statstable');
      }
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n          Statistics Table\n        ")])], 1), _c('q-btn', {
    staticClass: "text-dark",
    staticStyle: {
      "padding": "0px",
      "height": "40px"
    },
    attrs: {
      "color": "secondary",
      "flat": "",
      "size": "sm",
      "icon": "fa fa-bullseye",
      "label": _vm.transmittedSize,
      "disable": !_vm.hasHosted
    },
    on: {
      "click": function click($event) {
        return _vm.showStats('Data Transmitted', 'datatransmitted');
      }
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n          Data Transmitted\n        ")])], 1), _c('q-btn', {
    staticClass: "text-dark",
    staticStyle: {
      "padding": "0px",
      "height": "40px"
    },
    attrs: {
      "color": "secondary",
      "flat": "",
      "size": "sm",
      "icon": "fas fa-satellite-dish",
      "label": _vm.messageCount,
      "disable": !_vm.hasHosted
    },
    on: {
      "click": function click($event) {
        return _vm.showStats('Messages Transmitted', 'messagestransmitted');
      }
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n          Messages Transmitted\n        ")])], 1), _c('q-btn', {
    staticClass: "text-dark",
    staticStyle: {
      "padding": "0px",
      "height": "40px"
    },
    attrs: {
      "color": "secondary",
      "flat": "",
      "size": "sm",
      "icon": "las la-play",
      "label": _vm.stats.processors_starting,
      "disable": !_vm.hasHosted
    },
    on: {
      "click": function click($event) {
        return _vm.showStats('Starting Processors', 'startingprocessors');
      }
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n          Starting Processors\n        ")])], 1), _c('q-btn', {
    staticClass: "text-dark",
    staticStyle: {
      "padding": "0px",
      "height": "40px"
    },
    attrs: {
      "color": "secondary",
      "flat": "",
      "size": "sm",
      "icon": "fa fa-play",
      "label": _vm.stats.processors_running,
      "disable": !_vm.hasHosted
    },
    on: {
      "click": function click($event) {
        return _vm.showStats('Running Processors', 'runningprocessors');
      }
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n          Running Processors\n        ")])], 1), _c('q-btn', {
    staticClass: "text-dark",
    staticStyle: {
      "padding": "0px",
      "height": "40px"
    },
    attrs: {
      "color": "secondary",
      "flat": "",
      "size": "sm",
      "icon": "fa fa-stop",
      "label": _vm.stats.processors_stopped,
      "disable": !_vm.hasHosted
    },
    on: {
      "click": function click($event) {
        return _vm.showStats('Stopped Processors', 'stoppedprocessors');
      }
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n          Stopped Processors\n        ")])], 1), _c('q-btn', {
    staticClass: "text-dark",
    staticStyle: {
      "padding": "0px",
      "height": "40px"
    },
    attrs: {
      "color": "secondary",
      "flat": "",
      "size": "sm",
      "icon": "fa fa-warning invalid",
      "label": _vm.stats.processors_errored,
      "disable": !_vm.hasHosted
    },
    on: {
      "click": function click($event) {
        return _vm.showStats('Errored Processors', 'erroredprocessors');
      }
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n          Errored Processors\n        ")])], 1), _c('q-btn', {
    staticClass: "text-dark",
    staticStyle: {
      "padding": "0px",
      "height": "40px",
      "font-size": "1em"
    },
    attrs: {
      "color": "secondary",
      "flat": "",
      "size": "sm",
      "icon": _vm.mdiEmailFast,
      "label": _vm.queuedTasks,
      "disable": !_vm.hasHosted
    },
    on: {
      "click": function click($event) {
        return _vm.showStats('Queued Tasks', 'queuedtasks');
      }
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n          Queued Tasks\n        ")])], 1), _c('q-btn', {
    staticClass: "text-dark",
    staticStyle: {
      "padding": "0px",
      "height": "40px",
      "font-size": "1em"
    },
    attrs: {
      "color": "secondary",
      "flat": "",
      "size": "sm",
      "icon": _vm.mdiEmailAlert,
      "label": _vm.stats.tasks_failure,
      "disable": !_vm.hasHosted
    },
    on: {
      "click": function click($event) {
        return _vm.showStats('Errored Tasks', 'erroredtasks');
      }
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n          Errored Tasks\n        ")])], 1), _c('q-btn', {
    staticClass: "text-dark",
    staticStyle: {
      "padding": "0px",
      "height": "40px",
      "font-size": "1em"
    },
    attrs: {
      "color": "secondary",
      "flat": "",
      "size": "sm",
      "icon": _vm.mdiEmailCheck,
      "label": _vm.stats.tasks_success,
      "disable": !_vm.hasHosted
    },
    on: {
      "click": function click($event) {
        return _vm.showStats('Completed Tasks', 'completedtasks');
      }
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n          Completed Tasks\n        ")])], 1), _c('q-space'), _vm.$auth.isAuthenticated ? _c('q-btn', {
    attrs: {
      "dense": "",
      "flat": "",
      "color": "secondary"
    },
    on: {
      "click": function click($event) {
        _vm.chooseplan = true;
      }
    }
  }, [_vm._v("\n        Upgrade Plan\n      ")]) : _vm._e(), !_vm.$auth.isAuthenticated ? _c('q-btn', {
    attrs: {
      "dense": "",
      "flat": "",
      "color": "secondary"
    },
    on: {
      "click": function click($event) {
        _vm.chooseplan = true;
      }
    }
  }, [_vm._v("\n        Subscribe\n      ")]) : _vm._e(), _c('q-input', {
    staticClass: "q-ml-md text-dark bg-white",
    staticStyle: {
      "width": "20%",
      "border-left": "1px solid lightgrey"
    },
    attrs: {
      "dark": "",
      "dense": "",
      "standout": "",
      "placeholder": "Search...",
      "input-class": "text-left text-dark"
    },
    on: {
      "keyup": _vm.searchString
    },
    scopedSlots: _vm._u([{
      key: "append",
      fn: function fn() {
        return [_vm.text === '' ? _c('q-icon', {
          attrs: {
            "color": "dark",
            "size": "sm",
            "name": "search"
          }
        }) : _c('q-icon', {
          staticClass: "cursor-pointer text-dark",
          attrs: {
            "name": "clear",
            "color": "dark",
            "size": "sm"
          },
          on: {
            "click": function click($event) {
              _vm.text = '';
            }
          }
        })];
      },
      proxy: true
    }]),
    model: {
      value: _vm.text,
      callback: function callback($$v) {
        _vm.text = $$v;
      },
      expression: "text"
    }
  })], 1)], 1), _c('q-splitter', {
    staticStyle: {
      "overflow": "hidden"
    },
    attrs: {
      "vertical": "",
      "limits": [60, 100],
      "unit": "%"
    },
    scopedSlots: _vm._u([{
      key: "before",
      fn: function fn() {
        return [_c('div', {
          staticStyle: {
            "height": "100vh",
            "width": "100%",
            "position": "relative",
            "top": "95px",
            "overflow": "hidden"
          }
        }, [_vm._l(_vm.flows, function (flow) {
          return _c('q-tab-panels', {
            key: flow.id,
            attrs: {
              "keep-alive": ""
            },
            model: {
              value: _vm.tab,
              callback: function callback($$v) {
                _vm.tab = $$v;
              },
              expression: "tab"
            }
          }, [_c('q-tab-panel', {
            ref: 'flow' + flow.id,
            refInFor: true,
            staticStyle: {
              "height": "calc(100vh - 165px)",
              "padding": "0px",
              "overflow": "hidden"
            },
            attrs: {
              "name": 'flow' + flow.id
            }
          }, [_c('Designer', {
            ref: 'flow' + flow.id + 'designer',
            refInFor: true,
            attrs: {
              "flowcode": flow.code,
              "flowname": flow.filename,
              "flowuuid": flow._id,
              "flowid": flow.id,
              "surface-id": 'flow' + flow.id,
              "showtoolbar": "true",
              "navigate": "true"
            },
            on: {
              "update-name": _vm.updateFlow
            }
          })], 1)], 1);
        }), _c('q-tabs', {
          staticClass: "bg-primary",
          attrs: {
            "dense": "",
            "align": "left",
            "narrow-indicator": "",
            "active-color": "dark",
            "indicator-color": "accent",
            "active-bg-color": "accent"
          },
          on: {
            "input": _vm.tabChanged
          },
          model: {
            value: _vm.tab,
            callback: function callback($$v) {
              _vm.tab = $$v;
            },
            expression: "tab"
          }
        }, [_vm._l(_vm.flows, function (flow) {
          return _c('q-tab', {
            key: flow.id,
            staticClass: "text-dark",
            attrs: {
              "name": 'flow' + flow.id,
              "label": flow.filename
            }
          });
        }), _c('q-btn', {
          attrs: {
            "flat": "",
            "dense": "",
            "size": "md",
            "icon": "las la-plus",
            "color": "dark"
          },
          on: {
            "click": _vm.addNewFlow
          }
        }, [_c('q-tooltip', {
          attrs: {
            "content-class": "",
            "content-style": "font-size: 16px",
            "offset": [10, 10]
          }
        }, [_vm._v("\n              Add New Flow\n            ")])], 1)], 2), _c('q-btn', {
          staticStyle: {
            "z-index": "9999",
            "position": "absolute",
            "right": "0px"
          },
          attrs: {
            "flat": "",
            "dense": "",
            "size": "md",
            "color": "primary",
            "icon": "menu",
            "aria-label": "Menu"
          },
          on: {
            "click": function click($event) {
              _vm.drawer = !_vm.drawer;
            }
          }
        })], 2)];
      },
      proxy: true
    }, {
      key: "after",
      fn: function fn() {
        return [_c('div', {
          staticStyle: {
            "height": "100vh",
            "width": "100%",
            "padding-top": "5px",
            "position": "relative",
            "top": "95px",
            "overflow": "hidden"
          }
        }, [false ? undefined : _vm._e(), _c('q-tabs', {
          staticClass: "bg-primary",
          attrs: {
            "dense": "",
            "align": "left",
            "narrow-indicator": "",
            "active-color": "dark",
            "indicator-color": "primary",
            "active-bg-color": "accent"
          },
          on: {
            "input": _vm.tabChanged
          },
          model: {
            value: _vm.drawertab,
            callback: function callback($$v) {
              _vm.drawertab = $$v;
            },
            expression: "drawertab"
          }
        }, [_c('q-tab', {
          staticClass: "text-dark",
          staticStyle: {
            "font-size": "16px"
          },
          attrs: {
            "name": "console",
            "icon": "las la-terminal",
            "label": "Console"
          }
        }), _c('q-tab', {
          staticClass: "text-dark",
          staticStyle: {
            "font-size": "16px"
          },
          attrs: {
            "name": "messages",
            "icon": "las la-envelope",
            "label": "Messages"
          }
        }), _c('q-tab', {
          staticClass: "text-dark",
          staticStyle: {
            "font-size": "16px"
          },
          attrs: {
            "name": "queues",
            "icon": "input",
            "label": "Queues"
          }
        }), _c('q-tab', {
          staticClass: "text-dark",
          staticStyle: {
            "font-size": "16px"
          },
          attrs: {
            "name": "monitor",
            "icon": "las la-desktop",
            "label": "Monitor",
            "disable": ""
          }
        }), _c('q-tab', {
          staticClass: "text-dark",
          staticStyle: {
            "font-size": "16px"
          },
          attrs: {
            "name": "error",
            "icon": "las la-exclamation",
            "label": "Errors",
            "disable": ""
          }
        })], 1), _c('q-tab-panels', {
          attrs: {
            "keep-alive": ""
          },
          model: {
            value: _vm.drawertab,
            callback: function callback($$v) {
              _vm.drawertab = $$v;
            },
            expression: "drawertab"
          }
        }, [_c('q-tab-panel', {
          ref: "console",
          staticStyle: {
            "padding": "0px",
            "width": "100%",
            "padding-top": "0px",
            "height": "calc(100vh - 170px)"
          },
          attrs: {
            "name": "console"
          }
        }, [_c('q-scroll-area', {
          staticStyle: {
            "padding": "10px",
            "height": "calc(100vh - 240px)",
            "width": "100%"
          }
        }, _vm._l(_vm.consolelog, function (log) {
          return _c('div', [_c('span', {
            staticStyle: {
              "font-weight": "bold"
            }
          }, [_vm._v(_vm._s(log.name) + ":")]), _c('span', [_vm._v(_vm._s(log.date))]), _c('pre', [_vm._v(_vm._s(log.msg))])]);
        }), 0), _c('q-toolbar', {
          staticStyle: {
            "padding": "20px"
          }
        }, [_c('q-space'), _c('q-btn', {
          attrs: {
            "flat": "",
            "dense": "",
            "color": "secondary"
          },
          on: {
            "click": function click($event) {
              _vm.consolelog = [];
            }
          }
        }, [_vm._v("\n                Clear\n              ")])], 1)], 1), _c('q-tab-panel', {
          ref: "messages",
          staticStyle: {
            "padding": "0px",
            "width": "100%",
            "padding-top": "0px",
            "height": "calc(100vh - 170px)"
          },
          attrs: {
            "name": "messages"
          }
        }, [_c('q-table', {
          staticStyle: {
            "height": "100%",
            "width": "100%",
            "border-top-radius": "0px",
            "border-bottom-radius": "0px"
          },
          attrs: {
            "dense": "",
            "columns": _vm.messageColumns,
            "data": _vm.msglogs,
            "row-key": "name",
            "flat": "",
            "virtual-scroll": "",
            "pagination": _vm.initialPagination
          }
        })], 1), _c('q-tab-panel', {
          ref: "queues",
          staticStyle: {
            "padding": "0px",
            "width": "100%",
            "padding-top": "0px",
            "height": "calc(100vh - 130px)"
          },
          attrs: {
            "name": "queues"
          }
        }, [_c('q-splitter', {
          staticStyle: {
            "height": "calc(100% - 40px)"
          },
          attrs: {
            "separator-style": "background-color: #e3e8ec;height:5px",
            "horizontal": ""
          },
          scopedSlots: _vm._u([{
            key: "before",
            fn: function fn() {
              return [_c('q-table', {
                staticStyle: {
                  "height": "calc(100vh - 170px)"
                },
                attrs: {
                  "dense": "",
                  "data": _vm.queues,
                  "columns": _vm.columns,
                  "row-key": "name",
                  "rows-per-page-options": [50],
                  "virtual-scroll": ""
                },
                scopedSlots: _vm._u([{
                  key: "body",
                  fn: function fn(props) {
                    return [_c('q-tr', {
                      attrs: {
                        "props": props
                      }
                    }, [_c('q-td', {
                      key: "name",
                      attrs: {
                        "props": props,
                        "width": 150
                      }
                    }, [_c('a', {
                      staticClass: "text-secondary",
                      staticStyle: {
                        "z-index": "99999",
                        "cursor": "pointer",
                        "width": "100%",
                        "min-width": "250px",
                        "font-size": "1.3em"
                      },
                      on: {
                        "click": function click($event) {
                          return _vm.showQueueDetail(props.row.name);
                        }
                      }
                    }, [_vm._v("\n                          " + _vm._s(props.row.name) + "\n                        ")])]), _c('q-td', {
                      key: "messages",
                      attrs: {
                        "props": props
                      }
                    }, [_vm._v("\n                        " + _vm._s(props.row.messages) + "\n                      ")]), _c('q-td', {
                      key: "ready",
                      attrs: {
                        "props": props
                      }
                    }, [_c('a', {
                      staticClass: "text-secondary",
                      staticStyle: {
                        "z-index": "99999",
                        "cursor": "pointer",
                        "width": "100%",
                        "min-width": "250px",
                        "font-size": "1.3em"
                      },
                      on: {
                        "click": function click($event) {
                          _vm.queuename = props.row.name;
                          _vm.viewQueueDialog = true;
                        }
                      }
                    }, [_vm._v("\n                          " + _vm._s(props.row.ready) + "\n                        ")])]), _c('q-td', {
                      key: "unacked",
                      attrs: {
                        "props": props
                      }
                    }, [_vm._v("\n                        " + _vm._s(props.row.unacked) + "\n                      ")]), _c('q-td', {
                      key: "bytes",
                      attrs: {
                        "width": 200,
                        "props": props
                      }
                    }, [_vm._v("\n                        " + _vm._s(props.row.bytes) + "\n                      ")]), _c('q-td', {
                      key: "actions",
                      staticStyle: {
                        "width": "25px"
                      },
                      attrs: {
                        "props": props
                      }
                    }, [_c('q-btn', {
                      staticClass: "bg-white text-primary",
                      attrs: {
                        "flat": "",
                        "round": "",
                        "dense": "",
                        "size": "sm",
                        "id": props.row.name,
                        "width": "100",
                        "icon": "remove_circle"
                      },
                      on: {
                        "click": function click($event) {
                          return _vm.showPurgeConfirm(props.row.name);
                        }
                      }
                    }, [_c('q-tooltip', {
                      attrs: {
                        "content-class": "",
                        "content-style": "font-size: 16px",
                        "offset": [10, 10]
                      }
                    }, [_vm._v("\n                            Purge Messages\n                          ")])], 1), _c('q-btn', {
                      staticClass: "bg-white text-primary",
                      attrs: {
                        "flat": "",
                        "round": "",
                        "dense": "",
                        "size": "sm",
                        "id": props.row.name,
                        "width": "100",
                        "icon": "fas fa-cog"
                      }
                    }, [_c('q-tooltip', {
                      attrs: {
                        "content-class": "",
                        "content-style": "font-size: 16px",
                        "offset": [10, 10]
                      }
                    }, [_vm._v("\n                            Configure\n                          ")])], 1), _c('q-btn', {
                      staticClass: "bg-white text-primary",
                      attrs: {
                        "flat": "",
                        "round": "",
                        "dense": "",
                        "size": "sm",
                        "id": props.row.name,
                        "width": "100",
                        "icon": "delete"
                      }
                    }, [_c('q-tooltip', {
                      attrs: {
                        "content-class": "",
                        "content-style": "font-size: 16px",
                        "offset": [10, 10]
                      }
                    }, [_vm._v("\n                            Delete Queue\n                          ")])], 1)], 1)], 1)];
                  }
                }])
              })];
            },
            proxy: true
          }, {
            key: "after",
            fn: function fn() {
              return [_c('q-tabs', {
                staticClass: "bg-primary",
                attrs: {
                  "dense": "",
                  "align": "left",
                  "narrow-indicator": "",
                  "active-color": "dark",
                  "indicator-color": "primary",
                  "active-bg-color": "accent"
                },
                model: {
                  value: _vm.queuedetailtab,
                  callback: function callback($$v) {
                    _vm.queuedetailtab = $$v;
                  },
                  expression: "queuedetailtab"
                }
              }, [_c('q-tab', {
                staticClass: "text-dark",
                attrs: {
                  "name": "stats",
                  "label": "Stats"
                }
              }), _c('q-tab', {
                staticClass: "text-dark",
                attrs: {
                  "name": "json",
                  "label": "JSON"
                }
              }), _c('q-tab', {
                staticClass: "text-dark",
                attrs: {
                  "name": "history",
                  "label": "History"
                }
              })], 1), _c('q-tab-panels', {
                staticStyle: {
                  "height": "100%"
                },
                attrs: {
                  "keep-alive": ""
                },
                model: {
                  value: _vm.queuedetailtab,
                  callback: function callback($$v) {
                    _vm.queuedetailtab = $$v;
                  },
                  expression: "queuedetailtab"
                }
              }, [_c('q-tab-panel', {
                ref: "stats",
                staticStyle: {
                  "padding": "0px",
                  "width": "100%",
                  "padding-top": "0px",
                  "height": "100%"
                },
                attrs: {
                  "name": "stats"
                }
              }, [_c('q-table', {
                staticStyle: {
                  "height": "100%",
                  "width": "100%",
                  "border-top-radius": "0px",
                  "border-bottom-radius": "0px"
                },
                attrs: {
                  "dense": "",
                  "columns": _vm.queueDetailColumns,
                  "data": _vm.queueDetailData,
                  "row-key": "name",
                  "flat": "",
                  "virtual-scroll": "",
                  "pagination": _vm.initialPagination
                }
              })], 1), _c('q-tab-panel', {
                ref: "json",
                staticStyle: {
                  "padding": "0px",
                  "width": "100%",
                  "padding-top": "0px",
                  "height": "calc(100% - 25px)"
                },
                attrs: {
                  "name": "json",
                  "keep-alive": ""
                }
              }, [_c('editor', {
                ref: "queueDetailEditor",
                staticStyle: {
                  "font-size": "1.5em"
                },
                attrs: {
                  "lang": "javascript",
                  "theme": "chrome",
                  "width": "100%",
                  "height": "100%"
                },
                on: {
                  "init": _vm.queueDetailEditorInit
                },
                model: {
                  value: _vm.queueDetailContent,
                  callback: function callback($$v) {
                    _vm.queueDetailContent = $$v;
                  },
                  expression: "queueDetailContent"
                }
              })], 1)], 1)];
            },
            proxy: true
          }]),
          model: {
            value: _vm.queueTableSplitter,
            callback: function callback($$v) {
              _vm.queueTableSplitter = $$v;
            },
            expression: "queueTableSplitter"
          }
        })], 1), _c('q-tab-panel', {
          ref: "monitor",
          staticStyle: {
            "padding": "0px",
            "width": "100%",
            "padding-top": "0px"
          },
          attrs: {
            "name": "monitor"
          }
        }), _c('q-tab-panel', {
          ref: "error",
          staticStyle: {
            "padding": "0px",
            "width": "100%",
            "padding-top": "0px"
          },
          attrs: {
            "name": "error"
          }
        })], 1)], 1)];
      },
      proxy: true
    }]),
    model: {
      value: _vm.splitterModel,
      callback: function callback($$v) {
        _vm.splitterModel = $$v;
      },
      expression: "splitterModel"
    }
  }), _c('q-footer', {
    staticStyle: {
      "background-color": "rgba(249, 250, 251, 0.9)",
      "height": "32px",
      "font-size": "16px",
      "padding": "5px",
      "font-weight": "bold"
    },
    attrs: {
      "elevated": ""
    }
  }, [_c('q-toolbar', {
    staticStyle: {
      "padding": "0px",
      "margin-top": "-12px"
    }
  }, [_c('q-btn', {
    attrs: {
      "flat": "",
      "dense": "",
      "color": "primary"
    }
  }, [_c('q-item-label', {
    staticClass: "text-dark"
  }, [_vm._v("\n          " + _vm._s(_vm.status) + "\n        ")])], 1), _c('q-space'), _c('q-btn-toggle', {
    staticClass: "text-primary",
    staticStyle: {
      "margin-right": "40px"
    },
    attrs: {
      "push": "",
      "flat": "",
      "dense": "",
      "toggle-color": "secondary",
      "options": [{
        label: 'Disconnected',
        value: 'disconnected',
        slot: 'one'
      }, {
        label: 'Connected',
        value: 'connected',
        slot: 'two'
      }, {
        label: 'Streaming',
        value: 'streaming',
        slot: 'three'
      }]
    },
    scopedSlots: _vm._u([{
      key: "one",
      fn: function fn() {
        return [_c('q-icon', {
          attrs: {
            "name": _vm.mdiFlashOutline
          }
        }), _c('q-tooltip', {
          attrs: {
            "content-style": "font-size: 16px",
            "content-class": "bg-black text-white"
          }
        }, [_vm._v("\n            Disconnected\n          ")])];
      },
      proxy: true
    }, {
      key: "two",
      fn: function fn() {
        return [_c('q-icon', {
          attrs: {
            "name": _vm.mdiFlash
          }
        }), _c('q-tooltip', {
          attrs: {
            "content-style": "font-size: 16px",
            "content-class": "bg-black text-white"
          }
        }, [_vm._v("\n            Connected\n          ")])];
      },
      proxy: true
    }, {
      key: "three",
      fn: function fn() {
        return [_c('q-icon', {
          attrs: {
            "name": _vm.mdiWavesArrowRight
          }
        }), _c('q-tooltip', {
          attrs: {
            "content-style": "font-size: 16px",
            "content-class": "bg-black text-white"
          }
        }, [_vm._v("\n            Streaming\n          ")])];
      },
      proxy: true
    }]),
    model: {
      value: _vm.modeModel,
      callback: function callback($$v) {
        _vm.modeModel = $$v;
      },
      expression: "modeModel"
    }
  }), _c('q-btn', {
    attrs: {
      "flat": "",
      "dense": "",
      "color": "primary",
      "icon": "chat"
    },
    on: {
      "click": _vm.toggleChat
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n          AI Chatbot\n        ")])], 1), _c('q-btn', {
    attrs: {
      "flat": "",
      "dense": "",
      "color": "primary",
      "icon": "menu"
    },
    on: {
      "click": _vm.toggleSplitter
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-style": "font-size: 16px",
      "content-class": "bg-black text-white"
    }
  }, [_vm._v("\n          Streaming Data\n        ")])], 1)], 1)], 1), _c('q-drawer', {
    staticStyle: {
      "overflow": "hidden"
    },
    attrs: {
      "side": "right",
      "bordered": "",
      "width": 512
    },
    model: {
      value: _vm.searchdrawer,
      callback: function callback($$v) {
        _vm.searchdrawer = $$v;
      },
      expression: "searchdrawer"
    }
  }, [_c('q-scroll-area', {
    staticStyle: {
      "height": "calc(100vh - 300px)",
      "width": "100%"
    }
  }, [_c('q-list', {
    attrs: {
      "separator": ""
    }
  }, _vm._l(_vm.items, function (item) {
    return _c('q-item', {
      key: item.id,
      attrs: {
        "id": 'row' + item.id
      }
    }, [_c('q-item-section', {
      attrs: {
        "avatar": ""
      }
    }, [_c('q-icon', {
      staticClass: "text-secondary",
      attrs: {
        "name": "fas fa-microchip"
      }
    })], 1), _c('q-item-section', [_c('q-item-label', [_c('a', {
      staticClass: "text-secondary",
      staticStyle: {
        "z-index": "99999",
        "cursor": "pointer",
        "width": "100%",
        "min-width": "250px",
        "font-size": "1.3em"
      },
      on: {
        "click": function click($event) {
          return _vm.centerNode(item.id);
        }
      }
    }, [_vm._v("\n                " + _vm._s(item.name) + "\n              ")])]), _c('q-item-label', {
      attrs: {
        "caption": "",
        "lines": "2"
      }
    }, [_vm._v("\n              " + _vm._s(item.description) + "\n            ")])], 1), _c('q-space')], 1);
  }), 1)], 1), _c('q-inner-loading', {
    staticStyle: {
      "z-index": "9999999"
    },
    attrs: {
      "showing": false
    }
  }, [_c('q-spinner-gears', {
    attrs: {
      "size": "50px",
      "color": "primary"
    }
  })], 1)], 1), _c('q-drawer', {
    staticStyle: {
      "overflow": "hidden"
    },
    attrs: {
      "side": "right",
      "bordered": "",
      "width": 750
    },
    model: {
      value: _vm.chatdrawer,
      callback: function callback($$v) {
        _vm.chatdrawer = $$v;
      },
      expression: "chatdrawer"
    }
  }, [_c('q-tabs', {
    staticClass: "bg-primary",
    attrs: {
      "dense": "",
      "align": "left",
      "narrow-indicator": "",
      "active-color": "dark",
      "indicator-color": "primary",
      "active-bg-color": "accent"
    },
    model: {
      value: _vm.pythontabs,
      callback: function callback($$v) {
        _vm.pythontabs = $$v;
      },
      expression: "pythontabs"
    }
  }, [_c('q-tab', {
    attrs: {
      "name": "pythonconsole",
      "label": "Scratchpad"
    }
  }), _c('q-tab', {
    attrs: {
      "name": "chatconsole",
      "label": "AI Coder"
    }
  })], 1), _c('q-tab-panels', {
    attrs: {
      "keep-alive": ""
    },
    model: {
      value: _vm.pythontabs,
      callback: function callback($$v) {
        _vm.pythontabs = $$v;
      },
      expression: "pythontabs"
    }
  }, [_c('q-tab-panel', {
    ref: "pythonconsole",
    staticStyle: {
      "padding": "0px"
    },
    attrs: {
      "name": "pythonconsole"
    }
  }, [!_vm.$auth.isAuthenticated ? _c('q-inner-loading', {
    staticStyle: {
      "z-index": "9999"
    },
    attrs: {
      "showing": true
    }
  }, [_c('q-item-label', [_vm._v("Not Logged In")])], 1) : _vm._e(), _c('Console')], 1), _c('q-tab-panel', {
    ref: "chatconsole",
    staticStyle: {
      "padding": "0px"
    },
    attrs: {
      "name": "chatconsole"
    }
  }, [!_vm.$auth.isAuthenticated || !_vm.isProPlan ? _c('q-inner-loading', {
    staticStyle: {
      "z-index": "9999"
    },
    attrs: {
      "showing": true
    }
  }, [!_vm.$auth.isAuthenticated ? _c('q-item-label', [_vm._v("\n            Not Logged In\n          ")]) : _vm._e(), _vm.$auth.isAuthenticated || !_vm.isProPlan ? _c('q-item-label', [_vm._v("\n            Upgrade to Pro Plan\n          ")]) : _vm._e()], 1) : _vm._e(), _c('q-toolbar', {
    staticClass: "bg-accent",
    staticStyle: {
      "padding": "0px",
      "padding-left": "10px"
    }
  }, [_c('q-item-label', {
    staticStyle: {
      "font-size": "1.5em",
      "font-family": "'Indie Flower', cursive",
      "margin-top": "5px",
      "margin-right": "1em"
    }
  }, [_vm._v("\n            AI Coding Buddy\n          ")])], 1), _c('q-input', {
    staticStyle: {
      "width": "100%",
      "padding": "10px",
      "resize": "none !important"
    },
    attrs: {
      "label": "Hi! Ask me anything...I can even write code!",
      "type": "textarea"
    },
    model: {
      value: _vm.question,
      callback: function callback($$v) {
        _vm.question = $$v;
      },
      expression: "question"
    }
  }), _c('q-toolbar', [_c('q-space'), _c('q-btn', {
    staticStyle: {
      "margin-right": "30px",
      "margin-bottom": "30px"
    },
    attrs: {
      "label": "Go!",
      "color": "secondary"
    },
    on: {
      "click": _vm.sendChat
    }
  })], 1), _c('q-separator'), _c('q-scroll-area', {
    staticStyle: {
      "height": "calc(100vh - 420px)"
    }
  }, [_c('q-markdown', {
    attrs: {
      "src": _vm.answer
    }
  }), _c('q-inner-loading', {
    staticStyle: {
      "z-index": "9999999"
    },
    attrs: {
      "showing": _vm.loadingchat
    }
  }, [_c('q-spinner-gears', {
    attrs: {
      "size": "50px",
      "color": "primary"
    }
  })], 1)], 1)], 1)], 1)], 1), _c('q-drawer', {
    staticStyle: {
      "overflow": "hidden"
    },
    attrs: {
      "side": "right",
      "bordered": "",
      "width": 750
    },
    model: {
      value: _vm.blocksdrawer,
      callback: function callback($$v) {
        _vm.blocksdrawer = $$v;
      },
      expression: "blocksdrawer"
    }
  }, [_c('q-tabs', {
    staticClass: "bg-primary",
    attrs: {
      "dense": "",
      "align": "left",
      "narrow-indicator": "",
      "active-color": "dark",
      "indicator-color": "primary",
      "active-bg-color": "accent",
      "color": "accent"
    },
    model: {
      value: _vm.blockstabs,
      callback: function callback($$v) {
        _vm.blockstabs = $$v;
      },
      expression: "blockstabs"
    }
  }, [_c('q-tab', {
    staticClass: "text-dark",
    attrs: {
      "name": "blocksregistry",
      "label": "Blocks",
      "icon": "las la-cube"
    }
  }), _c('q-tab', {
    staticClass: "text-dark",
    attrs: {
      "name": "blockspublic",
      "label": "Public",
      "icon": "las la-globe"
    }
  }), _c('q-tab', {
    staticClass: "text-dark",
    attrs: {
      "name": "blocksmine",
      "label": "Private",
      "icon": "las la-user"
    }
  })], 1), _c('q-tab-panels', {
    attrs: {
      "keep-alive": ""
    },
    model: {
      value: _vm.blockstabs,
      callback: function callback($$v) {
        _vm.blockstabs = $$v;
      },
      expression: "blockstabs"
    }
  }, [_c('q-tab-panel', {
    ref: "blocksregistry",
    staticStyle: {
      "display": "grid",
      "grid-gap": "10px",
      "grid-template-columns": "repeat(auto-fill, minmax(150px, 1fr))",
      "justify-content": "space-around",
      "padding": "10px"
    },
    attrs: {
      "name": "blocksregistry"
    }
  }, [_vm._l(_vm.blocks, function (block) {
    return _c('q-btn', {
      key: block.data.id,
      staticClass: "brightness text-primary",
      staticStyle: {
        "cursor": "pointer",
        "font-size": "2em",
        "border-radius": "10px",
        "border": "1px lightgrey solid",
        "padding": "20px"
      },
      attrs: {
        "flat": "",
        "color": "secondary",
        "icon": block.data.node.icon,
        "id": 'block' + block.data.id,
        "disable": block.disabled
      },
      on: {
        "click": function click($event) {
          return _vm.showBlock(block.data.node);
        }
      }
    }, [_c('div', {
      staticStyle: {
        "font-size": "18px",
        "font-family": "arial"
      }
    }, [_vm._v("\n            " + _vm._s(block.data.node.name) + "\n          ")])]);
  }), !_vm.$auth.isAuthenticated ? _c('q-inner-loading', {
    staticStyle: {
      "z-index": "9999"
    },
    attrs: {
      "showing": true
    }
  }, [_c('q-item-label', [_vm._v("Not Logged In")])], 1) : _vm._e()], 2)], 1)], 1), _c('q-drawer', {
    staticStyle: {
      "overflow": "hidden",
      "padding-top": "35px"
    },
    attrs: {
      "side": "right",
      "bordered": "",
      "width": 650
    },
    model: {
      value: _vm.blockdrawer,
      callback: function callback($$v) {
        _vm.blockdrawer = $$v;
      },
      expression: "blockdrawer"
    }
  }, [_c('q-toolbar', {
    staticClass: "bg-primary text-dark",
    staticStyle: {
      "padding": "5px"
    }
  }, [_c('q-icon', {
    staticStyle: {
      "font-size": "2em",
      "margin-right": "10px"
    },
    attrs: {
      "name": _vm.blockshown.icon
    }
  }), _c('q-item-label', {
    staticStyle: {
      "font-size": "2em",
      "font-style": "italic",
      "margin-top": "5px",
      "margin-right": "1em"
    }
  }, [_vm._v("\n        " + _vm._s(_vm.blockshown.name) + "\n      ")]), _c('q-space'), _c('q-btn', {
    attrs: {
      "dense": "",
      "flat": "",
      "size": "md",
      "color": "secondary",
      "icon": "close"
    },
    on: {
      "click": function click($event) {
        _vm.blockdrawer = false;
      }
    }
  })], 1), _c('div', {
    staticStyle: {
      "padding": "20px"
    }
  }, [_c('span', {
    staticStyle: {
      "font-size": "1.5em",
      "font-family": "'Indie Flower', cursive",
      "margin-top": "5px",
      "margin-right": "1em"
    }
  }, [_vm._v("Description")]), _c('p', {
    staticClass: "text-secondary",
    staticStyle: {
      "margin-left": "20px",
      "margin-bottom": "25px"
    }
  }, [_vm._v("\n        " + _vm._s(_vm.blockshown.description) + "\n      ")]), _c('span', {
    staticStyle: {
      "font-size": "1.5em",
      "font-family": "'Indie Flower', cursive",
      "margin-top": "25px",
      "margin-right": "1em"
    }
  }, [_vm._v("Package")]), _c('p', {
    staticClass: "text-secondary",
    staticStyle: {
      "margin-left": "20px",
      "margin-bottom": "25px"
    }
  }, [_vm._v("\n        " + _vm._s(_vm.blockshown.package) + "\n      ")]), _c('span', {
    staticStyle: {
      "font-size": "1.5em",
      "font-family": "'Indie Flower', cursive",
      "margin-top": "25px",
      "margin-right": "1em"
    }
  }, [_vm._v("Version")]), _c('p', {
    staticClass: "text-secondary",
    staticStyle: {
      "margin-left": "20px",
      "margin-bottom": "25px"
    }
  }, [_vm._v("\n        " + _vm._s(_vm.blockshown.version) + "\n      ")]), _c('span', {
    staticStyle: {
      "font-size": "1.5em",
      "font-family": "'Indie Flower', cursive",
      "margin-top": "25px",
      "margin-right": "1em"
    }
  }, [_vm._v("Container")]), _c('div', {
    staticStyle: {
      "padding-left": "25px"
    }
  }, [_c('p', {
    staticClass: "text-secondary",
    staticStyle: {
      "margin-left": "20px",
      "margin-bottom": "25px"
    }
  }, [_vm._v("\n          Container: " + _vm._s(_vm.blockshown.container) + "\n        ")]), _c('p', {
    staticClass: "text-secondary",
    staticStyle: {
      "margin-left": "20px",
      "margin-bottom": "25px"
    }
  }, [_vm._v("\n          Container Image: " + _vm._s(_vm.blockshown.containerimage) + "\n        ")])])])], 1), _c('q-drawer', {
    staticStyle: {
      "overflow": "hidden"
    },
    attrs: {
      "side": "right",
      "bordered": "",
      "width": 512
    },
    model: {
      value: _vm.librarydrawer,
      callback: function callback($$v) {
        _vm.librarydrawer = $$v;
      },
      expression: "librarydrawer"
    }
  }, [_c('Library', {
    staticStyle: {
      "width": "100%"
    },
    attrs: {
      "objecttype": 'template',
      "icon": 'fas fa-wrench',
      "collection": 'library'
    }
  })], 1), _c('q-dialog', {
    attrs: {
      "transition-show": "none",
      "persistent": ""
    },
    model: {
      value: _vm.infodialog,
      callback: function callback($$v) {
        _vm.infodialog = $$v;
      },
      expression: "infodialog"
    }
  }, [_c('q-card', {
    staticStyle: {
      "width": "50vw",
      "max-width": "30vw",
      "overflow": "hidden",
      "height": "70vh",
      "padding": "10px",
      "padding-left": "30px",
      "padding-top": "40px"
    }
  }, [_c('q-card-section', {
    staticClass: "bg-secondary",
    staticStyle: {
      "position": "absolute",
      "left": "0px",
      "top": "0px",
      "width": "100%",
      "height": "40px"
    }
  }, [_c('div', {
    staticStyle: {
      "font-weight": "bold",
      "font-size": "18px",
      "margin-left": "10px",
      "margin-top": "-5px",
      "margin-right": "5px",
      "color": "#fff"
    }
  }, [_c('q-toolbar', [_c('q-item-label', [_vm._v(_vm._s(_vm.infotitle))]), _c('q-space'), _c('q-btn', {
    staticClass: "text-primary",
    staticStyle: {
      "z-index": "10"
    },
    attrs: {
      "flat": "",
      "dense": "",
      "round": "",
      "size": "sm",
      "icon": "fas fa-close"
    },
    on: {
      "click": function click($event) {
        _vm.infodialog = false;
      }
    }
  })], 1)], 1)]), _c('q-scroll-area', {
    staticStyle: {
      "height": "calc(70vh - 50px)",
      "width": "100%",
      "padding": "20px"
    }
  }, [_c('div', {
    staticStyle: {
      "min-height": "60vh"
    }
  })])], 1)], 1), _c('q-dialog', {
    attrs: {
      "transition-show": "none",
      "persistent": ""
    },
    model: {
      value: _vm.chooseplan,
      callback: function callback($$v) {
        _vm.chooseplan = $$v;
      },
      expression: "chooseplan"
    }
  }, [_c('q-card', {
    staticStyle: {
      "width": "70vw",
      "max-width": "40vw",
      "overflow": "hidden",
      "height": "70vh",
      "padding": "10px",
      "padding-left": "30px",
      "padding-top": "40px"
    }
  }, [_c('q-card-section', {
    staticClass: "bg-secondary",
    staticStyle: {
      "position": "absolute",
      "left": "0px",
      "top": "0px",
      "width": "100%",
      "height": "40px"
    }
  }, [_c('div', {
    staticStyle: {
      "font-weight": "bold",
      "font-size": "18px",
      "color": "white",
      "margin-left": "10px",
      "margin-top": "-5px",
      "margin-right": "5px"
    }
  }, [_c('q-toolbar', [_c('q-item-label', [_vm._v("Choose a Plan")]), _c('q-space'), _c('q-btn', {
    staticClass: "text-primary",
    staticStyle: {
      "z-index": "10"
    },
    attrs: {
      "flat": "",
      "dense": "",
      "round": "",
      "size": "sm",
      "icon": "fas fa-close"
    },
    on: {
      "click": function click($event) {
        _vm.chooseplan = false;
      }
    }
  })], 1)], 1)]), _c('q-scroll-area', {
    staticStyle: {
      "height": "calc(100% - 20px)",
      "width": "100%"
    }
  }, [_c('table', {
    staticStyle: {
      "width": "100%"
    },
    attrs: {
      "cellpadding": "10px"
    }
  }, [_c('thead', {
    staticStyle: {
      "font-weight": "bold"
    }
  }, [_c('tr', [_c('td'), _c('td', [_vm._v("Guest")]), _c('td', [_vm._v("Free")]), _c('td', [_vm._v("Developer")]), _c('td', [_vm._v("Pro")]), _c('td', [_vm._v("Hosted")]), _c('td', [_vm._v("Enterprise")])])]), _c('tr', {
    staticStyle: {
      "background-color": "rgb(244, 246, 247) !important",
      "border-top": "1px solid black"
    }
  }, [_c('td', [_vm._v("\n              Execute Data Flows "), _c('i', {
    staticClass: "fas fa-info-circle text-secondary",
    staticStyle: {
      "font-size": "1em",
      "cursor": "pointer"
    },
    on: {
      "click": function click($event) {
        return _vm.info('Execute Data Flows');
      }
    }
  })]), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1)]), _c('tr', [_c('td', [_vm._v("\n              Browser Execution "), _c('i', {
    staticClass: "fas fa-info-circle text-secondary",
    staticStyle: {
      "font-size": "1em",
      "cursor": "pointer"
    },
    on: {
      "click": function click($event) {
        return _vm.info('Browser Execution');
      }
    }
  })]), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1)]), _c('tr', {
    staticStyle: {
      "background-color": "rgb(244, 246, 247) !important"
    }
  }, [_c('td', [_vm._v("\n              Save Data Flows "), _c('i', {
    staticClass: "fas fa-info-circle text-secondary",
    staticStyle: {
      "font-size": "1em",
      "cursor": "pointer"
    },
    on: {
      "click": function click($event) {
        return _vm.info('Save Data Flows');
      }
    }
  })]), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1)]), _c('tr', [_c('td', [_vm._v("\n              GIT Integration "), _c('i', {
    staticClass: "fas fa-info-circle text-secondary",
    staticStyle: {
      "font-size": "1em",
      "cursor": "pointer"
    },
    on: {
      "click": function click($event) {
        return _vm.info('GIT Integration');
      }
    }
  })]), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1)]), _c('tr', {
    staticStyle: {
      "background-color": "rgb(244, 246, 247) !important"
    }
  }, [_c('td', [_vm._v("\n              Generate Code "), _c('i', {
    staticClass: "fas fa-info-circle text-secondary",
    staticStyle: {
      "font-size": "1em",
      "cursor": "pointer"
    },
    on: {
      "click": function click($event) {
        return _vm.info('Generate Code');
      }
    }
  })]), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1)]), _c('tr', [_c('td', [_vm._v("\n              REST API "), _c('i', {
    staticClass: "fas fa-info-circle text-secondary",
    staticStyle: {
      "font-size": "1em",
      "cursor": "pointer"
    },
    on: {
      "click": function click($event) {
        return _vm.info('REST API');
      }
    }
  })]), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1)]), _c('tr', {
    staticStyle: {
      "background-color": "rgb(244, 246, 247) !important"
    }
  }, [_c('td', [_vm._v("\n              AI Assistant "), _c('i', {
    staticClass: "fas fa-info-circle text-secondary",
    staticStyle: {
      "font-size": "1em",
      "cursor": "pointer"
    },
    on: {
      "click": function click($event) {
        return _vm.info('AI Assistant');
      }
    }
  })]), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1)]), _c('tr', [_c('td', [_vm._v("\n              Script Library "), _c('i', {
    staticClass: "fas fa-info-circle text-secondary",
    staticStyle: {
      "font-size": "1em",
      "cursor": "pointer"
    },
    on: {
      "click": function click($event) {
        return _vm.info('Script Library');
      }
    }
  })]), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1)]), _c('tr', {
    staticStyle: {
      "background-color": "rgb(244, 246, 247) !important"
    }
  }, [_c('td', [_vm._v("\n              Patterns "), _c('i', {
    staticClass: "fas fa-info-circle text-secondary",
    staticStyle: {
      "font-size": "1em",
      "cursor": "pointer"
    },
    on: {
      "click": function click($event) {
        return _vm.info('Patterns');
      }
    }
  })]), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1)]), _c('tr', [_c('td', [_vm._v("\n              Secure Processors "), _c('i', {
    staticClass: "fas fa-info-circle text-secondary",
    staticStyle: {
      "font-size": "1em",
      "cursor": "pointer"
    },
    on: {
      "click": function click($event) {
        return _vm.info('Secure Processors');
      }
    }
  })]), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1)]), _c('tr', {
    staticStyle: {
      "background-color": "rgb(244, 246, 247) !important"
    }
  }, [_c('td', [_vm._v("\n              Hosted Services "), _c('i', {
    staticClass: "fas fa-info-circle text-secondary",
    staticStyle: {
      "font-size": "1em",
      "cursor": "pointer"
    },
    on: {
      "click": function click($event) {
        return _vm.info('Hosted Services');
      }
    }
  })]), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1)]), _c('tr', [_c('td', [_vm._v("\n              Transactional "), _c('i', {
    staticClass: "fas fa-info-circle text-secondary",
    staticStyle: {
      "font-size": "1em",
      "cursor": "pointer"
    },
    on: {
      "click": function click($event) {
        return _vm.info('Transactional');
      }
    }
  })]), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1)]), _c('tr', {
    staticStyle: {
      "background-color": "rgb(244, 246, 247) !important"
    }
  }, [_c('td', [_vm._v("\n              Co-Development "), _c('i', {
    staticClass: "fas fa-info-circle text-secondary",
    staticStyle: {
      "font-size": "1em",
      "cursor": "pointer"
    },
    on: {
      "click": function click($event) {
        return _vm.info('Co-Development');
      }
    }
  })]), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1)]), _c('tr', [_c('td', [_vm._v("\n              Streaming "), _c('i', {
    staticClass: "fas fa-info-circle text-secondary",
    staticStyle: {
      "font-size": "1em",
      "cursor": "pointer"
    },
    on: {
      "click": function click($event) {
        return _vm.info('Streaming');
      }
    }
  })]), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1)]), _c('tr', {
    staticStyle: {
      "background-color": "rgb(244, 246, 247) !important"
    }
  }, [_c('td', [_vm._v("\n              CLI "), _c('i', {
    staticClass: "fas fa-info-circle text-secondary",
    staticStyle: {
      "font-size": "1em",
      "cursor": "pointer"
    },
    on: {
      "click": function click($event) {
        return _vm.info('CLI');
      }
    }
  })]), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1)]), _c('tr', [_c('td', [_vm._v("\n              On Prem "), _c('i', {
    staticClass: "fas fa-info-circle text-secondary",
    staticStyle: {
      "font-size": "1em",
      "cursor": "pointer"
    },
    on: {
      "click": function click($event) {
        return _vm.info('On Prem');
      }
    }
  })]), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-close2"
    }
  })], 1), _c('td', [_c('q-icon', {
    attrs: {
      "name": "fas fa-check"
    }
  })], 1)]), _c('tr', [_c('td'), _c('td'), _c('td', [!_vm.$auth.isAuthenticated ? _c('q-btn', {
    attrs: {
      "dense": "",
      "padding": "10px 15px",
      "size": "md",
      "label": "Register"
    },
    on: {
      "click": _vm.login
    }
  }) : _vm._e()], 1), _c('td', [_vm.$auth.isAuthenticated && this.sublevel[this.$store.state.designer.subscription] < _vm.DEVELOPER ? _c('q-btn', {
    attrs: {
      "dense": "",
      "padding": "10px 15px",
      "size": "md",
      "label": "Upgrade"
    },
    on: {
      "click": function click($event) {
        return _vm.upgrade('ec_developer-USD-Monthly');
      }
    }
  }) : _vm._e(), _vm.$auth.isAuthenticated && this.$store.state.designer.subscription === 'ec_developer-USD-Monthly' ? _c('q-btn', {
    attrs: {
      "dense": "",
      "padding": "10px 15px",
      "size": "md",
      "color": "secondary",
      "label": "My Plan"
    },
    on: {
      "click": _vm.manage
    }
  }) : _vm._e()], 1), _c('td', [_vm.$auth.isAuthenticated && this.sublevel[this.$store.state.designer.subscription] < _vm.PRO ? _c('q-btn', {
    attrs: {
      "dense": "",
      "padding": "10px 15px",
      "size": "md",
      "label": "Upgrade"
    },
    on: {
      "click": function click($event) {
        return _vm.upgrade('ec_pro-USD-Monthly');
      }
    }
  }) : _vm._e(), _vm.$auth.isAuthenticated && this.$store.state.designer.subscription === 'ec_pro-USD-Monthly' ? _c('q-btn', {
    attrs: {
      "dense": "",
      "padding": "10px 15px",
      "size": "md",
      "color": "secondary",
      "label": "My Plan"
    },
    on: {
      "click": _vm.manage
    }
  }) : _vm._e()], 1), _c('td', [_vm.$auth.isAuthenticated && this.sublevel[this.$store.state.designer.subscription] < _vm.HOSTED ? _c('q-btn', {
    attrs: {
      "dense": "",
      "padding": "10px 15px",
      "size": "md",
      "label": "Contact Us"
    },
    on: {
      "click": _vm.contact
    }
  }) : _vm._e(), _vm.$auth.isAuthenticated && this.$store.state.designer.subscription === 'ec_hosted-USD-Yearly' ? _c('q-btn', {
    attrs: {
      "dense": "",
      "padding": "10px 15px",
      "size": "md",
      "color": "secondary",
      "label": "My Plan"
    },
    on: {
      "click": _vm.manage
    }
  }) : _vm._e()], 1), _c('td', [_vm.$auth.isAuthenticated ? _c('q-btn', {
    attrs: {
      "dense": "",
      "padding": "10px 15px",
      "size": "md",
      "label": "Contact Us"
    },
    on: {
      "click": _vm.contact
    }
  }) : _vm._e()], 1)])])]), _c('q-card-actions', {
    attrs: {
      "align": "left"
    }
  }, [_c('q-btn', {
    staticClass: "bg-secondary text-white",
    staticStyle: {
      "position": "absolute",
      "bottom": "0px",
      "left": "0px",
      "width": "100px"
    },
    attrs: {
      "flat": "",
      "label": "Manage",
      "color": "primary"
    },
    on: {
      "click": _vm.manage
    }
  })], 1), _c('q-card-actions', {
    attrs: {
      "align": "right"
    }
  }, [_c('q-btn', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    staticClass: "bg-secondary text-white",
    staticStyle: {
      "position": "absolute",
      "bottom": "0px",
      "right": "0px",
      "width": "100px"
    },
    attrs: {
      "flat": "",
      "label": "Close",
      "color": "primary"
    }
  })], 1)], 1)], 1), _c('q-dialog', {
    attrs: {
      "transition-show": "none",
      "persistent": ""
    },
    model: {
      value: _vm.viewQueueDialog,
      callback: function callback($$v) {
        _vm.viewQueueDialog = $$v;
      },
      expression: "viewQueueDialog"
    }
  }, [_c('q-card', {
    staticStyle: {
      "width": "70vw",
      "max-width": "70vw",
      "height": "80vh",
      "padding": "10px",
      "padding-left": "30px",
      "padding-top": "40px"
    }
  }, [_c('q-card-section', {
    staticClass: "bg-secondary",
    staticStyle: {
      "position": "absolute",
      "left": "0px",
      "top": "0px",
      "width": "100%",
      "height": "40px"
    }
  }, [_c('div', {
    staticStyle: {
      "font-weight": "bold",
      "font-size": "18px",
      "color": "white",
      "margin-left": "10px",
      "margin-top": "-5px",
      "margin-right": "5px"
    }
  }, [_c('q-toolbar', [_c('q-item-label', [_vm._v("Queue " + _vm._s(_vm.queuename))]), _c('q-space'), _c('q-btn', {
    staticClass: "text-primary",
    staticStyle: {
      "z-index": "10"
    },
    attrs: {
      "flat": "",
      "dense": "",
      "round": "",
      "size": "sm",
      "icon": "fas fa-close"
    },
    on: {
      "click": function click($event) {
        _vm.viewQueueDialog = false;
      }
    }
  })], 1)], 1)]), _c('q-splitter', {
    staticStyle: {
      "height": "calc(100% - 40px)"
    },
    attrs: {
      "separator-style": "background-color: #e3e8ec;height:5px",
      "horizontal": ""
    },
    scopedSlots: _vm._u([{
      key: "before",
      fn: function fn() {
        return [_c('q-table', {
          staticStyle: {
            "height": "calc(100% - 0px)",
            "width": "100%",
            "border-top-radius": "0px",
            "border-bottom-radius": "0px"
          },
          attrs: {
            "dense": "",
            "columns": _vm.queuecolumns,
            "data": _vm.queuedata,
            "row-key": "name",
            "flat": "",
            "pagination": _vm.queuePagination
          },
          scopedSlots: _vm._u([{
            key: "body",
            fn: function fn(props) {
              return [_c('q-tr', {
                key: _vm.getUuid,
                attrs: {
                  "props": props
                }
              }, [_c('q-td', {
                key: props.cols[0].name,
                attrs: {
                  "props": props
                }
              }, [_vm._v("\n                  " + _vm._s(props.cols[0].value) + "\n                ")]), _c('q-td', {
                key: props.cols[1].name,
                attrs: {
                  "props": props
                }
              }, [_c('a', {
                staticClass: "text-secondary",
                on: {
                  "click": function click($event) {
                    return _vm.showMessagePayload(props.row.payload);
                  }
                }
              }, [_vm._v("\n                    " + _vm._s(props.cols[1].value) + "\n                  ")])]), _c('q-td', {
                key: props.cols[2].name,
                attrs: {
                  "props": props
                }
              }, [_vm._v("\n                  " + _vm._s(props.cols[2].value) + "\n                ")]), _c('q-td', {
                key: props.cols[3].name,
                attrs: {
                  "props": props
                }
              }, [_vm._v("\n                  " + _vm._s(props.cols[3].value) + "\n                ")]), _c('q-td', {
                key: props.cols[4].name,
                attrs: {
                  "props": props
                }
              }, [_vm._v("\n                  " + _vm._s(props.cols[4].value) + "\n                ")]), _c('q-td', {
                key: props.cols[5].name,
                attrs: {
                  "props": props
                }
              }, [_vm._v("\n                  " + _vm._s(props.cols[5].value) + "\n                ")])], 1)];
            }
          }])
        })];
      },
      proxy: true
    }, {
      key: "after",
      fn: function fn() {
        return [_c('div', {
          staticStyle: {
            "height": "100%",
            "width": "100%"
          }
        }, [_c('editor', {
          ref: "resultEditor",
          staticStyle: {
            "font-size": "1.5em"
          },
          attrs: {
            "lang": "javascript",
            "theme": "chrome",
            "width": "100%",
            "height": "100%"
          },
          on: {
            "init": _vm.resultEditorInit
          }
        })], 1)];
      },
      proxy: true
    }]),
    model: {
      value: _vm.queueSplitter,
      callback: function callback($$v) {
        _vm.queueSplitter = $$v;
      },
      expression: "queueSplitter"
    }
  }), _c('q-card-actions', {
    attrs: {
      "align": "left"
    }
  }, [_c('q-btn', {
    staticClass: "bg-secondary text-dark",
    staticStyle: {
      "position": "absolute",
      "bottom": "0px",
      "left": "0px",
      "width": "100px"
    },
    attrs: {
      "flat": "",
      "icon": "refresh",
      "color": "primary"
    },
    on: {
      "click": _vm.refreshQueues
    }
  })], 1), _c('q-card-actions', {
    attrs: {
      "align": "right"
    }
  }, [_c('q-btn', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    staticClass: "bg-secondary text-white",
    staticStyle: {
      "position": "absolute",
      "bottom": "0px",
      "right": "0px",
      "width": "100px"
    },
    attrs: {
      "flat": "",
      "label": "Close",
      "color": "primary"
    }
  })], 1), _c('q-inner-loading', {
    staticStyle: {
      "z-index": "99999"
    },
    attrs: {
      "showing": _vm.queueloading
    }
  }, [_c('q-spinner-gears', {
    attrs: {
      "size": "50px",
      "color": "primary"
    }
  })], 1)], 1)], 1), _c('q-dialog', {
    attrs: {
      "persistent": ""
    },
    model: {
      value: _vm.viewEdgeDialog,
      callback: function callback($$v) {
        _vm.viewEdgeDialog = $$v;
      },
      expression: "viewEdgeDialog"
    }
  }, [_c('q-card', {
    staticStyle: {
      "padding": "10px",
      "padding-top": "30px",
      "min-width": "40vw",
      "height": "50%"
    }
  }, [_c('q-card-section', {
    staticClass: "bg-secondary",
    staticStyle: {
      "position": "absolute",
      "left": "0px",
      "top": "0px",
      "width": "100%",
      "height": "40px"
    }
  }, [_c('div', {
    staticStyle: {
      "font-weight": "bold",
      "font-size": "18px",
      "margin-left": "10px",
      "margin-top": "-5px",
      "margin-right": "5px",
      "color": "#fff"
    }
  }, [_c('q-toolbar', [_c('q-icon', {
    staticStyle: {
      "margin-right": "10px"
    },
    attrs: {
      "name": "fas fa-cog",
      "color": "primary"
    }
  }), _c('q-item-label', [_vm._v("Edge")]), _c('q-space'), _c('q-icon', {
    staticClass: "text-primary",
    staticStyle: {
      "z-index": "10",
      "cursor": "pointer"
    },
    attrs: {
      "name": "fas fa-close"
    },
    on: {
      "click": function click($event) {
        _vm.viewEdgeDialog = false;
      }
    }
  })], 1)], 1)]), _c('q-card-section', {
    staticClass: "row items-center",
    staticStyle: {
      "height": "120px",
      "width": "100%"
    }
  }), _c('q-card-actions', {
    attrs: {
      "align": "right"
    }
  }, [_c('q-btn', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    staticClass: "bg-secondary text-white",
    staticStyle: {
      "position": "absolute",
      "bottom": "0px",
      "right": "0px",
      "width": "100px"
    },
    attrs: {
      "flat": "",
      "label": "Close",
      "color": "primary"
    }
  })], 1)], 1)], 1), _c('q-dialog', {
    attrs: {
      "persistent": ""
    },
    model: {
      value: _vm.viewEdgeDialog,
      callback: function callback($$v) {
        _vm.viewEdgeDialog = $$v;
      },
      expression: "viewEdgeDialog"
    }
  }, [_c('q-card', {
    staticStyle: {
      "padding": "10px",
      "padding-top": "30px",
      "min-width": "40vw",
      "height": "50%"
    }
  }, [_c('q-card-section', {
    staticClass: "bg-secondary",
    staticStyle: {
      "position": "absolute",
      "left": "0px",
      "top": "0px",
      "width": "100%",
      "height": "40px"
    }
  }, [_c('div', {
    staticStyle: {
      "font-weight": "bold",
      "font-size": "18px",
      "margin-left": "10px",
      "margin-top": "-5px",
      "margin-right": "5px",
      "color": "#fff"
    }
  }, [_c('q-toolbar', [_c('q-icon', {
    staticStyle: {
      "margin-right": "10px"
    },
    attrs: {
      "name": "fas fa-cog",
      "color": "primary"
    }
  }), _c('q-item-label', [_vm._v("Edge")]), _c('q-space'), _c('q-icon', {
    staticClass: "text-primary",
    staticStyle: {
      "z-index": "10",
      "cursor": "pointer"
    },
    attrs: {
      "name": "fas fa-close"
    },
    on: {
      "click": function click($event) {
        _vm.viewEdgeDialog = false;
      }
    }
  })], 1)], 1)]), _c('q-card-section', {
    staticClass: "row items-center",
    staticStyle: {
      "height": "120px",
      "width": "100%"
    }
  }), _c('q-card-actions', {
    attrs: {
      "align": "right"
    }
  }, [_c('q-btn', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    staticClass: "bg-secondary text-white",
    staticStyle: {
      "position": "absolute",
      "bottom": "0px",
      "right": "0px",
      "width": "100px"
    },
    attrs: {
      "flat": "",
      "label": "Close",
      "color": "primary"
    }
  })], 1)], 1)], 1), _c('q-dialog', {
    attrs: {
      "persistent": ""
    },
    model: {
      value: _vm.newQueueDialog,
      callback: function callback($$v) {
        _vm.newQueueDialog = $$v;
      },
      expression: "newQueueDialog"
    }
  }, [_c('q-card', {
    staticStyle: {
      "padding": "10px",
      "padding-top": "30px",
      "width": "50%",
      "height": "50%"
    }
  }, [_c('q-card-section', {
    staticClass: "bg-secondary",
    staticStyle: {
      "position": "absolute",
      "left": "0px",
      "top": "0px",
      "width": "100%",
      "height": "40px"
    }
  }, [_c('div', {
    staticStyle: {
      "font-weight": "bold",
      "font-size": "18px",
      "color": "white",
      "margin-left": "10px",
      "margin-top": "-5px",
      "margin-right": "5px"
    }
  }, [_c('q-toolbar', [_c('q-item-label', [_vm._v("New Queue")]), _c('q-space'), _c('q-icon', {
    staticClass: "text-primary",
    attrs: {
      "name": "far fa-envelope"
    }
  })], 1)], 1)]), _c('q-card-section', {
    staticClass: "row items-center",
    staticStyle: {
      "height": "120px"
    }
  }, [_c('span', {
    staticClass: "q-ml-sm"
  }, [_vm._v("Create queue form here")])]), _c('q-card-actions', {
    attrs: {
      "align": "right"
    }
  }, [_c('q-btn', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    staticClass: "bg-accent text-dark",
    staticStyle: {
      "position": "absolute",
      "bottom": "0px",
      "right": "100px",
      "width": "100px"
    },
    attrs: {
      "flat": "",
      "label": "Cancel",
      "color": "primary"
    }
  }), _c('q-btn', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    staticClass: "bg-secondary text-white",
    staticStyle: {
      "position": "absolute",
      "bottom": "0px",
      "right": "0px",
      "width": "100px"
    },
    attrs: {
      "flat": "",
      "label": "Create",
      "color": "primary"
    },
    on: {
      "click": _vm.newQueue
    }
  })], 1)], 1)], 1), _c('q-dialog', {
    attrs: {
      "persistent": ""
    },
    model: {
      value: _vm.resolutiondialog,
      callback: function callback($$v) {
        _vm.resolutiondialog = $$v;
      },
      expression: "resolutiondialog"
    }
  }, [_c('q-card', {
    staticStyle: {
      "padding": "10px",
      "padding-top": "30px"
    }
  }, [_c('q-card-section', {
    staticClass: "bg-secondary",
    staticStyle: {
      "position": "absolute",
      "left": "0px",
      "top": "0px",
      "width": "100%",
      "height": "40px"
    }
  }, [_c('div', {
    staticStyle: {
      "font-weight": "bold",
      "font-size": "18px",
      "color": "white",
      "margin-left": "10px",
      "margin-top": "-5px",
      "margin-right": "5px"
    }
  }, [_c('q-toolbar', [_c('q-item-label', [_c('i', {
    staticClass: "fas fa-exclamation",
    staticStyle: {
      "margin-right": "20px"
    }
  }), _vm._v("Recommended Resolution\n            ")]), _c('q-space'), _c('q-icon', {
    staticClass: "text-primary",
    attrs: {
      "name": "fas fa-trash"
    }
  })], 1)], 1)]), _c('q-card-section', {
    staticClass: "row items-center",
    staticStyle: {
      "height": "120px"
    }
  }, [_c('span', {
    staticClass: "q-ml-sm"
  }, [_vm._v("\n          Your current monitor resolution does not meet the recommended size of 2460x1440 for best user experience.\n        ")])]), _c('q-card-actions', {
    attrs: {
      "align": "right"
    }
  }, [_c('q-btn', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    staticClass: "bg-secondary text-white",
    staticStyle: {
      "position": "absolute",
      "bottom": "0px",
      "right": "0px",
      "width": "100px"
    },
    attrs: {
      "flat": "",
      "label": "Ok",
      "color": "primary"
    },
    on: {
      "click": function click($event) {
        _vm.resolutiondialog = false;
      }
    }
  })], 1)], 1)], 1), _c('q-dialog', {
    attrs: {
      "persistent": ""
    },
    model: {
      value: _vm.betanoticedialog,
      callback: function callback($$v) {
        _vm.betanoticedialog = $$v;
      },
      expression: "betanoticedialog"
    }
  }, [_c('q-card', {
    staticStyle: {
      "padding": "10px",
      "padding-top": "30px"
    }
  }, [_c('q-card-section', {
    staticClass: "bg-secondary",
    staticStyle: {
      "padding": "0px !important",
      "position": "absolute",
      "left": "0px",
      "top": "0px",
      "width": "100%",
      "height": "40px"
    }
  }, [_c('div', {
    staticStyle: {
      "font-weight": "bold",
      "font-size": "18px",
      "margin-left": "0px",
      "margin-top": "-5px",
      "margin-right": "0px",
      "color": "#fff"
    }
  }, [_c('q-toolbar', {
    staticClass: "bar"
  }, [_c('q-space')], 1)], 1)]), _c('q-card-section', {
    staticClass: "row items-center",
    staticStyle: {
      "height": "450px"
    }
  }, [_c('span', {
    staticClass: "text-black q-ml-sm",
    staticStyle: {
      "color": "black",
      "margin-top": "30px",
      "margin-bottom": "30px"
    }
  }, [_c('p', {
    staticClass: "text-black",
    staticStyle: {
      "font-size": "20px"
    }
  }, [_vm._v("Welcome to ElasticCode Early Access! We are glad you stopped by. It is important to understand this software is currently an incomplete development pre-release. Not all features are implemented in this version. Any feedback, bugs reports, or feature requests are highly encouraged! Please submit them "), _c('a', {
    staticStyle: {
      "text-decoration": "underline",
      "color": "#6b8791"
    },
    attrs: {
      "target": "support",
      "href": "https://elasticcode.atlassian.net/servicedesk/customer/portals"
    }
  }, [_vm._v("here")])]), _c('br'), _c('hr'), _c('br'), _c('p', {
    staticClass: "text-black",
    staticStyle: {
      "font-size": "16px"
    }
  }, [_c('b', [_vm._v("NOTE")]), _vm._v(": If the app doesn't display fully on your display, trying scaling it down from your browser until it fits completely.")]), _c('br'), _c('b', [_vm._v("Recommended Settings:")]), _c('ul', {
    staticStyle: {
      "margin-left": "40px"
    }
  }, [_c('li', [_vm._v("Monitor Resolution 2560x1440 or higher resolution")]), _c('li', [_vm._v("Google Chrome")])])])]), _c('q-card-actions', {
    attrs: {
      "align": "right"
    }
  }, [_c('q-btn', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    staticClass: "bg-secondary text-white",
    staticStyle: {
      "position": "absolute",
      "bottom": "0px",
      "right": "0px",
      "width": "150px"
    },
    attrs: {
      "flat": "",
      "label": "I Understand",
      "color": "primary"
    }
  })], 1)], 1)], 1), _c('q-dialog', {
    attrs: {
      "persistent": ""
    },
    model: {
      value: _vm.confirmQueuePurge,
      callback: function callback($$v) {
        _vm.confirmQueuePurge = $$v;
      },
      expression: "confirmQueuePurge"
    }
  }, [_c('q-card', {
    staticStyle: {
      "padding": "10px",
      "padding-top": "30px"
    }
  }, [_c('q-card-section', {
    staticClass: "bg-secondary",
    staticStyle: {
      "position": "absolute",
      "left": "0px",
      "top": "0px",
      "width": "100%",
      "height": "40px"
    }
  }, [_c('div', {
    staticStyle: {
      "font-weight": "bold",
      "font-size": "18px",
      "color": "white",
      "margin-left": "10px",
      "margin-top": "-5px",
      "margin-right": "5px"
    }
  }, [_c('q-toolbar', [_c('q-item-label', [_vm._v("Purge Queue")]), _c('q-space'), _c('q-icon', {
    staticClass: "text-primary",
    attrs: {
      "name": "fas fa-trash"
    }
  })], 1)], 1)]), _c('q-card-section', {
    staticClass: "row items-center",
    staticStyle: {
      "height": "120px"
    }
  }, [_c('q-avatar', {
    attrs: {
      "icon": "fas fa-exclamation",
      "color": "primary",
      "text-color": "white"
    }
  }), _c('span', {
    staticClass: "q-ml-sm"
  }, [_vm._v("\n          Are you sure you want to purge queue " + _vm._s(_vm.purgeQueueName) + "?\n        ")])], 1), _c('q-card-actions', {
    attrs: {
      "align": "right"
    }
  }, [_c('q-btn', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    staticClass: "bg-accent text-dark",
    staticStyle: {
      "position": "absolute",
      "bottom": "0px",
      "right": "100px",
      "width": "100px"
    },
    attrs: {
      "flat": "",
      "label": "Cancel",
      "color": "primary"
    }
  }), _c('q-btn', {
    directives: [{
      name: "close-popup",
      rawName: "v-close-popup"
    }],
    staticClass: "bg-secondary text-white",
    staticStyle: {
      "position": "absolute",
      "bottom": "0px",
      "right": "0px",
      "width": "100px"
    },
    attrs: {
      "flat": "",
      "label": "Clear",
      "color": "primary"
    },
    on: {
      "click": function click($event) {
        return _vm.purgeQueue(_vm.purgeQueueName);
      }
    }
  })], 1)], 1)], 1)], 1);
};

var staticRenderFns = [];

// CONCATENATED MODULE: ./src/layouts/MainLayout.vue?vue&type=template&id=47e28f36&

// EXTERNAL MODULE: ./node_modules/@quasar/app/lib/webpack/loader.transform-quasar-imports.js!./node_modules/babel-loader/lib??ref--2-0!./node_modules/@quasar/app/lib/webpack/loader.auto-import-client.js?kebab!./node_modules/vue-loader/lib??vue-loader-options!./src/layouts/MainLayout.vue?vue&type=script&lang=js&
var MainLayoutvue_type_script_lang_js_ = __webpack_require__("49de");

// CONCATENATED MODULE: ./src/layouts/MainLayout.vue?vue&type=script&lang=js&
 /* harmony default export */ var layouts_MainLayoutvue_type_script_lang_js_ = (MainLayoutvue_type_script_lang_js_["a" /* default */]); 
// EXTERNAL MODULE: ./src/layouts/MainLayout.vue?vue&type=style&index=0&id=47e28f36&prod&lang=css&
var MainLayoutvue_type_style_index_0_id_47e28f36_prod_lang_css_ = __webpack_require__("81fa");

// EXTERNAL MODULE: ./node_modules/vue-loader/lib/runtime/componentNormalizer.js
var componentNormalizer = __webpack_require__("2877");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/layout/QLayout.js
var QLayout = __webpack_require__("4d5a");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/inner-loading/QInnerLoading.js
var QInnerLoading = __webpack_require__("74f7");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/spinner/QSpinnerGears.js
var QSpinnerGears = __webpack_require__("cf57");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/header/QHeader.js
var QHeader = __webpack_require__("e359");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/toolbar/QToolbar.js
var QToolbar = __webpack_require__("65c6");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/btn/QBtn.js
var QBtn = __webpack_require__("9c40");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/tooltip/QTooltip.js
var QTooltip = __webpack_require__("05c0");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/separator/QSeparator.js
var QSeparator = __webpack_require__("eb85");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/btn-toggle/QBtnToggle.js
var QBtnToggle = __webpack_require__("6a67");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/space/QSpace.js
var QSpace = __webpack_require__("2c91");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/input/QInput.js + 2 modules
var QInput = __webpack_require__("27f9");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/icon/QIcon.js
var QIcon = __webpack_require__("0016");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/splitter/QSplitter.js
var QSplitter = __webpack_require__("8562");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/tab-panels/QTabPanels.js
var QTabPanels = __webpack_require__("adad");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/tab-panels/QTabPanel.js
var QTabPanel = __webpack_require__("823b");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/tabs/QTabs.js
var QTabs = __webpack_require__("429b");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/tabs/QTab.js
var QTab = __webpack_require__("7460");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/scroll-area/QScrollArea.js
var QScrollArea = __webpack_require__("4983");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/table/QTable.js + 18 modules
var QTable = __webpack_require__("eaac");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/table/QTr.js
var QTr = __webpack_require__("bd08");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/table/QTd.js
var QTd = __webpack_require__("db86");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/footer/QFooter.js
var QFooter = __webpack_require__("7ff0");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/item/QItemLabel.js
var QItemLabel = __webpack_require__("0170");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/drawer/QDrawer.js
var QDrawer = __webpack_require__("9404");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/item/QList.js
var QList = __webpack_require__("1c1c");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/item/QItem.js
var QItem = __webpack_require__("66e5");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/item/QItemSection.js
var QItemSection = __webpack_require__("4074");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/dialog/QDialog.js
var QDialog = __webpack_require__("24e8");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/card/QCard.js
var QCard = __webpack_require__("f09f");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/card/QCardSection.js
var QCardSection = __webpack_require__("a370");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/card/QCardActions.js
var QCardActions = __webpack_require__("4b7e");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/avatar/QAvatar.js
var QAvatar = __webpack_require__("cb32");

// EXTERNAL MODULE: ./node_modules/quasar/src/directives/ClosePopup.js
var ClosePopup = __webpack_require__("7f67");

// EXTERNAL MODULE: ./node_modules/@quasar/app/lib/webpack/runtime.auto-import.js
var runtime_auto_import = __webpack_require__("eebe");
var runtime_auto_import_default = /*#__PURE__*/__webpack_require__.n(runtime_auto_import);

// CONCATENATED MODULE: ./src/layouts/MainLayout.vue






/* normalize component */

var component = Object(componentNormalizer["a" /* default */])(
  layouts_MainLayoutvue_type_script_lang_js_,
  render,
  staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* harmony default export */ var MainLayout = __webpack_exports__["default"] = (component.exports);

































runtime_auto_import_default()(component, 'components', {QLayout: QLayout["a" /* default */],QInnerLoading: QInnerLoading["a" /* default */],QSpinnerGears: QSpinnerGears["a" /* default */],QHeader: QHeader["a" /* default */],QToolbar: QToolbar["a" /* default */],QBtn: QBtn["a" /* default */],QTooltip: QTooltip["a" /* default */],QSeparator: QSeparator["a" /* default */],QBtnToggle: QBtnToggle["a" /* default */],QSpace: QSpace["a" /* default */],QInput: QInput["a" /* default */],QIcon: QIcon["a" /* default */],QSplitter: QSplitter["a" /* default */],QTabPanels: QTabPanels["a" /* default */],QTabPanel: QTabPanel["a" /* default */],QTabs: QTabs["a" /* default */],QTab: QTab["a" /* default */],QScrollArea: QScrollArea["a" /* default */],QTable: QTable["a" /* default */],QTr: QTr["a" /* default */],QTd: QTd["a" /* default */],QFooter: QFooter["a" /* default */],QItemLabel: QItemLabel["a" /* default */],QDrawer: QDrawer["a" /* default */],QList: QList["a" /* default */],QItem: QItem["a" /* default */],QItemSection: QItemSection["a" /* default */],QDialog: QDialog["a" /* default */],QCard: QCard["a" /* default */],QCardSection: QCardSection["a" /* default */],QCardActions: QCardActions["a" /* default */],QAvatar: QAvatar["a" /* default */]});runtime_auto_import_default()(component, 'directives', {ClosePopup: ClosePopup["a" /* default */]});


/***/ }),

/***/ "81fa":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _node_modules_mini_css_extract_plugin_dist_loader_js_ref_7_oneOf_2_0_node_modules_css_loader_dist_cjs_js_ref_7_oneOf_2_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_src_index_js_ref_7_oneOf_2_2_node_modules_quasar_app_lib_webpack_loader_auto_import_client_js_kebab_node_modules_vue_loader_lib_index_js_vue_loader_options_MainLayout_vue_vue_type_style_index_0_id_47e28f36_prod_lang_css___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__("3792");
/* harmony import */ var _node_modules_mini_css_extract_plugin_dist_loader_js_ref_7_oneOf_2_0_node_modules_css_loader_dist_cjs_js_ref_7_oneOf_2_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_src_index_js_ref_7_oneOf_2_2_node_modules_quasar_app_lib_webpack_loader_auto_import_client_js_kebab_node_modules_vue_loader_lib_index_js_vue_loader_options_MainLayout_vue_vue_type_style_index_0_id_47e28f36_prod_lang_css___WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_mini_css_extract_plugin_dist_loader_js_ref_7_oneOf_2_0_node_modules_css_loader_dist_cjs_js_ref_7_oneOf_2_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_src_index_js_ref_7_oneOf_2_2_node_modules_quasar_app_lib_webpack_loader_auto_import_client_js_kebab_node_modules_vue_loader_lib_index_js_vue_loader_options_MainLayout_vue_vue_type_style_index_0_id_47e28f36_prod_lang_css___WEBPACK_IMPORTED_MODULE_0__);
/* unused harmony reexport * */


/***/ }),

/***/ "b213":
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__.p + "img/fontawesome-webfont.c1e38fd9.svg";

/***/ }),

/***/ "c37a":
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__.p + "fonts/fontawesome-webfont.f691f37e.woff";

/***/ }),

/***/ "c37e":
/***/ (function(module, exports, __webpack_require__) {

// extracted by mini-css-extract-plugin

/***/ }),

/***/ "ce28":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony import */ var _node_modules_mini_css_extract_plugin_dist_loader_js_ref_7_oneOf_2_0_node_modules_css_loader_dist_cjs_js_ref_7_oneOf_2_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_src_index_js_ref_7_oneOf_2_2_node_modules_quasar_app_lib_webpack_loader_auto_import_client_js_kebab_node_modules_vue_loader_lib_index_js_vue_loader_options_ModelToolPalette_vue_vue_type_style_index_0_id_9e3a0e0a_prod_scoped_true_lang_css___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__("d558");
/* harmony import */ var _node_modules_mini_css_extract_plugin_dist_loader_js_ref_7_oneOf_2_0_node_modules_css_loader_dist_cjs_js_ref_7_oneOf_2_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_src_index_js_ref_7_oneOf_2_2_node_modules_quasar_app_lib_webpack_loader_auto_import_client_js_kebab_node_modules_vue_loader_lib_index_js_vue_loader_options_ModelToolPalette_vue_vue_type_style_index_0_id_9e3a0e0a_prod_scoped_true_lang_css___WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_mini_css_extract_plugin_dist_loader_js_ref_7_oneOf_2_0_node_modules_css_loader_dist_cjs_js_ref_7_oneOf_2_1_node_modules_vue_loader_lib_loaders_stylePostLoader_js_node_modules_postcss_loader_src_index_js_ref_7_oneOf_2_2_node_modules_quasar_app_lib_webpack_loader_auto_import_client_js_kebab_node_modules_vue_loader_lib_index_js_vue_loader_options_ModelToolPalette_vue_vue_type_style_index_0_id_9e3a0e0a_prod_scoped_true_lang_css___WEBPACK_IMPORTED_MODULE_0__);
/* unused harmony reexport * */


/***/ }),

/***/ "d558":
/***/ (function(module, exports, __webpack_require__) {

// extracted by mini-css-extract-plugin

/***/ }),

/***/ "d9c5":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";

// EXTERNAL MODULE: ./node_modules/core-js/modules/es.function.name.js
var es_function_name = __webpack_require__("b0c0");

// EXTERNAL MODULE: ./node_modules/core-js/modules/es.symbol.js
var es_symbol = __webpack_require__("a4d3");

// EXTERNAL MODULE: ./node_modules/core-js/modules/es.symbol.description.js
var es_symbol_description = __webpack_require__("e01a");

// CONCATENATED MODULE: ./node_modules/@quasar/app/lib/webpack/loader.transform-quasar-imports.js!./node_modules/babel-loader/lib??ref--2-0!./node_modules/vue-loader/lib/loaders/templateLoader.js??ref--7!./node_modules/@quasar/app/lib/webpack/loader.auto-import-client.js?kebab!./node_modules/vue-loader/lib??vue-loader-options!./src/components/Library.vue?vue&type=template&id=3e6a54f4&




var render = function render() {
  var _vm = this,
      _c = _vm._self._c;

  return _c('div', {
    staticStyle: {
      "height": "fit"
    }
  }, [_c('div', {
    staticClass: "bg-accent text-secondary",
    staticStyle: {
      "border-bottom": "1px solid #abbcc3",
      "overflow": "hidden"
    }
  }, [!_vm.$auth.isAuthenticated ? _c('q-inner-loading', {
    staticStyle: {
      "z-index": "9999"
    },
    attrs: {
      "showing": true
    }
  }, [_c('q-item-label', [_vm._v("Not Logged In")])], 1) : _vm._e(), _c('q-breadcrumbs', [_c('div', {
    staticStyle: {
      "margin-left": "20px"
    }
  }, [_c('q-toolbar', {
    staticStyle: {
      "padding": "0px"
    }
  }, [_vm._l(_vm.paths, function (path) {
    return path.icon && _vm.showpath ? _c('q-breadcrumbs-el', {
      key: path.id,
      staticClass: "breadcrumb",
      attrs: {
        "icon": path.icon,
        "label": path.text
      },
      on: {
        "click": function click($event) {
          return _vm.breadcrumbClick(path);
        }
      }
    }) : _vm._e();
  }), _vm._l(_vm.paths, function (path) {
    return !path.icon && _vm.showpath ? _c('q-breadcrumbs-el', {
      key: path.id,
      staticClass: "breadcrumb",
      staticStyle: {
        "margin-left": "10px"
      },
      attrs: {
        "label": '/' + path.text
      },
      on: {
        "click": function click($event) {
          return _vm.breadcrumbClick(path);
        }
      }
    }) : _vm._e();
  })], 2)], 1), _vm.showaddfolder ? _c('div', {
    staticStyle: {
      "margin-left": "0px",
      "margin-top": "-16px",
      "margin-bottom": "0px"
    }
  }, [_c('q-toolbar', {
    staticStyle: {
      "margin-top": "20px",
      "margin-bottom": "0px"
    }
  }, [_c('q-input', {
    staticClass: "bg-white text-primary",
    attrs: {
      "dense": "",
      "flat": ""
    },
    model: {
      value: _vm.newfolder,
      callback: function callback($$v) {
        _vm.newfolder = $$v;
      },
      expression: "newfolder"
    }
  }), _c('q-btn', {
    attrs: {
      "dense": "",
      "flat": "",
      "label": "Add",
      "disabled": _vm.newfolder.length === 0
    },
    on: {
      "click": _vm.addFolder
    }
  }), _c('q-space'), _c('q-btn', {
    attrs: {
      "dense": "",
      "flat": "",
      "size": "xs",
      "icon": "cancel"
    },
    on: {
      "click": function click($event) {
        _vm.showaddfolder = false;
        _vm.showpath = true;
      }
    }
  })], 1)], 1) : _vm._e(), _c('q-space'), _c('q-btn', {
    staticClass: "q-mr-xs",
    staticStyle: {
      "padding": "0"
    },
    attrs: {
      "flat": "",
      "round": "",
      "icon": "fas fa-sync-alt",
      "size": "xs",
      "color": "primary"
    },
    on: {
      "click": _vm.synchronize
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-class": "",
      "content-style": "font-size: 16px",
      "offset": [10, 10]
    }
  }, [_vm._v("\n          Refresh\n        ")])], 1), _c('q-btn', {
    staticClass: "q-mr-xs",
    staticStyle: {
      "padding": "0"
    },
    attrs: {
      "flat": "",
      "round": "",
      "icon": "fas fa-plus",
      "size": "xs",
      "color": "primary"
    },
    on: {
      "click": function click($event) {
        _vm.showpath = false;
        _vm.showaddfolder = true;
      }
    }
  }, [_c('q-tooltip', {
    attrs: {
      "content-class": "",
      "content-style": "font-size: 16px",
      "offset": [10, 10]
    }
  }, [_vm._v("\n          Add Folder\n        ")])], 1)], 1)], 1), _c('q-scroll-area', {
    staticStyle: {
      "height": "calc(100vh - 180px)",
      "width": "100%"
    }
  }, [_c('q-list', {
    attrs: {
      "separator": ""
    }
  }, _vm._l(_vm.items, function (item) {
    return _c('q-item', {
      key: item.id,
      staticClass: "dragrow text-primary",
      attrs: {
        "id": 'row' + item.id
      }
    }, [_c('q-item-section', {
      attrs: {
        "avatar": ""
      }
    }, [item.type === 'folder' ? _c('q-icon', {
      staticClass: "text-primary",
      attrs: {
        "name": item.icon,
        "size": "md"
      }
    }) : _vm._e(), item.type !== 'folder' ? _c('q-icon', {
      staticClass: "text-secondary",
      attrs: {
        "name": item.icon,
        "size": "lg"
      }
    }) : _vm._e()], 1), _c('q-item-section', {
      staticClass: "absolute",
      staticStyle: {
        "margin-left": "50px",
        "width": "100%"
      }
    }, [_c('a', {
      staticClass: "text-secondary",
      staticStyle: {
        "z-index": "99999",
        "cursor": "pointer",
        "width": "100%",
        "min-width": "250px",
        "font-size": "1.3em"
      },
      on: {
        "click": function click($event) {
          return _vm.selectFileOrFolder(item);
        }
      }
    }, [_vm._v(_vm._s(item.filename ? item.filename : item.name))]), _c('span', {
      staticClass: "text-caption text-secondary"
    }, [_vm._v(_vm._s(item.description ? item.description : "rwxr--r--"))])]), _c('q-space'), _c('q-toolbar', [_c('q-space'), _c('q-btn', {
      class: _vm.darkStyle,
      staticStyle: {
        "font-size": ".8em"
      },
      attrs: {
        "flat": "",
        "dense": "",
        "rounded": "",
        "icon": "fas fa-thumbtack"
      }
    }, [_c('q-tooltip', {
      attrs: {
        "content-style": "font-size: 16px",
        "offset": [10, 10]
      }
    }, [_vm._v("\n              Pin\n            ")])], 1), _c('q-btn', {
      class: _vm.darkStyle,
      attrs: {
        "flat": "",
        "dense": "",
        "rounded": "",
        "icon": "edit"
      }
    }, [_c('q-tooltip', {
      attrs: {
        "content-style": "font-size: 16px",
        "offset": [10, 10]
      }
    }, [_vm._v("\n              Rename\n            ")])], 1), _c('q-btn', {
      class: _vm.darkStyle,
      attrs: {
        "flat": "",
        "dense": "",
        "rounded": "",
        "icon": "delete"
      },
      on: {
        "click": function click($event) {
          return _vm.showDeleteObject(item);
        }
      }
    }, [_c('q-tooltip', {
      attrs: {
        "content-style": "font-size: 16px",
        "offset": [10, 10]
      }
    }, [_vm._v("\n              Delete\n            ")])], 1)], 1)], 1);
  }), 1)], 1), _c('q-inner-loading', {
    attrs: {
      "showing": _vm.loading
    }
  }, [_c('q-spinner-gears', {
    attrs: {
      "size": "50px",
      "color": "primary"
    }
  })], 1)], 1);
};

var staticRenderFns = [];

// CONCATENATED MODULE: ./src/components/Library.vue?vue&type=template&id=3e6a54f4&

// EXTERNAL MODULE: ./node_modules/@babel/runtime/helpers/asyncToGenerator.js
var asyncToGenerator = __webpack_require__("c973");
var asyncToGenerator_default = /*#__PURE__*/__webpack_require__.n(asyncToGenerator);

// EXTERNAL MODULE: ./node_modules/regenerator-runtime/runtime.js
var runtime = __webpack_require__("96cf");

// EXTERNAL MODULE: ./node_modules/core-js/modules/es.regexp.exec.js
var es_regexp_exec = __webpack_require__("ac1f");

// EXTERNAL MODULE: ./node_modules/core-js/modules/es.string.split.js
var es_string_split = __webpack_require__("1276");

// EXTERNAL MODULE: ./node_modules/core-js/modules/web.dom-collections.for-each.js
var web_dom_collections_for_each = __webpack_require__("159b");

// EXTERNAL MODULE: ./src/components/util/DataService.ts
var DataService = __webpack_require__("7c43");

// CONCATENATED MODULE: ./node_modules/@quasar/app/lib/webpack/loader.transform-quasar-imports.js!./node_modules/babel-loader/lib??ref--2-0!./node_modules/@quasar/app/lib/webpack/loader.auto-import-client.js?kebab!./node_modules/vue-loader/lib??vue-loader-options!./src/components/Library.vue?vue&type=script&lang=js&










var dd = __webpack_require__("4d3a");

/* harmony default export */ var Libraryvue_type_script_lang_js_ = ({
  components: {},
  computed: {},
  props: ['objecttype', 'collection', 'icon', 'toolbar'],
  mounted: function mounted() {
    if (this.$auth.isAuthenticated) {
      this.synchronize();
      this.$root.$on('update.' + this.collection, this.synchronize);
      window.root.$on('add.library', this.addToLibrary);
    }
  },
  watch: {
    '$store.state.designer.token': function $storeStateDesignerToken(val) {
      if (val) {
        this.synchronize();
        this.$root.$on('update.' + this.collection, this.synchronize);
        window.root.$on('add.library', this.addToLibrary);
      } else {
        this.$root.off('update.' + this.collection, this.synchronize);
        window.root.off('add.library');
      }
    }
  },
  methods: {
    addToLibrary: function addToLibrary(obj) {
      var _this = this;

      return asyncToGenerator_default()( /*#__PURE__*/regeneratorRuntime.mark(function _callee() {
        var me;
        return regeneratorRuntime.wrap(function _callee$(_context) {
          while (1) {
            switch (_context.prev = _context.next) {
              case 0:
                console.log('ADD LIBRARY', obj);
                me = _this;
                _context.next = 4;
                return DataService["a" /* default */].newFile('library', _this.foldername, obj.id, obj.name, false, 'template', obj.icon, JSON.stringify(obj), _this.$store.state.designer.token).then(function (response) {
                  me.synchronize();
                  me.$q.notify({
                    color: 'secondary',
                    timeout: 2000,
                    position: 'top',
                    message: 'Add to library succeeded!',
                    icon: 'save'
                  });
                }).catch(function (_ref) {
                  var response = _ref.response;
                  console.log(response);
                  me.loading = false;
                  me.saveas = false;

                  if (response.status === 409) {
                    console.log('File name exists ', response.data.id);
                    me.overwriteflow = true;
                    me.flowuuid = response.data.id;
                    me.notifyMessage('dark', 'error', 'The file name already exists.');
                  }
                });

              case 4:
              case "end":
                return _context.stop();
            }
          }
        }, _callee);
      }))();
    },
    addFolder: function addFolder() {
      var me = this;
      this.showaddfolder = false;
      this.showpath = true;
      this.loading = true;
      console.log('FOLDERNAME', this.foldername + '/' + this.newfolder);
      DataService["a" /* default */].newFolder('library', this.foldername + '/' + this.newfolder, this.$store.state.designer.token).then(function () {
        me.synchronize();
      }).catch(function () {
        me.loading = false;
        me.notifyMessage('dark', 'error', 'There was an error creating the folder');
      });
    },
    breadcrumbClick: function breadcrumbClick(crumb) {
      console.log('CRUMB:', crumb.path);
      var path = crumb.path;

      if (crumb.path[0] === '/') {
        path = path.substr(1);
      }

      var p = path.split('/');
      var paths = this.paths = [];
      var _path = '';
      p.forEach(function (path) {
        _path += '/' + path;
        paths.push({
          text: path,
          path: _path,
          id: paths.length
        });
      });
      paths[0].icon = 'home';
      this.navigate(path);
    },
    navigate: function navigate(folder) {
      this.foldername = folder;
      this.synchronize();
    },
    selectFileOrFolder: function selectFileOrFolder(item) {
      console.log('selectFileOrFolder ', item.id, item, this.objecttype);
      item._id = item.id;
      this.flowuuid = item.id;

      if (item.type === 'folder') {
        this.foldername = item.path + '/' + item.filename;
        var p = this.foldername.split('/');
        var paths = this.paths = [];
        var _path = '';
        p.forEach(function (path) {
          _path += '/' + path;
          paths.push({
            text: path,
            path: _path,
            id: paths.length
          });
        });
        paths[0].icon = 'home';
        this.paths = paths;
        console.log('PATHS:', this.paths);
        this.synchronize();
      }
    },
    notifyMessage: function notifyMessage(color, icon, message) {
      this.$q.notify({
        color: color,
        timeout: 2000,
        position: 'top',
        message: message,
        icon: icon
      });
    },
    synchronize: function synchronize() {
      this.loading = true;
      var me = this;
      var token = this.$store.state.designer.token;

      if (!this.$auth.isAuthenticated && token || !token || token === 'none') {
        console.log('Library: Not yet authenticated, returning');
        return;
      }

      try {
        console.log('Library: ', this.$auth.isAuthenticated, token);
        var files = DataService["a" /* default */].getFiles(this.collection, this.foldername, this.$store.state.designer.token);
        files.then(function (result) {
          setTimeout(function () {
            me.loading = false;
          }, 100);
          result = result.data;
          result.forEach(function (entry) {
            if (entry.code.length > 0) {
              var code = JSON.parse(entry.code);
              entry.description = code.description;
            }
          });
          me.items = result;
          setTimeout(function () {
            var _loop = function _loop(i) {
              if (result[i].type === 'folder') return "continue"; // var el = document.querySelector("[id='" + result[i]._id + "']");

              var el = document.querySelector("[id='row" + result[i].id + "']");

              if (el) {
                el.data = result[i];
                el.data.type = 'template';
                var draghandle = dd.drag(el, {
                  image: true // default drag image

                });
                if (!result[i].columns) result[i].columns = [];
                draghandle.on('start', function (setData, e) {
                  console.log('drag:start:', el, e);
                  var code = JSON.parse(result[i].code);
                  setData('object', JSON.stringify({
                    node: code
                  }));
                });
              }
            };

            for (var i = 0; i < result.length; i++) {
              var _ret = _loop(i);

              if (_ret === "continue") continue;
            }
          }, 1000);
        }).catch(function (error) {
          console.log(error);
          me.loading = false;
          me.notifyMessage('dark', 'error', 'There was an error synchronizing this view.');
        });
      } catch (error) {
        me.loading = false;
        me.notifyMessage('dark', 'error', 'There was an error synchronizing this view.');
      }
    }
  },
  data: function data() {
    return {
      showpath: true,
      showaddfolder: false,
      columns: [{
        name: 'type',
        align: 'left',
        label: 'Type',
        field: 'type'
      }, {
        name: 'name',
        required: true,
        label: 'Name',
        align: 'left',
        field: 'name',
        sortable: true
      }, {
        name: 'action',
        align: 'center',
        label: 'Action',
        icon: 'trashcan',
        sortable: true
      }],
      folderprompt: false,
      foldername: 'Library',
      newfolder: '',
      loading: false,
      deleteobject: false,
      flowname: null,
      overwriteflow: false,
      deleteobjectname: null,
      deleteobjectid: null,
      deleteobjecttype: null,
      items: [],
      paths: [{
        text: 'Library',
        icon: 'fas fa-book',
        id: 0
      }]
    };
  }
});
// CONCATENATED MODULE: ./src/components/Library.vue?vue&type=script&lang=js&
 /* harmony default export */ var components_Libraryvue_type_script_lang_js_ = (Libraryvue_type_script_lang_js_); 
// EXTERNAL MODULE: ./src/components/Library.vue?vue&type=style&index=0&id=3e6a54f4&prod&lang=css&
var Libraryvue_type_style_index_0_id_3e6a54f4_prod_lang_css_ = __webpack_require__("5d52");

// EXTERNAL MODULE: ./node_modules/vue-loader/lib/runtime/componentNormalizer.js
var componentNormalizer = __webpack_require__("2877");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/inner-loading/QInnerLoading.js
var QInnerLoading = __webpack_require__("74f7");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/item/QItemLabel.js
var QItemLabel = __webpack_require__("0170");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/breadcrumbs/QBreadcrumbs.js
var QBreadcrumbs = __webpack_require__("ead5");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/toolbar/QToolbar.js
var QToolbar = __webpack_require__("65c6");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/breadcrumbs/QBreadcrumbsEl.js
var QBreadcrumbsEl = __webpack_require__("079e");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/input/QInput.js + 2 modules
var QInput = __webpack_require__("27f9");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/btn/QBtn.js
var QBtn = __webpack_require__("9c40");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/space/QSpace.js
var QSpace = __webpack_require__("2c91");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/tooltip/QTooltip.js
var QTooltip = __webpack_require__("05c0");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/scroll-area/QScrollArea.js
var QScrollArea = __webpack_require__("4983");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/item/QList.js
var QList = __webpack_require__("1c1c");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/item/QItem.js
var QItem = __webpack_require__("66e5");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/item/QItemSection.js
var QItemSection = __webpack_require__("4074");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/icon/QIcon.js
var QIcon = __webpack_require__("0016");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/spinner/QSpinnerGears.js
var QSpinnerGears = __webpack_require__("cf57");

// EXTERNAL MODULE: ./node_modules/@quasar/app/lib/webpack/runtime.auto-import.js
var runtime_auto_import = __webpack_require__("eebe");
var runtime_auto_import_default = /*#__PURE__*/__webpack_require__.n(runtime_auto_import);

// CONCATENATED MODULE: ./src/components/Library.vue






/* normalize component */

var component = Object(componentNormalizer["a" /* default */])(
  components_Libraryvue_type_script_lang_js_,
  render,
  staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* harmony default export */ var Library = __webpack_exports__["a"] = (component.exports);
















runtime_auto_import_default()(component, 'components', {QInnerLoading: QInnerLoading["a" /* default */],QItemLabel: QItemLabel["a" /* default */],QBreadcrumbs: QBreadcrumbs["a" /* default */],QToolbar: QToolbar["a" /* default */],QBreadcrumbsEl: QBreadcrumbsEl["a" /* default */],QInput: QInput["a" /* default */],QBtn: QBtn["a" /* default */],QSpace: QSpace["a" /* default */],QTooltip: QTooltip["a" /* default */],QScrollArea: QScrollArea["a" /* default */],QList: QList["a" /* default */],QItem: QItem["a" /* default */],QItemSection: QItemSection["a" /* default */],QIcon: QIcon["a" /* default */],QSpinnerGears: QSpinnerGears["a" /* default */]});


/***/ }),

/***/ "e44f":
/***/ (function(module, exports) {

module.exports = "data:font/woff2;base64,d09GMgABAAAAABVMAA0AAAAAK6AAABT0AAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP0ZGVE0cGh4GVgCCYhEICskYvUYLQgABNgIkA0gEIAWDDweDFBukJCMR9nrVcouo0swF/HMhm2NY3TqVOScoKyL7jp+t4rIjtPQR78/z2/xzX8B79APeA5tQcWGvjDkUG6NXGPwpuLUYqF8WJasoXbsMV61zP+ePXv7yyGY6IzDMPBgERoKVzoCsZrfdbXV3kj7hF5v4yYiJoE24TZkS+EdwgzHtm3/penWpPTAQhKn2uApg12nf3n7r7Wp1+EkynkKSUWfUmYCquEoJrAuRfphLACqToklRpqnTpyxtY9jCN+dychxYvYZWrzF4pQHaQ0l25qGmLm2cHRDgi/vFNvYDAOTDq7/vOOkTOy1vjcBqUZQIhxhzWhz8AAFB5bER3o0WAwkUNhc7AwDz6Qr0BsIR1mwMicOfqyEZtCjHllQOxm7oduOWnhoYgZfAwk8eFY6VdymxSATdCDB6IqAAs+8durnu/t1Dut09AbqerIjwU9W4qlvVpVoFCP5shHhT0f8J52KO/z0I/o1GPXef1BCj1nIm8Q4A6YnhC5pp4J3x+CAFiYXErhCNdBsmBhxIQhACQjMCjI3Ft7KskqMMgUqZTBtEESrlMNnWK0jJJ8QgTznDL3hwHw9J+4lEElFvGesnl8uIBPEhl5FRsthXIqFF1QLKwFHSYMrw20TxSflJUgMZa2ACDApvkq545TGUQRVH9KEM3jXCaB42bXKHrh169hni79WnR6jH3BmDOnCHAMwbdyjQq2tgevcYadSNCQCRGWKxKSKqApHOAUiUyTSziDgq6UwgCpV55kjjoGhxSWNmYdZusmyqmBowsEujdhzr3ousmE0eQOaoJmOh5Fy3WRibhUSE5BSqCwO8zG8uHj/L8J8uzdSshPQWACj6ZMI5mRUbRDdMs+AgrDVLe7Z4dkDcQVWJvmRj0Dyofu7JILenAVJsBploJFKke2SH2ryFOJfrdAW9qsr1pgweWbqimyG2UNjm+kq00qEatIojG1D1KJAelgNSY2/MbGIzuwXkqKuzBB9MghyWm3RveB7krGbSc1qR5eA8m5FFVETIpg1VyCHSgxqBVM/NYxkuH9gUJ+1QpufWqLDCISdsRede3uHGVuk4ia0uql63rZvYHwPhZEKys/JvIyAGqfjCkIRVlQYI8cWBcpdW2INCr4zlq+scpzlkhy3XEUpLq6gcDFHiQ+muvl/51IMAZASkXEfHg7vHdBBnrwhWMWdMNwMwCor5GNl51dpheO8SyBb2s25NfBKa1ibEOEHkK3721ethF7AeLuGOZbcSjQgdgWBdDlWtu2DJNEztXsrI8hXy1bTlp8pTPa9A+guAQ6pa4Nor/KqfiRpdqU6ORFNNwfkLi9WvvXtPTv949ZiffZ3JzyfW/ZAnVfgg7IsHpom9bthCYQG6MXR7RcjicmvdAIKPuime32ma1GOq0w/lI97NJ2u0CGLVCKGufLD2prF1Yi6ga2zkfvdgFdGvWqlOX35hwXxrilxv8uCTuR2p0LMKaVEqRezg0zIbq2pVxQfSlQUF1X3u3aQNlar1mU15fp5NuNijXIp5ZI7GMmqJbnk+KLyaB0HUytqyRMSlMyHKQDGdMMQSmMH6xyiq+chaUlppj09I1HJHkdvNRGVsVqQEsrzUYGTuhfUJkHf10PUPSVdQbSYca32pguKoHaYMUqyvoqrsUp/icIZUaOJqd1Q04hZOiugCttcPr53M0d4rjQRGtGV1h/u4sULPhuXaHjnIqkUnwsmgdxOV3ZPD2uW7JTZL2TmHZod3Lg5Og8dVTuqRGnnS1Ys1bhH84kRd4eFfLWrk1uOffrKwe56yzZca8WSVzSasgU402V3zrJPyqDZVi01+K+0xV6lchlYjwcnq1ebdVDBTy3gWiW4+Zd7fZElXVNVEFjBySezLUstgS9t647oAc5u9lShy+lE/+8jk5607DzVNY7fokj9jMl0Pmzf/5/Z4GR6eBNlM5KJSiLtL0CyZIQ1tzEU26cAcobapbFoAADG9XaVGPZcMM52j+30IDGA0fTPJQfPbYFNoi7MVSFt4wWYbIPb2yPMExiGhkfEc9CqXa9PBiB30zPA6oagTAi8hH8nD2AIGryIk4C0E13y9qZxHqis+vJLjskSU6sHZIqqU44SmYOr6Y9LD5i1wLsY/wThICGaGoLrRxCadDrpND9iUn/a+9/Rf7R51FOY8qJA631MC/1z3Nr5l8774GeksJGgHQYYtl4LrJuPeB3514IGCwpTJ1JPipuB+e6Mh08TIy+JAcwCg7WDVWgNWu8+ogpGmfjyQ777RjSzHZc95sUB1uhlmoycup5Pgezx5lJrEsNqR/pgvMUwMpHWo0DRWo1y/KtAGJz4chbOsKDb2nvD1kCyRAe6HMkSzgwcdl1+jJMLVKhvDLz37W9WGCp+C/OFq87APpDRq0pQE2a269nN1oOu6qGJ6WrTJhfq/VHTpi25MfDpcOJn7oF7Er9VzPxth2Wk2UyOqo5NP/T/9i/rVfJU7Farviw/YfAX5Te4ukU/9fexFZ/+cK+Kvq78C0l6EnW4+fNB1lRMSi1i/KYlavpBIhBA8ZPawN6/j4HHysgf1YhVQF+Gz191D3fHBFUwNtLDG46Jc1Z3LP/CiBPLvecqLs003bqAqV4ST0XGRKgBPUrrX0jB09WGsXAZZ2rqSrpRRWa53qAjut2VAGMS928HdBg0q3OKENG3r0IHRNGdyuMqmPMSikIyUQIJewLZYlFGQ7iG2y18LbxlRS4QN6l8/3mgpfXYq8ouU6u411v+Vi0tWlV5MmyUOl/7rqDHdGE88s27cmDhXyyfGtyCA0I4T8tjZBvQs2UxX/lRMQ9pRtOg2RCX0hxk8f00iasv1zjPtkPmLGHMX8FJ2pjrLXOBZ7BMR15Kn3nj34VUA4Ibigwevs2zSL18+6s5hhap8/fH9IbNqLF2hOM4meNUljE014LC1aU5MByTG5O1AIHE9kyw7nsFTZI6P5Dq5ak0cUPtEz1wSn7SxhJYk9MbUMfIW3djXLEWhwekTdP6n05c5HASO6ji/sOs3miqS2TKfuVZvNrV2Y8LSi86Hmz4FAfV2MlUpZsSARiPgujsR9KUmv6VUZUXpjeZkreuiH3a/EsFX1l7F8KQcuOR2p+OLp9N0rkx4N3Pec4DKDXm8nPgGb82af7Yj4O/lI4ilg5IcDZr+IyoW5fgciEUI5JdzRKN6izD0pyUFCxQRwSslT12SuYA834+OrRVMHFUGA97w30WkJEf8TNjvIpM5Kvfj2KhmVD+rGPU7+pi5gIuOW7bhnOAH1u8N8vZVsrqRvSK0pvzg1FxrnFZB7LePvzp0ykmNX2+11BLTJ3Bw65W0pG2tsSO94jTeGg3jnWgOSwnTMT7e//f4IE9fsWqk94l5N2ZbDBAFVUGGRZGTGSwH2ZJLm5OTVvhrCJFtV0jAmr8/zxmgKNkwdXKbW4iFoV+iK9gAUvC/8Cqb0GtfUSGEfd297HiGcdikjAmR7C+cgxMTkz0XejsdyYuLVVyzabnY9AlbdraJvK5HYMMGUxujvG+hzFspb9toWlqf+z7hFlo5cWxrRSIGpM/pQn1uXBivDpW9nPvZXV2LVhdGUYMV8u0LFAUIQ0jQe1SO6LK/pOIJMLJgoWI7dZOOpaKS1LaVXCc3L516ZX6ZWC4eHbMMSH2Brkc34cKFQbMy/Rkn4x/2exRjTHAY9MNON/rr4xOaFQfNBjdzc9SFoxhVDKHMgWEj1GZ1h2664jD3btoZHuNzGUtKILYm0lK0pBawcK7AXFOBsl25nWzLGUPoUvAdYJFVrvDFPaWH86Pys2MSDjcE+Ov0WBg/IiWlXL3fEVODjcaQgN0JS6cGeScZjE6TiDb5T71nrXKZ8cU8MnXHnwfWLVeb1Qaz2nxlxK4+GrAhgxrijX1CQhLzwtu/j7YsdXZ25t+9m4gZjE2Xd8amWYOWx+zIvPYkn3G58l8+t/UuHRLD7Lvt69TV+ap863RO31fNhA5lR8p9nM3nGLnb/HQU96xsZuxFNf1rfYGXn84EDrXVw9WKbA32rw2/pg71r5/Cr1WTFOpP+h79J3XYtvKvGScjpJ644zU3R0bYdzXFpZRnx5SkBP5qsrLMbuqDq8iKrcySNYptNT+vz44dPzBX5a0QhgzEeFhwru+xpH7t5tgJg+J5voq/HX6huT5HIfLwXozrZB9LV+4xm8ceGLWk/mJGLF0plol3hlogXlmy+KIH43FRjVFtN/1+d//yIC5814Z49+2ldWt8l9jgqfRJWliddpmzbmPN6XcejKwnR8z1bi1zfAwAu5zZtnVrXu1iV+PjR42uxc6Cpqa2aYa2/pIhw4YbZf3ankSUzp5dGv7doU1dbzZWDS6xBSXnTWltmZKXHFRXElf1f4qYFDXSll2zwNX4aJiI6uy64uhGeUBSVtupspIC3EvCZ8Sssr4+f/ze2hoiHTwkhV7zGDezXKt8OpDRzdQz40QVhIPyixhnIbU3lzGkWxgMj1jdmj3eerlvvde86ZT01YhXUsqxttTz3rNGNyKGlyTWjt0zz6t+EmzIBCQqYOywvl2+Tt1sH5VvrX+db8ds3zpds0+nTzNd3CMpyChS5Ure/GzFovuF23lA0J3gXRvLThn3eGdM1A6U+a2Jj2uii5c6O1/n3b2j139uXV5RFRHhmpwPD0Nl+nAry9d8yZbMFDG/u99Vn24om0MgS153XyVR+MyaYrLfHvdb4W906/EKL0/vm6yEh13xRMJHpPRtohMZ+VmtCf+Xlz/LwtQx/hmZ5uEqs9rc4EhXm9WqO+aQ7Lnv6qzNbqt1+t8LK4aMcWPGxBnnCS9S5Z1B5r+adshcW6heKEY4JphYRwPa6sjm4fnGZFz1DUlwdhEllOwrOwLtb9CrGqVadP/D4K9OWwA5CLRbU7nvr3denLl2zdX2vU9wUXTV1Hdr/Sq+1EG/te+nVvtVWy92FRGQRyDYVOfuAdowDItn/keRAeQmBKSTXB213GYK/BNLt9PHNTn28IPg9OHR+6RRVl+qcMTIVRfm8XhVyvOClgbxCe5eejX8fvmPdUuKG1L6dkcgnHYjzP+hq+nf57txIUZjyOzB65fHn2WpnHk3HamBXN1sde9DVqvclGfFqWfjKAwPffktrnLWqUSFvZ2v2UbWEK+fHOBxCpoarObexufabEOkFVIEdvQtnh2VXmpyg7pO095+pSDvv+AFup0O91s4axo1U+h8dF9HYBiCRw/08eR0TCEPx+7jCf44oOt+ArqdPkPfpi/RjoqCPMafxEgDhGs2DlAOaGkoK7HNoG/Qd+iLdAf9llBQ+f2MgUKhIX1QCSD5MEHti+ej34WFm0xFlKA7dS9vPbcOeWzy7OfZzDE2xiX0XCJsEi7xFH5xvs+9xC4YfJn+TDGTJv3S0NlZ/8svaRnNzlsO1eSrqPlNJ0ZVBBbV2wKH4loM4/lJB4/XWd3NIqVDa26w+M5nmRazxnhDPyYklH8pmbfKFZ/m3LeNV/uAzm2aWIAw9GbcoDCej5pRY1hUkvfVKbTxjBkw4PN4fD3L6rPo3/AhlfNJkYiXD+HMpj6ToorEAXkhfbXZq7O1Q7O1bm12X38uYWVL7omWKtFwl6vF5RreN1s7R5vdJ4Az7byUe7JlqdiQGT08Ps7SBN7d9GN57r81o79AoPxrzRBlL3cvehIKcu/80ODI0N219gr+fRfbzIPDj7wVtAsu8FaM5t1g/ysr0RkEBp1Qf9TPQuFzBGQhCWiWNHXs1Aqaq8roGSBNmftBWn/FACWIr+nYKhrde8hKWaHs6+iQ+tCCPJ2BNujGeNsM+mLFNq1e03/lRcGMyGUziCLivlDYKBTeXyyYrpdv+f3ah6PkprQIEsPxSFOqfNrRN8EeJCLwyMTU8FdTlR9vH5gSLiAQjum6EOrScR9XLmkA9M+7mZiYedyWG7F6ZEOjZXVEru1k9qxZWScrdo+aqSufTordHNdP1M9SDBiG6WXmNAQUhSAlUx9GMMUWk8jEqhiFHidw2Y2ZX+ywHc8Yt2tSYkaELevkrFkns26fynobaNtVPqvdmjVVxcUMzsvNSIXZsLR0loc0wFOZe9U63QAVQVny02zibIpK5pclIxw0ulBUMqk5pYw/ZoDIHU1FRegiZecRJFgsM914e5YtbTRuQMMblK29Z6YteV6Fjf6L8luiH3fYmvoPc10s1ufDAHZboTCoY7qwiv2Fi0kff2TlqbSlbCdXJXFdk1Rxd7j16xLOyJRlPomJpd5KZv/6hCUOPVH9VKh3N+aXUkuPmomjV3IyxkdImp6d8oTTO9TCL9Cuf7TYTtYndQzJkDiVOwlPGS0XGDocwiqukx3rUUk9m0zZeTHN23mVYkZspyY/U9oJa56pXwBH2HEywD8yId6K26luF2UXM/8MAZ7ITrveHpzjqDOdbxcxymI4gkTVqMIBHDm/GrG5VNHCVUmDqBj6JrVtWcfx2WoSo5kz5/cqJglEv3+SLGIFCGFIvXJnx7JtZEoNL5YaVLhgFaMND7MsnShY4iGwU0/WFFMTT6eQA4scZKagXZACMiqhFKCnGu/GLUDg4b+Jgp6d+A+4GLQ9jjaUS1ws9uyDI4U4gCY10SVg6JlK8PFCQAD4Z/3J/DCpVBr7nhLi3f+XwehZ6IjHkoZUNqGXzumeHIw4QSO0r3cDCP4IYiwIQHM+G9pCiFplIoeV6fo+WgBpGP04DfIFKVtDAm0Mxl5qZZiEgAI5fyIGfOhzIg56+PJEAig4ciIJQniIPB/+Ht0NEbQm4/FEDCTgdSIOyRCJRFx604kkcHAaeTn8GmwwDiaCE+vNnwA1AIinAZgmDJAHFWCH2kaTrOAA2O5qFEByOrPR0SpcARqIgBAICxiNFyfLI95ACIao2C0CwuxwgC/2tHoAh71CExESponWLE7Z8sDgqGCua62hRVI0wQHVMDrsaCC8DQXk7d6Hh4RJrAsGhUhN5LOCDUuyomq6YQrLdlzPx5BTUGJxVNQ8ePLizYdv2GonTKgYF2wtL+dTP6aI+JHBFJHJy5EktCNFlhkMTkmSAMrS+85TDuu6GxMoi4J7VpacdyAjKITklAo+AoekbsPmFrQWa8ISlYJD0uvBU1YaykBWWbEP0KZVZH0xJcgzgnlRM6XQURg94cqK22VvzH96wGh7BT9LUDaUKj4tpYSDFWQoNb8aH2+dBAAAAA=="

/***/ }),

/***/ "eaff":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* unused harmony export Store */
/* unused harmony export mappedState */
/* unused harmony export mappedGetters */
/* unused harmony export mappedActions */
/* harmony import */ var vuex__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__("2f62");

const STORE_NAME = 'Store';
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
                commit(INCREMENT, increment);
                resolve();
            }, delayMs);
        });
    }
};
const Store = {
    namespaced: true,
    state: {
        count: 0,
        meta: {
            mutationCount: 0
        }
    },
    getters,
    mutations: {
        [INCREMENT](state, increment = 1) {
            state.meta.mutationCount += 1;
            state.count += increment;
        }
    },
    actions
};
const mappedState = Object(vuex__WEBPACK_IMPORTED_MODULE_0__[/* mapState */ "d"])(STORE_NAME, [
    'count',
    'meta'
]);
const mappedGetters = Object(vuex__WEBPACK_IMPORTED_MODULE_0__[/* mapGetters */ "c"])(STORE_NAME, [
    'isEven'
]);
const mappedActions = Object(vuex__WEBPACK_IMPORTED_MODULE_0__[/* mapActions */ "b"])(STORE_NAME, [
    'performAsyncIncrement'
]);


/***/ }),

/***/ "ecb4":
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__.p + "fonts/fontawesome-webfont.8b43027f.eot";

/***/ })

}]);
//# sourceMappingURL=4.9e804562.js.map