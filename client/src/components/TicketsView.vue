<template id="tickets-table">
  <v-card>
    <v-card-title>
      Current Tickets
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="search"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="ticketsToShow"
      :search="search"
    >
      <template slot="items" slot-scope="props">
        <td class="text-xs-right">{{ props.item.pendingTickets }}</td>
        <td class="text-xs-right">{{ props.item.ongoingTickets }}</td>
        <td class="text-xs-right">{{ props.item.fixedTickets }}</td>
      </template>
      <v-alert slot="no-results" :value="true" color="error" icon="warning">
        Your search for "{{ search }}" found no results.
      </v-alert>
    </v-data-table>
    <button class="btn btn-default" v-on:click = getTickets>BOTON</button>
  </v-card>
</template>

<script>
  import axios from 'axios'
  export default {
      
    data () {
      return {
        search: '',
        headers: [
          { text: 'Pending Tickets', value: 'pending' },
          { text: 'Ongoing Tickets', value: 'ongoing' },
          { text: 'Fixed Tickets', value: 'fixed' }
        ],
        ticketsToShow: [
          {
            value: false,
            name: '01'
          },
          {
            value: false,
            name: '02'
          }
        ]
      }
    },

    methods:{

      //product ID, Ticket ID, descripcion, ubicacion, imagen
      //TODO create variable en el config dev, URL_API

      getTickets: function () {
        axios.get('http://10.43.96.216:8080/inventory?item=0123456789')
        .then(response => {
            console.log(response.data);
            //this.ticketsToShow = response.data
        })
        .catch(error => {
          console.log(error);
        })
      }

    }
  }
</script>