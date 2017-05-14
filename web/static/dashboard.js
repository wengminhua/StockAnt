function initBenchmarkTable() {
   $("#benchmark-table").bootstrapTable({
      method: "GET",
      dataType: "json",
      cache: false,
      sidePagination: "client",
      url: "/api/benchmark",
      pagination: true,
      search: true,
      columns: [{
            field: "id",
            title: "ID",
            align: "right",
            formatter: function (value, row, index) {
                return index + 1;
            }
        },{
            field: "code",
            title: "Code",
            align: "center",
            sortable: true,
            formatter: function (value, row, index) {
                return ["<a href=\"javascript:onClickStock('" + value + "');\">",
                        value,
                        "</a>"].join('');
            }
        },{
            field: "pnl",
            title: "P&L",
            align: "right",
            sortable: true,
            formatter: function (value, row, index) {
                var color = "grey";
                if (value > 0) {
                    color = "red";
                } else if (value < 0) {
                    color = "green";
                }
                return ["<font color='" + color + "'>",
                        $.getFormattedCurrency(value),
                        "</font>"].join('');
            }
        }]
   });
}

function initTradeTable() {
    $("#trade-table").bootstrapTable({
      cache: false,
      sidePagination: "client",
      pagination: true,
      search: true,
      columns: [{
                    field: "id",
                    title: "ID",
                    align: "right",
                    formatter: function (value, row, index) {
                        return index + 1;
                    }
                },{
                    field: "date",
                    title: "Date",
                    align: "center",
                    sortable: true,
                    formatter: function (value, row, index) {
                        return ["<a href=\"javascript:onClickTradeDate('" + value + "')\">",
                                value,
                                "</a>"].join('');
                    }
                },{
                    field: "price",
                    title: "Price",
                    align: "right",
                    sortable: false,
                    formatter: function (value, row, index) {
                        return $.getFormattedCurrency(value);
                    }
                },{
                    field: "volume",
                    title: "Volume",
                    align: "right",
                    sortable: false,
                    formatter: function (value, row, index) {
                        var color = "grey";
                        var direction = "";
                        if (row.direction == "buy") {
                            color = "red";
                            direction = "+";
                        } else if (row.direction == "sell") {
                            color = "green";
                            direction = "-";
                        }
                        return ["<font color='" + color + "'>",
                                direction,
                                value,
                                "</font>"].join('');
                    }
                }]
   });
}

function initTradeChart() {
    if(window.tradeChart && window.tradeChart!=null) {
        echarts.dispose(document.getElementById("trade-chart"));
        window.tradeChart = null;
    }
    window.tradeChart = echarts.init(document.getElementById("trade-chart"));
}

function loadTradeTable(code) {
    $.ajax({
        type: "GET",
        url: "/api/trade/" + code,
        dataType: "json",
        success: function(result) {
            $("#trade-table").bootstrapTable("load", result);
        },
        error: function() {
            $("#trade-table").bootstrapTable("removeAll");
            alert("Load trade information failed.");
        }
    });
}

function loadTradeChart(code) {
    $.ajax({
        type: "GET",
        url: "/api/chart/" + code,
        dataType: "json",
        success: function(result) {
            showTradeChart(code, result);
        },
        error: function() {
            initTradeChart();
            alert("Load chart information failed.");
        }
    });
}

function showTradeChart(code, result) {
    // TOP_MARGIN contains the height of legend
    var TOP_MARGIN = 40;
    var LEFT_MARGIN = 50;
    var RIGHT_MARGIN = 50;
    // PADDING contains the height of x-axis
    var PADDING = 30;
    var TRADE_HEIGHT = 20;
    var KLINE_HEIGHT = 550;
    var VOLUME_HEIGHT = 160;
    var ZOOM_SLIDER_HEIGHT = 35;

    // Adjust Chart Height
    var totalHeight = TOP_MARGIN
                      + KLINE_HEIGHT + PADDING
                      + VOLUME_HEIGHT + PADDING
                      + ZOOM_SLIDER_HEIGHT;
    $("#trade-chart").css("height", totalHeight + "px");
    initTradeChart();

    var option = {
        title: {
            text: "",
            left: 0
        },
        tooltip: {
            trigger: "axis",
            axisPointer: {
                type: "cross"
            }
        },
        legend: {
            top: 10,
            data: ["K-Line","Buy","Sell"]
        },
        grid: [
            {
                left: LEFT_MARGIN,
                right: RIGHT_MARGIN,
                top: TOP_MARGIN,
                height: KLINE_HEIGHT
            },
            {
                left: LEFT_MARGIN,
                right: RIGHT_MARGIN,
                top: TOP_MARGIN + KLINE_HEIGHT + PADDING,
                height: VOLUME_HEIGHT
            },
            {
                left: LEFT_MARGIN,
                right: RIGHT_MARGIN,
                top: TOP_MARGIN,
                height: TRADE_HEIGHT
            }
        ],
        xAxis: [
            {
                type: 'category',
                data: result.categoryData,
                scale: true,
                boundaryGap: false,
                axisLine: {onZero: false},
                splitLine: {show: false},
                splitNumber: 20,
                min: "dataMin",
                max: "dataMax"
            },
            {
                type: 'category',
                gridIndex: 1,
                data: result.categoryData,
                scale: true,
                boundaryGap: false,
                axisLine: {onZero: false},
                axisTick: {show: false},
                splitLine: {show: false},
                axisLabel: {show: false},
                splitNumber: 20,
                min: "dataMin",
                max: "dataMax"
            },
            {
                type: 'category',
                gridIndex: 2,
                data: result.categoryData,
                scale: true,
                boundaryGap: false,
                axisLine: {show: false},
                axisTick: {show: false},
                splitLine: {show: false},
                axisLabel: {show: false},
                splitNumber: 20,
                min: "dataMin",
                max: "dataMax"
            }
        ],
        yAxis: [
            {
                scale: true,
                splitArea: {show: true}
            },
            {
                scale: true,
                gridIndex: 1,
                splitNumber: 2,
                axisLabel: {show: false},
                axisLine: {show: true},
                axisTick: {show: false},
                splitLine: {show: false}
            },
            {
                scale: true,
                gridIndex: 2,
                splitNumber: 2,
                min: -1,
                max: 1,
                axisLabel: {show: false},
                axisLine: {show: false},
                axisTick: {show: false},
                splitLine: {show: false}
            }
        ],
        dataZoom: [
            {
                type: "inside",
                xAxisIndex: [0, 1, 2],
                start: 95,
                end: 100
            },
            {
                show: true,
                xAxisIndex: [0, 1, 2],
                type: "slider",
                y: TOP_MARGIN + KLINE_HEIGHT + PADDING + VOLUME_HEIGHT + PADDING,
                height: ZOOM_SLIDER_HEIGHT,
                start: 95,
                end: 100
            }
        ],
        series: [
            {
                name: "K-Line",
                type: "candlestick",
                data: result.kLineData
            },
            {
                name: "Volume",
                type: "bar",
                xAxisIndex: 1,
                yAxisIndex: 1,
                data: result.volumeData
            },
            {
                name: "Buy",
                type: "scatter",
                symbol: "circle",
                xAxisIndex: 2,
                yAxisIndex: 2,
                data: result.tradeData.buyData
            },
            {
                name: "Sell",
                type: "scatter",
                symbol: "diamond",
                xAxisIndex: 2,
                yAxisIndex: 2,
                data: result.tradeData.sellData
            }
        ]
    };
    // Append strategy chart option
    for(var i=0; i<result.strategyChartList.length; i++) {
        strategyChart = result.strategyChartList[i];
        if(strategyChart.index==0) {
            strategySeries = {
                name: strategyChart.name,
                type: strategyChart.type,
                data: strategyChart.data
            };
            option.series.push(strategyChart);
            option.legend.data.push(strategyChart.name);
        }
    }

    window.tradeChart.setOption(option);
}

function chartZoomTo(zoomDate) {
    var DAY_HALF_RANGE = 15;
    var dateList = window.tradeChart.getOption().xAxis[0].data;
    var zoomDateIndex = -1;
    for(var i=0; i<dateList.length; i++) {
        if(dateList[i]==zoomDate) {
            zoomDateIndex = i;
            break;
        }
    }
    if(zoomDateIndex>=0)
    {
        var startDateIndex = zoomDateIndex - DAY_HALF_RANGE;
        if(startDateIndex<0) {
            startDateIndex = 0;
        }
        var endDateIndex = startDateIndex + DAY_HALF_RANGE * 2;
        if(endDateIndex>=dateList.length) {
            endDateIndex = dateList.length - 1;
        }
        var option = {
            dataZoom: [
                {
                    startValue: dateList[startDateIndex],
                    endValue: dateList[endDateIndex]
                },
                {
                    startValue: dateList[startDateIndex],
                    endValue: dateList[endDateIndex]
                }
            ],
        };
        window.tradeChart.setOption(option);
    }
}

function onClickStock(code) {
    $("#trade-table-title").html(code);
    loadTradeTable(code);
    loadTradeChart(code);
}

function onClickTradeDate(date) {
    chartZoomTo(date);
}
