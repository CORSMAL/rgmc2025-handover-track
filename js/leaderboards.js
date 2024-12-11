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
