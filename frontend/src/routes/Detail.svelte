<script>
  import fastapi from "../lib/api";
  import Error from "../components/Error.svelte"

    //Detail 컴포넌트 호출 시 전달한 파라미터값을 읽기위해 params변수 선언
    export let params = {}
    let question_id = params.question_id
    let question = {answers:[]}
    let content = ""
    let error = {detail:[]}

    function get_question(){
        fastapi("get","/api/question/detail/" + question_id, {}, (json) =>{
            question = json
        })
    }

    function post_answer(event){
        event.preventDefault();
        let url = "/api/answer/create/" + question_id;
        let params = {
            content : content
        }
        fastapi("post",url,params,(json) => {
            content = ''
            error = {detail:[]}
            get_question()
        },(err_json) => {
            error = err_json
        })
    }

    get_question()
</script>

<h1>{question.subject}</h1>
<div>
    {question.content}
</div>
<ul>
    {#each question.answers as answer}
    <li>
        {answer.content}
    </li>
    {/each}
</ul>
<Error error={error}/>
<form method="post">
    <textarea rows="15" bind:value={content}></textarea>
    <input type="submit" value="답변등록" on:click="{post_answer}">
</form>