
var clock = document.getElementById('clock');
var hexColor = document.getElementById('hex-color');
var block = document.getElementById('timing');
var daytime = document.getElementById('daytime');
var thing1 = document.getElementById('thing1');
var thing2 = document.getElementById('thing2');
var thing3 = document.getElementById('thing3');


function hexClock() {
    var time = new Date();
    var hours = time.getHours().toString();
    var minutes = time.getMinutes().toString();
    var seconds = time.getSeconds().toString();
    var year = time.getFullYear().toString();
    var month = (time.getMonth()+1).toString();
    var date = time.getDate().toString();
    
    if (hours.length < 2) {
        hours = '0' + hours;
    }

    if (minutes.length < 2) {
        minutes = '0' + minutes;
    }

    if (seconds.length < 2) {
        seconds = '0' + seconds;
    }
    if (month.length < 2){
        month = '0' + month;
    }
    if(date.length < 2) {
        date = '0' + date;
    }

    var clockStr = hours + ' : ' + minutes;
    var hexColorStr = '#' + hours + minutes + seconds;

    clock.textContent = clockStr;
    hexColor.textContent = hexColorStr;
    block.style.backgroundColor = hexColorStr;
    thing1.placeholder = year + '/' + month + '/' + date;
    thing2.placeholder = year + '/' + month + '/' + date;
    thing3.placeholder = year + '/' + month + '/' + date;


    if (parseInt(hours) >= 5 && parseInt(hours) < 12){
        daytime.textContent = " morning,";
    }
    if (parseInt(hours) >= 12 && parseInt(hours) < 18){
        daytime.textContent = " afternoon,";
    }
    if (parseInt(hours) >= 18 || parseInt(hours) < 5) {
        daytime.textContent = " evening,";
    }

}

hexClock();
setInterval(hexClock, 1000);