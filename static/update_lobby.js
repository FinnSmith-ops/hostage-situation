async function updateLobby(){
    game_code = parseInt(game_code)
    const response = await fetch("/update_lobby", {
        method: "POST",
        headers: {
            "Content-Type" : "application/json"
        
        },
        body: JSON.stringify({
            game_id : game_code
        })
    })
    let answer = await response
    data = await answer.json()
    for(const i of data){
        if(!people.includes(i)){
            let name = document.createElement("li");
            name.innerHTML = i;
            document.getElementById("playerList").appendChild(name);
            people.push(i)
        }
}   
}

let people = []
setInterval(updateLobby, 2000)
