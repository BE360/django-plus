/**
 * Created by reza on 5/31/18.
 */

export function json_to_html(json) {
    if (json === "")
        return "";

    let data_dict = JSON.parse(json);
    // if we have a dictionary we convert it to an array of length one
    if (!Array.isArray(data_dict)){
        data_dict = [data_dict]
    }

    let tableStructure = "<table class='table table-hover' style='display: inline'><thead><tr>{{head}}</tr></thead><tbody>{{body}}</tbody></table>";
    let body = "";

    for (let i in data_dict) {

        if (data_dict.hasOwnProperty(i))
        {
            let row_data = data_dict[i];

            if (row_data){
                let rowHtml = "";

                for (let tr in Object.values(row_data)) {
                    rowHtml += "<td>" + tr + "</td>";
                }

                body += "<tr>" + rowHtml + "</tr>";
            }
        }
    }

    let head = "";

    for (let th in Object.keys(data_dict[0])){
        head += "<td style='font-weight: bold'>" + th + "</td>"
    }

    return tableStructure.replace("{{head}}", head).replace("{{body}}", body);
}
