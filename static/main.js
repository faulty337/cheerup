function login() {
  let user_id = $("#header-idinput").val();
  let user_pw = $("#header-pwinput").val();
  if (user_id == "" || user_pw == "") {
    alert("입력되지 않은 칸이 존재합니다.");
    return;
  }
  $.ajax({
    type: "POST",
    url: "/login",
    data: { user_id: user_id, user_pw: user_pw },
    success: function (response) {
      if (response["result"] == "success") {
        // 이 토큰을 mytoken이라는 키 값으로 쿠키에 저장
        $.cookie("cutoken", response["token"]);

        alert("로그인 완료!");
        window.location.href = "/";
      } else {
        // 로그인이 안되면 에러메시지
        alert(response["message"]);
      }
    },
  });
}
function signup() {
  user_id = $("#signup_user_id").val();
  user_pw = $("#signup_user_pw").val();
  user_pw2 = $("#signup_user_pw2").val();
  user_name = $("#signup_user_name").val();
  if (user_id == "" || user_pw == "" || user_pw2 == "" || user_name == "") {
    alert("입력되지 않은 칸이 존재합니다.");
    return;
  }
  $.ajax({
    type: "POST",
    url: "/signup",
    data: {
      user_id: user_id,
      user_pw: user_pw,
      user_name: user_name,
      user_pw2: user_pw2,
    },
    success: function (response) {
      if (response["result"] == "success") {
        alert("회원가입 완료!");
        window.location.href = "/";
      } else {
        alert(response["message"]);
      }
    },
  });
}
function signupPopup() {
  let popup = document.querySelector(".signup");
  popup.style.display = "block";
}
function signupPopdown() {
  let popup = document.querySelector(".signup");
  popup.style.display = "none";
}
function postPopdown() {
  let popup = document.querySelector(".create-post");
  popup.style.display = "none";
}
function detailPopdown() {
  let popup = document.querySelector(".modal");
  popup.style.display = "none";
}
function logout() {
  $.removeCookie("cutoken");
  window.location.href = "/";
}

$(document).ready(function () {
  $("#myagony").hide();
  if ($.cookie("cutoken") == undefined) {
    // 내가 쓴 글 숨기기
  } else {
    user_listing(); //
  }
  listing();
});
function listing() {
  $.ajax({
    type: "GET",
    url: "/get_post",
    data: {},
    success: function (response) {
      let rows = response["post_list"].reverse();

      console.log(rows);
      for (let i = 0; i < rows.length; i++) {
        let post_num = rows[i]["post_num"];
        let create_date = rows[i]["create_date"];
        let title = rows[i]["title"];
        let user_name = rows[i]["user_name"];
        let content = rows[i]["content"];
        temp_html = `<div class="col cardform" onclick="detail(${post_num})">
      <div class="card h-100 border-info">
        <div class="card-body">
          <h3 class="card-title text-info text-truncate cardtitle">
            ${title}
          </h3>
          <div class="cardwriter">
            <h6 class="card-subtitle mb-2 text-muted">${user_name}</h6>
          </div>
          <div class="cardtime">
            <h6 class="card-subtitle mb-2 text-muted">${create_date}</h6>
          </div>
          <div class="card-custom-content">
            <p class="card-text text-dark">
              ${content}
            </p>
          </div>
        </div>
      </div>
    </div>`;
        $("#cards-box").append(temp_html);
      }
    },
  });
}
function user_listing() {
  $.ajax({
    type: "GET",
    url: "/user/get_post",
    data: {},
    success: function (response) {
      let rows = response["post_list"].reverse();
      if (rows != null) {
        for (let i = 0; i < rows.length; i++) {
          let post_num = rows[i]["post_num"];
          let create_date = rows[i]["create_date"];
          let title = rows[i]["title"];
          let user_name = rows[i]["user_name"];
          let content = rows[i]["content"];
          temp_html = `<div class="col cardform" onclick="detail(${post_num})">
                    <div class="card h-100 border-info">
                        <div class="card-body">
                        <h3 class="card-title text-info text-truncate cardtitle">
                            ${title}
                        </h3>
                        <div class="cardwriter">
                            <h6 class="card-subtitle mb-2 text-muted">${user_name}</h6>
                        </div>
                        <div class="cardtime">
                            <h6 class="card-subtitle mb-2 text-muted">${create_date}</h6>
                        </div>
                        <div class="card-custom-content">
                            <p class="card-text text-dark">
                            ${content}
                            </p>
                        </div>
                        </div>
                    </div>
                </div>`;
          $("#my-cards-box").append(temp_html);
          $("#myagony").show();
        }
      }
    },
  });
}
function save_post() {
  let title = $("#input-title").val();
  let content = $("#input-post-content").val();
  if (title == "" || content == "") {
    alert("입력하지 않은 칸이 존재합니다.");
    return;
  }
  $.ajax({
    type: "POST",
    url: "/set_post",
    data: { title: title, content: content },
    success: function (response) {
      if (response["result"] == "success") {
        window.location.reload();
      } else {
        alert(response["message"]);
        window.location.href = "/";
      }
    },
  });
}
function save_comment() {
  let content = $(".comment-write").val();
  let post_num = $(".post-number").attr("id");
  if (content == "") {
    alert("입력하지 않은 칸이 존재합니다.");
    return;
  }
  $.ajax({
    type: "POST",
    url: "/comment_write",
    data: { post_num: post_num, content: content },
    success: function (response) {
      console.log(response);
      if (response["result"] == "success") {
        window.location.reload();
      } else {
        alert(response["message"]);
        window.location.href = "/";
      }
    },
  });
}

function detail(post_num) {
  $.ajax({
    type: "GET",
    url: "/detail",
    data: { post_num: post_num },
    success: function (response) {
      console.log(response);
      let post = response[0]["post_detail"][0];
      let post_num = post["post_num"];
      let title = post["title"];
      let user_name = post["user_name"];
      let content = post["content"];
      let date = post["create_date"];

      $(".post-number").attr("id", post_num);
      $("#post-title").text(title);
      $("#post-username").text(user_name);
      $("#post-content").text(content);
      $("#post-date").text(date);

      let rows = response[1]["comment_list"];

      $("#comment_list").empty();
      for (let i = 0; i < rows.length; i++) {
        let name = rows[i]["user_name"];
        let content = rows[i]["content"];
        let temp_html = `<div class="comment-box-custom">
            <div class="write-style-custom">${name} :</div>
            <div class="comment-style-custom">${content}</div>
          </div>
<hr class="line2">`;

        $("#comment_list").append(temp_html);
      }
      detailPopup();
    },
  });
}
function detailPopup() {
  popup = document.querySelector(".modal");
  popup.style.display = "block";
}
function postPopup() {
  popup = document.querySelector(".create-post");
  popup.style.display = "block";
}
$(document).mouseup(function (e) {
  var container = $(".modal");
  var postcontainer = $(".create-post");

  if (postcontainer.has(e.target).length === 0) {
    postcontainer.css("display", "none");
  }

  if (container.has(e.target).length === 0) {
    container.css("display", "none");
  }
});
