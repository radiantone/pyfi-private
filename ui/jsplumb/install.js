/**
 * This runs as a preinstall. It recurses through the directories in the project and runs `npm install` anywhere it finds
 * a `package.json` (it skips `node_modules` directories)
 */

"use strict";

const path = require('path')
const fs = require('fs')
const child_process = require('child_process')

const root = process.cwd()
const dist = "dist"

let npmErrors = [];
let angularErrors = [];
let gruntErrors = [];
let typescriptErrors = [];
let vueErrors = [];

npm_install_recursive(root)
grunt_do_recursive(root)
tsc_do_recursive(root)
vue_do_recursive(root)

// Since this script is intended to be run as a "preinstall" command,
// it will be `npm install` inside root in the end.
console.log('===================================================================')
console.log('   Finished.\n\n')
if (npmErrors.length > 0) {
    console.log('WARN: We encountered errors running "npm install". Is npm installed? Whilst this is not entirely fatal - you can still use the Toolkit JS - it does mean that none of the demonstrations have been initialised.')
    console.log('These demonstrations were not initialised: [' + npmErrors.join(",") + ']');
    console.log('\n')
}

if (gruntErrors.length > 0) {
    console.log('WARN: We encountered errors running Grunt. Is it installed? This is not fatal; it just means that one or more of the demonstrations was not initialised.')
    console.log('These demonstrations were not initialised: [' + gruntErrors.map(ge => ge[0]).join(",") + ']');
    console.log('\n')
}

if (typescriptErrors.length > 0) {
    console.log('WARN: We encountered errors running the Typescript compiler. Is Typescript installed? This is not fatal; it just means that one or more of the demonstrations was not initialised.')
    console.log('These demonstrations were not initialised: [' + typescriptErrors.join(",") + ']');
    console.log('\n')
}

if (angularErrors.length > 0) {
    console.log('WARN: We encountered errors running the Angular CLI compiler. Is Angular CLI installed? This is not fatal; it just means that one or more of the demonstrations was not initialised.')
    console.log('These demonstrations were not initialised: [' + angularErrors.join(",") + ']');
    console.log('\n')
}

if (vueErrors.length > 0) {
    console.log('WARN: We encountered errors running the Vue CLI compiler. This is not fatal; it just means that one or more of the demonstrations was not initialised.')
    console.log('These demonstrations were not initialised: [' + vueErrors.join(",") + ']');
    console.log('\n')
}

console.log('===================================================================')



function npm_install_recursive(folder)
{
    const has_package_json = fs.existsSync(path.join(folder, 'package.json'))

    // Since this script is intended to be run as a "preinstall" command,
    // skip the root folder, because it will be `npm install`ed in the end.
    if (folder !== root && folder !== dist && has_package_json)
    {
        console.log('===================================================================')
        console.log(`Performing "npm install" inside ${folder === root ? 'root folder' : './' + path.relative(root, folder)}`)
        console.log('===================================================================')

        npm_install(folder)
    }

    for (let subfolder of subfolders(folder))
    {
        npm_install_recursive(subfolder)
    }
}

function trimPath(where) {
    let idx = where.lastIndexOf("/") || where.lastIndexOf("\\")
    return where.substring(idx + 1)
}

function npm_install(where)
{
    try {
        child_process.execSync('npm install', {cwd: where, env: process.env, stdio: 'inherit'})
    }
    catch (e) {
        npmErrors.push(trimPath(where));
    }
}

function subfolders(folder)
{
    return fs.readdirSync(folder)
            .filter(subfolder => fs.statSync(path.join(folder, subfolder)).isDirectory())
.filter(subfolder => subfolder !== 'node_modules' && subfolder[0] !== '.')
.map(subfolder => path.join(folder, subfolder))
}

function grunt_do_recursive(folder)
{
    const has_gruntfile = fs.existsSync(path.join(folder, 'Gruntfile.js'))
    const has_webpack = fs.existsSync(path.join(folder, 'webpack.config.js'))

    // Since this script is intended to be run as a "preinstall" command,
    // skip the root folder, because it will be `npm install`ed in the end.
    if (folder !== root && folder !== dist)
    {
        if (has_webpack) {
            webpack_do(folder);
        } else if (has_gruntfile) {
            grunt_do(folder, "build");
        }
    }

    for (let subfolder of subfolders(folder))
    {
        grunt_do_recursive(subfolder)
    }
}

function grunt_do(where, what)
{
    console.log('===================================================================')
    console.log(`Performing "grunt ${what}" inside ${where === root ? 'root folder' : './' + path.relative(root, where)}`)
    console.log('===================================================================')

    try {
        child_process.execSync('grunt ' + what, { cwd: where, env: process.env, stdio: 'inherit' });

    }
    catch (e) {
        gruntErrors.push([trimPath(where), what]);
    }
}

function webpack_do(where)
{
    console.log('===================================================================')
    console.log(`Performing webpack build inside ${where === root ? 'root folder' : './' + path.relative(root, where)}`)
    console.log('===================================================================')

    try {
        child_process.execSync('node ./node_modules/webpack/bin/webpack.js', { cwd: where, env: process.env, stdio: 'inherit' });

    }
    catch (e) {
        gruntErrors.push([trimPath(where), "webpack"]);
    }
}

function tsc_do_recursive(folder)
{
    const has_tsc= fs.existsSync(path.join(folder, 'tsconfig.json'))
    const has_angular_cli =  fs.existsSync(path.join(folder, '.angular-cli.json')) || fs.existsSync(path.join(folder, 'angular.json'))

    // Since this script is intended to be run as a "preinstall" command,
    // skip the root folder, because it will be `npm install`ed in the end.
    if (folder !== root && folder !== dist)
    {
        if (has_angular_cli) {
            angular_cli_do(folder)
        } else if (has_tsc) {
            tsc_do(folder)
        }
    }

    for (let subfolder of subfolders(folder))
    {
        tsc_do_recursive(subfolder)
    }
}

function tsc_do(where)
{
    console.log('===================================================================')
    console.log(`Performing "npm run tsc" inside ${where === root ? 'root folder' : './' + path.relative(root, where)}`)
    console.log('===================================================================')

    try {
        child_process.execSync('npm run tsc', { cwd: where, env: process.env, stdio: 'inherit' });
    }
    catch (e) {
        typescriptErrors.push(trimPath(where));
    }
}

function angular_cli_do(where)
{
    console.log('===================================================================')
    console.log(`Performing "ng build" inside ${where === root ? 'root folder' : './' + path.relative(root, where)}`)
    console.log('===================================================================')

    try {
        child_process.execSync('./node_modules/\@angular/cli/bin/ng build --prod --base-href .', {cwd: where, env: process.env, stdio: 'inherit'});
    }
    catch (e) {
        angularErrors.push(trimPath(where));
    }
}

function vue_do_recursive(folder)
{
    const isVue = fs.existsSync(path.join(folder, 'vue.config.js'));

    // Since this script is intended to be run as a "preinstall" command,
    // skip the root folder, because it will be `npm install`ed in the end.
    if (folder !== root && folder !== dist)
    {
        if (isVue) {
            vue_do(folder)
        }
    }

    for (let subfolder of subfolders(folder))
    {
        vue_do_recursive(subfolder)
    }

}

function vue_do(where)
{
    console.log('===================================================================')
    console.log(`Performing "vue-cli-service build" inside ${where === root ? 'root folder' : './' + path.relative(root, where)}`)
    console.log('===================================================================')

    try {
        child_process.execSync('node ./node_modules/\@vue/cli-service/bin/vue-cli-service.js build', {cwd: where, env: process.env, stdio: 'inherit'});
        child_process.execSync('cp -R ./data ./dist', {cwd: where, env:process.env, stdio: 'inherit'});
    }
    catch (e) {
        vueErrors.push(trimPath(where));
    }
}



