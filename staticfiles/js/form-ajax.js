$(document).on('submit', '#user-post-profile', function(e){
    e.preventDefault();
    $.ajax({
        type: 'POST',
        url: '/profile/likepost',
        data: {
            post_id: $("#post_id").val(),
            path: $("#path").val(),
            csrfmiddlewaretoken: $('input[csrfmiddlewaretoken]').val()
        },
        success: function(){
            alart('Form sent!');
        }
    });

});
