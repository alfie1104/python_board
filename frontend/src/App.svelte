<script>
    import Router from "svelte-spa-router"
    import Home from "./routes/Home.svelte"

    const routes = {
        "/":Home,
        "/detail/:question_id" : None ,
        "/question-create":None,
        "/question-modify/:question_id":None,
        "/user-login":None,
        "/user-create":None,
        "/answer-modify/:answer_id":None,
    }
    
</script>

<Router {routes}/>