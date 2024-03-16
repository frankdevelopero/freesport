const app_vue = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            isLoading: false,
            error_message: "¡Lo sentimos!. Ocurrió un error inesperado",
            selectedCity: '',
            selectedSport: '',
            selectedDate: '',
            selectedTime: '',
            searchResults: [],
            totalResults: 0,
        };
    },
    computed: {},
    methods: {
        search() {
            if (this.selectedCity && this.selectedSport && this.selectedDate && this.selectedTime) {
                const searchURL = `/api/v1/search/fields/?sport_id=${this.selectedSport}&date_time=${this.selectedDate}T${this.selectedTime}:00Z&district_id=${this.selectedCity}`;
                axios.get(searchURL)
                    .then(response => {
                        console.log(response.data);
                        this.searchResults = response.data;
                        this.totalResults = response.data.length;

                    })
                    .catch(error => {
                        console.error(error);
                        this.error_message = "Error al realizar la búsqueda: " + error.message;
                    });
            } else {
                console.log(this.selectedCity, this.selectedSport, this.selectedDate, this.selectedTime)
                console.log("Error: Complete todos los datos por favor")
                this.error_message = "Por favor selecciona la ciudad, deporte, fecha y hora.";
            }
        },
        getDetailUrl(businessId) {
            return detailUrlBase.replace('/0/', '/' + businessId + '/');
        }

    },
    mounted: function () {


    },
});
const root_vue = app_vue.mount("#vue_search");