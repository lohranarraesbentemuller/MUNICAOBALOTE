<?php
include("config.php");
include("session.php");
include("menu.php");
echo '<script src="https://code.jquery.com/jquery-3.3.1.js"></script>';
?>
<script type="text/javascript" language="javascript" src="https://code.jquery.com/jquery-3.3.1.js"></script>
<script>
    if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
    }
</script>
<html>

<!--- teste -->
<style type="text/css">
/*.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;}
.tg .tg-llyw{background-color:#c0c0c0;border-color:inherit;text-align:left;vertical-align:top}
.tg .tg-rq3n{background-color:#ffffff;border-color:inherit;text-align:center;vertical-align:middle}
.tg .tg-c6of{background-color:#ffffff;border-color:inherit;text-align:left;vertical-align:top}*/
</style>
<style>

  #titulo{
	  font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";
	  padding:10px;
	  text-align: center;
  }
  label{
	  font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";
	  font-size:12px;
  }
  #datatables_length{
	  font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";
	  font-size:12px;
  }
  #example_info{
	  font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";
	  font-size:12px;
  }
  #input{
	  font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";
	  font-size:12px;
  }
  #example{
	  font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";
	  font-size:12px;
  }
  label{
	  font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";
  }
  .paginate_button{
	    background-color: white;
        color: black;
        border: 2px solid black; /* Green */
		font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";
		font-size:12px;
		margin:2%;
  }
    .paginate_button:hover{
	    background-color: black;
        color: white;
        border: 1px solid black; /* Green */
		font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";
		font-size:14px;
  }
  </style>

 <head>
 <link rel="shortcut icon" type="image/png" href="/favicon.png"/>

	<meta http-equiv="Content-type" content="text/html; charset=utf-8">
	<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
	<title>Escalas</title>
	
	<link rel="alternate" type="application/rss+xml" title="RSS 2.0" href="http://www.datatables.net/rss.xml">
	
	<!--<link rel="stylesheet" type="text/css" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">-->
	<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.20/css/dataTables.bootstrap.min.css">
	<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/fixedheader/3.1.6/css/fixedHeader.bootstrap.min.css">
	<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/responsive/2.2.3/css/responsive.bootstrap.min.css">
	<style type="text/css" class="init">
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
	</style>

   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
	<!-- Bootstrap Date-Picker Plugin -->
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.4.1/js/bootstrap-datepicker.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.4.1/css/bootstrap-datepicker3.css"/>
    
	<link rel="stylesheet" href="../zTree_v3-master/css/zTreeStyle/zTreeStyle.css" type="text/css">
	<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
	<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/1.10.20/js/dataTables.bootstrap.min.js"></script>
	<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/fixedheader/3.1.6/js/dataTables.fixedHeader.min.js"></script>
	
	<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/responsive/2.2.3/js/responsive.bootstrap.min.js"></script>
<script src="https://cdn.datatables.net/buttons/1.6.0/js/dataTables.buttons.min.js"></script>
<script src="https://cdn.datatables.net/buttons/1.6.0/js/buttons.flash.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.1.3/jszip.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/pdfmake.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/vfs_fonts.js"></script>
<script src="https://cdn.datatables.net/buttons/1.6.0/js/buttons.html5.min.js"></script>
<script src="https://cdn.datatables.net/buttons/1.6.0/js/buttons.print.min.js"></script>
	<script type="text/javascript" class="init"></script>
<script>
$(document).ready(function() {
	    $('td').css("vertical-align","middle");
        $('td').css("font-size","12px");
        $('th').css("font-size","13px");

	var date_input=$('input[name="data"]'); //our date input has the name "date"
      var container=$('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : "body";
      var options={
        //format: 'mm/dd/yyyy',
		format: 'yyyy-mm-dd',
        container: container,
        todayHighlight: true,
        autoclose: true,
      };
      date_input.datepicker(options);
	
	
	var table = $('#example').DataTable( {
	 responsive: true,
         dom: 'Blfrtip',
         buttons: ['excel'],
		     
        "iDisplayLenght": 100,
        "aLengthMenu":[[10,25,50,100,500,1000,10000],[10,25,50,100,500,1000,'10mil']],
	       "language": {
                        "sProcessing":   "",
                        "sLengthMenu":   "_MENU_ por página",
                        "sZeroRecords":  "Não foram encontrados resultados",
                        "sInfo":         "_START_ até _END_ de _TOTAL_ elementos",
                        "sInfoEmpty":    "0 registros",
                        "sInfoFiltered": "",
                        "sInfoPostFix":  "",
                        "sSearch":       "Buscar:",
                        "sUrl":          "",
                        "oPaginate": {
                                "sFirst":    "Primeiro",
                                "sPrevious": "Anterior",
                                "sNext":     "Seguinte",
                                "sLast":     "Último"
                        }
                 },

         columns: [
		 { data: "nome"},
		 { data: "lat"},
          { data: "lng"},
		  { data: "data"},
		  { data: "placa"}
	  
	],
        "ajax": 'getEstabelecimentos.php',
     //   "columnDefs": [
      //      {
       //         "render": function ( data, type, row ) { 
        //            return " <a class =\"fancy\" data-fancybox-type=\"iframe\" href=\"entrada_usuario?id=" + row['id'] + " \">"  + data  + "</a>";//data +' ('+ row[3]+')';
       //         },
       //         "targets": 0
        //    },
	//		{ "visible": false,  "targets": [ 0 ] }
     //   ],
	
 
			
	
	} );
var table = $('#example2').DataTable( {
	 responsive: true,
         dom: 'Blfrtip',
         buttons: ['excel'],
		     
        "iDisplayLenght": 100,
        "aLengthMenu":[[10,25,50,100,500,1000,10000],[10,25,50,100,500,1000,'10mil']],
	       "language": {
                        "sProcessing":   "",
                        "sLengthMenu":   "_MENU_ por página",
                        "sZeroRecords":  "Não foram encontrados resultados",
                        "sInfo":         "_START_ até _END_ de _TOTAL_ elementos",
                        "sInfoEmpty":    "0 registros",
                        "sInfoFiltered": "",
                        "sInfoPostFix":  "",
                        "sSearch":       "Buscar:",
                        "sUrl":          "",
                        "oPaginate": {
                                "sFirst":    "Primeiro",
                                "sPrevious": "Anterior",
                                "sNext":     "Seguinte",
                                "sLast":     "Último"
                        }
                 },

         columns: [
		 { data: "id"},
          { data: "nome"},
		  { data: "mensagem"},
		  { data: "resposta"},
		  { data: "data"}
	  
	],
        "ajax": 'getAuditoria.php',
     //   "columnDefs": [
      //      {
       //         "render": function ( data, type, row ) { 
        //            return " <a class =\"fancy\" data-fancybox-type=\"iframe\" href=\"entrada_usuario?id=" + row['id'] + " \">"  + data  + "</a>";//data +' ('+ row[3]+')';
       //         },
       //         "targets": 0
        //    },
	//		{ "visible": false,  "targets": [ 0 ] }
     //   ],
	
 
			
	
	} );


	$("#data").change(function(){
		 
	var ano=($(this).val()).split("-")[0];
	var mes=($(this).val()).split("-")[1];
	var dia=($(this).val()).split("-")[2];
	var data=new Date(ano, mes, dia);
	var url="Dia_da_semana.php?data="+$(this).val();
	console.log(url);
    $.get(url,function(data){
	    //console.log(data); 
		//sabado é 6
		if(data==5)
		{
			$('#cor').val("Azul");
		}
		if(data==6)
		{
			$('#cor').val("Vermelha");
		}
		if(data==0)
		{
			$('#cor').val("Vermelha");
		}
		if(data>0 && data<5)
			$('#cor').val("Preta");
     });
	});
	
	$(".a").css("display","none");//teste aqui
	$("#Postoss").css("display","none");
	$("#sort").change(function(){
		var escala=$(this).val();
		//console.log(escala);
		$(".a").css("display","inline");//teste aqui
		$("#Postoss").css("display","inline");
		$("#checkboxes").children().each(function(index){
			$(this).prop("checked", false);
			var a =($(this).attr("class"));
			if(a!=null)
			{
			a=a.toString();
			a=a.split(escala);
			console.log(a);
			
			//if($(this).attr("class")==escala)
			if(a.length>1)	
			{
			  $(this).css("display","inline");
			}
			else
			{
		      $(this).css("display","none");
			}
			}
		});
	});


$(function(){
    //$('.myCalendar').calendar({
	//date = new Date(),
	//autoSelect: true,
	//select: function(date){
	//console.log('SELECT',date);
//	}
//	 toggle: function(y, m) {
  //  console.log('TOGGLE', y, m)
   // }
  // });

//$('.myCalendar').calendar({
 // date: new Date(),
 // autoSelect: true
//});



});
	
});


 
</script>
<style>
/*
button span {
  display: none;
}
.mobile-container {
  max-width: 480px;
  margin: auto;
  height: 500px;
  color: black;
  border-radius: 10px;
}

.topnav {
  overflow: hidden;
  background-color: #333;
  position: relative;
}

.topnav #myLinks {
  display: none;
}

.topnav a {
  color: white;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 17px;
  display: block;
}

.topnav a.icon {
  background: black;
  display: block;
  position: absolute;
  right: 0;
  top: 0;
}

.topnav a:hover {
  background-color: #ddd;
  color: black;
}

.active { */
/*  background-color: #007bff;
  background-color: silver;
  color: white;
}*/

</style>
<link rel="stylesheet" href="../APMB2/responsive-nao-calendar/aicon/style.css">
<link rel="stylesheet" href="../APMB2/responsive-nao-calendar/css/jquery-nao-calendar.css">
<script src="../APMB2/responsive-nao-calendar/jquery-nao-calendar.js"></script>	
	<style>
.myCalendar.nao-month td {
  padding: 15px;
}

.myCalendar .month-head>div,
.myCalendar .month-head>button {
  padding: 15px;
}
</style>


</head>
<div class="container">
<h3 style="margin-top:10%;"> Estabelecimentos </h3>
<table id="example" class="table table-striped table-bordered nowrap" style="width:100%;margin-top:10%;">
<thead>
   <tr>
                        <th >Nome</th>
						<th >Lat</th>
                        <th >Lng</th>  
						<th >Data</th>  
						<th >Mensagem</th>  



   </tr>
</thead> 
</table>
 
</div>
	<script src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"> </script>

<script type="text/javascript" src="../roosevelt/arrive-master/src/arrive.js"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
<script src= "../zTree_v3-master/js/jquery.ztree.core.js"></script>
