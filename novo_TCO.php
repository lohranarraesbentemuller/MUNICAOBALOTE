<?php
 include("config.php");
 include("session.php");
if($_SERVER["HTTPS"] != "on")
{
    header("Location: https://" . $_SERVER["HTTP_HOST"] . $_SERVER["REQUEST_URI"]);
 //   exit();
}
$flag=True;

if($_SERVER["REQUEST_METHOD"] == "POST") {
 
 


if($_POST['tipo_penal']=="") $flag=False;
//echo $flag;
if($_POST['fonte']=="") $flag=False;
//echo $flag;
if(htmlspecialchars($_POST['descricao']=="")) $flag=False;
//echo $flag;
if($_POST['tags_reais']=="") $flag=False;
//echo $flag;
if(htmlspecialchars($_POST['cabe_tco']=="")) $flag=False;
//echo $flag;
if(htmlspecialchars($_POST['ncabe_tco']=="")) $flag=False;
//echo $flag;
if(htmlspecialchars($_POST['atencao']=="")) $flag=False;
 //echo $flag;
 
 //exit();
if($flag==False)
{
	//echo '<script type="text/javascript" language="javascript" src="https://code.jquery.com/jquery-3.3.1.js"></script>';
	echo '<script type="text/javascript" language="javascript" src="../jquery-3.6.0.min.js"></script>';
	echo "<script>$(document).ready(function(){";
	
	if($_POST['tipo_penal']=="")  echo '$("#alerta_tipo_penal").css("display","inherit");';
	if($_POST['fonte']=="")  echo '$("#alerta_fonte").css("display","inherit");';
	if($_POST['descricao']=="")  echo '$("#alerta_descricao").css("display","inherit");';
	if($_POST['tags_reais']=="")  echo '$("#alerta_tags").css("display","inherit");';
	if($_POST['cabe_tco']=="")  echo '$("#alerta_cabe_tco").css("display","inherit");';
	if($_POST['ncabe_tco']=="")  echo '$("#alerta_ncabe_tco").css("display","inherit");';
	if($_POST['atencao']=="")  echo '$("#alerta_atencao").css("display","inherit");';
	 
	echo "});</script>";
}
else{

$sql="insert into TCO(contador,tipo_penal,fonte,descricao,tags,cabe_tco,ncabe_tco,atencao) values(".$_GET['id'].",'".$_POST['tipo_penal']."','".$_POST['fonte']. "','".htmlspecialchars($_POST['descricao'])."','".$_POST['tags_reais']."','".htmlspecialchars($_POST['cabe_tco'])."','".htmlspecialchars($_POST['ncabe_tco'])."','".htmlspecialchars($_POST['atencao'])."')";

$result=mysqli_query($db,$sql);
//echo $sql;exit();

header("location:index.php");
}
}
//if($flag==True) echo '<script type="text/javascript" language="javascript" src="https://code.jquery.com/jquery-3.3.1.js"></script>';
if($flag==True) echo '<script type="text/javascript" language="javascript" src="../jquery-3.6.0.min.js"></script>';
?>
 <!--<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script> -->
 <script src="../jquery-ui-1.12.1/jquery-ui.js"></script> 
 
<script src="../ckeditor/ckeditor.js"></script>
<link href="../FO/dropzone.css" type="text/css" rel="stylesheet" />
<link href='https://fonts.googleapis.com/css?family=Source+Sans+Pro' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="../APMB2/Gallery-2.36.0/css/blueimp-gallery.css" />
    <link rel="stylesheet" href="../APMB2/Gallery-2.36.0/css/blueimp-gallery-indicator.css" />
    <link rel="stylesheet" href="../APMB2/Gallery-2.36.0/css/blueimp-gallery-video.css" />
   <!-- <link rel="stylesheet" href="Gallery-2.36.0/css/demo/demo.css" /> -->

<style>
.skin-blue .main-header .navbar{background-color:#154D6E}.skin-blue .main-header .navbar .nav>li>a{color:#fff}.skin-blue .main-header .navbar .nav>li>a:hover,.skin-blue .main-header .navbar .nav>li>a:active,.skin-blue .main-header .navbar .nav>li>a:focus,.skin-blue .main-header .navbar .nav .open>a,.skin-blue .main-header .navbar .nav .open>a:hover,.skin-blue .main-header .navbar .nav .open>a:focus,.skin-blue .main-header .navbar .nav>.active>a{background:rgba(0,0,0,0.1);color:#f6f6f6}.skin-blue .main-header .navbar .sidebar-toggle{color:#fff}.skin-blue .main-header .navbar .sidebar-toggle:hover{color:#f6f6f6;background:rgba(0,0,0,0.1)}.skin-blue .main-header .navbar .sidebar-toggle{color:#fff}.skin-blue .main-header .navbar .sidebar-toggle:hover{background-color:#154D6E}@media (max-width:767px){.skin-blue .main-header .navbar .dropdown-menu li.divider{background-color:rgba(255,255,255,0.1)}.skin-blue .main-header .navbar .dropdown-menu li a{color:#fff}.skin-blue .main-header .navbar .dropdown-menu li a:hover{background:#154D6E}}.skin-blue .main-header .logo{background-color:#154D6E;color:#fff;border-bottom:0 solid transparent}.skin-blue .main-header .logo:hover{background-color:#154D6E}.skin-blue .main-header li.user-header{background-color:#154D6E}.skin-blue .content-header{background:transparent}.skin-blue .wrapper,.skin-blue .main-sidebar,.skin-blue .left-side{background-color:#154D6E}.skin-blue .user-panel>.info,.skin-blue .user-panel>.info>a{color:#fff}.skin-blue .sidebar-menu>li.header{color:#4b646f;background:#1a2226}.skin-blue .sidebar-menu>li>a{border-left:3px solid transparent}.skin-blue .sidebar-menu>li:hover>a,.skin-blue .sidebar-menu>li.active>a{color:#fff;background:#1e282c;border-left-color:#3c8dbc}.skin-blue .sidebar-menu>li>.treeview-menu{margin:0 1px;background:#2c3b41}.skin-blue .sidebar a{color:#b8c7ce}.skin-blue .sidebar a:hover{text-decoration:none}.skin-blue .treeview-menu>li>a{color:#8aa4af}.skin-blue .treeview-menu>li.active>a,.skin-blue .treeview-menu>li>a:hover{color:#fff}.skin-blue .sidebar-form{border-radius:3px;border:1px solid #374850;margin:10px 10px}.skin-blue .sidebar-form input[type="text"],.skin-blue .sidebar-form .btn{box-shadow:none;background-color:#374850;border:1px solid transparent;height:35px}.skin-blue .sidebar-form input[type="text"]{color:#666;border-top-left-radius:2px;border-top-right-radius:0;border-bottom-right-radius:0;border-bottom-left-radius:2px}.skin-blue .sidebar-form input[type="text"]:focus,.skin-blue .sidebar-form input[type="text"]:focus+.input-group-btn .btn{background-color:#fff;color:#666}.skin-blue .sidebar-form input[type="text"]:focus+.input-group-btn .btn{border-left-color:#fff}.skin-blue .sidebar-form .btn{color:#999;border-top-left-radius:0;border-top-right-radius:2px;border-bottom-right-radius:2px;border-bottom-left-radius:0}.skin-blue.layout-top-nav .main-header>.logo{background-color:#154D6E;color:#fff;border-bottom:0 solid transparent}.skin-blue.layout-top-nav .main-header>.logo:hover{background-color:#3b8ab8}

.cont-items-monitor {
  position: absolute;

  z-index: 5;
  background-color: #fff;
  padding: 5px;
  border: 1px solid #999;
  text-align: center;
  /*font-family: 'Roboto','sans-serif';*/
  line-height: 30px;
  padding-left: 10px;
  overflow:visible;
  height:auto;
  width:auto;
  
  
  -moz-border-radius:7px;-webkit-border-radius:7px; border-radius:7px;
}
</style>

<script src="../APMB2/responsive-nao-calendar/jquery-nao-calendar.js"></script>
<script>
    if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
    }
</script>


 <!doctype html>
<html lang="en">
<head>
<!-- menu lateral-->

    <!-- jQuery CDN - Slim version (=without AJAX) -->
<!--    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>-->
    <!-- Popper.JS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js" integrity="sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ" crossorigin="anonymous"></script>
    <!-- Bootstrap JS -->
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js" integrity="sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm" crossorigin="anonymous"></script>
    <!-- jQuery Custom Scroller CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/malihu-custom-scrollbar-plugin/3.1.5/jquery.mCustomScrollbar.concat.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/malihu-custom-scrollbar-plugin/3.1.5/jquery.mCustomScrollbar.min.css">

<!--fim do menu -->
<style>
<link href="jumbotron.css" rel="stylesheet">

@import url(https://fonts.googleapis.com/css?family=Raleway:300,400,600);

body {
  color: blue;
}
a {
  color: inherit; /* blue colors for links too */
  text-decoration: inherit; /* no underline */
}
body{
    margin: 0;
    font-size: .9rem;
    font-weight: 400;
    line-heigth: 1.6;<nav.
    color: #212529;
    text-align: left;
    background-color: #f5f8fa;
}

.navbar-laravel
{
    box-shadow: 0 2px 4px rgba(0,0,0,.04);
}

.navbar-brand , .nav-link, .my-form, .login-form
{
    font-family: Raleway, sans-serif;
}

.my-form
{
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
}

.my-form .row
{
    margin-left: 0;
    margin-right: 0;
}

.login-form
{
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
}

.login-form .row
{
    margin-left: 0;
    margin-right: 0;
}
</style>

    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Fonts -->
    <link rel="dns-prefetch" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css?family=Raleway:300,400,600" rel="../APMB2/stylesheet" type="text/css">

    <!--<link rel="stylesheet" href="../roosevelt/css/style.css">-->

    <link rel="icon" href="Favicon.png">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.4.1/js/bootstrap-datepicker.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.4.1/css/bootstrap-datepicker3.css"/>
    <title>Genesis PMDF</title>
	<meta http-equiv="Content-type" content="text/html; charset=utf-8">
	<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
	
	<!--datatables-->
  <!-- datatables -->
    <link rel="alternate" type="application/rss+xml" title="RSS 2.0" href="http://www.datatables.net/rss.xml">
	<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.20/css/dataTables.bootstrap.min.css">
	<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/fixedheader/3.1.6/css/fixedHeader.bootstrap.min.css">
	<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/responsive/2.2.3/css/responsive.bootstrap.min.css">
	<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>
	<!--<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/1.10.20/js/dataTables.bootstrap.min.js"></script>-->
	<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/fixedheader/3.1.6/js/dataTables.fixedHeader.min.js"></script>
	<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/responsive/2.2.3/js/dataTables.responsive.min.js"></script>
	<script type="text/javascript" language="javascript" src="https://cdn.datatables.net/responsive/2.2.3/js/responsive.bootstrap.min.js"></script>
	
<!--<script src="https://cdn.datatables.net/buttons/1.6.0/js/dataTables.buttons.min.js"></script>
<script src="https://cdn.datatables.net/buttons/1.6.0/js/buttons.flash.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.1.3/jszip.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/pdfmake.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/vfs_fonts.js"></script>
<script src="https://cdn.datatables.net/buttons/1.6.0/js/buttons.html5.min.js"></script>
<script src="https://cdn.datatables.net/buttons/1.6.0/js/buttons.print.min.js"></script>-->
	<link rel="stylesheet" href="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.min.css">
<!--	 <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">-->
	 <script src="https://kit.fontawesome.com/a073e3cdd7.js" crossorigin="anonymous"></script>


	<!---->
	
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"> 
<style>
span {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    font-family: 'Source Sans Pro','Helvetica Neue',Helvetica,Arial,sans-serif;
    font-weight: 400;
    overflow-x: hidden;
    overflow-y: auto;
	font-size: 14px;
    line-height: 1.42857143;
    color: #333;
    background-color: #fff;
}
</style>




<!--teste -->
 

<script>
 
</script>
<!-- fim teste -->

</head>

<body>

 
 <?php //include("menu.php");?>
 
 <img id="topo" style="" src="topo.png"/>
 <img id="topo_mobile" style="display:none;" src="topo_mobile.png"/>
 
 
 

 

<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
   <form  method="post">
   <div class="container" style="margin-top:5%;">
<?php
$sql="SHOW TABLE STATUS FROM nobrega  where name like 'ocorrencia'";
$result=mysqli_query($db,$sql);
$row=mysqli_fetch_array($result,MYSQLI_ASSOC);
?>
    <button type="button" class="btn btn-info" id="mostrar_urls">Mostrar lista de Imagens e arquivos</button>
	
	 <div id="URLS" style="display:none;" class="cont-items-monitor">
 <button type="button" id = "x2" class="btn btn-warning">
            X
        </button>
  <table class="table" id="table_float">
  <thead class="thead-dark">
    <tr>
      
      <th scope="col">Preview</th>
      <th scope="col">URL</th>
    </tr>
  </thead>
  <tbody>
    <tr id="tr1">
    </tr>
	</tbody>
	</table>
</div> 
	
	
	
    <div class="row">
 
	 <div class="col">
	 <div id="alerta_tipo_penal" style="display:none;" class="alert alert-danger" role="alert">Preencha o tipo penal</div>
	 <span class="hidden-sm hidden-md"><h4><span class="fa fa-edit"></span> Tipo penal</h4></span>
	 <input type="text" name="tipo_penal" class="form-control genesis" autocomplete="off"/>
	 </div></div>
	 <div class="row">
	 <div class="col">
	 <div  style="display:none;" id="alerta_fonte" class="alert alert-danger" role="alert">Preencha a fonte</div>
	 <span class="hidden-sm hidden-md"><h4><span class="fa fa-quora"></span> Fonte</h4></span>
	 <div class="form-group">
	 <input type="text"  name="fonte" class="form-control genesis data" autocomplete="off"/>
	 </div>
	 </div>
	 </div>
	 <div class="row">
	 <div class="col">
	 <div  style="display:none;" id="alerta_descricao" class="alert alert-danger" role="alert">Preencha a descrição</div>
	 <span class="hidden-sm hidden-md"><h4><span class="fa fa-file-text"></span> Descrição</h4></span>
	 <div class="form-group">
	 <textarea   id="descricao" name="descricao" class="form-control genesis" autocomplete="off"></textarea>
	 </div>
	 </div>	 </div>
	 <div class="row">
	 <div class="col">
	 <div  style="display:none;" id="alerta_tags" class="alert alert-danger" role="alert">Preencha as tags para busca</div>
	 <span class="hidden-sm hidden-md"><h4><span class="fa fa-hashtag"></span> Tags</h4></span>
	 <input type="text"  id ="tags" name="tags" class="form-control genesis" autocomplete="off"/>
	 <input type="text" style="display:none;" id="tags_reais" name="tags_reais"></input>
	 </div>	</div>
	 <div class="row">
	 <div class="col">
	 <div id="alerta_cabe_tco" style="display:none;" class="alert alert-danger" role="alert">Preencha o campo indicado</div>
	 <span class="hidden-sm hidden-md"><h4><span class="fa fa-check"></span> Casos que cabe TCO</h4></span>
	 <textarea  name="cabe_tco" id="cabe_tco" class="form-control genesis" ></textarea>
	 </div>
   	</div>

    <div class="row">
	 <div class="col">
	 <div id="alerta_ncabe_tco" style="display:none;" class="alert alert-danger" role="alert">Preencha o campo indicado</div>
     <span class="hidden-sm hidden-md"><h4><span class="fa fa-times"></span> Caso que não cabe TCO</h4></span>
	 <textarea  name="ncabe_tco" id="ncabe_tco" class="form-control genesis"></textarea>
     </div>
	 </div>
	 <div class="row">
	 <div class="col">
	 <div id="alerta_atencao" style="display:none;" class="alert alert-danger" role="alert">Preencha o campo de atenção</div>
	 <span class="hidden-sm hidden-md"><h4><span class="fa fa-exclamation-triangle"></span> Ponto de Atenção!</h4></span>
	 <textarea   name="atencao" id="atencao" class="form-control genesis"></textarea>
	 </div>
	 </div>
	 
	
    
   
	
	 <script src="../dropzone-master/dist/dropzone.js"></script>
 
   	</div>	

 
 
	
	   <div class="row">
     <div class="col"></div>
	 <div class="col"></div>
	 <div class="col"></div>
	 <div class="col"></div>
	 <div class="col"></div>
	 <div class="col"></div>
     <div class="col">
       <button class="btn btn-primary"  style="margin-top:10%;" >Gerar</button>
	  </div>
   </div>
	</form>
<div class="wrapper" style="margin-left:25%;width:50%;cursor: pointer;">
 <div class="row" >
 <div class="col">
 <form action="upload.php?id=<?php echo $_GET['id'];?>" class="dropzone dz-clickable"></form>
 
 
 
   </div>
</div>   
</div>
</div>
</body>
 

      <!-- Main jumbotron for a primary marketing message or call to action -->
  
<script>

function dragElement(elmnt) {
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  if (document.getElementById(elmnt.id)) {
    // if present, the header is where you move the DIV from:
    document.getElementById(elmnt.id).onmousedown = dragMouseDown;
  } else {
    // otherwise, move the DIV from anywhere inside the DIV:
    elmnt.onmousedown = dragMouseDown;
  }

  function dragMouseDown(e) {
    e = e || window.event;
    e.preventDefault();
    // get the mouse cursor position at startup:
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDrag;
  }

  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    // set the element's new position:
    elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
    elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
  }

  function closeDragElement() {
    // stop moving when mouse button is released:
    document.onmouseup = null;
    document.onmousemove = null;
  }
}


  $(document).ready(function(){
	  $('.td_url').click(function(){
		  alert("AQUI");
	    $(this).html().select();
        $(this).html().setSelectionRange(0, 99999);
		document.execCommand("copy");
	  });
	  
	  dragElement(document.getElementById("URLS"));
	  $( "#x2" ).click(function() {
      $('#URLS').css("display","none");
      });
	  $('#mostrar_urls').click(function(){
		  $('#URLS').css("display","none");
	//	  alert("AQUI");
	valor="";	  
$.ajax({ 
 type:"POST", 
 url: "mostrar_diretorio.php?id=<?php echo $_GET['id'];?>", 
 data:valor,
  success: function(data){
   // alert("teste");
   // console.log(valor);
    // console.log(data);
 	//alert(data);
	$('#table_float').html('');
	$('#table_float').append('<thead class="thead-dark">');
    $('#table_float').append('<thead class="thead-dark"><tr><th scope="col">Preview</th><th scope="col">URL</th></tr></thead>');
    $('#table_float').append('<tr id="tr1"></tr>');
	
	for (var i = 0; i < data.split('#').length; i++)  
		{
			//alert(data.split("#")[i]);
			if (data.split("#")[i].length>2)
			{
				if((data.split("#")[i].split(".")[1].toLowerCase() =="jpg" ) || (data.split("#")[i].split(".")[1].toLowerCase() =="png" ) || (data.split("#")[i].split(".")[1].toLowerCase() =="bmp" ))
				   $('#tr1').after('<tr><td><img style="width:75px;" src="./uploads/<?php echo $_GET["id"] ;?>/'+data.split("#")[i]+'"></img></td><td class="td_url"><a href="./uploads/<?php echo $_GET['id'] ;?>/'+data.split("#")[i]+'">'+"./uploads/<?php echo $_GET["id"] ;?>/"+data.split("#")[i]+'</a></td></tr>');
				else
				    $('#tr1').after('<tr><td><span class="fa fa-file"></span></td><td class="td_url"><a href="./uploads/<?php echo $_GET['id'] ;?>/'+data.split("#")[i]+'">'+"./uploads/<?php echo $_GET["id"] ;?>/"+data.split("#")[i]+'</a></td></tr>');
			}      
		}
	$('#URLS').css("display","inherit");
   },
  error: function (jqXHR, exception) {
    var msg = "";
	console.log("deu ruim");
    if (jqXHR.status === 0) {
      msg = "Not connect.\n Verify Network.";
    } else if (jqXHR.status == 404) {
     msg = "Requested page not found. [404]";
	}
    else if (jqXHR.status == 500) {
     msg = "Internal Server Error [500].";
    } else if (exception === "parsererror") {
     msg = "Requested JSON parse failed.";
    } else if (exception === "timeout") {
     msg = "Time out error.";
    } else if (exception === "abort") {
     msg = "Ajax request aborted.";
    } else {
     msg = "Uncaught Error.\n" + jqXHR.responseText;
    }
//alert(html(msg));
}, 
});	
	
		  
		  
	  });
	  
  });
</script>
 


<script>

var isMobile = false; //initiate as false
// device detection
if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent) 
    || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0,4))) { 
    isMobile = true;
}
function retira_acentos(palavra) { 
    com_acento = 'áàãâäéèêëíìîïóòõôöúùûüÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÖÔÚÙÛÜ'; 
    sem_acento = 'aaaaaeeeeiiiiooooouuuuAAAAAEEEEIIIIOOOOOUUUU'; 
    nova=''; 
    for(i=0;i<palavra.length;i++) { 
        if (com_acento.search(palavra.substr(i,1))>=0) { 
            nova+=sem_acento.substr(com_acento.search(palavra.substr(i,1)),1); 
        } 
        else { 
            nova+=palavra.substr(i,1); 
        } 
    } 
    return nova; 
}
 



</script>

  <!--<link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />-->
  <!--<link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">-->
  <link rel="stylesheet" href="../jquery-ui-1.12.1/jquery-ui.css">
  <!--<link rel="stylesheet" href="../roosevelt/resources/demos/style.css">-->

 
 
 
  <!--<img src="DETALHES.png" style="width:40%;"/>-->
 
 
</div>
  



<img src="baixo.PNG"/>
<script  src="../ESCALA/jQuery-Mask-Plugin-master/src/jquery.mask.js"></script>
<script type="text/javascript"  src="../jQuery-Autocomplete-master/src/jquery.autocomplete.js"></script>
<script type="text/javascript" src="../roosevelt/arrive-master/src/arrive.js"></script>
<script>

CKEDITOR.replace( 'descricao' );
CKEDITOR.replace( 'atencao' );
CKEDITOR.replace( 'cabe_tco' );
CKEDITOR.replace( 'ncabe_tco' );
$(document).ready(function(){
 
  $(document).arrive(".badge",function(){
	  $(this).dblclick(function(){
		  $(this).css("display","none");
		  var valor= $(this).html();
		  //alert(valor);
		  $('#tags_reais').val($('#tags_reais').val().split('#'+valor)[0]+$('#tags_reais').val().split('#'+valor)[1]);
	  });
  });

 
 $('#tags').keydown(function(e) {
	 //alert(e.key);
	 //console.log(e.key);
	 if (e.key==" ")
	 {
		 var valor=$(this).val();
		 var tag = '<span class="badge" style="background-color: rgb(209, 218, 222); margin: 2%; width: 230px; height: 20px; color: black; box-shadow: black 0px 8px 6px -6px;">'+$(this).val()+'</span>'
		 $(this).val("");
		 $(this).after(tag);
		 $('#tags_reais').val($('#tags_reais').val()+'#'+valor);
	 }
  //alert( "Handler for .keydown() called." );
});
	
$(window).keydown(function(event){ //formulario não vai com enter
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  }); 
  
  
$('.dz-message').children('span').each(function()
	 {
 
		 
		 ($(this).html("Arraste imagens ou ocorrências que possam ajudar na confecção desse tipo de TCO"));
		 
	 });
	 
	 
});
</script>
<!--<script src="../dropzone-master/dist/dropzone.js"></script>-->
<script src="../ckeditor/ckeditor.js"></script>
</html>