function json_to_html(json) {
    if (json === "")
        return "";

    var data_dict = JSON.parse(json);
    // if we have a dictionary we convert it to an array of length one
    if (!Array.isArray(data_dict)){
        data_dict = [data_dict]
    }

    var tableStructure = "<table class='table table-hover' style='display: inline'><thead><tr>{{head}}</tr></thead><tbody>{{body}}</tbody></table>";
    var body = "";

    for (var i in data_dict) {

        if (data_dict.hasOwnProperty(i))
        {
            var row_data = data_dict[i];

            if (row_data){
                var rowHtml = "";

                var values = Object.values(row_data);

                for (var j in values) {
                    rowHtml += "<td>" + values[j] + "</td>";
                }

                body += "<tr>" + rowHtml + "</tr>";
            }
        }
    }

    var head = "";

    var keys = Object.keys(data_dict[0]);

    for (var i in keys){
        head += "<td style='font-weight: bold'>" + keys[i] + "</td>"
    }

    return tableStructure.replace("{{head}}", head).replace("{{body}}", body);
}

(function ($) {
    $(document).ready(function () {
        var tf_fields = $('.ap-table-field');
        for (var i = 0; i < tf_fields.length; ++i){
            var tf_selector = $(tf_fields[i]);

            var json_data = tf_selector.attr('data-table-content');
            json_data = json_data.replace(new RegExp('\'', 'g'), '"');
            tf_selector.html(json_to_html(json_data));
        }
    });
})(django.jQuery);