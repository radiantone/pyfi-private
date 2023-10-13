<template />
<style>
@import "//cdnjs.cloudflare.com/ajax/libs/font-awesome/5.13.0/css/all.min.css";
/* ----------------------------------------------------------------------------------------------------- */
/* --- Node common -------------------------------------------------------------------------------- */
/* ----------------------------------------------------------------------------------------------------- */

.q-splitter--vertical > .q-splitter__separator > div {
  cursor: col-resize;
}

.brightness {
  background-color:rgba(227,232,236,0.4);
}

.q-field__bottom {
    padding-left: 0px !important;
}

.brightness:hover {
  background-color:rgba(227,232,236,1.0);
}

.outlet-icon {
  display: block;
  text-indent: -9999px;
  width: 16px;
  height: 16px;
  background: url("~assets/images/outlet.svg");
  background-size: 16px 16px;
}
.q-item__section--side>.q-icon {
    font-size: 16px !important;
}

.bar {
  background: url("~assets/images/bar.png");
  background-size: cover;
}

.outlet-icon2 {
  display: block;
  text-indent: -9999px;
  width: 45px;
  height: 45px;
  margin-left: -5px;
  background: url("~assets/images/outlet.svg");
  background-size: 45px 45px;
}

.q-tree__node--selected {
  background-color: #e3e8ec !important;
  color: black;
}

.outlet-svg {
  fill: red;
}
.q-dialog > .q-card > .q-card__section--vert {
  padding: 0px !important;
}
.shadow-1-null:before {
  content: "";
  height: 7px;
  width: 280px;
  position: absolute;
  bottom: 0px;
  background: white;
  z-index: 2;
}
.shadow-2 {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);

  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}
.shadow-1 {
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}
.table,
.view {
  background-color: #f2f6fd;
  cursor: pointer;
  font-size: 12px;
  position: absolute;
  /*z-index: 11;*/
  overflow: hidden;
  min-width: 80px;
  min-height: 30px;
  width: auto;
}
.q-btn--rectangle {
  border-radius: 0px;
}
.q-dialog__inner > div {
  border-radius: 0px !important;
}

.q-card {
  border-radius: 0px !important;
}
.jtk-miniview-panner {
  background-color: rgb(144 145 145);
}

.table .name,
.view .name,
.table li.jtk-draggable,
.view li.jtk-draggable {
  background-color: rgba(43, 162, 253, 0.93);
  color: black;
  cursor: move;
  font-size: 13px;
  padding: 6px;
  height: 70px;
  display: flex;
  align-items: center;
}

.table li.jtk-draggable,
.view li.jtk-draggable {
  min-width: 100px;
}

.table .name span,
.view .name span {
  cursor: pointer;
  margin-left: auto;
  margin-right: auto;
}

.table .name .buttons,
.view .name .buttons {
  display: flex;
  align-items: center;
  cursor: pointer;
}

/* ----------------------------------------------------------------------------------------------------- */
/* --- Table nodes -------------------------------------------------------------------------------- */
/* ----------------------------------------------------------------------------------------------------- */

.table {
  margin-bottom: 0;
  min-width: 400px;
  display: block;
}

.table-columns {
  margin: 0;
  padding: 0;
}

.table-column {
  list-style-type: none;
  padding: 4px 6px;
}

.table-column-delete,
.view-delete {
  color: #000;
  padding: 2px;
  cursor: pointer;
  float: left;
  font-size: 10px;
  line-height: 10px;
}

.table-column-edit {
  color: #407364;
  float: right;
  cursor: pointer;
}

.new-column,
.delete,
.table-column-delete {
  -webkit-transition: background-color 0.15s ease-in;
  -moz-transition: background-color 0.15s ease-in;
  -o-transition: background-color 0.15s ease-in;
  transition: background-color 0.15s ease-in;
}

.edit-name {
  margin-right: 7px;
}

.new-column:hover,
.delete:hover,
.edit-name:hover {
  color: #ff8000;
}

.table-column-delete:hover {
  color: #434343;
}

.table-column-type-varchar {
  background-color: rgba(93, 173, 221, 0.22);
}

.table-column-type-integer {
  background-color: rgba(93, 173, 221, 0.22);
}

.table-column-type-date {
  background-color: rgba(93, 173, 221, 0.22);
}

.table-column[primary-key="true"] {
  background-color: rgba(99, 219, 249, 0.12);
}

/* ----------------------------------------------------------------------------------------------------- */
/* --- View nodes -------------------------------------------------------------------------------------- */
/* ----------------------------------------------------------------------------------------------------- */

.view {
  margin-bottom: 0;
  width: 400px;
  overflow: hidden;
  background-color: white;
}

.view-details {
  font-size: 10px;
  font-family: Courier, sans-serif;
  padding: 10px;
}

.view .view-delete {
  color: #f7ebca;
  padding: 2px;
  cursor: pointer;
  float: left;
  font-size: 10px;
  line-height: 20px;
}

.view .view-delete:hover,
.view .view-edit:hover {
  color: #ff8000;
}

.view-edit {
  position: absolute;
  right: 7px;
  top: 39px;
}

.txtViewQuery {
  width: 272px;
  height: 132px;
}

/* ---------------------------------------------------------------------------------------------------- */
/* --- Drag/drop interactions ------------------------------------------------------------------------- */
/* ---------------------------------------------------------------------------------------------------- */
.drop-hover {
  background-color: lightblue !important;
  color: black !important;
}

/* ----------------------------------------------------------------------------------------------------- */
/* --- Edge styles ------------------------------------------------------------------------------------- */
/* ----------------------------------------------------------------------------------------------------- */

.delete-relationship-anchor {
  border-radius: 12px;
  cursor: pointer;
  padding: 5px;
  background-color: white;
  font-size: 18px;
  border: 1px solid black;
  text-align: center;
}

.delete-relationship {
  border-radius: 12px;
  padding: 5px;
  z-index: 1;
  cursor: pointer;
  background-color: #6b8791;
  font-size: 18px;
  border: 1px solid black;
  text-align: center;
}

.delete-relationship:hover {
  color: #fff;
  background-color: #abbcc3;
  padding: 4px;
}

.common-edge path {
  stroke-width: 2;
  //stroke: #000;
}

.common-edge.jtk-hover path {
  stroke: #434343;
}

/* ----------------------------------------------------------------------------------------------------- */
/* --- dialogs ------------------------- */
/* ----------------------------------------------------------------------------------------------------- */

.form-labels-float {
  float: left;
  font-weight: bold;
  text-align: right;
  padding-right: 6px;
  padding-top: 6px;
  font-size: 14px;
}

.form-labels {
  font-weight: bold;
  text-align: left;
  padding-right: 6px;
  font-size: 14px;
}

.checkbox-id {
  margin-top: 6px;
  margin-left: 22px;
}

.btn-icon-margin {
  line-height: 18px;
  margin-left: 10px;
}

.pull-left {
  float: left;
}
.clearfix {
  clear: both;
}
</style>

<script>
export default {}
</script>
