var count = 0;
function qty() {
    var i = document.getElementById('srch').value;
    return i
}


function nm() {
    var n = document.getElementById('nm').value;
    return n
}

function savemany() {

    var ticks = document.getElementsByTagName("table")[0].getElementsByClassName("deleted");

    for (var i = 0; i < ticks.length; i++) {
        var a = ticks[i].getAttribute("id");
        saveQuestionAnswer(a)
    }
    alert("Измененные элементы сохранены");
    location.reload();
}
function merge(){
    var ticks = document.getElementsByTagName("table")[0].getElementsByClassName("deleted");
    function comp(a, b) {
        if (a.attributes['is-count'].value > b.attributes['is-count'].value) return 1;
        else if (a.attributes['is-count'].value < b.attributes['is-count'].value) return -1;
        else return 0;
    }
    ticks = [...ticks].sort(comp)
    for(var i = 1; i < ticks.length; i++){
        var merged = ticks[i].getAttribute("id")
        merging(ticks[0].getAttribute("id"), merged)
    }
    console.log([...ticks].sort(comp));
    alert('Пользователи успешно объединены')
    location.reload()
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

function getid(elem) {
    var x = parseInt(elem.parentNode.parentNode.rowIndex);
    var val = $(".somId")[x-1].innerText;
    return val
}

function chekchek(name, id) {
    if (name !== $('td[data-id="uid-' + id + '"]').text()) {
            document.querySelector("input#" + id).setAttribute("class", "deleted");
            document.querySelector("input#" + id).setAttribute("checked", "checked");
            document.querySelector("input#" + id).checked = true;
    }
}

function chekchek2(checkbox, name, id) {
    if (checkbox.checked) {
        document.querySelector("input#" + id).setAttribute("class", "deleted");
        document.querySelector("input#" + id).setAttribute("checked", "checked");
        document.querySelector("input#" + id).setAttribute("is-count", count);
        document.querySelector("input#" + id).checked = true;
        count++;
    }
    else {
        document.querySelector("input#" + id).classList.remove("deleted");
        document.querySelector("input#" + id).removeAttribute("checked");
        document.querySelector("input#" + id).removeAttribute("is-count");
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

function merging(base, id) {
    // editableQuestion = $('td[data-id="uid-' + id + '"]'); //this will get data-id=question-1 where 1 is the question ID
    //
    // // no change change made then return false
    // if ($(editableQuestion).attr('data-old_value') === editableQuestion.innerHTML)
    //     return false;

    // send ajax to update value
    $.ajax({
        url: "merge_names/",
        type: "GET",
        dataType: "json",
        data: {
            "base": base,
            "merged": id
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
            checkList[i].setAttribute("is-count", count);
            checkList[i].checked = true;
            count++;
        }
    } else
        for (let i = 1; i < checkList.length; ++i) {
            checkList[i].checked = false;
            checkList[i].classList.remove("deleted");
            checkList[i].removeAttribute("checked");
            checkList[i].removeAttribute("is-count");

        }
}