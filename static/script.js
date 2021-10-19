function getCurrentDate(){
    setInterval(getCurrentDate,1000)
    var currentDate=new Date();
    var dateTime = "Actualizat: " + currentDate.getDate()+ "/"
                    +(currentDate.getMonth()+1) + "/"
                    + currentDate.getFullYear() + "  "
                    + currentDate.getHours() + ":"
                    + currentDate.getMinutes() +":"
                    +currentDate.getSeconds();
    document.getElementById("currentdate").innerHTML=dateTime;
}
