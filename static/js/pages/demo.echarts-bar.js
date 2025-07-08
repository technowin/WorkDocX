


const app = () => {

    const basicBarChartInit = () => {
        const chartElement = document.querySelector(".echart-basic-bar-chart-example");

        var myChart = echarts.init(chartElement);

        const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        const data = [1020, 1160, 1300, 958, 1240, 1020, 1409, 1200, 1051, 1120, 1240, 1054];

        var option;

        option = {
            tooltip: {
                trigger: "axis",
                padding: [7, 10],
                backgroundColor: '#fff3cd',
                borderColor: '#cbd0dd',
                textStyle: { color: '#141824' },
                borderWidth: 1,
                // formatter: tooltipFormatter,
                transitionDuration: 0,
                axisPointer: { type: "none" }
            },
            xAxis: {
                type: "category",
                data: months,
                axisLine: { lineStyle: { color: '#cbd0dd', type: "solid" } },
                axisTick: { show: false },
                axisLabel: {
                    color: '#8a94ad',
                    formatter: label => label.substring(0, 3),
                    margin: 15
                },
                splitLine: { show: false }
            },
            yAxis: {
                type: "value",
                boundaryGap: true,
                axisLabel: { show: true, color: '#8a94ad', margin: 15 },
                splitLine: { show: true, lineStyle: { color: '#e3e6ed' } },
                axisTick: { show: false },
                axisLine: { show: false },
                min: 600
            },
            series: [{
                type: "bar",
                name: "Total",
                data: data,
                lineStyle: { color: '#536de6' },
                itemStyle: { color: '#536de6', barBorderRadius: [3, 3, 0, 0] },
                showSymbol: false,
                symbol: "circle",
                smooth: false,
                hoverAnimation: true
            }],
            grid: { right: "3%", left: "10%", bottom: "10%", top: "5%" }
        }

        if (option && typeof option === "object") {
            option && myChart.setOption(option);
        }
    };

    const horizontalBarChartInit = () => {
        const chartElement = document.querySelector(".echart-horizontal-bar-chart-example");
        var myChart = echarts.init(chartElement);

        const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        const data = [1020, 1160, 1300, 958, 1240, 1020, 1409, 1200, 1051, 1120, 1240, 1054];

        var option;

        option = {
            tooltip: {
                trigger: "axis",
                padding: [7, 10],
                backgroundColor: '#fff3cd',
                borderColor: '#cbd0dd',
                textStyle: { color: '#141824' },
                borderWidth: 1,
                // formatter: tooltipFormatter,
                transitionDuration: 0,
                axisPointer: { type: "none" }
            },
            xAxis: {
                type: "value",
                boundaryGap: false,
                axisLine: { show: true, lineStyle: { color: '#cbd0dd' } },
                axisTick: { show: true },
                axisLabel: { color: '#8a94ad' },
                splitLine: { show: false },
                min: 600
            },
            yAxis: {
                type: "category",
                data: months,
                boundaryGap: true,
                axisLabel: {
                    formatter: label => label.substring(0, 3),
                    show: true,
                    color: '#8a94ad',
                    margin: 15
                },
                splitLine: { show: true, lineStyle: { color: '#e3e6ed' } },
                axisTick: { show: false },
                axisLine: { lineStyle: { color: '#cbd0dd' } }
            },
            series: [{
                type: "bar",
                name: "Total",
                data: data,
                lineStyle: { color: '#536de6' },
                itemStyle: { color: '#536de6', barBorderRadius: [0, 3, 3, 0] },
                showSymbol: false,
                symbol: "circle",
                smooth: false,
                hoverAnimation: true
            }],
            grid: { right: "3%", left: "10%", bottom: "10%", top: "0%" }
        }

        if (option && typeof option === "object") {
            option && myChart.setOption(option);
        }
    };

    const barNegativeChartInit = () => {
        const chartElement = document.querySelector(".echart-bar-negative-chart-example");
        var myChart = echarts.init(chartElement);

        var option;

        option = {
            tooltip: {
                trigger: "axis",
                axisPointer: { type: "shadow" },
                padding: [7, 10],
                backgroundColor: '#fff3cd',
                borderColor: '#cbd0dd',
                textStyle: { color: '#141824' },
                borderWidth: 1,
                transitionDuration: 0,
                // formatter: tooltipFormatter
            },
            grid: { top: 5, bottom: 5, left: 5, right: 5 },
            xAxis: {
                type: "value",
                position: "top",
                splitLine: { lineStyle: { type: "dashed", color: '#e3e6ed' } }
            },
            yAxis: {
                type: "category",
                axisLine: { show: false },
                axisLabel: { show: false },
                axisTick: { show: false },
                splitLine: { show: false },
                data: ["Ten", "Nine", "Eight", "Seven", "Six", "Five", "Four", "Three", "Two", "One"]
            },
            series: [{
                name: "Cost",
                type: "bar",
                stack: "total",
                label: { show: true, formatter: "{b}", color: "#fff" },
                itemStyle: { color: '#536de6' },
                data: [-0.15, -0.45, 0.3, 0.55, -0.23, 0.09, -0.56, 0.47, -0.36, 0.32]
            }]
        }

        if (option && typeof option === "object") {
            option && myChart.setOption(option);
        }
    };

    const seriesBarChartInit = () => {
        const chartElement = document.querySelector(".echart-series-bar-chart-example");
        var myChart = echarts.init(chartElement);

        var option;

        option = {
            colors: ["#727cf5", "#0acf97", "#fa5c7c", "#ffbc00"],
            tooltip: {
                trigger: "axis",
                axisPointer: { type: "shadow" },
                padding: [7, 10],
                backgroundColor: '#fff3cd',
                borderColor: '#cbd0dd',
                textStyle: { color: '#141824' },
                borderWidth: 1,
                transitionDuration: 0,
                // formatter: tooltipFormatter
            },
            xAxis: {
                type: "value",
                axisLabel: {
                    formatter: label => `${label / 1000}k`,
                    color: '#8a94ad'
                },
                axisLine: { show: true, lineStyle: { color: '#cbd0dd', type: "solid" } },
                splitLine: { lineStyle: { type: "dashed", color: '#e3e6ed' } }
            },
            yAxis: {
                type: "category",
                axisLine: { show: true, lineStyle: { color: '#cbd0dd', type: "solid" } },
                axisLabel: { color: '#8a94ad' },
                axisTick: { show: false },
                splitLine: { show: false },
                data: ["Brazil", "Indonesia", "USA", "India", "China"]
            },
            series: [{
                name: "2011",
                type: "bar",
                data: [131744, 104970, 29034, 235481, 132541],
                itemStyle: { barBorderRadius: [0, 3, 3, 0] }
            }, {
                name: "2012",
                type: "bar",
                data: [147734, 123220, 30070, 219210, 138240],
                itemStyle: { barBorderRadius: [0, 3, 3, 0] }
            }]
        }

        if (option && typeof option === "object") {
            option && myChart.setOption(option);
        }
    };

    const stackedBarChartInit = () => {
        const chartElement = document.querySelector(".echart-stacked-bar-chart-example");
        var myChart = echarts.init(chartElement);

        var option;

        option = {
            colors: ["#727cf5", "#0acf97", "#fa5c7c", "#ffbc00"],
            tooltip: {
                trigger: "axis",
                axisPointer: { type: "shadow" },
                padding: [7, 10],
                backgroundColor: '#fff3cd',
                borderColor: '#cbd0dd',
                textStyle: { color: '#141824' },
                borderWidth: 1,
                transitionDuration: 0,
                // formatter: tooltipFormatter
            },
            legend: {
                data: ["Direct", "Mail Ad", "Affiliate Ad", "Video Ad"],
                textStyle: { color: '#8a94ad' },
                itemWidth: 10,
                itemHeight: 10,
                icon: "circle",
                left: "0%"
            },
            xAxis: {
                type: "category",
                axisLine: { lineStyle: { color: '#cbd0dd', type: "solid" } },
                axisLabel: { color: '#8a94ad' },
                axisTick: { show: false },
                splitLine: { show: false },
                data: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            },
            yAxis: {
                type: "value",
                axisLine: { show: true, lineStyle: { color: '#cbd0dd', type: "solid" } },
                axisLabel: { color: '#8a94ad' },
                axisTick: { show: false },
                splitLine: { lineStyle: { type: "dashed", color: '#e3e6ed' } }
            },
            series: [{
                name: "Direct",
                type: "bar",
                data: [320, 302, 301, 334, 390, 330, 320],
                itemStyle: { barBorderRadius: [3, 3, 0, 0] }
            }, {
                name: "Mail Ad",
                type: "bar",
                stack: "Ad",
                data: [120, 132, 101, 134, 90, 230, 210],
                itemStyle: { barBorderRadius: [3, 3, 0, 0] }
            }, {
                name: "Affiliate Ad",
                type: "bar",
                stack: "Ad",
                data: [220, 182, 191, 234, 290, 330, 310],
                itemStyle: { barBorderRadius: [3, 3, 0, 0] }
            }, {
                name: "Video Ad",
                type: "bar",
                stack: "Ad",
                data: [150, 212, 201, 154, 190, 330, 410],
                itemStyle: { barBorderRadius: [3, 3, 0, 0] }
            }]
        }

        if (option && typeof option === "object") {
            option && myChart.setOption(option);
        }
    };

    const stackedHorizontalBarChartInit = () => {
        const chartElement = document.querySelector(".echart-stacked-horizontal-bar-chart-example");
        var myChart = echarts.init(chartElement);

        var option;

        option = {
            colors: ["#727cf5", "#0acf97", "#fa5c7c", "#ffbc00"],
            tooltip: {
                trigger: "axis",
                axisPointer: { type: "shadow" },
                padding: [7, 10],
                backgroundColor: '#fff3cd',
                borderColor: '#cbd0dd',
                textStyle: { color: '#141824' },
                borderWidth: 1,
                transitionDuration: 0,
                // formatter: tooltipFormatter
            },
            legend: {
                data: ["Direct", "Mail Ad", "Affiliate Ad", "Video Ad"],
                textStyle: { color: '#8a94ad' },
                itemWidth: 10,
                itemHeight: 10,
                icon: "circle",
                left: "0%"
            },
            xAxis: {
                type: "value",
                axisLine: { show: true, lineStyle: { color: '#cbd0dd', type: "solid" } },
                axisLabel: { color: '#8a94ad' },
                axisTick: { show: false },
                splitLine: { lineStyle: { type: "dashed", color: '#e3e6ed' } }
            },
            yAxis: {
                type: "category",
                axisLine: { lineStyle: { color: '#cbd0dd', type: "solid" } },
                axisLabel: { color: '#8a94ad' },
                axisTick: { show: false },
                splitLine: { show: false },
                data: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            },
            series: [{
                name: "Direct",
                type: "bar",
                data: [320, 302, 301, 334, 390, 330, 320],
                itemStyle: { barBorderRadius: [0, 3, 3, 0] }
            }, {
                name: "Mail Ad",
                type: "bar",
                stack: "Ad",
                data: [120, 132, 101, 134, 90, 230, 210],
                itemStyle: { barBorderRadius: [0, 3, 3, 0] }
            }, {
                name: "Affiliate Ad",
                type: "bar",
                stack: "Ad",
                data: [220, 182, 191, 234, 290, 330, 310],
                itemStyle: { barBorderRadius: [0, 3, 3, 0] }
            }, {
                name: "Video Ad",
                type: "bar",
                stack: "Ad",
                data: [150, 212, 201, 154, 190, 330, 410],
                itemStyle: { barBorderRadius: [0, 3, 3, 0] }
            }]
        }

        if (option && typeof option === "object") {
            option && myChart.setOption(option);
        }
    };

    const barRaceChartInit = () => {
        const chartElement = document.querySelector(".echart-bar-race-chart-example");
        var myChart = echarts.init(chartElement);

        var option;

        option = {
            legend: {},
            tooltip: {
                trigger: "axis",
                axisPointer: { type: "shadow" }
            },
            dataset: {
                source: [
                    ["Product", "2015", "2016", "2017"],
                    ["Matcha", 43.3, 85.8, 93.7],
                    ["Milk", 83.1, 73.4, 55.1],
                    ["Cheese Cocoa", 86.4, 65.2, 82.5],
                    ["Walnut Brownie", 72.4, 53.9, 39.1]
                ]
            },
            xAxis: { type: "category" },
            yAxis: { type: "value" },
            series: [
                { type: "bar", seriesLayoutBy: "row", itemStyle: { color: '#536de6' } },
                { type: "bar", seriesLayoutBy: "row", itemStyle: { color: "#fa5c7c" } },
                { type: "bar", seriesLayoutBy: "row", itemStyle: { color: "#0acf97" } }
            ]
        }

        if (option && typeof option === "object") {
            option && myChart.setOption(option);
        }
    };

    const barGradientChartInit = () => {
        const chartElement = document.querySelector(".echart-bar-gradient-chart-example");
        var myChart = echarts.init(chartElement);

        var option;

        option = {
            tooltip: {
                trigger: "axis",
                axisPointer: { type: "shadow" },
                padding: [7, 10],
                backgroundColor: '#fff3cd',
                borderColor: '#cbd0dd',
                textStyle: { color: '#141824' },
                borderWidth: 1,
                transitionDuration: 0,
                // formatter: tooltipFormatter
            },
            xAxis: {
                type: "category",
                axisLine: { lineStyle: { color: '#cbd0dd' } },
                axisLabel: { color: '#8a94ad' }
            },
            yAxis: {
                type: "value",
                axisLine: { show: true, lineStyle: { color: '#cbd0dd' } },
                splitLine: { lineStyle: { type: "dashed", color: '#e3e6ed' } },
                axisLabel: { color: '#8a94ad' }
            },
            series: [{
                data: [40, 60, 80, 100, 120, 140, 160, 180, 200],
                type: "bar",
                lineStyle: { color: '#536de6' },
                itemStyle: {
                    color: new window.echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: '#536de6' },
                        { offset: 1, color: '#ffbc00' }
                    ])
                }
            }]
        }

        if (option && typeof option === "object") {
            option && myChart.setOption(option);
        }
    };

    const barTimelineChartInit = () => {
        const chartElement = document.querySelector(".echart-bar-timeline-chart-example");
        var myChart = echarts.init(chartElement);

        const months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ];

        const data = {};

        const transformData = (input) => Object.keys(input).reduce((acc, year) => ({
            ...acc,
            [year]: input[year].map((value, index) => ({
                name: months[index],
                value: value
            }))
        }), {});

        data.dataTI = transformData({
            2016: [88.68, 112.38, 1400, 262.42, 589.56, 882.41, 625.61, 684.6, 90.26, 1461.51, 892.83, 966.5],
            2017: [88.8, 103.35, 1461.81, 276.77, 634.94, 939.43, 672.76, 750.14, 93.81, 1545.05, 925.1, 1011.03],
            2018: [101.26, 110.19, 1804.72, 311.97, 762.1, 1133.42, 783.8, 915.38, 101.84, 1816.31, 986.02, 1200.18],
            2019: [112.83, 122.58, 2034.59, 313.58, 907.95, 1302.02, 916.72, 1088.94, 111.8, 2100.11, 1095.96, 1418.09],
            2020: [118.29, 128.85, 2207.34, 477.59, 929.6, 1414.9, 980.57, 1154.33, 113.82, 2261.86, 1163.08, 1495.45],
            2021: [124.36, 145.58, 2562.81, 554.48, 1095.28, 1631.08, 1050.15, 1302.9, 114.15, 2540.1, 1360.56, 1729.02],
            2022: [136.27, 159.72, 2905.73, 641.42, 1306.3, 1915.57, 1277.44, 1701.5, 124.94, 3064.78, 1583.04, 2015.31]
        });

        data.dataSI = transformData({
            2016: [2026.51, 2135.07, 5271.57, 2357.04, 1773.21, 3869.4, 1580.83, 2971.68, 4381.2, 10524.96, 7164.75, 2245.9],
            2017: [2191.43, 2457.08, 6110.43, 2755.66, 2374.96, 4566.83, 1915.29, 3365.31, 4969.95, 12282.89, 8511.51, 2711.18],
            2018: [2509.4, 2892.53, 7201.88, 3454.49, 3193.67, 5544.14, 2475.45, 3695.58, 5571.06, 14471.26, 10154.25, 3370.96],
            2019: [2626.41, 3709.78, 8701.34, 4242.36, 4376.19, 7158.84, 3097.12, 4319.75, 6085.84, 16993.34, 11567.42, 4198.93],
            2020: [2855.55, 3987.84, 8959.83, 3993.8, 5114, 7906.34, 3541.92, 4060.72, 6001.78, 18566.37, 11908.49, 4905.22],
            2021: [3388.38, 4840.23, 10707.68, 5234, 6367.69, 9976.82, 4506.31, 5025.15, 7218.32, 21753.93, 14297.93, 6436.62],
            2022: [3752.48, 5928.32, 13126.86, 6635.26, 8037.69, 12152.15, 5611.48, 5962.41, 7927.89, 25203.28, 16555.58, 8309.38]
        });

        data.dataPI = transformData({
            2016: [4854.33, 1658.19, 3340.54, 1611.07, 1542.26, 3295.45, 1413.83, 1857.42, 4776.2, 6612.22, 5360.1, 2137.77],
            2017: [5837.55, 1902.31, 3895.36, 1846.18, 1934.35, 3798.26, 1687.07, 2096.35, 5508.48, 7914.11, 6281.86, 2390.29],
            2018: [7236.15, 2250.04, 4600.72, 2257.99, 2467.41, 4486.74, 2025.44, 2493.04, 6821.11, 9730.91, 7613.46, 2789.78],
            2019: [8375.76, 2886.65, 5276.04, 2759.46, 3212.06, 5207.72, 2412.26, 2905.68, 7872.23, 11888.53, 8799.31, 3234.64],
            2020: [9179.19, 3405.16, 6068.31, 2886.92, 3696.65, 5891.25, 2756.26, 3371.95, 8930.85, 13629.07, 9918.78, 3662.15],
            2021: [10600.84, 4238.65, 7123.77, 3412.38, 4209.03, 6849.37, 3111.12, 4040.55, 9833.51, 17131.45, 12063.82, 4193.69],
            2022: [12363.18, 5219.24, 8483.17, 3960.87, 5015.89, 8158.98, 3679.91, 4918.09, 11142.86, 20842.21, 14180.23, 4975.96]
        });

        var option;

        option = {
            baseOption: {
                timeline: {
                    axisType: "category",
                    autoPlay: false,
                    playInterval: 1000,
                    data: [
                        "2016-01-01", "2017-01-01", "2018-01-01",
                        "2019-01-01", "2020-01-01", "2021-01-01", "2022-01-01"
                    ],
                    label: { formatter: (value) => new Date(value).getFullYear() },
                    // lineStyle: { color: getColor("info") },
                    // itemStyle: { color: getColor("secondary") },
                    checkpointStyle: {
                        // color: getColor("primary"),
                        shadowBlur: 0,
                        shadowOffsetX: 0,
                        shadowOffsetY: 0
                    },
                    // controlStyle: { color: getColor("info") }
                },
                // title: { textStyle: { color: getColor("tertiary-color") } },
                tooltip: {
                    trigger: "axis",
                    axisPointer: { type: "shadow" },
                    padding: [7, 10],
                    // backgroundColor: getColor("body-highlight-bg"),
                    // borderColor: getColor("border-color"),
                    // textStyle: { color: getColor("light-text-emphasis") },
                    borderWidth: 1,
                    transitionDuration: 0,
                    formatter: tooltipFormatter
                },
                legend: {
                    left: "right",
                    data: ["Primary industry", "Secondary industry", "Tertiary Industry"],
                    // textStyle: { color: getColor("tertiary-color") }
                },
                calculable: true,
                xAxis: [{
                    type: "category",
                    data: months,
                    splitLine: { show: false },
                    // axisLabel: { color: getColor("quaternary-color") },
                    // axisLine: { lineStyle: { color: getColor("quaternary-color") } }
                }],
                yAxis: [{
                    type: "value",
                    axisLabel: {
                        formatter: (value) => value / 1000 + "k",
                        // color: getColor("quaternary-color")
                    },
                    // splitLine: { lineStyle: { color: getColor("secondary-bg") } }
                }],
                series: [
                    {
                        name: "Primary industry",
                        type: "bar",
                        itemStyle: {
                            // color: getColor("primary"),
                            barBorderRadius: [3, 3, 0, 0]
                        }
                    },
                    {
                        name: "Secondary industry",
                        type: "bar",
                        itemStyle: {
                            // color: getColor("info"),
                            barBorderRadius: [3, 3, 0, 0]
                        }
                    },
                    {
                        name: "Tertiary Industry",
                        type: "bar",
                        itemStyle: {
                            // color: getColor("warning"),
                            barBorderRadius: [3, 3, 0, 0]
                        }
                    }
                ],
                grid: {
                    top: "10%",
                    bottom: "15%",
                    left: 5,
                    right: 10,
                    containLabel: true
                }
            },
            options: [
                {
                    title: { text: "2016" },
                    series: [
                        { data: data.dataPI[2016] },
                        { data: data.dataSI[2016] },
                        { data: data.dataTI[2016] }
                    ]
                },
                {
                    title: { text: "2017" },
                    series: [
                        { data: data.dataPI[2017] },
                        { data: data.dataSI[2017] },
                        { data: data.dataTI[2017] }
                    ]
                },
                {
                    title: { text: "2018" },
                    series: [
                        { data: data.dataPI[2018] },
                        { data: data.dataSI[2018] },
                        { data: data.dataTI[2018] }
                    ]
                },
                {
                    title: { text: "2019" },
                    series: [
                        { data: data.dataPI[2019] },
                        { data: data.dataSI[2019] },
                        { data: data.dataTI[2019] }
                    ]
                },
                {
                    title: { text: "2020" },
                    series: [
                        { data: data.dataPI[2020] },
                        { data: data.dataSI[2020] },
                        { data: data.dataTI[2020] }
                    ]
                },
                {
                    title: { text: "2021" },
                    series: [
                        { data: data.dataPI[2021] },
                        { data: data.dataSI[2021] },
                        { data: data.dataTI[2021] }
                    ]
                },
                {
                    title: { text: "2022" },
                    series: [
                        { data: data.dataPI[2022] },
                        { data: data.dataSI[2022] },
                        { data: data.dataTI[2022] }
                    ]
                }
            ]
        }

        if (option && typeof option === "object") {
            option && myChart.setOption(option);
        }
    };

    document.addEventListener("DOMContentLoaded", () => {
        basicBarChartInit();
        horizontalBarChartInit();
        barNegativeChartInit();
        seriesBarChartInit();
        stackedBarChartInit();
        stackedHorizontalBarChartInit();
        barRaceChartInit();
        barGradientChartInit();
        barTimelineChartInit();
    });
}

app()



