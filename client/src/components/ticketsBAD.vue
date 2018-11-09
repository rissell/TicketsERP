<template id="tickets-table">
  <v-card>
    <v-card-title>
      <h1>
        Current Tickets
      </h1>
      <v-spacer></v-spacer>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="ticketsToShow"
      :search="search"
    >
      <template slot="items" slot-scope="props">
        <td class="text-xs-right">{{ props }}</td>
        <td class="text-xs-right">{{ props[0][1] }}</td>
      </template>

    </v-data-table>
    <h1>hello</h1>

    <button class="btn btn-default" v-on:click = getTickets>BOTON</button>
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
          {
                ticketId: tickets[0][0],
                ticketDate: tickets[0][1]
          },

        ],
      }
    },

    methods:{

      //product ID, Ticket ID, descripcion, ubicacion, imagen
      //TODO create variable en el config dev, URL_API. Crear un POST
      //dropdown 

      getTickets: function () {
        
        axios.get('http://10.43.102.7:8080/tickets')
        .then(response => {
            console.log(response.data);
            var tickets = response.data;
            var ticketsJson = [
              {
                ticketId: tickets[0][0],
                ticketDate: tickets[0][1]
              },
              {
                ticketId: tickets[1][0],
                ticketDate: tickets[1][1]
              }
            ]
            console.log(ticketsJson);            
            ticketsToShow = ticketsJson;
            
            //this..push(response.data);
        })
        .catch(error => {
          console.log(error);
        })
      },

    }
  
    
  }


</script>
