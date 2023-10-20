<script>
    import Router from "svelte-spa-router"
    import Home from "./routes/Home.svelte"

    const routes = {
        "/":Home,
        // "/detail/:question_id" : null ,
        // "/question-create":null,
        // "/question-modify/:question_id":null,
        // "/user-login":null,
        // "/user-create":null,
        // "/answer-modify/:answer_id":null,
    }
    
</script>

<Router {routes}/>