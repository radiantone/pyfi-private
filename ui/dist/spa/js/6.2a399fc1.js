(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[6],{dead:function(t,e,a){"use strict";a.r(e);var r=function(){var t=this,e=t._self._c;return e("q-layout",{staticClass:"bg-white",attrs:{view:"lHh Lpr lFf"}},[e("q-header",{attrs:{elevated:""}},[e("q-toolbar",{staticClass:"bg-blue"},[e("q-btn",{attrs:{flat:"",dense:"",round:"","aria-label":"Menu",icon:"menu"},on:{click:t.toggleLeftDrawer}}),e("q-toolbar-title",[t._v("\n        Quasar App\n      ")])],1)],1),e("q-drawer",{staticClass:"bg-grey-2",attrs:{"show-if-above":"",bordered:""},model:{value:t.leftDrawerOpen,callback:function(e){t.leftDrawerOpen=e},expression:"leftDrawerOpen"}},[e("q-list",[e("q-item-label",{attrs:{header:""}},[t._v("\n        Essential Links\n      ")]),e("q-item",{attrs:{clickable:"",target:"_blank",rel:"noopener",href:"https://quasar.dev"}},[e("q-item-section",{attrs:{avatar:""}},[e("q-icon",{attrs:{name:"school"}})],1),e("q-item-section",[e("q-item-label",[t._v("Docs")]),e("q-item-label",{attrs:{caption:""}},[t._v("\n            https://quasar.dev\n          ")])],1)],1),e("q-item",{attrs:{clickable:"",target:"_blank",rel:"noopener",href:"https://github.quasar.dev"}},[e("q-item-section",{attrs:{avatar:""}},[e("q-icon",{attrs:{name:"code"}})],1),e("q-item-section",[e("q-item-label",[t._v("GitHub")]),e("q-item-label",{attrs:{caption:""}},[t._v("\n            github.com/quasarframework\n          ")])],1)],1),e("q-item",{attrs:{clickable:"",target:"_blank",rel:"noopener",href:"http://chat.quasar.dev"}},[e("q-item-section",{attrs:{avatar:""}},[e("q-icon",{attrs:{name:"chat"}})],1),e("q-item-section",[e("q-item-label",[t._v("Discord Chat Channel")]),e("q-item-label",{attrs:{caption:""}},[t._v("\n            https://chat.quasar.dev\n          ")])],1)],1),e("q-item",{attrs:{clickable:"",target:"_blank",rel:"noopener",href:"https://forum.quasar.dev"}},[e("q-item-section",{attrs:{avatar:""}},[e("q-icon",{attrs:{name:"record_voice_over"}})],1),e("q-item-section",[e("q-item-label",[t._v("Forum")]),e("q-item-label",{attrs:{caption:""}},[t._v("\n            https://forum.quasar.dev\n          ")])],1)],1),e("q-item",{attrs:{clickable:"",target:"_blank",rel:"noopener",href:"https://twitter.quasar.dev"}},[e("q-item-section",{attrs:{avatar:""}},[e("q-icon",{attrs:{name:"rss_feed"}})],1),e("q-item-section",[e("q-item-label",[t._v("Twitter")]),e("q-item-label",{attrs:{caption:""}},[t._v("\n            @quasarframework\n          ")])],1)],1),e("q-item",{attrs:{clickable:"",rel:"noopener"},on:{click:function(e){return t.$router.push("/")}}},[e("q-item-section",{attrs:{avatar:""}},[e("q-icon",{attrs:{name:"public"}})],1),e("q-item-section",[e("q-item-label",[t._v("Designer")]),e("q-item-label",{attrs:{caption:""}},[t._v("\n            Back to Designer\n          ")])],1)],1)],1)],1),e("q-page-container",[e("div",{staticClass:"q-pa-md",staticStyle:{"max-width":"1200px","max-height":"600px"}},[e("q-input",{attrs:{filled:"",type:"textarea"},model:{value:t.text,callback:function(e){t.text=e},expression:"text"}}),e("q-btn",{attrs:{label:"Fetch"},on:{click:t.fetch}})],1)])],1)},n=[],i=a("7c43"),l={name:"AppLayout",data:function(){return{leftDrawerOpen:!1,text:"No Data"}},mounted:function(){i["a"].getMock().then((function(t){console.log("DATA MOCK FROM APP",t)}))},methods:{toggleLeftDrawer:function(){leftDrawerOpen.value=!leftDrawerOpen.value},fetch:function(){var t=this;i["a"].getMock().then((function(e){t.text=JSON.stringify(e.data)}))}}},o=l,s=a("2877"),c=a("4d5a"),q=a("e359"),m=a("65c6"),u=a("9c40"),b=a("6ac5"),p=a("9404"),v=a("1c1c"),f=a("0170"),h=a("66e5"),d=a("4074"),g=a("0016"),k=a("09e3"),w=a("27f9"),_=a("eebe"),D=a.n(_),Q=Object(s["a"])(o,r,n,!1,null,null,null);e["default"]=Q.exports;D()(Q,"components",{QLayout:c["a"],QHeader:q["a"],QToolbar:m["a"],QBtn:u["a"],QToolbarTitle:b["a"],QDrawer:p["a"],QList:v["a"],QItemLabel:f["a"],QItem:h["a"],QItemSection:d["a"],QIcon:g["a"],QPageContainer:k["a"],QInput:w["a"]})}}]);