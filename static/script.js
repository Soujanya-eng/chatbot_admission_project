function toggleChat(){

let chat=document.getElementById("chatbot");
let input=document.getElementById("userInput");

if(chat.style.display==="block"){
chat.style.display="none";
}
else{
chat.style.display="block";

setTimeout(()=>{
input.focus();
},200);

}

}

function sendMessage(){

let input=document.getElementById("userInput");
let message=input.value.trim();

if(message==="") return;

let chatbox=document.getElementById("chatbox");

chatbox.innerHTML+=`<div class="message user">${message}</div>`;

fetch("/get",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({message:message})
})
.then(res=>res.json())
.then(data=>{

chatbox.innerHTML+=`<div class="message bot">${data.reply}</div>`;

chatbox.scrollTop=chatbox.scrollHeight;

});

input.value="";
}

document.getElementById("userInput").addEventListener("keypress",function(e){

if(e.key==="Enter"){
e.preventDefault();
sendMessage();
}

});

