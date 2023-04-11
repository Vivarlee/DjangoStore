var currDim=1
var form

function addRow()
{
    let y1=document.createElement('input')
    y1.type='number'
    y1.value='0'
    form.appendChild(y1)
    let y2=document.createElement('input')
    y2.type='number'
    y2.value='0'
    form.appendChild(y2)
    let y3=document.createElement('input')
    y3.type='number'
    y3.value='0'
    form.appendChild(y3)
    form.appendChild(document.createElement('br'))
}

function onDimChange(ev)
{
    let dim = ev.target
    if (dim.value > currDim)
        for (let i =0;i<dim.value-currDim;i++) addRow()

    else if (dim.value < currDim)
    {
        for (let i =0;i<(currDim-dim.value)*4;i++)
        {
            form.removeChild(form.children[form.children.length-1])
        }
    }
    currDim=dim.value
}

async function submit(ev)
{
    let arr=[['dim',currDim],['values',[]]]
    let button=ev.target
    for(let i =[...form.children].indexOf(button)+1;i<form.children.length;i++)
    {
        if (form.children[i].tagName==='INPUT')
        {
            //arr.push(['a'+i,form.children[i].value])
            arr[1][1].push(form.children[i].value)
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
    form=document.getElementById('gauss')
    addRow()
    var dim=document.getElementById('dim')
    dim.addEventListener("change",onDimChange)
}