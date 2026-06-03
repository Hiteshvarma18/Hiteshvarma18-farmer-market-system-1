const API = "http://127.0.0.1:8000/api/auth";

function validPhone(phone){
    return /^\d{10}$/.test(phone);
}

function strongPassword(password){
    return /^(?=.*[A-Za-z])(?=.*\d).{6,}$/.test(password);
}

function togglePassword(id){

    const field = document.getElementById(id);

    if(field.type === "password"){
        field.type = "text";
    }else{
        field.type = "password";
    }
}