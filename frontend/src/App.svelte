<script>
  import Router from "svelte-spa-router"
  import Home from "./routes/Home.svelte"
  import Detail from "./routes/Detail.svelte";

    const routes = {
        "/":Home,
        "/detail/:question_id" : Detail,
        // "/question-create":null,
        // "/question-modify/:question_id":null,
        // "/user-login":null,
        // "/user-create":null,
        // "/answer-modify/:answer_id":null,
    }
    
</script>

<Router {routes}/>