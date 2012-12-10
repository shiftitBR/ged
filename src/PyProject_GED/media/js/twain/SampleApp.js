﻿var WebTWAIN;
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
    strObjectFF += " class='divcontrol' pluginspage='../media/twain/resources/DynamicWebTwain.xpi'></embed>";

    var strObject = GetObject();
		
	var obj = document.getElementById("maindivIElimit");
    obj.style.display = "none";
	
    if (ExplorerType() == "IE" && navigator.userAgent.indexOf("Win64") != -1 && navigator.userAgent.indexOf("x64") != -1) {
        strObject = "<object id='mainDynamicWebTwainIE' codebase='../media/twain/resources/DynamicWebTWAINx64.cab#version=8,0,1' class='divcontrol' " + "classid='clsid:E7DA7F8D-27AB-4EE9-8FC0-3FEC9ECFE758' viewastext> " + strObject;
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
    	strObject = "<object id='mainDynamicWebTwainIE' codebase='../media/twain/resources/DynamicWebTWAIN.cab#version=8,0,1' class='divcontrol' " + "classid='clsid:E7DA7F8D-27AB-4EE9-8FC0-3FEC9ECFE758' viewastext> " + strObject;
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

function btnUpload_onclick()
{
	
	var grupoID;
	var userID;
	var empresaID;
	var pastaID;
	var strActionPage;
	var strHostIP;

	var CurrentPathName = unescape(location.pathname); // get current PathName in plain ASCII 
	var CurrentPath = CurrentPathName.substring(0, CurrentPathName.lastIndexOf("/") + 1); 
	//strActionPage = CurrentPath + "upload"; //the ActionPage's file path
	userID= document.getElementById("user_id").value
	grupoID= document.getElementById("grupo_id").value
	empresaID= document.getElementById("empresa_id").value
	pastaID= document.getElementById("pasta_id").value
	
	strActionPage = "/multiuploader_digitalizacao/"+userID+"/"+grupoID+"/"+empresaID+"/"+pastaID+"/"; //the ActionPage's file path
	strHostIP = "54.243.50.54"; //The host's IP or name

	WebTWAIN.HTTPPort = 80; 
	WebTWAIN.HTTPUploadAllThroughPostAsPDF(strHostIP,strActionPage,"imageData.pdf");

	if (WebTWAIN.ErrorCode != 0){
		alert(WebTWAIN.ErrorString);
    }
	else{ //succeded
		alert("Imagem enviado com sucesso!");
    }
} 