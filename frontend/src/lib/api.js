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

  if (method !== "get") {
    options["body"] = body;
  }

  fetch(_url, options).then((response) => {
    response
      .json()
      .then((json) => {
        if (response.status >= 200 && response.status < 300) {
          //성공
          if (success_callback) {
            success_callback(json);
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
