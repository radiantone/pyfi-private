# jsPlumb Toolkit Edition

Welcome to the Toolkit edition of jsPlumb.


---

## Requirements
 To get started, you'll need these things installed:

    - NodeJS  (version 5 or higher)
    - npm     (this is installed with NodeJS)
    
    
### Optional 

In order to clone an existing application or install a Webpack demo, you need: 

    - Grunt   (after installing Node, `npm install grunt-cli -g` will install this)

---

## Setup

The Toolkit ships with demonstrations that are in "vanilla" JS, as well as some in Angular, React and Vue. 

### Setup everything at once

You can choose to setup everything at one time by running this command in the root directory of your download:


```
npm install
```
    
This will iterate through every demonstration and run:
 
    - `npm install` for all demos 
    - `grunt webpack` for those demos that use Webpack
    - `npm run prod-build` for Angular demos
    - `npm run build` for React or Vue demos 

It can take a little while to run this, but it's a good idea to do it as you can then get an overview of everything the
Toolkit has to offer.

Once you've installed everything, you can either host this entire directory on a webserver somewhere, or you can use
the embedded webserver:

---

## Hosting the Toolkit package

After installation, you can spin up a webserver to host the package using one of these commands: 

### Mac/Linux/Unix

```
npm run start
```

### Windows

```
npm run start_windows
```

By default, this will start up a webserver on port 8910.


### Setup a single demonstration

Navigate to `demo/demo name` and run `npm i`.

Then, you may need to take extra steps, depending on the demonstration:

    - for Vanilla demonstrations there is nothing left to do. You will need to serve the demonstration via a webserver in order for the javascript to work.
    - for Angular, you can either run `ng serve` to get the demo going, or you can run `npm run prod_build` to build the app.
    - for React, you can either run `npm run start` to get the demo going, or you can run `npm run build` to build the app.
    - For Vue, you can either run `npm run serve` to get the demo going, or you can run `npm run build` to build the app.

---

## Creating Applications

With Grunt you can get started straight away with a copy of an existing demo, or with an almost empty app you can use as a template.

### Cloning an existing demo

This will work for any demonstration

```
grunt clone --app=database-visualizer --o=&lt;your output directory&gt;
```

Valid values for `app` are:


    -database-visualiser
    -flowchart-builder
    -layouts
    -multiple-hierarchy
    -paths
    -multiple
    -skeleton
    -groups
    -active-filtering
    -angular-1.x
    -angular-1.x-groups
    -angular
    -database-visualizer-angular
    -database-visualizer-react
    -angular-1.x-groups
    -angular-groups
    -angular-skeleton
    -react
    -vue


### Creating a new skeleton app

For Vanilla JS you can use this:

```
grunt create --o=&lt;your output directory&gt;
```

For Angular/Vue we recommend using their respective CLI to create a new app. For React, we use `create-react-app` ourselves; it
seems to be the current standard.

### Creating a new app manually

See instructions at [https://docs.jsplumbtoolkit.com/toolkit/current/articles/getting-started.html](https://docs.jsplumbtoolkit.com/toolkit/current/articles/getting-started.html)

### Ingesting an existing jsPlumb instance

If you have an existing jsPlumb instance and you want to try the simplest upgrade path, this is for you.

See instructions at [https://docs.jsplumbtoolkit.com/toolkit/current/articles/getting-started.html#ingest](https://docs.jsplumbtoolkit.com/toolkit/current/articles/getting-started.html#ingest)

---

## Demonstrations


The full list of available demonstrations are the valid values for `app` described in the cloning a demo section above:

    - [Layouts](demo/layouts/index.html)
    - [Hierarchy Layout - Multiple Roots](demo/multiple-hierarchy/index.html)
    - [Multiple Renderers](demo/multiple/index.html)
    - [Path Traversal](demo/paths/index.html)
    - [Database Visualizer](demo/database-visualizer/index.html)       
    - [Flowchart Builder](demo/flowchart-builder/index.html)
    - [Database Visualizer - Angular](demo/database-visualizer-angular/dist/index.html)
    - [Flowchart Builder - Angular](demo/angular/dist/index.html)
    - [Angular Skeleton](demo/angular-skeleton/dist/index.html)
    - [Active Filtering](demo/active-filtering/index.html)
    - [Angular 1.x Integration](demo/angular-1.x/index.html)           
    - [Groups](demo/groups/index.html)
    - [Groups - Angular](demo/angular-groups/dist/index.html)
    - [Groups - Angular 1.x](demo/angular-1.x-groups/index.html)       
    - [React Flowchart Builder](demo/react/index.html)
    - [React Database Visualizer](demo/database-visualizer-react/index.html)
    - [React Integration Skeleton](demo/react-skeleton/index.html)
    - [Vue 2 Integration](demo/vue/dist/index.html)

You can also see the full list here:

[https://jsplumbtoolkit.com/demos.html](https://jsplumbtoolkit.com/demos.html)

All of the Toolkit demonstrations on this page are included in your evaluation or licensed distribution. If you serve
the Toolkit as discussed above in "Hosting the Toolkit package", the launch page at [http://localhost:8910](http://localhost:8910) provides links
to each of the demonstration pages.

---

## Documentation

Documentation for the jsPlumb Toolkit is available at [https://docs.jsplumbtoolkit.com](https://docs.jsplumbtoolkit.com)

