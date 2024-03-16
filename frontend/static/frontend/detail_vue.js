const app_vue = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            isLoading: false,
            error_message: "¡Lo sentimos!. Ocurrió un error inesperado",
            selectedField: '',
            startTime: '',
            endTime: ''
        };
    },
    computed: {},
    methods: {
        goTo() {
            this.$nextTick(() => {
                console.log("Fecha Vue: ", this.selectedField, this.startTime, this.endTime);
                if (this.selectedField && this.startTime && this.endTime) {
                    localStorage.setItem('fieldId', this.selectedField);
                    localStorage.setItem('startTime', this.startTime);
                    localStorage.setItem('endTime', this.endTime);
                    window.location.href = '/realizar-pago'; // Asegúrate de que esta es la URL correcta
                } else {
                    alert("Selecciona una cancha")

                    console.log("Error: Complete todos los datos por favor");
                    this.error_message = "Por favor selecciona la cancha y el horario.";
                }
            });
        },

        updateSelection(start, end) {
            console.log("Method: ", start, end)
            this.startTime = start;
            this.endTime = end;
        },


    },
    mounted: function () {


    },
});
const root_vue = app_vue.mount("#vue_detail");