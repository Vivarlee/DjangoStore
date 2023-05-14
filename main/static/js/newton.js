async function submit(ev)
{
    let expr = document.getElementById('expression-input')
    let x0 = document.getElementById('x0')
    let eps = document.getElementById('epsilon')
    let response=await fetch('/calc/newton?'+new URLSearchParams([
        ['expression', expr.value], ['x0', x0.value], ['atol', eps.value]
    ]),{
        method:'get',
        headers:{}
    })
    let data= await response.json()
    document.getElementById('answer').innerText=data.result
}