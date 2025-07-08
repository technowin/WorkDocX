// Only make changes if you really know what you're doing in gulpfile
const { series, src, dest, parallel, watch } = require("gulp");
const path = require('path');
const autoprefixer = require("gulp-autoprefixer");
const browsersync = require("browser-sync");
const concat = require("gulp-concat");
const CleanCSS = require("gulp-clean-css");
const del = require("del");
const fileinclude = require("gulp-file-include");
const newer = require("gulp-newer");
const rename = require("gulp-rename");
const rtlcss = require("gulp-rtlcss");
const sourcemaps = require("gulp-sourcemaps");
const sass = require("gulp-sass")(require("sass"));
const uglify = require("gulp-uglify");

const paths = {
    baseSrc: "src/",                          // source directory
    baseDist: "dist/",                        // build directory
    baseDistAssets: "dist/assets/",           // build assets directory
    baseSrcAssets: "src/assets/",             // source assets directory
    vendorFile: require("./vendor.config"),  // Import the plugins list
};

// Copying Third Party Plugins Assets
const plugins = function () {
    const out = paths.baseDistAssets + "vendor/";

    paths.vendorFile.forEach(({ name, vendorJS, vendorCSS, iconLibs, assets, fonts, font, media, img, images, webfonts }) => {

        const handleError = (label) => (err) => {
            const shortMsg = err.message.split('\n')[0];
            console.error(`\n${label} - ${shortMsg}`);
            throw new Error(`${label} failed`);
        };

        if (vendorJS) {
            src(vendorJS)
                .on('error', handleError('vendorJS'))
                .pipe(concat("vendor.min.js"))
                .pipe(dest(paths.baseDistAssets + "js/"));
        }

        if (vendorCSS) {
            src(vendorCSS)
                .pipe(concat("vendor.min.css"))
                .on('error', handleError('vendorCSS'))
                .pipe(dest(paths.baseDistAssets + "css/"));
        }

        if (iconLibs) {

            const tasks = iconLibs.map(lib => {
                return src(lib.assets, { base: 'node_modules' })
                    .on('error', handleError(lib.name))
                    .pipe(rename(filePath => {
                        const parts = filePath.dirname.split(path.sep);
                        if (parts.length >= 2) {
                            filePath.dirname = parts.slice(2).join(path.sep);
                        }
                    }))

                    .pipe(dest(paths.baseDistAssets + `css/` + lib.name));
            });

            return tasks;

        }

        if (assets) {
            src(assets)
                .on('error', handleError('assets'))
                .pipe(dest(`${out}${name}/`));
        }

        if (img) {
            src(img)
                .on('error', handleError('img'))
                .pipe(dest(`${out}${name}/`));
        }

        if (images) {
            src(images)
                .on('error', handleError('images'))
                .pipe(dest(`${out}${name}/images/`));
        }

        if (media) {
            src(media)
                .on('error', handleError('media'))
                .pipe(dest(`${out}${name}/`));
        }

        if (fonts) {
            src(fonts)
                .on('error', handleError('fonts'))
                .pipe(dest(`${out}${name}/`));
        }

        if (font) {
            src(font)
                .on('error', handleError('font'))
                .pipe(dest(`${out}${name}/`));
        }

        if (webfonts) {
            src(webfonts)
                .on('error', handleError('webfonts'))
                .pipe(dest(`${out}${name}/`));
        }
    });

    return Promise.resolve();
};

const html = function () {
    const srcPath = paths.baseSrc + "/";
    const out = paths.baseDist;
    return src([
        srcPath + "*.html",
        srcPath + "*.ico",
        srcPath + "*.png",
    ])
        .pipe(
            fileinclude({
                prefix: "@@",
                basepath: "@file",
                indent: true,
            })
        )
        .pipe(dest(out));
};

const data = function () {
    const outpdf = paths.baseDistAssets + "pdf/";
    src([paths.baseSrcAssets + "pdf/**/*"])
        .pipe(dest(outpdf));

    const out = paths.baseDistAssets + "data/";
    return src([paths.baseSrcAssets + "data/**/*"])
        .pipe(dest(out));
};

const fonts = function () {
    const out = paths.baseDistAssets + "fonts/";
    return src([paths.baseSrcAssets + "fonts/**/*"])
        .pipe(newer(out))
        .pipe(dest(out));
};

const images = function () {
    const out = paths.baseDistAssets + "images";
    return src(paths.baseSrcAssets + "images/**/*")
        .pipe(dest(out));
};

const javascript = function () {
    const out = paths.baseDistAssets + "js/";
    return src(paths.baseSrcAssets + "js/**/*.js")
        .pipe(uglify())
        .pipe(dest(out));
};

const scss = function () {
    const out = paths.baseDistAssets + "css/";
    return src(paths.baseSrcAssets + "scss/**/*.scss")
        .pipe(sourcemaps.init())
        .pipe(sass.sync().on('error', sass.logError))
        .pipe(autoprefixer({ overrideBrowserslist: ["last 2 versions"] }))
        .pipe(dest(out))
        .pipe(CleanCSS())
        .pipe(rename({ suffix: ".min" }))
        .pipe(sourcemaps.write("./"))
        .pipe(dest(out));
};

const rtl = function () {
    const out = paths.baseDistAssets + "css/";
    return src(paths.baseSrcAssets + "scss/**/*.scss")
        .pipe(sourcemaps.init())
        .pipe(sass.sync().on('error', sass.logError))
        .pipe(autoprefixer({ overrideBrowserslist: ["last 2 versions"] }))
        .pipe(rtlcss())
        .pipe(rename({ suffix: "-rtl" }))
        .pipe(dest(out))
        .pipe(CleanCSS())
        .pipe(rename({ suffix: ".min" }))
        .pipe(sourcemaps.write("./"))
        .pipe(dest(out));
};

const initBrowserSync = function (done) {
    const startPath = "/index.html";
    browsersync.init({
        startPath: startPath,
        server: {
            baseDir: paths.baseDist,
            middleware: [
                function (req, res, next) {
                    req.method = "GET";
                    next();
                },
            ],
        },
    });
    done();
};

const reloadBrowserSync = function (done) {
    browsersync.reload();
    done();
};

// Warning not show
process.removeAllListeners('warning');

const clean = function () {
    return del(paths.baseDist);
};

function watchFiles() {
    watch(paths.baseSrc + "partials/*.html", series(html, reloadBrowserSync));
    watch(paths.baseSrc + "*.html", series(html, reloadBrowserSync));
    watch(paths.baseSrcAssets + "data/**/*", series(data, reloadBrowserSync));
    watch(paths.baseSrcAssets + "images/**/*", series(images, reloadBrowserSync));
    watch([paths.baseSrcAssets + "js/**/*.js", "!" + paths.baseSrcAssets + "js/maps/*"], series(javascript, reloadBrowserSync));
    watch(paths.baseSrcAssets + "scss/**/*.scss", series(scss, reloadBrowserSync));
}

exports.clean = series(
    clean,
);

exports.default = series(
    html,
    plugins,
    parallel(data, images, fonts, javascript, scss),
    parallel(watchFiles, initBrowserSync)
);

exports.build = series(
    clean,
    html,
    plugins,
    parallel(data, images, fonts, javascript, scss)
);

exports.rtl = series(
    html,
    plugins,
    parallel(data, images, fonts, javascript, rtl),
    parallel(watchFiles, initBrowserSync)
);

exports.rtlBuild = series(
    clean,
    html,
    plugins,
    parallel(data, images, fonts, javascript, rtl)
);