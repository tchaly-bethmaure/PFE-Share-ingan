$(document).ready(function(){
    function addtoxic()
    {
        preg_twitter = "https:\/\/twitter.com\/(.+)";

        // Get pseudo search field
        pseudoToSearch = $("#pseudo_report").val();
        pseudoToSearch = pseudoToSearch;
        postlink = $("#post_link_to_report").val();

        if(postlink.match(preg_twitter))
        {
            $.ajax({
                url: "https://Tchaly.pythonanywhere.com/istoxic/report/" + pseudoToSearch,
                data: ""+postlink,
                type: 'POST',
                success: function(data) { 
                    if(data)
                    {
                        document.getElementById("toxic_report").innerHTML = "<b><font color='blue'>"+data+"</font></b>"; 
                    }
                    else
                    {
                        document.getElementById("toxic_report").innerHTML = "<b style='color:red;'>Error</b>"; 
                    }
                },
                error: function(err) {
                    console.log("error", err);
                }
            });
        }
        else
        {
            document.getElementById("toxic_report").innerHTML = "<b style='color:orange;'>Invalid link</b>"; 
        }
    }
    document.getElementById("btn_report").addEventListener('click', addtoxic, false);    
});
