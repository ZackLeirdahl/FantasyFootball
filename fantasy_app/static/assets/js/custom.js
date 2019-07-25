$(document).ready(function(){

    $("#teamsLink").hover(
        function()
        {
            $("#teamsLink").dropdown('toggle');
        },
        function(){}
    )

    $("#teamsDrop").mouseleave(function(){
        $("#teamsLink").dropdown('toggle');
    })

    $("#profileLink").hover(
        function(){
            $(this).dropdown('toggle');
        },
        function(){}
    )

    $("#profileDrop").mouseleave(function(){
        $("#profileLink").dropdown('toggle');
    })

    addFileName(document.getElementById('customFile'));
});

window.onload = function() {
    var page = window.location.href.split('/').slice(-1)[0];
    switch(page)
    {
        case "matchups":
            document.getElementById('matchupsLink').classList.add('active');
            return;
        case "standings":
            document.getElementById('standingsLink').classList.add('active');
            return;
        case "feed":
            document.getElementById('feedLink').classList.add('active');
            return;
        case "players":
            document.getElementById('playersLink').classList.add('active');
            return;
        case "weekly_awards":
            document.getElementById('weeklyLink').classList.add('active');
            return;
        case "teams":
            document.getElementById('teamsLink').classList.add('active');
            return;
    }}

function addFileName(cfile) {
    cfile.addEventListener('change', function () {
        document.getElementById('customFileLabel').innerText = event.srcElement.files[0].name;
    });
}

function changeImage(elem_id, post_id){
    var counter = parseInt(document.getElementById(elem_id.concat('p')).innerText);
    if (document.getElementById(elem_id).src == "http://127.0.0.1:5000/static/images/like.png")
    {
      document.getElementById(elem_id).src = "/static/images/unlike.png";
      document.getElementById(elem_id.concat('p')).innerText = counter + 1;
      sendLike(post_id,'1');
    }
    else
    {
      document.getElementById(elem_id).src = "/static/images/like.png";
      document.getElementById(elem_id.concat('p')).innerText = counter - 1;
      sendLike(post_id,'0');
    }
}

function sendLike(id, action) {
    var jqXHR = $.ajax({
        type: "POST",
        url: "/like",
        async: true,
        data: { id: id, action: action }
    });
    return jqXHR.responseText;
}



function collapse()
{
    $('.collapse').collapse('hide');
}





    
