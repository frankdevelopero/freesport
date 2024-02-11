const app_vue = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            label_submit_code: "Validar código",
            isLoading: false,
            show_error_message: false,
            first_name: "",
            last_name: "",
            phone_code: "+51",
            phone_number: "",
            email: "",
            password: "",
            business_title: "",
            business_ruc: "",
            business_slug: "",
            department: 0,
            province: 0,
            district: 0,
            line: 0,
            code_1: "",
            code_2: "",
            code_3: "",
            code_4: "",
            code_5: "",
            code_6: "",
            error_message: "¡Lo sentimos!. Ocurrió un error inesperado",

        };
    },
    computed: {},
    methods: {
        goToLogin() {
            window.location.href = "/inicia-sesion"
        },

        validatePhone() {
            changeViewLoading(true)
            axios.post(`/api/v1/users/auth/verify-phone`, JSON.stringify({
                email: this.email,
                code: `${this.code_1}${this.code_2}${this.code_3}${this.code_4}${this.code_5}${this.code_6}`,
            }), {
                headers: {
                    "Content-Type": "application/json",
                },
            }).then(function (res) {
                if (res.status === 200) {
                    changeViewLoading(false)
                    this.label_submit_code = "Inicia sesión"
                    successMessage()

                }
            }).catch(function (err) {
                errorMessage(err.response.data.message)
                changeViewLoading(false)
                console.log(err);
            }).then(function () {

            });
        },


        registerNewUser() {
            this.error_message = "";
            this.isLoading = true;
            this.show_error_message = false;
            let dataRequest = {
                first_name: this.first_name,
                last_name: this.last_name,
                email: this.email,
                password: this.password,
                role: 1
            };
            console.log(dataRequest);
            axios.post(`/api/v1/auth/register`, JSON.stringify(dataRequest), {
                headers: {
                    "Content-Type": "application/json",
                },
            }).then((res) => {
                console.log("exito", res);
                if (res.status === 200) {
                    console.log(res);
                    window.location.href = `/verifica-tu-cuenta?username=${res.data.email}`;
                }
            }).catch((err) => {
                this.show_error_message = true;
                this.isLoading = false;
                if (err.response && err.response.data) {
                    this.error_message = err.response.data.message;
                } else {
                    this.error_message = 'Ha ocurrido un error inesperado.';
                }
                console.log(err);
            });
        }

    },
    mounted: function () {

    },
});
const root_vue = app_vue.mount("#vue_signup");