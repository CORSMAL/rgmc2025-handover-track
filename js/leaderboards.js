window.TableLoader = {
    tables:{},
    register:function(table, func){
        this.tables[table] = func;
    },
    trigger:function(key){
        var self = this;

        if(this.tables[key]){
            this.tables[key]();
            this.tables[key] = function(){};

            var keys = Object.keys(this.tables);
            var index = keys.indexOf(key);

            if(index){
                this.tables[keys[index - 1]]();
                this.tables[keys[index - 1]] = function(){};
            }

            if(index < keys.length - 1){
                this.tables[keys[index + 1]]();
                this.tables[keys[index + 1]] = function(){};
            }
        }

        if(key == "theming"){
            var themes = Object.keys(this.tables).slice(-7);

            themes.forEach(function(item){
                self.trigger(item);
            })
        }
    },
    loadFirst:function(){
        first = Object.keys(this.tables)[0];

        if(first){
            this.trigger(first);
        }
    }
}

function AppearLegend(legend_id) {
    var x = document.getElementById(legend_id);
    if (x.style.display === "none") {
      x.style.display = "block";
    } else {
      x.style.display = "none";
    }
  }

// ///////////////////////////////////////////////////////////////////////////
// ICRA 2024 - 9th Robotic Grasping and Manipulation Competition
// 
// Essential Skills Sub-track 4: Human-to-Robot Handovers
// 
// 

var preparation_table =
[
    {id:1,team:"ETH SRL",score:0.00.toFixed(2)},
    {id:2,team:"SirsIIT",score:0.00.toFixed(2)},
    {id:3,team:"CIS-QMUL",score:0.00.toFixed(2)},
    {id:4,team:"Air-jnu",score:0.00.toFixed(2)},
    {id:5,team:"XJTU_Colab",score:0.00.toFixed(2)},
    {id:6,team:"TCS",score:0.00.toFixed(2)}
];

    // {id:3,team:"CASIA-YIT-HAIZHICHE",score:0.00.toFixed(2)},
    // {id:1,team:"BUPT DexRobot",score:0.00.toFixed(2)},

var competition_table =
[
    {id:1,team:"SirsIIT",score:0.00.toFixed(2)},
    {id:2,team:"TCS",score:0.00.toFixed(2)},
    {id:3,team:"ETH SRL",score:0.00.toFixed(2)},
    {id:4,team:"Air-jnu",score:0.00.toFixed(2)},
    {id:5,team:"XJTU_Colab",score:0.00.toFixed(2)}
];

var corsmal_table =
[
    {
        id:1,
        name:"Baseline", 
        score:0.32.toFixed(2), 
        s1:0.59.toFixed(2),
        s2:0.55.toFixed(2),
        s3:0.54.toFixed(2),
        s4:0.0.toFixed(2),
        s5:0.0.toFixed(2),
        s6:0.0.toFixed(2),
        s7:0.0.toFixed(2),
        s8:0.94.toFixed(2),
        s9:0.47.toFixed(2),
        s10:0.49.toFixed(2),
        s11:0.41.toFixed(2),
        s12:0.46.toFixed(2),
        s13:0.45.toFixed(2),
        vision:0.19.toFixed(2),
        robotics:0.31.toFixed(2),
        global:0.46.toFixed(2),
        cup1:0.33.toFixed(2),
        cup2:0.31.toFixed(2),
        cup3:0.33.toFixed(2),
        cup4:0.33.toFixed(2),
        empty:0.31.toFixed(2),
        filled:0.34.toFixed(2),
        grasp1:0.33.toFixed(2),
        grasp2:0.31.toFixed(2),
        grasp3:0.00.toFixed(2),
        left:0.34.toFixed(2),
        center:0.29.toFixed(2),
        right:0.33.toFixed(2)
    },
];



// ///////////////////////////////////////////////////////////////////////////
// const form = document.querySelector('form');
// form.addEventListener('submit', handleSubmit);

// function handleSubmit(event) {
//     const form = event.currentTarget;
//     const url = new URL(form.action);
//     const formData = new FormData(form);
//     const searchParams = new URLSearchParams(formData);

//     const fetchOptions = {
//       method: form.method,
//     };

//     if (form.method.toLowerCase() === 'post') {
//         if (form.enctype === 'multipart/form-data') {
//           fetchOptions.body = formData;
//         } else {
//           fetchOptions.body = searchParams;
//         }
//       } else {
//         url.search = searchParams;
//       }

//     fetch(url, fetchOptions);

//     event.preventDefault();
// }
