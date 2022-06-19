<template>
  <div
    class="table node jtk-node"
    style="overflow: unset !important;"
    :style="
      'background:transparent;top:' +
      obj.y +
      ';left:' +
      obj.x +
      ';min-width:' +
      obj.width +
      ';height:500px; '
    "
    @touchstart.stop
    @contextmenu.stop
  >
  <q-input
          style="width: 100px;position:absolute;top:50px;left:50px"
          type="number"
          v-model.number="concurrency"
        />
    <div :id="myid"></div>
    <div v-for="(el, index) in circles">
      <div
        :style="
          'position:absolute;top:' +
          getElTop(el) +
          'px;left:' +
          getElLeft(el) +
          'px;width:20px;height:20px'
        "
      >
        <span class="table-columns">
          <span class="table-column jtk-droppable table-column-type-Column">
            <jtk-source
              name="source"
              :port-id="'port' + index"
              scope="Column"
              filter=".table-column-delete, .table-column-delete-icon, span, .table-column-edit, .table-column-edit-icon"
              filter-exclude="true"
              :style="
                'position:absolute;top:' +
                getElTop(el) +
                'px;left:' +
                getElLeft(el) +
                'px;width:20px;height:20px'
              "
            />
          </span>
        </span>
      </div>
    </div>
  </div>
</template>
<style></style>
<script>
import { BaseNodeComponent } from 'jsplumbtoolkit-vue2';
import { v4 as uuidv4 } from 'uuid';

export default {
  name: 'ParallelTemplate',
  mixins: [BaseNodeComponent], // Mixin the components
  components: {},
  watch: {
    nodes: function (val) {
      this.update();
    },
    concurrency: function(val) {
      console.log("VAL CHANGED",val,this.lastvalue);
      if (val > this.lastvalue) {
        this.lastvalue = val;
        this.obj.concurrency = val;
          this.nodes['children'].push({
          name: 'boss5',
          colname: 'level2',
        });
        this.update();
      } else {
        this.lastvalue = val;
        this.nodes['children'].pop();
        this.update();
      }
      
    }
  },
  created() {},
  computed: {},
  mounted() {
    // set the dimensions and margins of the graph
    this.update();
    var me = this;

    /*
    setTimeout(() => {
      me.nodes['children'].push({
        name: 'boss5',
        colname: 'level2',
      });
      me.update();
    }, 3000);*/
  },
  data() {
    return {
      circles: [],
      lastvalue: 4,
      concurrency: 4,
      myid: 'id' + uuidv4().replaceAll('-', ''),
      obj: {
        id: this.myid,
        x: 0,
        concurrency: 4,
        y: 0,
      },
      nodes: {
        children: [
          {
            name: 'boss1',
            colname: 'level2',
          },
          {
            name: 'boss2',
            colname: 'level2',
          },
          {
            name: 'boss3',
            colname: 'level2',
          },
          {
            name: 'boss4',
            colname: 'level2',
          },
        ],
        name: 'Parallel',
      },
    };
  },
  methods: {
    getElTop(el) {
      console.log('ELY', el.getBBox().y);
      console.log('OBJ', this.obj);
      var body = document.body.getBoundingClientRect();
      var bb = el.getBoundingClientRect();
      var loc = window.toolkit.surface.mapLocation(bb.left-window.pageYOffset, bb.top);
      console.log('BBY', bb.top, bb.left, bb.x, bb.y);
      console.log("DATA-Y",el.getAttribute("data-y"));
      //return this.obj.y - el.y;
      return el.getAttribute("data-y")-this.obj.y - 165;
    },
    getElLeft(el) {
      console.log('ELX', el);
      var body = document.body.getBoundingClientRect();
      var bb = el.getBoundingClientRect();
      var loc = window.toolkit.surface.mapLocation(bb.left-window.pageYOffset, bb.top);
      console.log('BBX', bb.top, bb.left, loc);
      console.log("DATA-X",el.getAttribute("data-x"));
      //return this.obj.x - el.x;
      return el.getAttribute("data-x")-this.obj.x - 20;
    },
    update() {
      var me = this;

      setTimeout(() => {
        const width = 400;
        const height = 500;
        console.log('DRAW D3');
        // append the svg object to the body of the page
        d3.select('#' + me.myid).html('');

        d3.select('g.parent').selectAll('*').remove();

        const svg = d3
          .select('#' + me.myid)
          .append('svg')
          .attr('width', width)
          .attr('height', height)
          .append('g')
          .attr('transform', 'translate(40,0)'); // bit of margin on the left = 40

        // read json data
        var data = this.nodes;
        // Create the cluster layout:
        const cluster = d3.cluster().size([height, width - 100]); // 100 is the margin I will have on the right side

        // Give the data to this cluster layout:
        const root = d3.hierarchy(data, function (d) {
          return d.children;
        });
        cluster(root);

        // Add the links between nodes:
        svg
          .selectAll('path')
          .data(root.descendants().slice(1))
          .join('path')
          .attr('d', function (d) {
            return (
              'M' +
              d.y +
              ',' +
              d.x +
              'C' +
              (d.parent.y + 50) +
              ',' +
              d.x +
              ' ' +
              (d.parent.y + 150) +
              ',' +
              d.parent.x + // 50 and 150 are coordinates of inflexion, play with it to change links shape
              ' ' +
              d.parent.y +
              ',' +
              d.parent.x
            );
          })
          .style('fill', 'none')
          .attr('stroke', '#6b8791')
          .style('stroke-width', 6);
        var portid = 'port' + uuidv4().replaceAll('-', '');
        var node = svg
          .selectAll('g')
          .data(root.descendants())
          .join('g')
          .attr('transform', function (d) {
            return `translate(${d.y},${d.x})`;
          });

        node
          .append('circle')
          .attr('r', 9)
          //.attr('id','port'+uuidv4().replaceAll('-',''))
          .attr('class', 'table-column jtk-droppable table-column-type-Column')
          .style('fill', '#abbcc3')
          .style('stroke-width', 2);

        me.circles = svg.selectAll('circle');

        console.log('CIRCLES', me.circles);

        document.getElementsByTagName("circle").forEach( (el) => {
          var bb = el.getBoundingClientRect();
          console.log("CIRCLE EL",el, bb)
          el.setAttribute("data-x",bb.x)
          el.setAttribute("data-y",bb.y)
        })
        /*
            node.append('jtk-source')
            .attr('port-id',portid)
            .attr('scope','Column')
            .attr('filter',".table-column-delete, .table-column-delete-icon, span, .table-column-edit, .table-column-edit-icon")
            .attr('filter-exclude','true');
            */
      });
    },
  },
};
</script>
