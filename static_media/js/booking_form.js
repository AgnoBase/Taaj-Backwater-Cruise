function validation(){
    var phone= document.forms['form-booking']['cnum']
    var adults = document.forms['form-booking']['adults']
    var child = document.forms['form-booking']['child']
    var get_num = String(phone.value).charAt(0);
    if(isNaN(phone.value) || phone.value.length!=10)
    {
        alert('invalid contact number')
        return false
    }
    return true
}

function v(){
    alert('bhai email check kar')
}