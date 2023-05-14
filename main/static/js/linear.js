// get url from external var calc_url

var currDim=1
var rows = 0  // It's 0 at the start because we use addRow() in the code later to make an initial matrix
var columns = 3

function addRow()
{
    let matrix = document.getElementById('matrix')
    let row = document.createElement('div')
    row.className = 'row'
    for (let i = 0; i < columns; i++) {
        let column=document.createElement('input')
        column.type = 'number'
        column.value = '0'
        row.appendChild(column)
    }
    let b = document.createElement('input')
    b.type = 'number'
    b.value = '0'
    b.className = 'b'
    row.appendChild(b)
    matrix.appendChild(row)
    rows += 1
}

function removeRow()
{
    if (rows == 1) {
        return
    }
    let matrix = document.getElementById('matrix')
    matrix.children[matrix.children.length - 1].remove()
    rows -= 1
}

function addColumn()
{
    let matrix = document.getElementById('matrix')
    for (const element of matrix.children) {
        if (element.classList.contains('row')) {
            let column=document.createElement('input')
            column.type='number'
            column.value='0'
            element.children[element.children.length - 1].before(column)
        }
    }
    columns += 1
}

function removeColumn()
{
    if (columns == 1) {
        return
    }
    let matrix = document.getElementById('matrix')
    for (const element of matrix.children) {
        if (element.classList.contains('row')) {
            element.children[element.children.length - 2].remove()
        }
    }
    columns -= 1
}

async function submit(ev)
{
    let arr=[['dim',[rows, columns]],['values',[]], ['b', []]]
    let matrix = document.getElementById('matrix')
    for (const row of matrix.children) {
        for (let i = 0; i < row.children.length - 1; i++) {
            arr[1][1].push(row.children[i].value)
        }
        arr[2][1].push(row.children[row.children.length - 1].value)
    }
    let response=await fetch(calc_url + '?'+new URLSearchParams(arr),{
        method:'get',
        headers:{}
    })
    let data= await response.json()
    let error = document.getElementById('error-message')
    if (data.error != null && data.error != '') {
        error.hidden = false
        error.innerHTML = data.error
    } else {
        error.hidden = true
    }
    document.getElementById('answer').innerText=data.result
}

window.onload=function ()
{
    let button=document.getElementById('bub')
    button.addEventListener('click',submit)

    for (let i = 0; i < 3; i++) {
        addRow()
    }
}