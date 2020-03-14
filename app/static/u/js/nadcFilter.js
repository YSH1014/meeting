
Vue.component('nadc-filter-row', {
    props: ['ftKey', 'keyLocale', 'values', 'selected'],
    methods: {
        click: function (event) {
            key = event.currentTarget.attributes.ftkey.nodeValue;
            value = event.currentTarget.attributes.ftvalue.nodeValue;
            this.$emit('trigger', key, value)
        }
    },
    template: `
    <nav class="navbar navbar-expand-sm meeting-filter-navbar navbar-default">
        <a class="navbar-brand meeting-filterbox-navbrand">
            {{keyLocale}}
        </a>
        <button type="button" data-toggle="collapse" v-bind:data-target='"#navbarDropdown"+ftKey' v-bind:aria-controls="'#navbarDropdown'+ftKey" aria-expanded="false" aria-label="Toggle navigation" class="navbar-toggler collapsed">
            &#9660
        </button>
        <div v-bind:id="'navbarDropdown'+ftKey" class="navbar-collapse collapse">
            <ul class="navbar-nav  meeting-search-menu ft-menu">
                <li class="nav-item meeting-filterbox-listitem"
                    v-for="(value,index) in values"
                    v-if="index < 12"
                >    
                    <a href="#"
                     v-bind:ftKey="ftKey" 
                     v-bind:ftValue="value" 
                     v-on:click="click"
                     class="filter-tag nav-link index-topNav-link"
                     v-bind:style="{color:value==selected?'blue':'black'}">{{value}}</a>
                </li>
            </ul>
        </div>
    </nav>
    `
});
Vue.component('nadc-filter', {
    data: function () {
        return {
            conditions: {
                year: [],
                month: [],
                country: [],
                city: [],
                language: [],
            },              //筛选条件
            keyValue: {},   //所有key-value
            countryCityDict:{},//由国家得到城市列表
        }
    },
    methods: {
        trigger: function (key, value) {
            console.log(key + value)
            //这句无效，不能保证实时更新
            // this.conditions[key][0] = value;
            this.$set(this.conditions, key, [value])
            
            if(key == 'country'){
                this.keyValue.city = this.countryCityDict[value];
                this.$set(this.conditions,'city',[])   //重置城市
            }
            this.ft.trigger(this.conditions);
        },
        reset: function () {
            for(key in this.conditions){
                this.conditions[key] = [];
            }
            this.keyValue.city = this.countryCityDict.all;
            ft.reset();
        }
    },
    created: function () {
        //根据props传入的属性初始化私有变量
        //所有key,value
        for (key in this.ft._fields) {
            this.keyValue[key] = Object.keys(this.ft._fields[key]);
        }
        //country-city表
        //首先使用set保证唯一性。
        this.countryCityDict['all'] = new Set();
        for (meeting of ft._matrix){
            country  = meeting['country'][0];
            city = meeting['city'][0];
            
            if(!this.countryCityDict.hasOwnProperty(country)){
                this.countryCityDict[country] = new Set();
            }
            this.countryCityDict[country].add(city);
            this.countryCityDict['all'].add(city);
        }
        //然后转化为array，并排序
        for( country in this.countryCityDict){
            this.countryCityDict[country] = Array.from(this.countryCityDict[country]);
            this.countryCityDict[country].sort(function(city1,city2){
                return this.ft._fields.city[city2] - this.ft._fields.city[city1];
            });
        }
        //初始条件
        this.conditions = this.initConditions;
        this.ft.trigger(this.conditions);

    },
    props: ['ft',       //触发filter
        'localeKeyDict', //标签Key本地化显示（如 city:城市）
        'initConditions', //初始筛选条件
    ],            

    template: `
        <div >
            <nadc-filter-row
            v-for="values,key in keyValue"
            v-bind:ftKey="key"
            v-bind:keyLocale="localeKeyDict[key]"
            v-bind:values="values"
            v-on:trigger="trigger"
            v-bind:selected="conditions[key].length==0?'':conditions[key][0]"
            >
            </nadc-filter-row>
            <div align="center" style="margin-bottom: 15px;margin-top: 15px">
                <button id="reset" class="btn btn-sm btn-outline-danger" v-on:click="reset">重置条件</button>
            </div>
            
        </div>
    `
})