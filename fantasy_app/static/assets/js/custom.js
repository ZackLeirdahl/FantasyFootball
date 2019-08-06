$(document).ready(function(){

    $("#teamsLink").hover(
        function(){
            $("#teamsLink").dropdown('toggle');},
        function(){}
    )

    $("#teamsDrop").mouseleave(function(){
        $("#teamsLink").dropdown('toggle');
    })

    $("#profileLink").hover(
        function(){
            $(this).dropdown('toggle');},
        function(){}
    )

    $("#profileDrop").mouseleave(function(){
        $("#profileLink").dropdown('toggle');
    })
    
    $('#positionFilter').hover(
        function() {
            $(this).addClass('focus');},
        function() {
            $(this).removeClass('focus');}
    );

    $('#weekSelect').on('change', function() {
        document.forms['weekForm'].submit();
     });

     $("#tabs").tabs();

     $("tbody").sortable({
         items: "> tr",
         appendTo: "parent",
         helper: "clone"
     }).disableSelection();
 
     $("#tabs ul li a").droppable({
         hoverClass: "drophover",
         tolerance: "pointer",
         drop: function(e, ui) {
             var tabdiv = $(this).attr("href");
             $(tabdiv + " table tr:last").after("<tr>" + ui.draggable.html() + "</tr>");
             ui.draggable.remove();
         }
     });

    addFileName(document.getElementById('customFile'));
});

window.onload = function() {
    var links = window.location.href.split('/');
    if (links.includes('matchups') || links.includes('matchups#'))
    {
        document.getElementById('matchupsLink').classList.add('active');
    }
    if (links.includes('standings') || links.includes('standings#'))
    {
        document.getElementById('standingsLink').classList.add('active');
    }
    if (links.includes('feed') || links.includes('feed#'))
    {
        document.getElementById('feedLink').classList.add('active');
    }
    if (links.includes('players') || links.includes('players#'))
    {
        document.getElementById('playersLink').classList.add('active');
    }
    if (links.includes('teams') || links.includes('teams#'))
    {
        document.getElementById('teamsLink').classList.add('active');
    }

}
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
    
function initSliders() {
    var slide = $('.noUi-origin');
    var position = slide.position();
    var percent = parseFloat(position.left) / 390;
    alert(percent);
}

$(function () {
    $('.selectpicker').selectpicker();
});

function paginate()
{
    var recordPerPage = 25;
    if(($('#pagedTable').find('tbody tr:has(td)').length / recordPerPage) > 9)
    {
        recordPerPage = Math.ceil($('#pagedTable').find('tbody tr:has(td)').length/10);
    }
    var totalPages = Math.ceil($('#pagedTable').find('tbody tr:has(td)').length / recordPerPage);
    var $pages = $('<ul class="pagination justify-content-center"></ul>');
    for (i = 0; i < totalPages; i++) {
        $('<li class="page-item"><a class="page-link" href="#">&nbsp;' + (i + 1) + '</a></li>').appendTo($pages);
    }
    $pages.appendTo('#playersPage');

    $('.page-link').hover(
        function() {
            $(this).addClass('focus');},
        function() {
            $(this).removeClass('focus');}
    );

    $('table').find('tbody tr:has(td)').hide();
    var tr = $('table tbody tr:has(td)');
    for (var i = 0; i <= recordPerPage - 1; i++) {
        $(tr[i]).show();
    }
   
    $('.page-link').click(function(event) {
        $('#pagedTable').find('tbody tr:has(td)').hide();
        for (var i = ($(this).text() - 1) * recordPerPage; i <= $(this).text() * recordPerPage - 1; i++) {
            $(tr[i]).show();}
    });
}
function enableButton(btn_id){
    if(document.getElementById(btn_id).disabled == true)
    {
        document.getElementById(btn_id).disabled = false;
    }
}