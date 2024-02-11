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
        clearAllForm() {
            this.isLoading = false
            this.show_error_message = false
            this.first_name = ""
            this.last_name = ""
            this.email = ""
            this.password = ""
            this.phone_code = "+51"
            this.phone_number = ""
            this.successful_message = "Nuevo usuario registrado con éxito"
            this.role = 2
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
                role: parseInt(this.role)
            };
            console.log(dataRequest);
            let csrfToken = this.getCookie('csrftoken');
            axios.post(`/api/v1/users/new`, JSON.stringify(dataRequest), {
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
            }).then((res) => {
                if (res.status === 200) {
                    this.successful = true
                    this.successful_message = `El usuario ${this.email} ha sido registrado con éxito.`
                    let modalSuccellful = new bootstrap.Modal(document.getElementById('modalSuccessful'), {keyboard: false})
                    modalSuccellful.show()
                    this.clearAllForm()
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
        },

        getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
    },
    mounted: function () {

    },
});
const root_vue = app_vue.mount("#vue_users");