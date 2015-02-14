
function size_modify(itemid){
    var myinput_size=document.getElementById("myinput"+itemid);
    var mycomments_size=document.getElementById("mycomments"+itemid);
    var mydlike_size=document.getElementById("mydlike"+itemid);
    
	if (myinput_size.className=="myclass-largesize" && mycomments_size.className=="myclass-largesize"&& mydlike_size.className=="myclass-largesize"){
		myinput_size.className ="myclass-smallsize";
		mycomments_size.className="myclass-smallsize";
		mydlike_size.className="myclass-smallsize";
	}
	else{
        dlikes_sendRequest(itemid);
        comments_sendRequest(itemid);
        //grumbls_sendRequest();
		myinput_size.className ="myclass-largesize";
		mycomments_size.className="myclass-largesize";
		mydlike_size.className="myclass-largesize";
	}
}
function dlikes_sendRequest(itemid) {
    //console.log(itemid);
    var req;
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req.onreadystatechange =handleResponse;
    req.open("GET", "http://localhost:8000/grumblrApp/alldlikes/"+itemid, true);
    req.send();
    
    function handleResponse(){
        if (req.readyState != 4 || req.status != 200) {
            
            return;
        }
        var items = JSON.parse(req.responseText);
        //console.log(itemid);
        var span = $("#mydlike_username"+itemid);
        span.empty();
        for (var i = 0; i < items.length; i++) {
            var dislikeUsername = items[i]["fields"]["dlike_usrname"];
            var newp = "<h>"+dislikeUsername+"&nbsp;&nbsp;</h>";
            span.append($(newp));
        }
        
    }
}
// Sends a new request to update the to-do list

function comments_sendRequest(itemid) {
    //console.log(itemid);
    var req;
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req.onreadystatechange =handleResponse;
    req.open("GET", "http://localhost:8000/grumblrApp/allcomments/"+itemid, true);
    req.send();
    
    function handleResponse(){
        if (req.readyState != 4 || req.status != 200) {
            
            return;
        }
        var items = JSON.parse(req.responseText);
        //console.log(itemid);
        var list = document.getElementById("mycomments"+itemid);
        while (list.hasChildNodes()) {
            list.removeChild(list.firstChild);
        }
        for (var i = 0; i < items.length; i++) {
                var commentText = items[i]["fields"]["text"];
                var commentUserId = items[i]["fields"]["user"];
                var newli = document.createElement("li");
                newli.innerHTML ="<img style=\"margin:5px\" src=\"/grumblrApp/photo_userid/"+commentUserId+ "\" height=\"25px\"/>"+commentText;
                list.appendChild(newli);
        }
   
    }
}
//window.setInterval(get_first_grumblrID, 5000);
