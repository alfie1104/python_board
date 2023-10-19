<!-- <script>
    let message;

    fetch("http://localhost:8000/hello").then((response) => {
        response.json().then((json) => {
            message = json.message;
        })
    })
</script>

<h1>{message}</h1> -->

<script>
    async function hello(){
        const res = await fetch("http://localhost:8000/hello");
        const json = await res.json();

        if(res.ok){
            return json.message;
        }else{
            alert("error")
        }
    }

    let promise = hello();
</script>

{#await promise}
<p>...waiting</p>
{:then message}
<h1>{message}</h1>
{/await}