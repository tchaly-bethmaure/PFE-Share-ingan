$(document).ready(function(){
    // posts : 
    preg_twit = "https:\/\/.+\/(.+)\/status\/[0-9]+";
    // profil page : 
    preg_profil = "https:\/\/.+\/(.+)";

    twitt_match = window.location.href.match(preg_twit)
    profil_match = window.location.href.match(preg_profil)

    if(twitt_match || profil_match)
    {
        nickname = undefined;
        if(twitt_match)
        {
            nickname = twitt_match[1];
        }
        else
        {
            nickname = profil_match[1];
        }

        $.ajax({
            url: "http://127.0.0.1:7776/istoxic/get/"+nickname,
            data: "",
            type: 'GET',
            success: function(data) { 
                if(data){
                    qualification = "Safe";
                    if(0 >= parseInt(data))
                    {
                        color = 'green';
                        qualification = "Safe";
                    }
                    else if(parseInt(data) <= 100)
                    {
                        color = 'yellow';
                        qualification = "Toxic";
                    }
                    else if(1000 <= parseInt(data))
                    {
                        color = 'red';
                        qualification = "Really toxic";
                    }
                    else if(10000 <= parseInt(data))
                    {
                        color = 'violet';
                        qualification = "To avoid";
                    }
    
                    setTimeout(function(){
                        var mySpans = $("span:contains('"+nickname+"')");
                        for(var i=0; i < mySpans.length; i++){
                            console.log(mySpans[i].innerHTML+ " changed to "+color+" with "+qualification+" ("+data+" reports).");
                            mySpans[i].innerHTML = "<font color='"+color+"' title='"+qualification+" ("+data+" reports)'>"+mySpans[i].innerHTML+"</font>";
            
                            break;
                        }
                    }, 3500);
                }
                else
                {
                    document.getElementById("toxic_search").innerHTML = "<b><font color='green' title='Safe (not toxic)'>"+mySpans[i].innerHTML+"</font></b>"; 
                }
            },
            error: function(err) {
                console.log("error", err);
            }
        });   
    }
});           
            
         