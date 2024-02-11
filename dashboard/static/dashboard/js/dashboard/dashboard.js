const app_vue = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            isLoading: false,
            show_error_message: false,
            first_name: "",
            last_name: "",
            email: "",
            password: "",
            phone_code: "+51",
            phone_number: "",
            successful_message: "Nuevo usuario registrado con éxito",
            role: 2,
            users: [],
        };
    },
    computed: {},
    methods: {
        getTokenFromDjango() {

            axios.get('/api/v1/auth/get_token')
                .then(response => {
                    const token = response.data.token;
                    localStorage.setItem('token', token);
                    this.getBusinessDetail()
                    this.getCategories()
                    this.getPaymentMethods()
                })
                .catch(error => {
                    console.log(error);
                });
        },
    },
    mounted: function () {
        this.getTokenFromDjango()
    },
});
const root_vue = app_vue.mount("#vue_dashboard");