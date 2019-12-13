@extends('layout.master')
@section('content')

<!-- Styles -->
<style>
    #chartdiv {
        width: 100%;
        height: 500px
    }

    body {
        background-color: #e9efec;
        background-image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1NiIgaGVpZ2h0PSIxMDAiPgo8cGF0aCBkPSJNMjggNjZMMCA1MEwwIDE2TDI4IDBMNTYgMTZMNTYgNTBMMjggNjZMMjggMTAwIiBmaWxsPSJub25lIiBzdHJva2U9IiNmZmYiIHN0cm9rZS13aWR0aD0iMSI+PC9wYXRoPgo8L3N2Zz4=);
        font-family: "Oswald", "Helvetica Newe", Helvetica, sans-serif;
    }
</style>
<nav class="navbar navbar-expand-lg navbar-light bg-light" style="margin-bottom: 2em">
    <ul class="nav nav-pills">
        <li class="nav-item">
            <a class="nav-link active" href="/mapDashboard">Heat Map</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="/detailDashboard">Detail Dashboard</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="/stateDashboard">State Dashboard</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="/restaurantDashboard">Food Chain Dashboard</a>
        </li>
</nav>
<div class="container">
    <hr>
    <div class="row">
        <div class="col-sm-6 offset-4">
            <form method="POST" action="/viewMap" class="form-inline" name="restaurantSelectForm">
                {{-- <div class="form-group mb-2">
                        <label>Select State</label>
                    </div> --}}
                <div class="form-group mx-sm-3 mb-2">
                    <select class="form-control" id="restaurantSelect" name="restaurant" required>
                        @if (Request::isMethod('post'))
                        <option selected value="{{ $selected }}">{{ $selected }}</option>
                        @foreach ($restaurants as $restaurant)
                        <option>{{$restaurant}}</option>
                        @endforeach
                        @else
                        <option selected disabled value="">Select Food Chain...</option>
                        @foreach ($restaurants as $restaurant)
                        <option>{{$restaurant}}</option>
                        @endforeach
                        @endif
                    </select>
                </div>
                <input type="hidden" name="_token" value="{{ csrf_token() }}">
                <input type="submit" class="btn btn-primary mb-2" value="Go">
            </form>
        </div>
    </div>

    <hr>
    <?php if($_SERVER['REQUEST_METHOD'] == 'POST') { ?>
    <div>
        <p class="lead"><small class="text-muted">Most Popular </small> {{ $mostpos_key }} : {{ $mostpos }} </p>
    </div>
    <div>
        <p class="lead">Heat Map</p>
        {{-- @foreach ($popularity as $key => $value)
            dd{{ $key }}
        dd{{ $value }}
        @endforeach --}}
        <div id="chartdiv"></div>
    </div>
    <?php } ?>
</div>

<?php if($_SERVER['REQUEST_METHOD'] == 'POST') { ?>
<script src="https://www.amcharts.com/lib/4/core.js"></script>
<script src="https://www.amcharts.com/lib/4/maps.js"></script>
<script src="https://www.amcharts.com/lib/4/geodata/usaLow.js"></script>
<script src="https://www.amcharts.com/lib/4/themes/animated.js"></script>

<!-- Chart code -->
<script>
    am4core.ready(function() {
    
    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end
    
     // Create map instance
    var chart = am4core.create("chartdiv", am4maps.MapChart);
    
    // Set map definition
    chart.geodata = am4geodata_usaLow;
    
    // Set projection
    chart.projection = new am4maps.projections.AlbersUsa();
    
    // Create map polygon series
    var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());
    
    //Set min/max fill color for each area
    polygonSeries.heatRules.push({
      property: "fill",
      target: polygonSeries.mapPolygons.template,
      min: chart.colors.getIndex(1).brighten(1),
      max: chart.colors.getIndex(1).brighten(-0.3)
    });
    
    // Make map load polygon data (state shapes and names) from GeoJSON
    polygonSeries.useGeodata = true;
    
    // Set heatmap values for each state
    polygonSeries.data = [

        <?php
        // $i=1;
        // $end = count($popularity); 
        foreach($popularity as $key => $value) {
           
                echo '{ id: "US-'.$key.'",value: '.$value.'},'; 


        }
      ?>
      {}
    ];
    
    // Set up heat legend
    let heatLegend = chart.createChild(am4maps.HeatLegend);
    heatLegend.series = polygonSeries;
    heatLegend.align = "right";
    heatLegend.valign = "bottom";
    heatLegend.width = am4core.percent(20);
    heatLegend.marginRight = am4core.percent(4);
    heatLegend.minValue = 0;
    heatLegend.maxValue = 100;
    
    // Set up custom heat map legend labels using axis ranges
    var minRange = heatLegend.valueAxis.axisRanges.create();
    minRange.value = heatLegend.minValue;
    minRange.label.text = "Little";
    var maxRange = heatLegend.valueAxis.axisRanges.create();
    maxRange.value = heatLegend.maxValue;
    maxRange.label.text = "A lot!";
    
    // Blank out internal heat legend value axis labels
    heatLegend.valueAxis.renderer.labels.template.adapter.add("text", function(labelText) {
      return "";
    });
    
    // Configure series tooltip
    var polygonTemplate = polygonSeries.mapPolygons.template;
    polygonTemplate.tooltipText = "{name}: {value}";
    polygonTemplate.nonScalingStroke = true;
    polygonTemplate.strokeWidth = 0.5;
    
    // Create hover state and set alternative fill color
    var hs = polygonTemplate.states.create("hover");
    hs.properties.fill = am4core.color("#3c5bdc");
    
    }); // end am4core.ready()
</script>

<?php } ?>
@endsection