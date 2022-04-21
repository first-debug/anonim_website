function update_chat() {
    $('#chat_box').empty();
    $.getJSON( "/api/messages/" + chat_id, function( data ) {
         data.messages.forEach((element) => {
            var h4;
            if (element.type == 'msg') {
                h4 = jQuery('<h4>', {
                    class: 'message rounded bg-info w-25 container',
                    text: element.message,
                }).appendTo('#chat_box');
            }
            else {
                h4 = jQuery('<h4>');
                jQuery('<img>', {
                    class: 'message rounded w-25 container bg-opacity-10',
                    src: element.message,
                    alt: ''
                }).appendTo(h4);
                h4.appendTo('#chat_box');
            }
            h4.append(`<button class="btn-remove" data-id=${element.id}></button>`);
        });
        $('button.btn-remove').click(function () {
            event.preventDefault();
            var id = $(this).attr('data-id');
            $.ajax({
                url: '/api/message/' + id,
                type: 'DELETE'
            });
        })
    });
}
setInterval(update_chat, 1000);