<script>
  import fastapi from "../lib/api";
  import {link} from "svelte-spa-router"
  import {page, is_login} from "../lib/store"
  import moment from "moment/min/moment-with-locales"
  moment.locale('ko')

    let question_list = []
    let size = 10
    let total = 0
    $: total_page = Math.ceil(total/size) //svelte에서 변수앞에 $: 기호를 붙이면 해당 변수는 반응형변수가 됨. total의 값이 바뀌면 total_page의 값도 실시간으로 재계산됨

    function get_question_list(_page) {
        let params = {
            page : _page,
            size : size
        }

        fastapi('get','/api/question/list',params,(json) => {
            question_list = json.question_list
            $page = _page
            total = json.total
        })
    }

    $: get_question_list($page)
    
</script>

<!--use:link를 사용하면 href경로 앞에 #이 붙게 됨. 따라서 브라우저는 이 경로를 하나의 페이지로 인식함 (해시 기반 라우팅)-->

<div class="container my-3">
    <table class="table">
        <thead>
            <tr class="text-center table-dark">
                <th>번호</th>
                <th style="width:50%">제목</th>
                <th>글쓴이</th>
                <th>작성일시</th>
            </tr>
        </thead>
        <tbody>            
            {#each question_list as question,i}
            <tr class="text-center">
                <td>{total - ($page*size)-i}</td>
                <td class="text-start">
                    <a use:link href="/detail/{question.id}">{question.subject}</a>
                    {#if question.answers.length > 0}
                    <span class="text-danger small mx-2">{question.answers.length}</span>
                    {/if}
                </td>
                <td>{question.user ? question.user.username : ""}</td>
                <td>{moment(question.create_date).format("YYYY년 MM월 MM일 hh:mm a")}</td>
            </tr>
            {/each}
        </tbody>
    </table>

    <!-- 페이징처리 시작-->
    <ul class="pagination justify-content-center">
        <!--이전 페이지-->
        <li class="page-item {$page <= 0 && 'disabled'}">
            <button class="page-link" on:click="{() => get_question_list($page-1)}">이전</button>
        </li>
        <!-- 페이지 번호-->
        {#each Array(total_page) as _, loop_page}
        {#if loop_page >= $page-5 && loop_page <= $page+5}
        <li class="page-item {loop_page === $page && 'active'}">
            <button on:click="{()=>get_question_list(loop_page)}" class="page-link">{loop_page + 1}</button>
        </li>
        {/if}
        {/each}
        <!-- 다음 페이지-->
        <li class="page-item {$page >= total_page -1 && 'disabled'}">
            <button class="page-link" on:click="{() => get_question_list($page+1)}">다음</button>
        </li>
    </ul>
    <!-- 페이징 처리 끝-->

    <a use:link href="/question-create" class="btn btn-primary {$is_login ? "" : "disabled"}">질문 등록하기</a>
</div>