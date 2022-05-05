function update_chat() {
    $.getJSON( "/api/messages/" + chat_id, function( data ) {
         var container = jQuery('<div>');
         data.messages.forEach((element) => {
            var h4;
            if (element.type == 'msg') {
                h4 = jQuery('<h4>', {
                    class: 'message rounded button_color w-25 container',
                    text: element.message,
                }).appendTo(container);
            }
            else {
                h4 = jQuery('<h4>');
                jQuery('<img>', {
                    class: 'button_color rounded w-25 container bg-opacity-10',
                    src: element.message,
                    alt: ''
                }).appendTo(h4);
                h4.appendTo(container);
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
        $('#chat_box').empty();
        container.appendTo('#chat_box');
    });
}
setInterval(update_chat, 1000);