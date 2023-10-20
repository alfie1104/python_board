<script>
  import fastapi from "../lib/api";

    //Detail 컴포넌트 호출 시 전달한 파라미터값을 읽기위해 params변수 선언
    export let params = {}
    let question_id = params.question_id
    
    let question = {}

    function get_question(){
        fastapi("get","/api/question/detail/" + question_id, {}, (json) =>{
            question = json
        })
    }

    get_question()
</script>

<h1>{question.subject}</h1>
<div>
    {question.content}
</div>