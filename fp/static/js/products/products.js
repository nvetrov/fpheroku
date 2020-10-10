// Поиск в главной таблице

$(document).ready(function () {
    // get_product();

    $("#tableSearch").on("keyup", function () {
        // Filter table
        const value = $(this).val().toLowerCase();
        $("#myTable tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
    // YOURE CODE HERE
    console.log("Запуск приложения: Done");
})

//        function sendToServer(id,value,type){
//            console.log(id);
//            console.log(value);
//            console.log(type);
//            $.ajax({
//                url:"http://127.0.0.1:8000/savestudent",
//                type:"POST",
//                data:{id:id,type:type,value:value},
//            })
//            .done(function(response){
//                console.log(response);
//            })
//            .fail(function(){
//               console.log("Error Occured");
//            });
//
//        }


