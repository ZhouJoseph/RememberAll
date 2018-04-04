$(document).ready(function() {
    var oriText = "";
    var keys = 0;
    var $MyList = $("#MyList");
    

    function createNode(id, data){
      var li = $("<li id='" + id + "'>" + data + "</li>");
      var crossline = $("<span class='crossoff'>&#10003;</span>");
      var span = $("<span class='close'>&#215;</span>");
      li.append(crossline);
      li.append(span);
      $MyList.append(li);
    }

    function deleteTextbox() {
      var task = oriText;
      var idKey = $(this).parent().attr('id');

      var url = "/todo/delete";
      var settings = {
        type: "DELETE",
        // data : {data : task[0].innerHTML, key:task[1].innerHTML,},
        data: { data: task, key: idKey, },
        success: function (response) {
          oriText = "";
          console.log(response.success);
        },
        error: function (error) {
          console.log(error);
        }
      };
      $.ajax(url, settings);
      $(this).parent().remove();
    }


    $("#MyList").on('click', 'span>li', function (){
      $(this).prev().toggleClass('crossline');
      $(this).parent().toggleClass('crossline');
    });



    $("#form4").on("submit", function(event) {
        $.ajax({
            data: {
                InputData: $("#myInput").val(),
            },
            type: "POST",
            url: "/todo/create"
        })
        .done(function(data) {
            if (data.error) {
                alert("You must write something");
            } else {
                console.log(data.success);
                createNode(data.key,data.success);
                $("#myInput").val("");
            }
        });
        event.preventDefault();
    });



    $.ajax({
        type: "GET",
        url: "/todo/read"
    })
    .done(function(todo) {
        $.each(todo, function(index, item) { 
                createNode(item[0],item[1]);
        });
    });



    $("#MyList").on('click', '.close', function () {
      var task = $(this).parent().text().slice(0,-2);
      var idKey = $(this).parent().attr('id');

      var url = "/todo/delete";
      var settings = {type : "DELETE",
                      // data : {data : task[0].innerHTML, key:task[1].innerHTML,},
                      data : {data : task, key:idKey,},
                      success : function(response) {
                        oriText = "";
                        console.log(response.success);
                      },
                      error : function(error) {
                        console.log(error);
                      }};
      $.ajax(url, settings);
      $(this).parent().remove();
    });

    $("#MyList").on('click', 'li' , function() {
      if (oriText == "") {
        oriText = $(this).text().slice(0,-2);
        keys = $(this).attr('id');
        $(this).text("");
        $("<input id='newContent'type='text' style='width:80%;background:transparent;color:white;border:none;outline: none;'><span class='close '>&#215;</span>").appendTo(this).focus().val(oriText);
      }
    });
    $("#MyList").on('keypress', 'input', function (e) {
      if (e.keyCode == 13) {
        if ($("#newContent").val() == "") {
          $(this).parent().html(oriText + "<span class='crossoff'>&#10003;</span><span class='close'>&#215;</span>");
        } else {
          var task = $("#newContent").val()
          $(this).parent().html(task + "<span class='crossoff'>&#10003;</span><span class='close'>&#215;</span>");
          var url = "/todo/update";
          var settings = {type : "PUT",
                          data : {item : task, old : oriText, key : keys},
                          success : function(response) {
                            console.log(response.success);
                          },
                          error : function(error) {
                            console.log(error);
                          }};
          $.ajax(url, settings);
        }
        oriText = "";
      }
    });
    $("#MyList").on('focusout', 'li > input', function() {
        $(this).parent().html(oriText + "<span class='crossoff'>&#10003;</span><span class='close'>&#215;</span>");
        oriText = "";
  });
});