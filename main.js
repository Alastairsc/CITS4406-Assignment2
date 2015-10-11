function init(){
    //Setup H2 groups
    titleElements = document.getElementsByClassName("titleRow");
    for (i=0;i<titleElements.length;i++) {
        if (titleElements[i].id != "charts_header")
            titleElements[i].addEventListener("click", showHideGroup(titleElements[i]));
    }

    //Setup 'show more' list sections
    showElements = document.getElementsByClassName("showMore");
    for (i=0;i<showElements.length;i++) {
        showElements[i].addEventListener("click", ShowMore(showElements[i],"List"));
    }

        //Setup 'show more' table sections
    showTableElements = document.getElementsByClassName("showMoreTable");
    for (i=0;i<showTableElements.length;i++) {
        showTableElements[i].addEventListener("click", ShowMore(showTableElements[i],"Table"));
    }

    //Setup charts
    if(google) {
    google.load('visualization', '1.0', {
        packages: ['corechart'],
        callback: function() {}
    } )
}
}
$(function(){
  $("a[href^='#']").click(function(){
    $('html,body').animate({scrollTop: $($(this).attr("href")).offset().top}, 1000);
  });
});
function showChart(type, row,caller){
    document.getElementById("Stats_Chart").classList.remove("hidden");
    document.getElementById("Stats_Chart_data").classList.remove("hidden");

    dataRow = caller.parentNode.parentNode;
    headerRow = caller.parentNode.parentNode.parentNode.childNodes[0];
    document.getElementById("Stats_Chart_data").innerHTML="<table class=\"table table-bordered table-hover\"> "+headerRow.outerHTML+dataRow.outerHTML+"</table>";
    document.getElementById("Stats_Chart_data")
    var options;
    var data;
    var chart;
    if (type=="N"){//Numerical
        data = google.visualization.arrayToDataTable(numbData[row-1]);
        options = {title: 'Histogram:',legend: { position: 'none' },};
        chart = new google.visualization.Histogram(document.getElementById('Stats_Chart'));
    }else if(type=="B" || type=="E"){//boolean/enum = pie chart
        if (type=="B")//Boolean
            data = google.visualization.arrayToDataTable(boolData[row-1]);
        else if (type=="E")//Enum
            data = google.visualization.arrayToDataTable(enumData[row-1]);
        options = {title: 'Pie Chart:'};
        chart = new google.visualization.PieChart(document.getElementById('Stats_Chart'));
    }else if(type=="S"){//String
        data = google.visualization.arrayToDataTable(stringData[row-1]);
        options = {title: 'Column Graph - Top 10 common strings'};
        chart = new google.visualization.ColumnChart(document.getElementById('Stats_Chart'));
    }else if(type=="Em"){//Email
        data = google.visualization.arrayToDataTable(emailData[row-1]);
        options = {title: 'Column Graph - Top 10 common emails'};
        chart = new google.visualization.ColumnChart(document.getElementById('Stats_Chart'));
    }else if(type=="I"){//Identifier
        data = google.visualization.arrayToDataTable(identData[row-1]);
        options = {title: 'Column Graph - Top 10 common identifiers'};
        chart = new google.visualization.ColumnChart(document.getElementById('Stats_Chart'));
    }else if(type=="C"){//Currency
        data = google.visualization.arrayToDataTable(currencyData[row-1]);
        options = {title: 'Histogram:',legend: { position: 'none' },};
        chart = new google.visualization.Histogram(document.getElementById('Stats_Chart'));
    }
    chart.draw(data, options);

}

function ShowMore(ele, ListOrTable){
    return function(){
        var siblings = ele.parentNode.parentNode.childNodes;
        if (ListOrTable == "List")
            siblings = ele.parentNode.childNodes;
        for (i=0;i<siblings.length;i++){
            sib = siblings[i];
            if (sib.classList && sib.classList.contains('hidden')){
                sib.classList.remove('hidden');
                sib.classList.add('canhide');
            }else if (sib.classList && sib.classList.contains('canhide')){
                sib.classList.remove('canhide');
                sib.classList.add('hidden');
            }
        }
        if (ele.innerHTML=="Show More"){
            ele.innerHTML="Hide";
        }else{
            ele.innerHTML="Show More";
        }

    }
}

function showHideGroup(ele){
    return function(){
        var siblings = ele.parentNode.childNodes;
        passedMyself = false;
        for (i=0;i<siblings.length;i++){
            sib = siblings[i];
            if (sib==ele){
                passedMyself = true;
                continue;}
            if (passedMyself && sib.classList ){
                if (sib.tagName==="H2")
                break;
                if (sib.classList.contains('hidden'))
                    sib.classList.remove('hidden');
                else
                    sib.classList.add('hidden');
            }
        }
    } 
}