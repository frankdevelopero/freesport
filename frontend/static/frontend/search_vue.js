const app_vue = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            isLoading: false,
            error_message: "¡Lo sentimos!. Ocurrió un error inesperado",

        };
    },
    computed: {},
    methods: {




    },
    mounted: function () {

    },
});
const root_vue = app_vue.mount("#vue_search");