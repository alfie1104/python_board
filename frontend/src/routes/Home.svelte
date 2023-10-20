<script>
  import fastapi from "../lib/api";
  import {link} from "svelte-spa-router"

    let question_list = []

    function get_question_list() {
        fastapi('get','/api/question/list',{},(json) => {
            question_list = json
        })
    }

    get_question_list()
    
</script>

<!--use:link를 사용하면 href경로 앞에 #이 붙게 됨. 따라서 브라우저는 이 경로를 하나의 페이지로 인식함 (해시 기반 라우팅)-->

<ul>
    {#each question_list as question}
    <li><a use:link href="/detail/{question.id}">{question.subject}</a></li>
    {/each}
</ul>