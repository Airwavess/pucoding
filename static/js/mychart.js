  window.onload = function() {
    if ($("#search-name").val() !== "") 
      search()
  }
  var randomScalingFactor = function() {
    return (Math.random() > 0.5 ? 1.0 : -1.0) * Math.round(Math.random() * 100);
  };
  var randomColorFactor = function() {
    return Math.round(Math.random() * 255);
  };
  var randomColor = function() {
    return 'rgba(' + randomColorFactor() + ',' + randomColorFactor() + ',' + randomColorFactor() + ',.7)';
  };

  function changeColor() {
    var color = []
    for (var i = 0; i < 16; i++) {
      color[i] = randomColor()
    }
    return color
  }

  function showChart(level, num_of_cpl) {
    var ctx = document.getElementById("myChart");

    var data = {
      labels: level,
      datasets: [{
        label: "題數",
        backgroundColor: changeColor(),
        borderColor: changeColor(),
        data: num_of_cpl
      }]
    };

    var myChart = new Chart(ctx, {
      type: 'bar',
      data: data,
      options: {
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true,
              steps: 4,
              stepValue: 5,
              max: 10,
              scaleStepWidth: 5
            }
          }]
        }
      },
      xAxisID: "Name",
      yAxisID: "aaa",
    });
  }

  function search() {
    $.ajax({
      url: '/get_personal_score/',
      type: "POST",
      data: {
        "search-name": $("#search-name").val()
      },
      dataType: "json",
      success: function(json) {
        if (json.fail == "fail") {
          $('#myModal').modal('show')
        } else {
          var level = [];
          var num_of_cpl = [];
          for (var i = 0; i < json.length; i++) {
            level[i] = json[i].fields.sc_level.split("(初心者")[0]
            if (level[i].indexOf("(魔王") != -1)
              level[i] = json[i].fields.sc_level.split("(魔王")[0]
            num_of_cpl[i] = json[i].fields.sc_num_of_cpl
          }
          showChart(level, num_of_cpl)
        }
      }
    });
  }