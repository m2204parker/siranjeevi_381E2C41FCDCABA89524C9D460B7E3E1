function log()
{
    var overlay=document.getElementById("overlay")
    var pope=document.getElementById("pope")
    
        pope.style.display="block"
        overlay.style.display="block"
}
function sig(){
    var overlay=document.getElementById("overlay")
    var pop=document.getElementById("pop")
    var pope=document.getElementById("pope")
    
        pop.style.display="block"
        pope.style.display="none"
        user.textContent="Hello"
}
function del()
{
    pop.style.display="none"
    pope.style.display="none"
     overlay.style.display="none"
}
function sub() {
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const address = document.getElementById('address').value.trim();
    const password = document.getElementById('new_password').value.trim();
    const confirmPassword = document.getElementById('confirm_password').value.trim();
    const user = document.getElementById("username");

    // Check if any field is empty
    if (!name || !email || !phone || !address || !password || !confirmPassword) {
        alert("Please fill in all fields!");
        return;
    }

    // Check password match
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    // Set welcome message
    user.textContent = "Hello " + name;

    alert("Signup successful! (Form can be submitted here)");

    // Hide signup popup and show login popup
    document.getElementById("pop").style.display = "none";
    document.getElementById("pope").style.display = "none";
    document.getElementById("overlay").style.display = "none";
}

function add()
{
  window.location.href = "product.html";
  var img=document.getElementById("item")
  var pro=document.getElementById("pro")
  pro.value=item.value
  
}

  
