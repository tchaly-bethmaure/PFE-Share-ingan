$(document).ready(function(){
    var shareingan_enabled = true;

    if(shareingan_enabled == true)
    {
        console.log("Running ...");
        
        
        // tweet : 
        preg_twit = "https:\/\/.+\/(.+)\/status\/[0-9]+";
        // profil page : 
        preg_profil = "https:\/\/.+\/(.+)";
        // retweet :
        preg_retwit = "https:\/\/.+\/(.+)\/status\/[0-9]+";

        twitt_match = window.location.href.match(preg_twit)
        profil_match = window.location.href.match(preg_profil)

        // filter feed
        setTimeout(function(){
            setInterval(function(){
                var mySpans = $("span:contains('@')");
                for(var i=0; i < mySpans.length; i++){
                    nickname = mySpans[i].innerHTML.replace("@","");
                    console.log(nickname+" is evaluated ...");
                    $.ajax({
                        url: "https://Tchaly.pythonanywhere.com/istoxic/get/"+nickname,
                        data: "",
                        type: 'GET',
                        async:false,
                        success: function(data) { 
                            if(data){
                                console.log(nickname+" Found...");
                                qualification = "Safe";
                                if(0 >= parseInt(data))
                                {
                                    color = 'green';
                                    qualification = "Safe";
                                }
                                else if(parseInt(data) <= 5)
                                {
                                    color = 'orange';
                                    qualification = "Toxic";
                                }
                                else if(10 <= parseInt(data))
                                {
                                    color = 'red';
                                    qualification = "Really toxic";
                                }
                                else if(15 <= parseInt(data))
                                {
                                    color = 'violet';
                                    qualification = "To avoid";
                                }
                                console.log(nickname+" "+qualification+" ("+data+")");
                                console.log(nickname+ " changed to "+color+" with "+qualification+" ("+data+" reports).");
                                mySpans[i].innerHTML = "<font color='"+color+"' title='"+qualification+" ("+data+" reports)'>@"+nickname+" ("+data+") </font>";
                            }
                            else
                            {
                                console.log(nickname+" not found (Safe)");
                                mySpans[i].innerHTML = "<font color='"+color+"' title='"+qualification+" ("+data+" report)'>@"+nickname+"</font>";
                            }
                        },
                        error: function(err) {
                            console.log("error", err);
                        }
                    });   
                }
            }, 10000);
        }, 2000);
    }else
    {
        console.log("Plugin Disabled");
    }
});        