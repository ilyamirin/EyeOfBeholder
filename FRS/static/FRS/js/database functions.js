function qty() {
    var i = document.getElementById('srch').value;
    return i
}


function nm() {
    var n = document.getElementById('nm').value;
    return n
}

function savemany() {

    var ticks = document.getElementsByTagName("table")[0].getElementsByClassName("checked");

    for (var i = 0; i < ticks.length; i++) {
        var a = ticks[i].getAttribute("id");
        saveQuestionAnswer(a)
    }
    alert("Измененные элементы сохранены");
    location.reload();
}

function deletemany() {

    var ticks = document.getElementsByTagName("table")[0].getElementsByClassName("deleted");
    for (var i = 0; i < ticks.length; i++) {
        var a = ticks[i].getAttribute("id");
        deleteRow(a);
    }
    alert("Выбранные элементы удалены.");
    location.reload();
}

function chekchek(name, id) {
    if (name !== $('td[data-id="uid-' + id + '"]').text()) {
        document.querySelector("input#" + id).setAttribute("class", "checked");
        document.querySelector("input#" + id).setAttribute("checked", "checked");
        document.querySelector("input#" + id).checked = true;
    }
}

function chekchek2(checkbox, name, id) {
    if (checkbox.checked) {
        document.querySelector("input#" + id).setAttribute("class", "deleted");
        document.querySelector("input#" + id).setAttribute("checked", "checked");
        document.querySelector("input#" + id).checked = true;
    } else {
        document.querySelector("input#" + id).classList.remove("deleted");
        document.querySelector("input#" + id).removeAttribute("checked");
        document.querySelector("input#" + id).checked = false;
    }
}

function deleteRow(id) {

    editableQuestion = $('td[data-id="uid-' + id + '"]'); //this will get data-id=question-1 where 1 is the question ID
    // no change change made then return false
    if ($(editableQuestion).attr('data-old_value') === editableQuestion.innerHTML)
        return false;

    // send ajax to update value
    $.ajax({
        url: "delete_name/",
        type: "GET",
        dataType: "json",
        data: {
            "name": editableQuestion.text(),
            "uid": editableQuestion.attr('data-id')
        },
        error: function () {
            console.log("ошибка");
            alert("An error occurred")
        }
    });
}

function saveQuestionAnswer(id) {
    editableQuestion = $('td[data-id="uid-' + id + '"]'); //this will get data-id=question-1 where 1 is the question ID

    // no change change made then return false
    if ($(editableQuestion).attr('data-old_value') === editableQuestion.innerHTML)
        return false;

    // send ajax to update value
    $.ajax({
        url: "save_name/",
        type: "GET",
        dataType: "json",
        data: {
            "name": editableQuestion.text(),
            "uid": editableQuestion.attr('data-id')
        },
        error: function () {
            console.log("ошибка");
            alert("An error occurred")
        }
    });
}

function checkAll(checkbox) {
    let checkList = $("input[type='checkbox']");
    if (checkbox.checked) {
        for (let i = 1; i < checkList.length; ++i) {
            checkList[i].setAttribute("class", "deleted");
            checkList[i].setAttribute("checked", "checked");
            checkList[i].checked = true;
        }
    } else
        for (let i = 1; i < checkList.length; ++i) {
            checkList[i].checked = false;
            checkList[i].classList.remove("deleted");
            checkList[i].removeAttribute("checked");
        }
}