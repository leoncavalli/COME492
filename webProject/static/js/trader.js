
$(document).ready(function () {
  statvalues = $('.statvalue');

  cash = parseInt(cash);
  let initialBudget = parseInt(statvalues[0].textContent);
  let finalBudget = parseInt(statvalues[1].textContent);
  finalBudget = finalBudget + cash;

  let initialBudgetString = initialBudget.toLocaleString(
    undefined,
    { minimumFractionDigits: 2 }
  );
  let finalBudgetString = finalBudget.toLocaleString(
    undefined,
    { minimumFractionDigits: 2 }
  );
  statvalues[0].innerHTML = "$" + initialBudgetString;
  statvalues[1].innerHTML = "$" + finalBudgetString;


  let profitpercentage = (finalBudget / initialBudget * 100) - 100;
  profitpercentage = profitpercentage.toFixed(2);
  $('.chart').data('easyPieChart').update(profitpercentage);
  $('#profitchart span').text("%" + profitpercentage);


  finalportfolio = JSON.parse(finalportfolio.replace(/&quot;/g, '"'));
  latests=JSON.parse(latests.replace(/&quot;/g,'"'));

  Object.keys(finalportfolio).forEach(key => {
    if (finalportfolio[key] === 0) {
      delete finalportfolio[key];
    }
  });

  let currentvalue=0;
  Object.keys(finalportfolio).forEach(key=>{
      currentvalue+=latests[key]*finalportfolio[key];
  })
  let currentValueStr = currentvalue.toLocaleString(
    undefined,
    { minimumFractionDigits: 2 }
  );
  statvalues[2].innerHTML = "$" + currentValueStr;






  stocks = Object.keys(finalportfolio);
  stockquantity = Object.values(finalportfolio);

  if (stocks.length > 0)
   {
    var ctx = document.getElementById('myChart');
    data = {
      datasets: [{
        data: stockquantity,
        backgroundColor: ["#3e95cd", "#8e5ea2", "#00000", "#ccc", "#33333", "#55555", "#55555"],

      }],
      labels: stocks
    };
    var myDoughnutChart = new Chart(ctx, {
      type: 'pie',  
      data: data,
    });
  }
  else {
    let msg = "There are no stocks in your portfolio.";
    $('#chartjs-wrapper').text(msg);
  }
})

