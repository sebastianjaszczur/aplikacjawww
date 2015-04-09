
function saveForm(form_id)
{
    sessionStorage.setItem("formdata"+form_id,formToString(jQuery("#"+form_id)));
}

function restoreForm(form_id)
{
    var storedform = sessionStorage.getItem("formdata"+form_id);
    stringToForm(storedform, jQuery("#"+form_id));
}

function formToString(stringForm)
{
    formObject = new Object
    stringForm.find("input, select, textarea").each(function(){
        if (this.id)
        {
            if ($(this).attr("type") == 'checkbox' || $(this).attr("type") == 'radio')
            {
                formObject[this.id] = $(this).attr("checked");
            }
            else
            {
                formObject[this.id] = $(this).val();
            }
        }
    })  
    return JSON.stringify(formObject);
}
function stringToForm(formString, stringForm)
{
    formObject = JSON.parse(formString)
    stringForm.find("input, select, textarea").each(function(){
        if (this.id)
        {
            id = this.id;
            input = stringForm.find("[id=" + id +"]")   
            if (input.attr("type")=="checkbox" || input.attr("type")=="radio" )
            {
                input.attr("checked", formObject[id])
            }
            else
            {
                input.val(formObject[id])
            }

        }
    })
}