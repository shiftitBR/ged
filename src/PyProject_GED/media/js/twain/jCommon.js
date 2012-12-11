
//====================Page Onload  Start==================//
function ExplorerType() {
    ua = (navigator.userAgent.toLowerCase());
    if (ua.indexOf("msie") != -1) {
        return "IE";
    }
    else {
        return "notIE";
    }
}

function pause() {
    clearInterval(seed);
}

function GetObject() {
    var strObject = "";
    strObject += "	<param name='Manufacturer' value='DynamSoft Corporation' />";
    strObject += "	<param name='ProductFamily' value='Dynamic Web TWAIN' />";
    strObject += "	<param name='ProductName' value='Dynamic Web TWAIN' />";
    strObject += "	</object>";
    return strObject;
}

function GetEventString() {
    var strObjectFF = "";
    strObjectFF = " <embed style='display: inline' id='mainDynamicWebTWAINnotIE' type='Application/DynamicWebTwain-Plugin'";
    strObjectFF += " OnPostTransfer='DynamicWebTwain_OnPostTransfer' OnPostAllTransfers='DynamicWebTwain_OnPostAllTransfers'";
    strObjectFF += " OnMouseClick='DynamicWebTwain_OnMouseClick'  OnPostLoad='DynamicWebTwain_OnPostLoadfunction'";
    strObjectFF += " OnImageAreaSelected = 'DynamicWebTwain_OnImageAreaSelected'";
    strObjectFF += " OnImageAreaDeSelected = 'DynamicWebTwain_OnImageAreaDeselected'";
    strObjectFF += " OnMouseDoubleClick = 'DynamicWebTwain_OnMouseDoubleClick'";
    strObjectFF += " OnMouseRightClick = 'DynamicWebTwain_OnMouseRightClick'";
    strObjectFF += " OnTopImageInTheViewChanged = 'DynamicWebTwain_OnTopImageInTheViewChanged'";
    return strObjectFF;
}

function GetIEEventString() {
    WebTWAIN.attachEvent('OnPostTransfer', DynamicWebTwain_OnPostTransfer);
    WebTWAIN.attachEvent('OnPostAllTransfers', DynamicWebTwain_OnPostAllTransfers);
    WebTWAIN.attachEvent('OnMouseClick', DynamicWebTwain_OnMouseClick);
    WebTWAIN.attachEvent('OnPostLoad', DynamicWebTwain_OnPostLoadfunction);
    WebTWAIN.attachEvent('OnImageAreaSelected', DynamicWebTwain_OnImageAreaSelected);
    WebTWAIN.attachEvent('OnMouseDoubleClick', DynamicWebTwain_OnMouseDoubleClick);
    WebTWAIN.attachEvent('OnMouseRightClick', DynamicWebTwain_OnMouseRightClick);
    WebTWAIN.attachEvent('OnTopImageInTheViewChanged', DynamicWebTwain_OnTopImageInTheViewChanged);
    WebTWAIN.attachEvent('OnImageAreaDeSelected', DynamicWebTwain_OnImageAreaDeselected);
}


function AddResolution() {
    Resolution = document.getElementById("Resolution");
    Resolution.options.length = 0;
    Resolution.options.add(new Option("100", 100));
    Resolution.options.add(new Option("150", 150));
    Resolution.options.add(new Option("200", 200));
    Resolution.options.add(new Option("300", 300));
        
}

function AddPreviewMode() {
    PreviewMode = document.getElementById("PreviewMode");
    PreviewMode.options.length = 0;
    PreviewMode.options.add(new Option("1X1", 0));
    PreviewMode.options.add(new Option("2X2", 1));
    PreviewMode.options.add(new Option("3X3", 2));
    PreviewMode.options.add(new Option("4X4", 3));
    PreviewMode.options.add(new Option("5X5", 4));
    PreviewMode.selectedIndex = 0;
}

function AddInterpolationMethod() {

    InterpolationMethod = document.getElementById("InterpolationMethod");
    InterpolationMethod.options.length = 0;
    InterpolationMethod.options.add(new Option("NearestNeighbor", 1));
    InterpolationMethod.options.add(new Option("Bilinear", 2));
    InterpolationMethod.options.add(new Option("Bicubic", 3));
}

function SetFileName(){
    txt_fileNameforSave = document.getElementById("txt_fileNameforSave");
    txt_fileNameforSave.value = "WebTWAINImage";

    txt_fileName = document.getElementById("txt_fileName");
    txt_fileName.value = "WebTWAINImage";
}

function SetMultiPageInfo() {
    MultiPageTIFF_save = document.getElementById("MultiPageTIFF_save");
    MultiPageTIFF_save.disabled = true;
    MultiPagePDF_save = document.getElementById("MultiPagePDF_save");
    MultiPagePDF_save.disabled = true;
    MultiPageTIFF = document.getElementById("MultiPageTIFF");
    MultiPageTIFF.disabled = true;
    MultiPagePDF = document.getElementById("MultiPagePDF");
    MultiPagePDF.disabled = true;
}

function SetNoScanner() {
    pNoScanner = document.getElementById("pNoScanner");
    pNoScanner.style.display = "block";
    pNoScanner.style.textAlign = "center";
}

function SetShowOrCloseLoadImage() {
    for (var i = 0; i < document.links.length; i++) {
        if (document.links[i].className == "ShowtblLoadImage") {
            document.links[i].onclick = ShowtblLoadImage_onclick;
        }
        if (document.links[i].className == "ClosetblLoadImage") {
            if (WebTWAIN.SourceCount == 0)
                document.links[i].parentNode.removeChild(document.links[i]);
            else
                document.links[i].onclick = ClosetblLoadImage_onclick;
        }
    }
}

function DoWithNoSource() {
    if (WebTWAIN.SourceCount == 0) {
        document.getElementById("aNoScanner").style.color = "Red";
        document.getElementById("aNoScanner").innerHTML = "<b>No TWAIN compatible drivers detected:<b/>";
        document.getElementById("Resolution").style.display = "none";
        ShowtblLoadImage_onclick();
    }
    else
        document.getElementById("divBlank").style.display = "none";
}

function ShowtblLoadImage_onclick() {
    switch (document.getElementById("tblLoadImage").style.visibility) {
        case "hidden": document.getElementById("tblLoadImage").style.visibility = "visible";
                document.getElementById("Resolution").style.visibility = "hidden";
            break;
        case "visible":
            if (WebTWAIN.SourceCount != 0) {
                document.getElementById("tblLoadImage").style.visibility = "hidden";
                        document.getElementById("Resolution").style.visibility = "visible";
                        }
            break;
        default: break;
    }
    document.getElementById("tblLoadImage").style.top = ds_gettop(document.getElementById("pNoScanner")) + pNoScanner.offsetHeight + "px";
    document.getElementById("tblLoadImage").style.left = ds_getleft(document.getElementById("pNoScanner")) + 0 + "px";
    return false;
}
function ClosetblLoadImage_onclick() {
    document.getElementById("tblLoadImage").style.visibility = "hidden";
     document.getElementById("Resolution").style.visibility = "visible";
    return false;
}
//====================Page Onload End====================//

//====================Frequently Used Functions=======================//

function AppendMessage(strMessage) {
    var objMessage = document.getElementById("emessage");
    if (objMessage) {
        var tmp = objMessage.innerHTML;
        objMessage.innerHTML = tmp + strMessage;
        objMessage.scrollTop = objMessage.scrollHeight;
    }
}

function CheckIfImagesInBuffer() {
    if (WebTWAIN.HowManyImagesInBuffer == 0) {
        //em = em + "There is no image in buffer.<br />";
        //objEmessage.innerHTML = em;
        AppendMessage("There is no image in buffer.<br />");
        return false;
    }
    else {
        return true;
    }
}

function CheckErrorString() {
    if (WebTWAIN.ErrorCode == 0) {
        //em = em + "<span style='color:#cE5E04'><b>" + WebTWAIN.ErrorString + "</b></span><br />";
        //objEmessage.innerHTML = em;
        //objEmessage.scrollTop = objEmessage.scrollHeight;
        return true;
    }
    if (WebTWAIN.ErrorCode == -2115) //Cancel file dialog
        return true;
    else {
        if (WebTWAIN.ErrorCode == -2003) {
            var ErrorMessageWin = window.open("", "ErrorMessage", "height=500,width=750,top=0,left=0,toolbar=no,menubar=no,scrollbars=no, resizable=no,location=no, status=no");
            ErrorMessageWin.document.writeln(WebTWAIN.HTTPPostResponseString);
        }
        //em = em + "<span style='color:#cE5E04'><b>" + WebTWAIN.ErrorString + "</b></span><br />";
        //objEmessage.innerHTML = em;
        //objEmessage.scrollTop = objEmessage.scrollHeight;
        return false;
    }
}

function ds_getleft(el) {
    var tmp = el.offsetLeft;
    el = el.offsetParent
    while (el) {
        tmp += el.offsetLeft;
        el = el.offsetParent;
    }
    return tmp;
}
function ds_gettop(el) {
    var tmp = el.offsetTop;
    el = el.offsetParent
    while (el) {
        tmp += el.offsetTop;
        el = el.offsetParent;
    }
    return tmp;
}

function UpdatePageInfo() {
    TotalImage.value = WebTWAIN.HowManyImagesInBuffer;
    CurrentImage.value = WebTWAIN.CurrentImageIndexInBuffer + 1;
}

//====================Preview Group Start====================//
function btnFirstImage_onclick() {
    if (!CheckIfImagesInBuffer()) {
        return;
    }
    WebTWAIN.CurrentImageIndexInBuffer = 0;
    UpdatePageInfo();
}
function btnPreImage_onclick() {
    if (!CheckIfImagesInBuffer()) {
        return;
    }
    else if (WebTWAIN.CurrentImageIndexInBuffer == 0) {
        return;
    }
    WebTWAIN.CurrentImageIndexInBuffer = WebTWAIN.CurrentImageIndexInBuffer - 1;
    UpdatePageInfo();
}
function btnNextImage_onclick() {
    if (!CheckIfImagesInBuffer()) {
        return;
    }
    else if (WebTWAIN.CurrentImageIndexInBuffer == WebTWAIN.HowManyImagesInBuffer - 1) {
        return;
    }
    WebTWAIN.CurrentImageIndexInBuffer = WebTWAIN.CurrentImageIndexInBuffer + 1;
    UpdatePageInfo();
}
function btnLastImage_onclick() {
    if (!CheckIfImagesInBuffer()) {
        return;
    }
    WebTWAIN.CurrentImageIndexInBuffer = WebTWAIN.HowManyImagesInBuffer - 1;
    UpdatePageInfo();
}

function btnRemoveCurrentImage_onclick() {
    if (!CheckIfImagesInBuffer()) {
        return;
    }
    WebTWAIN.RemoveAllSelectedImages();
    if (WebTWAIN.HowManyImagesInBuffer == 0) {
        TotalImage.value = WebTWAIN.HowManyImagesInBuffer;
        CurrentImage.value = "";
        return;
    }
    else {
        UpdatePageInfo();
    }
}
function btnRemoveAllImages_onclick() {
    if (!CheckIfImagesInBuffer()) {
        return;
    }
    WebTWAIN.RemoveAllImages();
    TotalImage.value = "0";
    CurrentImage.value = "";
}
function slPreviewMode() {
    WebTWAIN.SetViewMode(parseInt(PreviewMode.selectedIndex + 1), parseInt(PreviewMode.selectedIndex + 1));
    if (ostype == "mac") {
        return;
    }
    else if (PreviewMode.selectedIndex != 0) {
        WebTWAIN.MouseShape = true;
    }
    else {
        WebTWAIN.MouseShape = false;
    }
}
//====================Preview Group End====================//

//====================Get Image Group Start=====================//

/*------------------Scan Image--------------------------*/
function btnScan_onclick() {
    WebTWAIN.SelectSourceByIndex(document.getElementById("source").selectedIndex);
    WebTWAIN.CloseSource();
    WebTWAIN.OpenSource();
    WebTWAIN.IfShowUI = false; //document.getElementById("ShowUI").checked;

    //var i;
    //for (i = 0; i < 3; i++) {
    //    if (document.getElementsByName("PixelType").item(i).checked == true)
    //        WebTWAIN.PixelType = i;
    //}
    WebTWAIN.PixelType = 0; //Color - (PB - Gray - RGB)
    WebTWAIN.Resolution = '150px';//Resolution.value;
    WebTWAIN.IfFeederEnabled = true; //document.getElementById("ADF").checked;
    WebTWAIN.IfDuplexEnabled = true; //document.getElementById("Duplex").checked;
    var strSCan = "Pixel Type: " + WebTWAIN.PixelType + "<br />Resolution: " + WebTWAIN.Resolution + "<br />";
    AppendMessage(strSCan);
    //objEmessage.innerHTML = em;
    //objEmessage.scrollTop = objEmessage.scrollHeight;
    WebTWAIN.IfDisableSourceAfterAcquire = true;
    WebTWAIN.AcquireImage();
}
//====================Get Image Group End=====================//

//====================Edit Image Group Start=====================//

function btnShowImageEditor_onclick() {//Dynamic Mac TWAIN doesn't support this method yet.
    if (!CheckIfImagesInBuffer()) {
        return;
    }
    WebTWAIN.ShowImageEditor();
}

function btnRotateRight_onclick() {
    if (!CheckIfImagesInBuffer()) {
        return;
    }
    WebTWAIN.RotateRight(WebTWAIN.CurrentImageIndexInBuffer);
}
function btnRotateLeft_onclick() {
    if (!CheckIfImagesInBuffer()) {
        return;
    }
    WebTWAIN.RotateLeft(WebTWAIN.CurrentImageIndexInBuffer);
}

function btnMirror_onclick() {
    if (!CheckIfImagesInBuffer()) {
        return;
    }
    WebTWAIN.Mirror(WebTWAIN.CurrentImageIndexInBuffer);
}
function btnFlip_onclick() {
    if (!CheckIfImagesInBuffer()) {
        return;
    }
    WebTWAIN.Flip(WebTWAIN.CurrentImageIndexInBuffer);
}

/*----------------------Crop Method---------------------*/
function btnCrop_onclick() {
    if (!CheckIfImagesInBuffer()) {
        return;
    }
    if (ileft != 0 || itop != 0 || iright != 0 || ibottom != 0) {
        WebTWAIN.Crop(
            WebTWAIN.CurrentImageIndexInBuffer,
            ileft, itop, iright, ibottom
        );
        ileft = 0;
        itop = 0;
        iright = 0;
        ibottom = 0;
        return;
    }
    switch (document.getElementById("Crop").style.visibility) {
        case "visible": document.getElementById("Crop").style.visibility = "hidden"; break;
        case "hidden": document.getElementById("Crop").style.visibility = "visible"; break;
        default: break;
    }
    document.getElementById("Crop").style.top = ds_gettop(document.getElementById("btnCrop")) + document.getElementById("btnCrop").offsetHeight + "px";
    document.getElementById("Crop").style.left = ds_getleft(document.getElementById("btnCrop")) - 80 + "px";
}

function btnCropCancel_onclick() {
    document.getElementById("Crop").style.visibility = "hidden";
}
function btnCropOKInner() {
    document.getElementById("img_left").className = "";
    document.getElementById("img_top").className = "";
    document.getElementById("img_right").className = "";
    document.getElementById("img_bottom").className = "";
    if (!re.test(document.getElementById("img_left").value)) {
        document.getElementById("img_left").className += " invalid";
        document.getElementById("img_left").focus();
        em = em + "Please input a valid <b>left</b> value.<br />";
        objEmessage.innerHTML = em;
        objEmessage.scrollTop = objEmessage.scrollHeight;
        return;
    }
    if (!re.test(document.getElementById("img_top").value)) {
        document.getElementById("img_top").className += " invalid";
        document.getElementById("img_top").focus();
        em = em + "Please input a valid <b>top</top> value.<br />";
        objEmessage.innerHTML = em;
        objEmessage.scrollTop = objEmessage.scrollHeight;
        return;
    }
    if (!re.test(document.getElementById("img_right").value)) {
        document.getElementById("img_right").className += " invalid";
        document.getElementById("img_right").focus();
        em = em + "Please input a valid <b>right</b> value.<br />";
        objEmessage.innerHTML = em;
        objEmessage.scrollTop = objEmessage.scrollHeight;
        return;
    }
    if (!re.test(document.getElementById("img_bottom").value)) {
        document.getElementById("img_bottom").className += " invalid";
        document.getElementById("img_bottom").focus();
        em = em + "Please input a valid <b>bottom</b> value.<br />";
        objEmessage.innerHTML = em;
        objEmessage.scrollTop = objEmessage.scrollHeight;
        return;
    }
    WebTWAIN.Crop(
        WebTWAIN.CurrentImageIndexInBuffer,
        document.getElementById("img_left").value,
        document.getElementById("img_top").value,
        document.getElementById("img_right").value,
        document.getElementById("img_bottom").value
    );
}


/*----------------Change Image Size--------------------*/
function btnChangeImageSize_onclick() {
    if (!CheckIfImagesInBuffer()) {
        return;
    }
    switch (document.getElementById("ImgSizeEditor").style.visibility) {
        case "visible": document.getElementById("ImgSizeEditor").style.visibility = "hidden"; break;
        case "hidden": document.getElementById("ImgSizeEditor").style.visibility = "visible"; break;
        default: break;
    }
    document.getElementById("ImgSizeEditor").style.top = ds_gettop(document.getElementById("btnChangeImageSize")) + document.getElementById("btnChangeImageSize").offsetHeight + "px";
    document.getElementById("ImgSizeEditor").style.left = ds_getleft(document.getElementById("btnChangeImageSize")) - 30 + "px";
}
function btnCancelChange_onclick() {
    document.getElementById("ImgSizeEditor").style.visibility = "hidden";
}

function btnChangeImageSizeOKInner() {
    document.getElementById("img_height").className = "";
    document.getElementById("img_width").className = "";
    if (!re.test(document.getElementById("img_height").value)) {
        document.getElementById("img_height").className += " invalid";
        document.getElementById("img_height").focus();
        em = em + "Please input a valid <b>height</b>.<br />";
        objEmessage.innerHTML = em;
        objEmessage.scrollTop = objEmessage.scrollHeight;
        return;
    }
    if (!re.test(document.getElementById("img_width").value)) {
        document.getElementById("img_width").className += " invalid";
        document.getElementById("img_width").focus();
        em = em + "Please input a valid <b>width</b>.<br />";
        objEmessage.innerHTML = em;
        objEmessage.scrollTop = objEmessage.scrollHeight;
        return;
    }
    WebTWAIN.ChangeImageSize(
        WebTWAIN.CurrentImageIndexInBuffer,
        document.getElementById("img_width").value,
        document.getElementById("img_height").value,
        InterpolationMethod.selectedIndex + 1
    );
}

//====================Edit Image Group End==================//

/*-----------------Save Image Group---------------------*/
function btnSave_onclick() {
    if (!CheckIfImagesInBuffer()) {
        return;
    }
    var i, strimgType_save;
    for (i = 0; i < 5; i++) {
        if (document.getElementsByName("imgType_save").item(i).checked == true) {
            strimgType_save = document.getElementsByName("imgType_save").item(i).value;
            break;
        }
    }
    WebTWAIN.IfShowFileDialog = true;
    txt_fileNameforSave.className = "";
    if (!strre.test(txt_fileNameforSave.value)) {
        txt_fileNameforSave.className += " invalid";
        txt_fileNameforSave.focus();
        em = em + "Please input a valid <b>file name</b>.<br />";
        objEmessage.innerHTML = em;
        objEmessage.scrollTop = objEmessage.scrollHeight;
        return;
    }
    var strFilePath = "C:\\" + txt_fileNameforSave.value + "." + strimgType_save;
    if (strimgType_save == "tif" && MultiPageTIFF_save.checked) {
        if ((WebTWAIN.SelectedImagesCount == 1) || (WebTWAIN.SelectedImagesCount == WebTWAIN.HowManyImagesInBuffer)) {
            WebTWAIN.SaveAllAsMultiPageTIFF(strFilePath);
        }
        else {
            WebTWAIN.SaveSelectedImagesAsMultiPageTIFF(strFilePath);
        }
    }
    else if (strimgType_save == "pdf" && MultiPagePDF_save.checked) {
        if ((WebTWAIN.SelectedImagesCount == 1) || (WebTWAIN.SelectedImagesCount == WebTWAIN.HowManyImagesInBuffer)) {
            WebTWAIN.SaveAllAsPDF(strFilePath);
        }
        else {
            WebTWAIN.SaveSelectedImagesAsMultiPagePDF(strFilePath);
        }
    }
    else {
        switch (i) {
            case 0: WebTWAIN.SaveAsBMP(strFilePath, WebTWAIN.CurrentImageIndexInBuffer); break;
            case 1: WebTWAIN.SaveAsJPEG(strFilePath, WebTWAIN.CurrentImageIndexInBuffer); break;
            case 2: WebTWAIN.SaveAsTIFF(strFilePath, WebTWAIN.CurrentImageIndexInBuffer); break;
            case 3: WebTWAIN.SaveAsPNG(strFilePath, WebTWAIN.CurrentImageIndexInBuffer); break;
            case 4: WebTWAIN.SaveAsPDF(strFilePath, WebTWAIN.CurrentImageIndexInBuffer); break;
        }
    }
    if (CheckErrorString()) {
        return;
    }
    else {
        alert(WebTWAIN.ErrorString);
    }
}
/*-------------------------------------------------------*/

/*-----------------Upload Image Group---------------------*/
function btnUploadInner(strHTTPServer, strPort, strActionPage, redirectURLifOK) {
    if (!CheckIfImagesInBuffer()) {
        return;
    }
    var i, strActionPage, strImageType;
    txt_fileName.className = "";
    if (!strre.test(txt_fileName.value)) {
        txt_fileName.className += " invalid";
        txt_fileName.focus();
        em = em + "please input <b>file name</b>.<br />";
        objEmessage.innerHTML = em;
        objEmessage.scrollTop = objEmessage.scrollHeight;
        return;
    }
    WebTWAIN.HTTPPort = strPort;
    
    for (i = 0; i < 4; i++) {
        if (document.getElementsByName("ImageType").item(i).checked == true) {
            strImageType = i + 1;
            break;
        }
    }

    var uploadfilename = txt_fileName.value + "." + document.getElementsByName("ImageType").item(i).value;
    if (strImageType == 2 && MultiPageTIFF.checked) {
        if ((WebTWAIN.SelectedImagesCount == 1) || (WebTWAIN.SelectedImagesCount == WebTWAIN.HowManyImagesInBuffer)) {
            WebTWAIN.HTTPUploadAllThroughPostAsMultiPageTIFF(
                strHTTPServer,
                strActionPage,
                uploadfilename
            );
        }
        else {
            WebTWAIN.HTTPUploadThroughPostAsMultiPageTIFF(
                strHTTPServer,
                strActionPage,
                uploadfilename
            );
        }
    }
    else if (strImageType == 4 && MultiPagePDF.checked) {
        if ((WebTWAIN.SelectedImagesCount == 1) || (WebTWAIN.SelectedImagesCount == WebTWAIN.HowManyImagesInBuffer)) {
            WebTWAIN.HTTPUploadAllThroughPostAsPDF(
                strHTTPServer,
                strActionPage,
                uploadfilename
            );
        }
        else {
            WebTWAIN.HTTPUploadThroughPostAsMultiPagePDF(
                strHTTPServer,
                strActionPage,
                uploadfilename
            );
        }
    }
    else {
        WebTWAIN.HTTPUploadThroughPostEx(
            strHTTPServer,
            WebTWAIN.CurrentImageIndexInBuffer,
            strActionPage,
            uploadfilename,
            strImageType
        );
    }
    em = em + "<b>Upload: </b>";
}

/*------------------radio response----------------------------*/
function rdTIFFsave_onclick() {
    MultiPageTIFF_save.disabled = false;

    MultiPageTIFF_save.checked = false;
    MultiPagePDF_save.checked = false;
    MultiPagePDF_save.disabled = true;
}
function rdPDFsave_onclick() {
    MultiPagePDF_save.disabled = false;

    MultiPageTIFF_save.checked = false;
    MultiPagePDF_save.checked = false;
    MultiPageTIFF_save.disabled = true;
}
function rdsave_onclick() {
    MultiPageTIFF_save.checked = false;
    MultiPagePDF_save.checked = false;

    MultiPageTIFF_save.disabled = true;
    MultiPagePDF_save.disabled = true;
}
function rdTIFF_onclick() {
    MultiPageTIFF.disabled = false;

    MultiPageTIFF.checked = false;
    MultiPagePDF.checked = false;
    MultiPagePDF.disabled = true;
}
function rdPDF_onclick() {
    MultiPagePDF.disabled = false;

    MultiPageTIFF.checked = false;
    MultiPagePDF.checked = false;
    MultiPageTIFF.disabled = true;
}
function rd_onclick() {
    MultiPageTIFF.checked = false;
    MultiPagePDF.checked = false;

    MultiPageTIFF.disabled = true;
    MultiPagePDF.disabled = true;
}

/*------------------select menu response----------------------------*/

function DynamicWebTwain_OnPostTransfer() {
    //if (document.getElementById("DiscardBlank").checked == true) {
        var NewlyScannedImage = WebTWAIN.CurrentImageIndexInBuffer;
        if (WebTWAIN.IsBlankImage(NewlyScannedImage)) {
            WebTWAIN.RemoveImage(NewlyScannedImage);
        }
        em = em + "<b>Blank Discard (On PostTransfer): </b>";
        if (CheckErrorString()) {
            UpdatePageInfo();
            return;
        }
    //}
    UpdatePageInfo();
}

function DynamicWebTwain_OnPostLoadfunction(path, name, type) {
    if (WebTWAIN.ErrorCode != 0) {
        //alert(WebTWAIN.ErrorString);
        ShowErrorInMessageBox(WebTWAIN.ErrorString);
    }
    //if (document.getElementById("DiscardBlank").checked == true) {
        var NewlyScannedImage = WebTWAIN.CurrentImageIndexInBuffer;
        if (WebTWAIN.IsBlankImage(NewlyScannedImage)) {
            WebTWAIN.RemoveImage(NewlyScannedImage);
        }
        em = em + "<b>Blank Discard (On PostLoad): </b>";
        if (CheckErrorString()) {
            UpdatePageInfo();
            return;
        }
    //}
    UpdatePageInfo();
}

function DynamicWebTwain_OnPostAllTransfers() {
    WebTWAIN.CloseSource();
}

var imageindex;
var imageindex2;
function DynamicWebTwain_OnMouseClick(index) {
    imageindex = index;
    CurrentImage.value = index + 1;
}

function DynamicWebTwain_OnMouseRightClick(index2) {
    if (!CheckIfImagesInBuffer()) {
        return;
    }
}

function DynamicWebTwain_OnImageAreaSelected(index, left, top, right, bottom) {
    ileft = left;
    itop = top;
    iright = right;
    ibottom = bottom;
}

function DynamicWebTwain_OnImageAreaDeselected(index) {
    ileft = 0;
    itop = 0;
    iright = 0;
    ibottom = 0;
}

function DynamicWebTwain_OnMouseDoubleClick() {//Dynamic Mac TWAIN doesn't support this event
    var StrextraInfo;
    StrextraInfo = "Image Width: " + WebTWAIN.GetImageWidth(WebTWAIN.CurrentImageIndexInBuffer) +
        " Image Height: " + WebTWAIN.GetImageHeight(WebTWAIN.CurrentImageIndexInBuffer) +
        " Image Bit Depth: " + WebTWAIN.GetImageBitDepth(WebTWAIN.CurrentImageIndexInBuffer);
    document.getElementById("extraInfo").innerHTML = StrextraInfo;
    clearTimeout(timeout);
    timeout = setTimeout(function() {
        document.getElementById("extraInfo").innerHTML = "";
    }, 10000);
}

function DynamicWebTwain_OnTopImageInTheViewChanged(index) {
    CurrentImage.value = index + 1;
}
