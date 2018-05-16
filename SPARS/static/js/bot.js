cbcore = {
  
  init:function(divID){
    this.mainDiv = $('#'+divID)
  },
  
  msg:function(msg){
    t='<div class="botui-message-content text">'+msg+'</div>'
    this.mainDiv.append(t)
  },
  
  textin:function(callback){
    ip = $('<input type="text" class="bot-inp" required/>')
    btn = $('<button type="button" autofocus="autofocus" class="btn-warning bot-btn"> Enter </button>')
    btn.click(function(){
      this.style.display='none'
      $(ip).prop('readonly',true)
      callback($(ip).val())     
    })
    t = $('<div class="botui-actions-buttons"></div>')
    t.append(ip)
    t.append(btn)
    this.mainDiv.append(t)
  },
  
  btns:function(btns,callback){
    t = $('<div class="botui-actions-buttons"></div>')
    for (i=0 ;i<btns.length; i++){
      b = $('<button type="button" autofocus="autofocus" class="btn-warning bot-btn" value="'+btns[i]['value']+'">'+btns[i]['label']+'</button>')
      b.click(function(){
        this.style.backgroundColor="red"
        $(t).children().attr('disabled','disabled')
        callback(this.value)
        
      })
      t.append(b)
      this.mainDiv.append(t)
    }
  },
}

spars = {
  user:null,
  start:function(a){
    cbcore.init(a)
    $.get("/get/user",null,function(obj){
      
      //obj = JSON.parse(data)
      cbcore.msg("Hi "+obj['name']+"!")
      spars.user=obj
      if (obj['new']==1){
        spars.newUser()
      }
      else {
        spars.oldUser()
      }
    })
    
  },
  newUser:function(){
    // ask what kind of games he likes
    cbcore.msg("Do you like playing video games?")
    cbcore.btns([{'label':'Yes','value':1},{'label':'No','value':0}], function(res){
      if (res=='1'){

      }
      else{
        cbcore.msg("Nonsense! Everyone likes playing some type of game.")
      }
      cbcore.msg("What types of games do you like?")
      cbcore.textin(spars.storeTags)
    })
  
  },
  oldUser:function(){
    $.get("/get/lastSuggestion", null, function(data){
      if (data==0){
        spars.newUser()
      }else{
        cbcore.msg("Did you enjoy "+data['app_name']+" ?")
        cbcore.btns([{'label':'Yes','value':2},{'label':'No','value':1}, {'label':'Not played it yet','value':0}],
          function(res){
            if (res==2){
              cbcore.msg("Awesome!")
              $.post("/store/game",{"data":data['spars_id']},function(){})
            }else if(res==1){
              cbcore.msg("I'm sorry to hear that :(")
              $.post("/store/game",{"data":data['spars_id']},function(){})
            }else{
              cbcore.msg("It's okay, take your time")
            }
            cbcore.msg("In the meanwhile, I have been looking for other games you might like, if you are interested.")
            cbcore.btns([{'label':'Sure','value':1},{'label':'Nah, I want something new','value':0}],
                function(res){
                  if (res==1){
                    spars.showRecos() 
                  }else{
                    cbcore.msg("What kind of games are you in the mood for?")
                    cbcore.textin(spars.storeTags)
                  }
                })          
            })
      }
    })
  
  },
  showRecos:function(){
    
    $.get("/get/recos",null, spars.suggest)
  },
  storeTags:function(line){
    $.post("/store/tags",{"data":line}, function(data){
      cbcore.msg("What is your favorite game?")
      cbcore.textin(spars.storeGame)
    })
  },
  storeGame:function(line){
    $.post("/store/game",{"data":line}, function(data){
      if(data=='0'){
        cbcore.msg("I havn't heard of that one before...")
        cbcore.msg("What other game do you like?")
        cbcore.textin(spars.storeGame)
      }
      else{
        if (data['rating']){
          r=data['rating']
          if (r>3){
            cbcore.msg(data['name']+" is a really good game!")
          }
          else if (r<2){
            cbcore.msg("Hmm... I don't judge.")
          }
          else {
            cbcore.msg("Not a bad choice.")
          }
          
        }
        else {
          cbcore.msg("Oooo... Interesting.")
        }
        cbcore.msg("I think I know a game you might like...")
        $.post("/get/similar", {"id":data['spars_id']}, spars.suggest)
      }
    })
  },
  suggest:function(data){
    spars.recos = data
    spars.pos=0
    
    spars.showSuggests(spars.pos)
  },  
  manage:function(data){
    if (data==2){
      $.post("/store/search",{"data":spars.recos[spars.pos]['spars_id']},function(){})
      cbcore.msg("No problem :)")
      cbcore.msg("come back to me after you've played it")
    }else{
      if (data==1){
        $.post("/store/game",{"data":spars.recos[spars.pos]['spars_id']},function(){})
      }
      spars.pos+=1
      if (spars.pos < Object.keys(spars.recos).length){
        spars.showSuggests(spars.pos)      
      }
      else{
        cbcore.msg("I'm all out of suggestions :(")
        cbcore.msg("What other game do you like?")
        cbcore.textin(spars.storeGame)
      }
    }
  },
  showSuggests: function(i){
    data=spars.recos[i]
    cbcore.msg("Try out "+data['app_name']+". I think you will like it. You can find it <a href='"+data['url']+"'>here</a>.")  
    cbcore.btns([{'label':'Thanks','value':2},{'label':'Already Played it','value':1}, {'label':'Not interested','value':0}], spars.manage)
  },

}


/*function nameLoad()
{
    Uname=document.getElementById("usrname");
    nameF= Uname.value;
    field = document.getElementById("stepOne");
    field.innerHTML = "So <i>"+nameF+"</i>, you like games?";
    con1=document.getElementById("containerOne");
    con2=document.getElementById("containerTwo");
    con1.style.visibility="visible";
    con2.style.visibility="visible";
}

function bye()
{
    field = document.getElementById("stepTwo");
    field.innerHTML = "See You Later, Bye!";
    con3=document.getElementById("containerThree");
    con3.style.visibility="visible";
    con4=document.getElementById("containerFour");
    con4.style.visibility="hidden";
}

function gameType()
{
    field = document.getElementById("stepTwo");
    field.innerHTML = "Tell me something about the type of games you would like to play?";
    con3=document.getElementById("containerThree");
    con3.style.visibility="visible";
    con4=document.getElementById("containerFour");
    con4.style.visibility="visible";
}

function submitGameType()
{
    Ugame=document.getElementById("gametype");
    gameF= Ugame.value;
    //xhr call to be made
    con5=document.getElementById("containerFive");
    con5.style.visibility="visible";
    con6=document.getElementById("containerSix");
    con6.style.visibility="visible";
}

function gameNames()
{
    g1=document.getElementById("game1");
    gameF1= g1.value;
    g2=document.getElementById("game2");
    gameF2= g2.value;
    g3=document.getElementById("game3");
    gameF3= g3.value;
    
    //Create JSON object of game names
    var json_string_games = "{g1: "+gameF1+", g2: "+gameF2+", g3: "+gameF3+"}"
    var json_games = JSON.parse(json_games)
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function(){
        if(this.readyState == 4  && this.status == 200){
            //Do something
            con7 = document.getElementById("containerSeven");
            con7.style.visibility="visible";
            
        }
    };
    xhr.open("GET", ".php?");
    xhr.send();
}
*/


