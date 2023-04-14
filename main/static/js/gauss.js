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
        column.type='number'
        column.value='0'
        row.appendChild(column)
    }
    matrix.appendChild(row)
    rows += 1
}

function removeRow()
{
    if (rows == 1) {
        return
    }
    let matrix = document.getElementById('matrix')
    matrix.removeChild(matrix.children[matrix.children.length - 1])
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
            element.appendChild(column)
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
            element.removeChild(element.children[element.children.length - 1])
        }
    }
    columns -= 1
}

async function submit(ev)
{
    let arr=[['dim',[rows, columns]],['values',[]]]
    let matrix = document.getElementById('matrix')
    for (const pot_row of matrix.children) {
        if (pot_row.classList.contains('row')) {
            for (const element of pot_row.children) {
                arr[1][1].push(element.value)
            }
        }
    }
    let response=await fetch('/calc/gauss?'+new URLSearchParams(arr),{
        method:'get',
        headers:{}
    })
    let data= await response.json()
    document.getElementById('answer').innerText=data.result
}

window.onload=function ()
{
    let button=document.getElementById('bub')
    button.addEventListener('click',submit)

    addRow()
}