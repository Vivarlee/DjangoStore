window.onload = function() {
    var form = document.getElementById("username")
    form.onchange = function() {
        fetch("/checkusername", {
            method: "POST",
            headers: {"X-CSRFtoken": csrf_token},
            body: JSON.stringify({username: form.value})
        })
        .then(response => response.json())
        .then(data => {
            var text = document.getElementById("userexists")
            var button = document.getElementById("registerbutton")
            text.hidden = false
            console.log(data)
            if (data.exists) {
                text.innerHTML = "This username exists"
                text.style = "color: rgb(200, 100, 50)"
                button.disabled=true
            }
            else {
                text.innerHTML = "This username doesn't exist"
                text.style = "color: rgb(100, 200, 50)"
                button.disabled=false
            }
        })
    }
}