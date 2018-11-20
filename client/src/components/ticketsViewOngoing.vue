<template id="tickets-table">
  <v-card>
    <v-card-title>
      <h2>
      Current Tickets
      </h2>
      <v-spacer></v-spacer>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="ticketsToShow"
    >
      <template slot="items" slot-scope="props">
        <td class="text-xs-right">{{ props.item.value }}</td>
        <td class="text-xs-right">{{ props.item.name }}</td>
      </template>
      <v-alert slot="no-results" :value="true" color="error" icon="warning">
        Your search for "{{ search }}" found no results.
      </v-alert>
    </v-data-table>
  </v-card>

</template>

<script>
  import axios from 'axios'
  import Vue from 'vue'
  export default {

    data () {
      return {
        search: '',
        headers: [
          { text: 'Ticket No.', value: 'pending' },
          { text: 'Date', value: 'ongoing' },
        ],
        ticketsToShow: [
        ]
      }
    },

    methods:{

      //product ID, Ticket ID, descripcion, ubicacion, imagen
      //TODO create variable en el config dev, URL_API
      //edit comlumn

      getTickets: function () {
        axios.get('http://10.43.97.120:8080/ongoing?user='+this.$g_username)
        .then(response => {
            console.log(response.data);
            let i=0;
            for(i in response.data){
                this.ticketsToShow.push({value: response.data[i][0], name: response.data[i][1]});
            }

        })
        .catch(error => {
          console.log(error);
        })
      }

    },

    mounted: function() {
      this.getTickets()
    }
  }

</script>
