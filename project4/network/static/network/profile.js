

document.addEventListener('DOMContentLoaded', function() {
    
 });



function editpost(e){
  window.t = e;
  var post_id = e.getAttribute("value");
  console.log(post_id);
  e.parentNode.style.display = 'none';
  document.querySelector('#p'+post_id).style.display = 'block';
  postId = post_id;

  
};

function savepost(e){
  var post_id = postId;
  console.log("这里是"+post_id)
  new_content = document.querySelector('#new-content'+post_id).value
  e.parentNode.style.display = 'none';
  var t = document.querySelector('#replaceTextarea'+post_id)
  t.style.display = 'block';
  fetch('/editAndLike/'+post_id, {
    method: 'PUT',
    body: JSON.stringify({
        content: new_content
    })
  })
  .then(response => response.json())
    .then(result => {
      let tmp = JSON.stringify(result);
      if(tmp.includes('error')){
        console.log(result);
        alert(JSON.stringify(result));
      }
      else{
        console.log(result);
      }
        
    });
    t.querySelector('#message').innerText = new_content;
    console.log(post_id);
    console.log(new_content);

}

function like(e){
  var post_id = e.getAttribute("value")
  var tmp = e.parentNode
  console.log(post_id);
  current_state = e.innerText;
  if (current_state == "Like"){
    e.innerText = "Unlike";
    old_number = tmp.querySelector('#like_number');
    new_number = parseInt(old_number.innerText) + 1;
    fetch('/editAndLike/'+post_id, {
      method: 'PUT',
      body: JSON.stringify({
          like: 1
      })
    })
    .then(response => response.json())
      .then(result => {
        let tmp = JSON.stringify(result);
        if(tmp.includes('error')){
          console.log(result);
          alert(JSON.stringify(result));
        }
        else{
          console.log(result);
        }
          
      });
    old_number.innerText = new_number;
  }
  else{
    e.innerText = "Like";
    old_number = tmp.querySelector('#like_number');
    new_number = parseInt(old_number.innerText) - 1;
    fetch('/editAndLike/'+post_id, {
      method: 'PUT',
      body: JSON.stringify({
          like: -1
      })
    })
    .then(response => response.json())
      .then(result => {
        let tmp = JSON.stringify(result);
        if(tmp.includes('error')){
          console.log(result);
          alert(JSON.stringify(result));
        }
        else{
          console.log(result);
        }
          
      });
    old_number.innerText = new_number;
  }
  

}

function unloginlike(){
  alert("You have to login to like this post.");
}