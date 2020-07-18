$(document).ready(function() {
    $("#list-items").sortable({
        update: function(event, ui) {
            const list_id = $("#list-items").attr("data-list-id");
            let elements = [];
            $("#list-items").children("li").each(function() {
                elements.push($(this).attr('data-item-id'));
            })
            let list_data = {
                'elements': elements.join("|"),
            }
            const url = `/list/${list_id}/reorder`;
            $.ajax(url, {
                method: 'PATCH',
                data: list_data,
            })

            // TODO: AJAX call to change order
        }
    });
    $("#list-items").disableSelection();
});
