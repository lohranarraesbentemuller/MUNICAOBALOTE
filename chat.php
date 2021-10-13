<html>
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<title>Munição Balote</title>
<script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha384-vk5WoKIaW/vJyUAd9n/wmopsmNhiy+L2Z+SBxGYnUkunIxVxAv/UtMOhba/xskxh" crossorigin="anonymous"></script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/velocity/1.5.2/velocity.min.js"></script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/velocity/1.5.2/velocity.ui.min.js"></script>
<link rel="stylesheet" type="text/css" href="chat-style.css">
<script type="text/javascript" src="chatModule.js"></script>
<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.10.2/css/all.min.css">
<style id="compiled-css" type="text/css">
  body { background: #fafafa; }
      #chat-context {
  height: 95vh;
}

.chat-response.robot:after {
    content: "";
    background: url('small pmdf.png') no-repeat center center;
    background-size: contain;
    opacity: .5;
}

.chat-response.user:after {
    color: var(--color-green);
    display: inline-block;
    font-style: normal;
    font-variant: normal;
    text-rendering: auto;
    -webkit-font-smoothing: antialiased;
    font-family: "Font Awesome 5 Free";
    font-weight: 900;
    content: "\f007";
}
  </style>
   <script type="text/javascript">//<![CDATA[
function valida_placa(placa)
{
        flag=true;
        if(placa.length!=7)
        {
                flag=false;
                return flag;
        }
        var letras=/[a-zA-Z]/g;
        var numeros=/[0-9]/g;

        if(placa.substring(0,3).match(letras).length!=3)
                flag=false;
        if(placa.substring(3,7).match(numeros).length<3)
                flag=false;

        return flag;

}


    $(window).on('load', function() {

var tags = [{
    type: "input",
    tag: "text",
    name: "name",
    "chat-msg": "Digite uma placa, nome, ou envia uma imagem"
  }
];
//img="";
function customTagRender () {
  //$('#ui-control').prepend('<div id="custom-input">Custom input! Practically, this would be a clickable map or image, or virtually anything that you can code up. Click the big button below to submit</div>');
  $('#ui-control').prepend('<img src="https://www.cfo2019.com/FO/logo/pmdf%20(2).png" style="width:auto:height:240px"></img>');
  //This custom data would be set by user interaction in the real world
  window.customData = "the possibilities are endless!";
}

$(document).ready(function() {

$(document).arrive('#response-text',function(){
    $('#response-text').keyup(function(){
	//alert("aqui");
	
    });


$(document).on('keypress',function(e) {
    if(e.which == 13) {
		
	   msg=$('#response-text').val();
	   //alert(msg);
valor="placa="+msg;	
if (valida_placa)
   {
$.ajax({ 
 type:"POST", 
 url: "getPlaca.php", 
 data:valor,
  success: function(data){
	  
	  if(data.length>0)
	  {
	  tags=[{
							type: "input",
							tag: "text",
							name: "name",
							"chat-msg": "Veículo com possível restrição de roubo ou furto"
							}];
	  }
	  else{
	  tags=[{
							type: "input",
							tag: "text",
							name: "name",
							"chat-msg": "Nenhuma placa encontrada"
							}];		  
	  }
	  Chat.start($('#chat-context'), tags);
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

}, 
});	   
	 		
	}	
    }

});

	$('#ui-submit').click(function(){
	   
	   msg=$('#response-text').val();
	  // alert(msg);
valor="placa="+msg;	
if (valida_placa)
   {
$.ajax({ 
 type:"POST", 
 url: "getPlaca.php", 
 data:valor,
  success: function(data){
	  //alert(data);
	  if(data.length>0)
	  {
	  tags=[{
							type: "input",
							tag: "text",
							name: "name",
							"chat-msg": "Veículo com possível restrição de roubo ou furto"
							}];
	  }
	  else{
	  tags=[{
							type: "input",
							tag: "text",
							name: "name",
							"chat-msg": "Nenhuma placa encontrada"
							}];		  
	  }
	  Chat.start($('#chat-context'), tags);
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

}, 
});	  
   } 
	   
	});
});



/*msg=$('#response-text').val();	
valor="placa="+msg;	
$.ajax({ 
 type:"POST", 
 url: "getPlaca.php", 
 data:valor,
  success: function(data){
	  alert(data);
	  tags=[{
							type: "input",
							tag: "text",
							name: "name",
							"chat-msg": data
							}];
	  Chat.start($('#chat-context'), tags);
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

}, 
}); */  

	
  Chat.start($('#chat-context'), tags);
  
  
	 $('#file').change(function(){
		 
		var fd = new FormData();
                var files = $('#file')[0].files[0];
                fd.append('file', files);
       
                $.ajax({
                    url: 'upload.php',
                    type: 'post',
                    data: fd,
                    contentType: false,
                    processData: false,
                    success: function(response){
					//	alert(response);
                        if(response != 0){
	var tags=[				
{
							type: "input",
							tag: "text",
							name: "name",
							"chat-msg": "file#"+response
							},	
  {
    type: "input",
    tag: "custom",
    name: "customTag",
//    submitBarStyle: 'full-submit',
    "chat-msg": "Imagem enviada",
    renderer: customTagRender,
    retriever: function() {
  //    $('#custom-input').remove();
      return {
        data: window.customData,
        friendly: ""}
    }
  }				];			
							
							/*var tags = [{
							type: "input",
							tag: "text",
							name: "name",
							"chat-msg": "file#"+response
							}];
							$('#chat-context').html('');*/
							Chat.start($('#chat-context'), tags);
							//msg="File uploaded";
							//Chat.addResponse(false, "imagem enviada");
							//Chat.addTags([{
                           // type: "msg",
                            //"chat-msg": msg,
                            // delay: 2000
                            // }]);
                           //alert('file uploaded');
                        }
                        else{
							var tags = [{
							type: "input",
							tag: "text",
							name: "name",
							"chat-msg": "Erro, tente enviar a foto novamente"
							}];
							$('#chat-context').html('');
							Chat.start($('#chat-context'), tags);
                        }
                    },
                });
		
  });  
  
});


    });

  //]]></script>

</head>

<body>
<div id="chat-context"></div>

<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-36251023-1']);
  _gaq.push(['_setDomainName', 'jqueryscript.net']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
</body>
<script type="text/javascript" src="../roosevelt/arrive-master/src/arrive.js"></script>
</html>
