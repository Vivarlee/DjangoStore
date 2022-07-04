async function addToOrder(item_id) {
    await fetch("/addtocart", {
        method: "POST",
        headers: {"X-CSRFtoken": csrf_token, 'X-Requested-With': 'XMLHttpRequest'},
        body: JSON.stringify({item_id: item_id})
    })
    .then(response => {
        var items_counter = document.getElementById("items-in-cart")
        items_counter.innerText = String(parseInt(items_counter.innerText) + 1);
    })

}

