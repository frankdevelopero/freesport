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
            phone_code: "",
            phone_number: "",
            role: 2,
            users: [],
        };
    },
    computed: {},
    methods: {

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
            axios.post(`/api/v1/users/register`, JSON.stringify(dataRequest), {
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
        },

        getAllCustomers() {
            this.isLoading = true;
            const token = localStorage.getItem('token');
            const headers = {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            };
            axios.get('/api/v1/users/', {headers})
                .then(response => {
                    this.users = response.data;
                    this.isLoading = false;
                    this.enableDataTable()
                })
                .catch(error => {
                    console.error(error);
                    this.isLoading = false;
                });

        },
        editUser(user) {
            console.log('Editar usuario', user);
        },

        deleteUser(user) {
            console.log('Eliminar usuario', user);
        },

        enableDataTable() {
            this.$nextTick(() => {
                $('#usersTable').DataTable({
                    language: {
                        "sProcessing": "Procesando...",
                        "sLengthMenu": "Mostrar _MENU_ registros",
                        "sZeroRecords": "No se encontraron resultados",
                        "sEmptyTable": "Ningún dato disponible en esta tabla",
                        "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
                        "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
                        "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
                        "sInfoPostFix": "",
                        "sSearch": "Buscar:",
                        "sUrl": "",
                        "sInfoThousands": ",",
                        "sLoadingRecords": "Cargando...",
                        "oPaginate": {
                            "sFirst": "Primero",
                            "sLast": "Último",
                            "sNext": "Siguiente",
                            "sPrevious": "Anterior"
                        },
                        "oAria": {
                            "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                            "sSortDescending": ": Activar para ordenar la columna de manera descendente"
                        }
                    }
                });
            });

        },

    },
    mounted: function () {
        this.getAllCustomers()
    },
});
const root_vue = app_vue.mount("#vue_users");