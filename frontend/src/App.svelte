<script>
  import Router from "svelte-spa-router"
  import Home from "./routes/Home.svelte"
  import Detail from "./routes/Detail.svelte";
  import QuestionCreate from "./routes/QuestionCreate.svelte";
  import Navigation from "./components/Navigation.svelte";
  import UserCreate from "./routes/UserCreate.svelte";

    const routes = {
        "/":Home,
        "/detail/:question_id" : Detail,
        "/question-create":QuestionCreate,
        // "/question-modify/:question_id":null,
        // "/user-login":null,
         "/user-create":UserCreate,
        // "/answer-modify/:answer_id":null,
    }
    
</script>

<Navigation/>
<Router {routes}/>