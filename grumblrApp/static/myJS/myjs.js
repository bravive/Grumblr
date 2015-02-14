$(document).ready( function() {
     //grumbls_sendRequest();
     get_first_grumblrID();
});
function ajax_submit_comment(itemid){
    var frm = $("#ajaxformcomment"+itemid);
    frm.submit(function(e)
       {
        //e.preventDefault();
       $(function () {$.ajaxSetup({headers: { "X-CSRFToken": getCookie("csrftoken") }});});
       var postData = frm.serializeArray();
       var formURL = $(this).attr("action");
       $.ajax(
          {
          url : formURL,
          type: "POST",
          data : postData,
          dataType: "json",
          success: function (data) {
              comments_sendRequest(itemid);
          }
          });
         e.preventDefault();
       });
}
function ajax_submit_dlike(itemid){
    var frm = $("#ajaxformdlike"+itemid);
    frm.submit(function(e)
       {
       $(function () {$.ajaxSetup({headers: { "X-CSRFToken": getCookie("csrftoken") }});});
       var postData = $(this).serializeArray();
       var formURL = $(this).attr("action");
       $.ajax(
        {
        url : formURL,
        type: "POST",
        data : postData,

        success: function (data) {
              dlikes_sendRequest(itemid);
        }
        });
       
       e.preventDefault();
       });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



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
/*
function size_myreply(itemid){
    var mysize=document.getElementById("`myinput"+itemid);
	if (mysize.className=="myclass-smallsize"){
		mysize.className ="myclass-largesize";
	}
	else{
		mysize.className ="myclass-smallsize";
	}
}
function size_mydlike(itemid){
    var mysize=document.getElementById("mydlike"+itemid);
	if (mysize.className=="myclass-smallsize"){
		mysize.className ="myclass-largesize";
	}
	else{
		mysize.className ="myclass-smallsize";
	}
}
function size_mycomments(itemid){
    var mysize=document.getElementById("mycomments"+itemid);
	if (mysize.className=="myclass-smallsize"){
		mysize.className ="myclass-largesize";
	}
	else{
		mysize.className ="myclass-smallsize";
	}
}*/


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

function grumbls_sendRequest(NowGrumblrId) {
    var req;
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req.onreadystatechange =handleResponse;
    req.open("GET", "http://localhost:8000/grumblrApp/updategrumbls/"+NowGrumblrId, true);
    req.send();
    
    function handleResponse(){
        if (req.readyState != 4 || req.status != 200) {
            
            return;
        }
        var items = JSON.parse(req.responseText);
        if (items.length!=0){
            var list = document.getElementById("mygrumbls");
            for (var i = items.length-1; i >=0; i--) {
                var grumblr = items[i]["fields"]["grumblr"];
                var grumblrId = items[i]["fields"]["grumblr_id"];
                
                //if(grumblrId<=NowGrumblrId){continue;}
                var grumblrUserId = items[i]["fields"]["grumblr_userid"];
                var grumblrUsername = items[i]["fields"]["grumblr_username"];
                var newli = document.createElement("li");
                newli.setAttribute("id", "grumblr"+grumblrId);
                
                var newGrumblrButton;
                var newGrumblrImg;
                var newGrumblrUsername;
                var newGrumblrComment;
                var newGrumblrDlike;
                var newGrumblrCommentInput;
                newGrumblrButton= "<button class=\"media list-group-item\" style=\"margin-top:0px; padding-bottom:10px; width:580px\" onclick=\"size_modify("+grumblrId+")\"> ";
                newGrumblrImg= "<img class=\"media-object pull-left\" src=\"/grumblrApp/photo_userid/"+ grumblrUserId +"\" width=\"50px\"/> ";

                newGrumblrUsername =" <p class=\"media-body media-heading\" style=\"float:left\"><a href=\"/profile_others.html/"+ grumblrUserId +"\"> <strong>"+grumblrUsername+"</strong></a> :"+grumblr+"</p></button>";
                newGrumblrComment="<ol id=\"mycomments"+grumblrId+ "\"class=\"myclass-smallsize\" style=\"list-style-type:none\"></ol>"
                
                newGrumblrDlike="<form id=\"ajaxformdlike"+grumblrId+"\" action=\"/dlike/"+grumblrId+"/1\"  method=\"post\"><div id=\"mydlike"+grumblrId+"\" class=\"myclass-smallsize\"><input type=\"submit\" class=\"btn btn-default\" value=\"Dislike\" onclick=\"ajax_submit_dlike("+grumblrId+")\"><span id=\"mydlike_username"+grumblrId+"\"></span></div></form>"
                
                newGrumblrCommentInput="<form id=\"ajaxformcomment"+grumblrId+"\" action=\"/addcomment_dynamic/"+grumblrId+"/1\" method=\"post\"><div id=\"myinput"+grumblrId+"\" class=\"myclass-smallsize\"><input type=\"submit\" class=\"btn btn-default\" value=\"Reply\"  onclick=\"ajax_submit_comment("+grumblrId+")\"><input name=\"comment_input_name"+grumblrId+"\" type=\"text\" placeholder=\"Reply...\" class=\"form-control\" style=\"width:100px\"></div></form>"
                //<input type=\"hidden\" name=\"csrfmiddlewaretoken\" value=\"$csrf_token\"/>
                newli.innerHTML=newGrumblrButton+newGrumblrImg+newGrumblrUsername+newGrumblrDlike+newGrumblrCommentInput+newGrumblrComment;
                //console.log("here"+grumblrId);
                list.insertBefore(newli, list.firstChild);
            }
        }
    }
}
function get_first_grumblrID(){
    grumblrid=0;
    if($("#mygrumbls").children().length > 0){
        first_sublist_id=$("#mygrumbls li:first-child").attr("id");
        grumblrid=first_sublist_id.replace(/[^\d]/g, "");
        //console.log(grumblrid);
        //return parseInt(grumblrid);
    }
    //console.log(grumblrid);
    grumbls_sendRequest(parseInt(grumblrid));
    //return 0;
}
window.setInterval(get_first_grumblrID, 10000);
//window.setInterval(grumbls_sendRequest, 5000);
//list = document.getElementById("grumblr"+grumblrUserId);
//console.log(list.getAttribute("id"));
/*
 $.get( "/grumblrApp/getUserNameById/"+grumblrUserId, function( data ) {
 username = data[0]["fields"]["username"];
 text = document.getElementById("grumblr_user_name"+grumblrId);
 text.innerHTML=username;
 console.log(text);
 });*/
//comments_sendRequest(grumblrId);


/*

function username_sendRequest(itemid) {
    var req;
    var items;
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req.onreadystatechange =function(items){
        if (req.readyState != 4 || req.status != 200) {
            
            return;
        }
        items = JSON.parse(req.responseText);
        return items[0]["fields"]["username"];
    };
    console.log(items);
    req.open("GET", "http://localhost:8000/grumblrApp/getUserNameById/"+itemid, true);
    req.send();
}
 */
// causes the posts_sendRequest function to run every 10 seconds
//

/*
 [
 {% for comment in comments %}
 {"text":"{{comment.text}}", "grumblr":"{{comment.item}}","grumblrid":"{{comment.item.id}}","user":"{{comment.user}}","userid":"{{comment.user.id}}"},
 {% endfor %}
 ]
 
 */
// This function is called for each request readystatechange,
// and it will eventually parse the XML response for the request



