$(document).ready(function(){
    function reportGo()
    {
        window.location = "share.html";
    }

    function searchGo()
    {
        window.location = "search.html";
    }

    document.getElementById("btn_go_report").addEventListener('click', reportGo, false);    
    document.getElementById("btn_go_search").addEventListener('click', searchGo, false);

});
