var WebTWAIN;
var ua;
var em = "";
var seed;
var objEmessage;
var re;
var strre;
var ileft, itop, iright, ibottom;
var timeout;
var Resolution, InterpolationMethod, txt_fileNameforSave, txt_fileName;
var CurrentImage, TotalImage, MultiPageTIFF_save, MultiPagePDF_save, MultiPageTIFF, MultiPagePDF, PreviewMode, pNoScanner;
var TWAINPlugInMSI, TWAINx64CAB, TWAINCAB;
window.onload = Pageonload;
//====================Page Onload  Start==================//

function Pageonload() {

    ua = (navigator.userAgent.toLowerCase());
    if (ua.indexOf("wow64") == -1) {
        document.getElementById("samplesource32bit").href = "http://www.dynamsoft.com/demo/DWT/Sources/twainkit.exe";
    }
    var strObjectFF = GetEventString(); 
    strObjectFF += " class='divcontrol' pluginspage='../../media/resources/DynamicWebTwain.xpi'></embed>";

    var strObject = GetObject();
		
	var obj = document.getElementById("maindivIElimit");
    obj.style.display = "none";
	
    if (ExplorerType() == "IE" && navigator.userAgent.indexOf("Win64") != -1 && navigator.userAgent.indexOf("x64") != -1) {
        strObject = "<object id='mainDynamicWebTwainIE' codebase='../../media/resources/DynamicWebTWAINx64.cab#version=8,0,1' class='divcontrol' " + "classid='clsid:E7DA7F8D-27AB-4EE9-8FC0-3FEC9ECFE758' viewastext> " + strObject;
        var objDivx64 = document.getElementById("maindivIEx64");
        objDivx64.style.display = "inline";
        objDivx64.innerHTML = strObject;
        var obj = document.getElementById("mainControlPluginNotInstalled");
        obj.style.display = "none";
        WebTWAIN = document.getElementById("mainDynamicWebTwainIE");
        document.getElementById("samplesource64bit").style.display = "inline";
        document.getElementById("samplesource32bit").style.display = "none";
		var obj = document.getElementById("maindivIElimit");
        obj.style.display = "none";
    }
    else if (ExplorerType() == "IE" && (navigator.userAgent.indexOf("Win64") == -1 || navigator.userAgent.indexOf("x64") == -1)) {
        strObject = "<object id='mainDynamicWebTwainIE' codebase='../../media/resources/DynamicWebTWAIN.cab#version=8,0,1' class='divcontrol' " + "classid='clsid:E7DA7F8D-27AB-4EE9-8FC0-3FEC9ECFE758' viewastext> " + strObject;
        var objDivx86 = document.getElementById("maindivIEx86");
        objDivx86.style.display = "inline";
        objDivx86.innerHTML = strObject;
        var obj = document.getElementById("mainControlPluginNotInstalled");
        obj.style.display = "none";
        WebTWAIN = document.getElementById("mainDynamicWebTwainIE");
		var obj = document.getElementById("maindivIElimit");
        obj.style.display = "none";
    }
	else if (ExplorerType() == "notIE" ){
		var objDivFF = document.getElementById("mainControlPlugin");
        objDivFF.innerHTML = strObjectFF;
		var obj = document.getElementById("maindivIE");
        obj.style.display = "none";
		var obj = document.getElementById("maindivIElimit");
        obj.style.display = "none";
        WebTWAIN = document.getElementById("mainDynamicWebTWAINnotIE");
	}
    else{
        var obj = document.getElementById("mainControlPluginNotInstalled");
        obj.style.display = "none";
		var obj = document.getElementById("maindivIE");
        obj.style.display = "none";
		var obj = document.getElementById("maindivIElimit");
        obj.style.display = "none";
    }
    
    CurrentImage = document.getElementById("CurrentImage");
    CurrentImage.value = "";
    TotalImage = document.getElementById("TotalImage");
    TotalImage.value = "0";

    seed = setInterval(ControlDetect, 500);
}

function ControlDetect() {
    if (WebTWAIN.ErrorCode == 0) {
        pause();
		
		if (ExplorerType() == "notIE" ){
			document.getElementById("mainControlPluginNotInstalled").style.display = "none";
            document.getElementById("mainControlPlugin").style.display = "inline";
		}
		
        var i;
        document.getElementById("source").options.length = 0;
        WebTWAIN.OpenSourceManager();

        if (WebTWAIN.SourceCount != 0) {
            //document.getElementById("aNoScanner").innerHTML = "<strong>Don't want to scan anything?</strong>";
            document.getElementById("notformac1").style.display = "none";
            document.getElementById("notformac2").style.display = "none";
            //document.getElementById("tblLoadImage").style.height = "120px";
            //SetNoScanner();
        }
        else {
            //SetNoScanner();
        }
        
        for (i = 0; i < WebTWAIN.SourceCount; i++) {
            document.getElementById("source").options.add(new Option(WebTWAIN.SourceNameItems(i), i));
        }
        WebTWAIN.MaxImagesInBuffer = 4096;
        WebTWAIN.MouseShape = false;
        
        //AddResolution();

        //AddInterpolationMethod();

        //SetFileName();

        //document.getElementById("ADF").checked = true;
        //SetMultiPageInfo(); 

        //AddPreviewMode();
        
        //objEmessage = document.getElementById("emessage");

        re = /^\d+$/;
        strre = /^\w+$/;

        ileft = 0;
        itop = 0;
        iright = 0;
        ibottom = 0;

        SetShowOrCloseLoadImage();
        
        //var allinputs = document.getElementsByTagName("input");
        //var j = 0;
        //for (var i = 0; i < allinputs.length; i++) {
        //    if (allinputs[i].type == "text") {
        //        allinputs[i].onkeyup = function () {
        //            if (event.keyCode != 37 && event.keyCode != 39) value = value.replace(/\D/g, '');
        //        }
        //    }
        //}
        //objEmessage.ondblclick = function () {
        //    em = "";
        //    this.innerHTML = "";
        //}
        if (ExplorerType() == "IE") {
            GetIEEventString();
        }
        
        
        DoWithNoSource();
    }
    else {
        if (navigator.userAgent.indexOf("Macintosh") != -1) {
            document.getElementById("MACmainControlNotInstalled").style.display = "inline";
            document.getElementById("mainControlPluginNotInstalled").style.display = "none";
            document.getElementById("mainControlInstalled").style.display = "none";
        }
        else if (ua.match(/chrome\/([\d.]+)/) || ua.match(/opera.([\d.]+)/) || ua.match(/version\/([\d.]+).*safari/)) {
            document.getElementById("mainControlPluginNotInstalled").style.display = "inline";
            document.getElementById("mainControlPlugin").style.display = "none";
            document.getElementById("MACmainControlNotInstalled").style.display = "none";
        }
    }
    timeout = setTimeout(function(){},10);
}
//====================Page Onload End====================//


//====================Preview Group Start====================//
function slPreviewMode() {
    WebTWAIN.SetViewMode(parseInt(document.getElementById("PreviewMode").selectedIndex + 1), parseInt(document.getElementById("PreviewMode").selectedIndex + 1));
    if (document.getElementById("PreviewMode").selectedIndex != 0) {
        WebTWAIN.MouseShape = true;
    }
    else {
        WebTWAIN.MouseShape = false;
    }
}
//====================Preview Group End====================//

//====================Get Image Group Start=====================//

/*-----------------Load Image---------------------*/
function btnLoad_onclick() {
    WebTWAIN.IfShowFileDialog = false;
	if(location.pathname.lastIndexOf('\\')>1)
		WebTWAIN.LoadImage(location.pathname.substring(1, location.pathname.lastIndexOf('\\')).replace(/%20/g," ") + "\\Images\\twain_associate.pdf");
	else
		WebTWAIN.LoadImage(location.pathname.substring(1, location.pathname.lastIndexOf('/')).replace(/%20/g," ") + "/Images/twain_associate.pdf");
    UpdatePageInfo();
    if (WebTWAIN.SourceCount != 0) {
        clearTimeout(timeout);
        timeout = setTimeout(function () {
            document.getElementById("tblLoadImage").style.visibility = "hidden";
            document.getElementById("Resolution").style.visibility = "visible";
        }, 1000);
    }
}

//====================Get Image Group End=====================//

//====================Edit Image Group Start=====================//

/*----------------------Crop Method---------------------*/

function btnCropOK_onclick() {
    btnCropOKInner();
}

/*----------------Change Image Size--------------------*/
function btnChangeImageSizeOK_onclick() {
    btnChangeImageSizeOKInner();
}

//====================Edit Image Group End==================//


/*-----------------Upload Image Group---------------------*/
function btnUpload_onclick_original(){

	console.log('>>>>>>>>>>>>>>>>>>>bntUpload_onclick');
    var CurrentPathName = unescape(location.pathname); // get current PathName in plain ASCII	
    console.log(CurrentPathName);
    var CurrentPath = CurrentPathName.substring(0, CurrentPathName.lastIndexOf("/") + 1);
    console.log(CurrentPath);
    var strActionPage = CurrentPath + "SaveToDB.aspx"; //the ActionPage's file path
    console.log(strActionPage);
    var redirectURLifOK = CurrentPath + "online_demo_list.aspx";
    console.log(redirectURLifOK);

    btnUploadInner("www.dynamsoft.com", 80, strActionPage, redirectURLifOK);
   
    if (CheckErrorString()) {
    	console.log('>>>>>>>>>>>>>>01');
        window.location = redirectURLifOK;
        console.log(redirectURLifOK);
    }	
}

function btnUpload_onclick()
{
	console.log('>>>>>>>>>>>>>>>>>>>>>>>>>>btnUpload_onclick');
	
	var grupoID;
	var userID;
	var empresaID;
	var pastaID;
	var strActionPage;
	console.log(strActionPage);
	var strHostIP;
	console.log(strHostIP);

	var CurrentPathName = unescape(location.pathname); // get current PathName in plain ASCII 
	console.log(CurrentPathName);
	var CurrentPath = CurrentPathName.substring(0, CurrentPathName.lastIndexOf("/") + 1); 
	console.log(CurrentPath);
	//strActionPage = CurrentPath + "upload"; //the ActionPage's file path
	console.log('--------------destino');
	userID= document.getElementById("user_id").value
	console.log(userID)
	
	grupoID= document.getElementById("grupo_id").value
	console.log(grupoID)
	
	empresaID= document.getElementById("empresa_id").value
	console.log(empresaID)
	
	pastaID= document.getElementById("pasta_id").value
	console.log(pastaID)
	
	
	strActionPage = "/multiuploader_digitalizacao/"+userID+"/"+grupoID+"/"+empresaID+"/"+pastaID+"/"; //the ActionPage's file path
	console.log(strActionPage);

	strHostIP = "54.243.50.54"; //The host's IP or name
	console.log(strHostIP);

	WebTWAIN.HTTPPort = 80; 
	WebTWAIN.HTTPUploadAllThroughPostAsPDF(strHostIP,strActionPage,"imageData.pdf");
	console.log('upou!')

	if (WebTWAIN.ErrorCode != 0){
		alert(WebTWAIN.ErrorString);
    }
	else{ //succeded
		alert("Imagem enviado com sucesso!");
    }
} 

function btnUpload_onclick_terceiro()
{
	console.log('>>>>>>>>>>>>>>>>>bntupload');
	// Grab the underlying form
    var form = $("#btnUpload").parent('form');

    console.log(form);
    var ORIG_ACTION = form.attr('action');
    console.log(ORIG_ACTION);
    var ORIG_METHOD = form.attr('method');
    console.log(ORIG_METHOD);
            
    var UID = null;
    console.log(UID);

    form.submit(function(){

        /* First, post the form */
        var data = $(this).serialize();
        console.log(data);

        $.ajax({
            url: '/twain/form/?orig='+ORIG_ACTION,
            method: ORIG_METHOD,
            data: data,
            dataType: 'json',
            success: function(data){
                UID = data.uid;
                console.log(UID);
                twain_instance.HTTPUploadAllThroughPostAsPDF(
                    SERVER, 
                    UPLOAD_PATH,
                    "upload["+UID+"].pdf"
                );

                //window.location.href="/twain/redirect/?uid="+UID;
                console.log('>>>>>>>>>>>>>>>>>>post');
                $.post('/digitalizar/'+UID+'/', function(data){});
                console.log('upou!');
            }

        });

        return false;
    });

} 