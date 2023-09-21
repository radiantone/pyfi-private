(window["webpackJsonp"] = window["webpackJsonp"] || []).push([[7],{

/***/ "7df3":
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

// CONCATENATED MODULE: ./node_modules/@quasar/app/lib/webpack/loader.transform-quasar-imports.js!./node_modules/babel-loader/lib??ref--2-0!./node_modules/vue-loader/lib/loaders/templateLoader.js??ref--7!./node_modules/@quasar/app/lib/webpack/loader.auto-import-client.js?kebab!./node_modules/vue-loader/lib??vue-loader-options!./src/layouts/BlockLayout.vue?vue&type=template&id=62d2eddb&




var render = function render() {
  var _vm = this,
      _c = _vm._self._c;

  return _c('q-layout', {
    staticClass: "bg-white",
    attrs: {
      "view": "lHh Lpr lFf"
    }
  }, [_c('q-header', {
    attrs: {
      "elevated": ""
    }
  }, [_c('q-toolbar', {
    staticClass: "bg-secondary"
  }, [_c('q-btn', {
    attrs: {
      "flat": "",
      "dense": "",
      "round": "",
      "aria-label": "Menu",
      "icon": "menu"
    },
    on: {
      "click": _vm.toggleLeftDrawer
    }
  }), _c('q-toolbar-title', [_vm._v("\n        " + _vm._s(_vm.block.name) + " Block\n      ")])], 1)], 1), _c('q-drawer', {
    staticClass: "bg-grey-2",
    attrs: {
      "show-if-above": "",
      "bordered": ""
    },
    model: {
      value: _vm.leftDrawerOpen,
      callback: function callback($$v) {
        _vm.leftDrawerOpen = $$v;
      },
      expression: "leftDrawerOpen"
    }
  }, [_c('q-list', [_c('q-item-label', {
    attrs: {
      "header": ""
    }
  }, [_vm._v("\n        Essential Links\n      ")]), _c('q-item', {
    attrs: {
      "clickable": "",
      "target": "_blank",
      "rel": "noopener",
      "href": "https://quasar.dev"
    }
  }, [_c('q-item-section', {
    attrs: {
      "avatar": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "school"
    }
  })], 1), _c('q-item-section', [_c('q-item-label', [_vm._v("Docs")]), _c('q-item-label', {
    attrs: {
      "caption": ""
    }
  }, [_vm._v("\n            https://quasar.dev\n          ")])], 1)], 1), _c('q-item', {
    attrs: {
      "clickable": "",
      "target": "_blank",
      "rel": "noopener",
      "href": "https://github.quasar.dev"
    }
  }, [_c('q-item-section', {
    attrs: {
      "avatar": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "code"
    }
  })], 1), _c('q-item-section', [_c('q-item-label', [_vm._v("GitHub")]), _c('q-item-label', {
    attrs: {
      "caption": ""
    }
  }, [_vm._v("\n            github.com/quasarframework\n          ")])], 1)], 1), _c('q-item', {
    attrs: {
      "clickable": "",
      "target": "_blank",
      "rel": "noopener",
      "href": "http://chat.quasar.dev"
    }
  }, [_c('q-item-section', {
    attrs: {
      "avatar": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "chat"
    }
  })], 1), _c('q-item-section', [_c('q-item-label', [_vm._v("Discord Chat Channel")]), _c('q-item-label', {
    attrs: {
      "caption": ""
    }
  }, [_vm._v("\n            https://chat.quasar.dev\n          ")])], 1)], 1), _c('q-item', {
    attrs: {
      "clickable": "",
      "target": "_blank",
      "rel": "noopener",
      "href": "https://forum.quasar.dev"
    }
  }, [_c('q-item-section', {
    attrs: {
      "avatar": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "record_voice_over"
    }
  })], 1), _c('q-item-section', [_c('q-item-label', [_vm._v("Forum")]), _c('q-item-label', {
    attrs: {
      "caption": ""
    }
  }, [_vm._v("\n            https://forum.quasar.dev\n          ")])], 1)], 1), _c('q-item', {
    attrs: {
      "clickable": "",
      "target": "_blank",
      "rel": "noopener",
      "href": "https://twitter.quasar.dev"
    }
  }, [_c('q-item-section', {
    attrs: {
      "avatar": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "rss_feed"
    }
  })], 1), _c('q-item-section', [_c('q-item-label', [_vm._v("Twitter")]), _c('q-item-label', {
    attrs: {
      "caption": ""
    }
  }, [_vm._v("\n            @quasarframework\n          ")])], 1)], 1), _c('q-item', {
    attrs: {
      "clickable": "",
      "rel": "noopener"
    },
    on: {
      "click": function click($event) {
        return _vm.$router.push('/');
      }
    }
  }, [_c('q-item-section', {
    attrs: {
      "avatar": ""
    }
  }, [_c('q-icon', {
    attrs: {
      "name": "public"
    }
  })], 1), _c('q-item-section', [_c('q-item-label', [_vm._v("Designer")]), _c('q-item-label', {
    attrs: {
      "caption": ""
    }
  }, [_vm._v("\n            Back to Designer\n          ")])], 1)], 1)], 1)], 1), _c('q-page-container', [_c('router-view'), _vm._v("\n    " + _vm._s(_vm.block.description) + "\n    " + _vm._s(_vm.block.package) + "\n    " + _vm._s(_vm.block.gitrepo) + "\n  ")], 1)], 1);
};

var staticRenderFns = [];

// CONCATENATED MODULE: ./src/layouts/BlockLayout.vue?vue&type=template&id=62d2eddb&

// CONCATENATED MODULE: ./node_modules/@quasar/app/lib/webpack/loader.transform-quasar-imports.js!./node_modules/babel-loader/lib??ref--2-0!./node_modules/@quasar/app/lib/webpack/loader.auto-import-client.js?kebab!./node_modules/vue-loader/lib??vue-loader-options!./src/layouts/BlockLayout.vue?vue&type=script&lang=js&
/* harmony default export */ var BlockLayoutvue_type_script_lang_js_ = ({
  name: 'MyLayout',
  data: function data() {
    return {
      leftDrawerOpen: false,
      block: {}
    };
  },
  mounted: function mounted() {
    this.block = this.$route.params.block;
  },
  methods: {
    toggleLeftDrawer: function toggleLeftDrawer() {
      this.leftDrawerOpen = !this.leftDrawerOpen;
    }
  }
});
// CONCATENATED MODULE: ./src/layouts/BlockLayout.vue?vue&type=script&lang=js&
 /* harmony default export */ var layouts_BlockLayoutvue_type_script_lang_js_ = (BlockLayoutvue_type_script_lang_js_); 
// EXTERNAL MODULE: ./node_modules/vue-loader/lib/runtime/componentNormalizer.js
var componentNormalizer = __webpack_require__("2877");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/layout/QLayout.js
var QLayout = __webpack_require__("4d5a");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/header/QHeader.js
var QHeader = __webpack_require__("e359");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/toolbar/QToolbar.js
var QToolbar = __webpack_require__("65c6");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/btn/QBtn.js
var QBtn = __webpack_require__("9c40");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/toolbar/QToolbarTitle.js
var QToolbarTitle = __webpack_require__("6ac5");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/drawer/QDrawer.js
var QDrawer = __webpack_require__("9404");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/item/QList.js
var QList = __webpack_require__("1c1c");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/item/QItemLabel.js
var QItemLabel = __webpack_require__("0170");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/item/QItem.js
var QItem = __webpack_require__("66e5");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/item/QItemSection.js
var QItemSection = __webpack_require__("4074");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/icon/QIcon.js
var QIcon = __webpack_require__("0016");

// EXTERNAL MODULE: ./node_modules/quasar/src/components/page/QPageContainer.js
var QPageContainer = __webpack_require__("09e3");

// EXTERNAL MODULE: ./node_modules/@quasar/app/lib/webpack/runtime.auto-import.js
var runtime_auto_import = __webpack_require__("eebe");
var runtime_auto_import_default = /*#__PURE__*/__webpack_require__.n(runtime_auto_import);

// CONCATENATED MODULE: ./src/layouts/BlockLayout.vue





/* normalize component */

var component = Object(componentNormalizer["a" /* default */])(
  layouts_BlockLayoutvue_type_script_lang_js_,
  render,
  staticRenderFns,
  false,
  null,
  null,
  null
  
)

/* harmony default export */ var BlockLayout = __webpack_exports__["default"] = (component.exports);













runtime_auto_import_default()(component, 'components', {QLayout: QLayout["a" /* default */],QHeader: QHeader["a" /* default */],QToolbar: QToolbar["a" /* default */],QBtn: QBtn["a" /* default */],QToolbarTitle: QToolbarTitle["a" /* default */],QDrawer: QDrawer["a" /* default */],QList: QList["a" /* default */],QItemLabel: QItemLabel["a" /* default */],QItem: QItem["a" /* default */],QItemSection: QItemSection["a" /* default */],QIcon: QIcon["a" /* default */],QPageContainer: QPageContainer["a" /* default */]});


/***/ })

}]);
//# sourceMappingURL=7.a864a240.js.map