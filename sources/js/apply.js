function isEmail(email) {
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
}

$("#submit_button").on('click', function(){
    var grade = $("#grade").val(), classroom=$("#class").val(), number = $("#number").val();
    if(! number) {
        alert("학번을 확인해주세요.");
        return null;
    }

    var name = $("#name").val();
    if(! name) {
        alert("성명을 확인해주세요.");
        return null;
    }

    var phone = $("#phone").val();
    if(! phone || phone.length !== 13) {
        alert("전화번호를 확인해주세요.");
        return null;
    }

    var email = $("#email").val();
    if(! email || !isEmail(email)) {
        alert("이메일을 확인해주세요.");
        return null;
    }

    try {
        $.post("./submit", {"name": name, "grade": grade, "classroom": classroom, "number": number, "phone": phone, "email": email}, function(resp){
            var data = JSON.parse(resp);

            if(data.err) {
                alert(data.message);
            } else {
                alert(data.message);
                location.href = data.goto;
            }
        });
    }
    catch(ex) {
        alert("서버에 오류가 발생하였습니다.");
    }

});