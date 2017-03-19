function formatNum(str){
	var newStr = "";
	var count = 0;

	if (str.indexOf(".") == -1) {
		for (var i = str.length - 1; i >= 0; i--) {
			if (count % 3 == 0 && count != 0) {
				newStr = str.charAt(i) + "," + newStr;
			} else {
				newStr = str.charAt(i) + newStr;
			}
			count++;
		}
		str = newStr + ".00"; 
		return str;
	} else {
			for (var i = str.indexOf(".") - 1; i >= 0; i--){
			if (count % 3 == 0 && count != 0) {
				newStr = str.charAt(i) + "," + newStr;
			} else {
				newStr = str.charAt(i) + newStr;
			}
			count++;
		}
		str = newStr + (str + "00").substr((str + "00").indexOf("."),3);
		return str;
	}
}

function showDetails(code) {
	$("#detailArea").empty();
	$("#detailArea").html("<table id='detailTable' class='striped'><tr><th>Code</th><th>Date</th><th>Direction</th><th>Volumn</th><th>Price</th></tr></table>");
	var detailTable = document.getElementById("detailTable");
	Papa.parse("/job/trade.csv", {
		download: true,
		complete: function(results) {
			var data = results.data;
			var detailTable = document.getElementById("detailTable");
			var detailTableRowNum = 1;
			for (var i = 1; i < data.length; i++) {
				var item = data[i];
				if (item[0] == code) {
					var row = detailTable.insertRow(detailTableRowNum++);
					for (j = 0; j < item.length; j++) {
						var cell = row.insertCell(j);
						if (j == 4) {
							var stockPrice = (parseFloat(item[j])).toFixed(2);
							cell.innerHTML = stockPrice;
						} else {
							cell.innerHTML = item[j];
						}
					}
				}
			}
		}
	});
}

$(document).ready(function() {
	var countProfit = 0;
	var countDeficit = 0;
	var countFair = 0;
	Papa.parse("/job/benchmark.csv", {
		download: true,
		complete: function(results) {
			// console.log(results);
			// console.log(results.data);
			var data = results.data;
			var sumTable = document.getElementById("sumTable"); 
			for (var i = 1; i < data.length; i++) {
				var item = data[i];
				if (item[1] > 0) {
					countProfit++;
				} else if (item[1] < 0) {
					countDeficit++;
				} else {
					countFair++;
				}
				var row = sumTable.insertRow(i);
				for (var j = 0; j < item.length; j++) {
					var cell = row.insertCell(j);
					if (j == 0) {
						cell.innerHTML = "<a style='cursor:pointer' onclick='showDetails(this.innerHTML)'>" + item[j] + "</a>";
					} else if (j == 1) {
						var profitValue = (parseFloat(item[j])).toFixed(2);
						if (profitValue > 0) {
							profitValue = formatNum(profitValue);
							cell.innerHTML = "<font color='red'>" + profitValue + "</font>";
						} else if (profitValue < 0) {
							profitValue = -(parseFloat(profitValue)) + "";
							profitValue = formatNum(profitValue.toString());
							profitValue = "-" + profitValue;
							cell.innerHTML = "<font color='green' >" + profitValue + "</font>";
						} else {
							cell.innerHTML = "<font color='grey' >" + profitValue + "</font>";
						}
					} else {
						cell.innerHTML = item[j];
					}
				}
				
			}
			console.log("Count for profit stocks: " + countProfit);
			console.log("Count for deficit stocks: " + countDeficit);
			console.log("Count for fair stocks: " + countFair);
			var chartData = [{name: "Profit", y: countProfit, color: "red", sliced: true, selected: true,},
							 {name: "Deficit", y: countDeficit, color: "green"},
							 {name: "Fair", y: countFair, color: "blue"}]
			var chart = {
				plotBackgroundColor: null,
				plotBorderWidth: null,
				plotShadow: false
			};
			var title = {
				text: "Stock Chart"
			}; 
			var plotOptions = {
				pie: {
					allowPointSelect: true,
					cursor: 'pointer',
					dataLabels: {
						enabled: false           
					},	
					showInLegend: true
				}
			};
			var series = [{
				type: "pie",
				name: "Count",
				data: chartData
			}];
			var json = {};
			json.chart = chart;
			json.title = title;
			json.plotOptions = plotOptions;
			json.series = series;
			$('#chartArea').highcharts(json);  
		}
	});
	var title = {
		text: "Strategy Analysis" 
	};
	var subtitle = {
		text: "Source: StockAnt.com"
	};
	var xAxis = {
		categories: ['2015-Jan', '2015-Feb', '2015-Mar', '2015-Apr', '2015-May', '2015-Jun', '2015-Jul', '2015-Aug', '2015-Sep', '2015-Oct', '2015-Nov', '2015-Dec']
	};
	var yAxis = {
		title: {
			text: "P & L(M)"
		}
	};
	var plotOptions = {
		line: {
			dataLabels: {
				enabled: true
			},   
			enableMouseTracking: false
		}
	};
	var series= [{
		name: 'Strategy1',
		data: [-2.8, 3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 15.3, 20.6]
		}
	];
	var curveJson = {};
	curveJson.title = title;
	curveJson.subtitle = subtitle;
	curveJson.xAxis = xAxis;
	curveJson.yAxis = yAxis;  
	curveJson.series = series;
	curveJson.plotOptions = plotOptions;
	$("#curveArea").highcharts(curveJson);
});