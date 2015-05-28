$(document).ready(function(){
    
    /* Submit task modal form to the server */
    $("#submitTaskButton").click(function(){
        datas = $("#submitTaskForm").serialize();
        console.log(datas);
        /* Send with post to localhost/task */
        $.post("http://localhost:8080/task/create", datas, function(data, status) {
            console.log(status);
            console.log(data);
            /* Check if the task succeed to record */
            if (status == "success" && data.status == 1) {
                $('#addTask').modal('hide');
                location.reload();
            }
        });
    });
    
    
    /* Delete a task */
    $(".delete").click(function(){
        var task = $(this).parent().parent();
        var task_id = task.attr('data-id');
        console.log(task_id);
        $.post("http://localhost:8080/task/delete", {"id":task_id}, function(data, status) {
            console.log(status);
            console.log(data);
            task.hide('slide');    
        });
    });
});
