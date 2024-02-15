$(document).ready(function(){
    function filter() {
        // Declare variables
        var filter;
        filter = $("#pseudo_search").val();

        if(filter.length <= 2)
            return;
        displayField = document.getElementById("toxic_result");
        $.ajax({
            url: "https://Tchaly.pythonanywhere.com/istoxic/get/reports/"+filter,
            data: "",
            type: 'GET',
            success: function(data) { 
                if(data){
                    i=1;
                    htmlToDisplay = "";
                    data.forEach(element => {
                        htmlToDisplay += "<li color='red'><a href='"+element+"' target='_blanck' >Report #"+i+"</a></li>";
                        i++;
                    });

                    document.getElementById("toxic_result").innerHTML = htmlToDisplay; 
                }
                else
                {
                    document.getElementById("toxic_search").innerHTML = "<li color='green'>None</li>"; 
                }
            },
            error: function(err) {
                console.log("error", err);
            }
        });
    }
    
    document.getElementById("pseudo_search").addEventListener('keyup', filter, false);  
});
