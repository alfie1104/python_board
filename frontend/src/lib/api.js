import qs from "qs";
import { access_token, username, is_login } from "./store";
import { get } from "svelte/store";
import { push } from "svelte-spa-router";

/***
 * @name fastapi
 * @param operation 데이터 처리 방법 (예 : get, post, put, delete)
 * @param url 요청 URL, 백엔드 서버의 호스트명 이후 URL만 전달 (예 : /api/question/list)
 * @param params 요청 데이터 (예 : {page:1, keyword:"마크다운"})
 * @param success_callback API 호출 성공시 수행할 함수
 * @param failure_callback API 호출 실패시 수행할 함수
 */
const fastapi = (
  operation,
  url,
  params,
  success_callback,
  failure_callback
) => {
  let method = operation;
  let content_type = "application/json";
  let body = JSON.stringify(params); //object형태의 param을 문자열로 변경

  if (operation === "login") {
    method = "post";
    content_type = "application/x-www-form-urlencoded";
    body = qs.stringify(params);
  }

  let _url = import.meta.env.VITE_SERVER_URL + url;
  if (method === "get") {
    _url += "?" + new URLSearchParams(params);
  }

  let options = {
    method: method,
    headers: {
      "Content-Type": content_type,
    },
  };

  const _access_token = get(access_token); //fastapi 함수는 svelte 컴포넌트가 아니므로 $기호로 참조할 수 없고 get함수를 이용하여 값을 읽어와야함. 마찬가지로 값을 저장할때는 access_token.set 처럼 set함수를 활용해야함
  if (_access_token) {
    options.headers["Authorization"] = "Bearer " + _access_token;
  }

  if (method !== "get") {
    options["body"] = body;
  }

  fetch(_url, options).then((response) => {
    if (response.status === 204) {
      //성공했으나 content가 없는 경우
      if (success_callback) {
        success_callback();
      }
      return;
    }

    response
      .json()
      .then((json) => {
        if (response.status >= 200 && response.status < 300) {
          //성공
          if (success_callback) {
            success_callback(json);
          } else if (operation !== "login" && response.status === 401) {
            //token time out
            //operation이 login인 경우에는 아이디 또는 비밀번호를 틀리게 입력했을 때 401 오류가 발생하므로 제외했음
            access_token.set("");
            username.set("");
            is_login.set(false);
            alert("로그인이 필요합니다.");
            push("/user-login");
          }
        } else {
          //실패
          if (failure_callback) {
            failure_callback(json);
          } else {
            alert(JSON.stringify(json));
          }
        }
      })
      .catch((error) => {
        alert(JSON.stringify(error));
      });
  });
};

export default fastapi;
