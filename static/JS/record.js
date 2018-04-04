

$(document).ready(function(){
    var time = new Date();
    ayear = time.getFullYear();
    amonth = time.getMonth() + 1;
    adate = time.getDate();

    function createHandler(id){
        $(id).on("submit", function (event) {
            $.ajax({
                data:{
                    year: ayear,
                    month: amonth,
                    date: adate,
                    thing1: $("#thing" + id.slice(5)).val(),
                },
                type: "POST",
                url: "/index/record"
            })
            .done(function (data) {
                console.log(data.well);
                $("#thing" + id.slice(5)).parent().html("<span style='font-size:35px;'>" + data.well + "  " + "</span>" + "<span class='thing" + id.slice(5) + "' id='delete'>&nbsp;&#215;</span>");
            });
            event.preventDefault();
        });
    }



    createHandler('#form1');
    createHandler('#form2');
    createHandler('#form3');

    $("#greetwords").on('click','#delete',function(){
        $.ajax({
            data: {
                year: ayear,
                month: amonth,
                date: adate,
                thing: $(this).parent().text().slice(0,-4),
            },
            type: "DELETE",
            url: "/index/delete"
        })
        .done(function(data){
            console.log("success");
            console.log(data.well);
        });
        var idKey = $(this).attr('class');
        $(this).parent().html("<input class='text-line' id='" + idKey + "' type='text' placeholder='" + ayear + "/" + amonth + "/" + adate + "/' autocomplete='off'>");
    });


    $.ajax({
        data: {
            year: ayear,
            month: amonth,
            date: adate,
        },
        type: "POST",
        url: "/index/read"
    })
    .done(function (records) {
        var counter = 1;
        $.each(records, function (index, item) {
            $('#thing'+counter).parent().html("<span style='font-size:35px;'>" + item[5] + "  " + "</span>" + "<span class='thing"+counter+"' id='delete'>&nbsp;&#215;</span>");
            counter +=1;
        });
    });



});