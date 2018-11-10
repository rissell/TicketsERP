<template>
    <v-app>
    <v-navigation-drawer
      :clipped="$vuetify.breakpoint.lgAndUp"
      v-model="drawer"
      fixed
      app
    >
      <v-list dense>
        <template v-for="item in leftBarItems">
          <v-layout
            v-if="item.heading"
            :key="item.heading"
            row
            align-center
          >
            <v-flex xs6>
              <v-subheader v-if="item.heading">
                {{ item.heading }}
              </v-subheader>
            </v-flex>
            <v-flex xs6 class="text-xs-center">
              <a href="#!" class="body-2 black--text">EDIT</a>
            </v-flex>
          </v-layout>
          <v-list-group
            v-else-if="item.children"
            v-model="item.model"
            :key="item.text"
            :prepend-icon="item.model ? item.icon : item['icon-alt']"
            append-icon=""
          >
            <v-list-tile slot="activator">
              <v-list-tile-content>
                <v-list-tile-title>
                  {{ item.text }}
                </v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
            <v-list-tile
              v-for="(child, i) in item.children"
              :key="i"
              @click=""
            >
              <v-list-tile-action v-if="child.icon">
                <v-icon>{{ child.icon }}</v-icon>
              </v-list-tile-action>
              <v-list-tile-content>
                <v-list-tile-title>
                  {{ child.text }}
                </v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list-group>
          <v-list-tile v-else :key="item.text" @click="">
            <v-list-tile-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-tile-action>
            <v-list-tile-content>
              <v-list-tile-title>
                {{ item.text }}
              </v-list-tile-title>
            </v-list-tile-content>
          </v-list-tile>
        </template>
      </v-list>
    </v-navigation-drawer>
    <v-toolbar
      :clipped-left="$vuetify.breakpoint.lgAndUp"
      color="#A94E93"
      dark
      app
      fixed
    >
      <v-toolbar-title style="width: 300px" class="ml-0 pl-3">
        <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
        <span class="hidden-sm-and-down">Odoo Tickets</span>
      </v-toolbar-title>
      
      <v-toolbar-title style="width: 300px" class="ml-0 pl-3">
        <span class="hidden-sm-and-down">Today, {{datetime}}</span>
      </v-toolbar-title>
      
      <v-spacer></v-spacer>
      <v-toolbar-title style="width: 300px" class="ml-0 pl-3">
        <span class="hidden-sm-and-down">Welcome, {{username}}</span>
      </v-toolbar-title>
      <v-btn icon>
        <v-icon>account_circle</v-icon>
      </v-btn>
    </v-toolbar>
    <v-content>
      <v-container fluid fill-height>
        <v-layout justify-center align-center>
            <v-card>    
                <v-card-title>
                    <h2>
                    Submitted tickets
                    </h2>
                    <v-spacer></v-spacer>
                </v-card-title>
                <v-data-table
                    :headers="adminHeaders"
                    :items="adminTickets"
                    hide-actions
                    class="elevation-1"
                >
                    <template slot="items" slot-scope="props">
                    <td>{{ props.item.ticketId }}</td>
                    <td class="text-xs-right">{{ props.item.itemName }}</td>
                    <td class="text-xs-right">{{ props.item.issueDescription }}</td>
                    <td class="text-xs-right">{{ props.item.status }}</td>
                    </template>
                </v-data-table>
            </v-card>
        </v-layout>
      </v-container>
    </v-content>
    <v-btn
      fab
      bottom
      right
      color="pink"
      dark
      fixed
      @click="newTicketDialog = !newTicketDialog"
    >
      <v-icon>add</v-icon>
    </v-btn>


    <v-dialog v-model="newTicketDialog" width="800px">
      <form method="post" @submit.prevent="submitTicket">
      <v-card>
        <v-card-title
          class="grey lighten-4 py-4 title"
        >
          Create Ticket
        </v-card-title>
        <v-container grid-list-sm class="pa-4">
          <v-layout row wrap>
            <v-flex xs12 align-center justify-space-between>
              <v-layout align-center>
              </v-layout>
            </v-flex>
            <v-flex xs12>
              <v-text-field
                prepend-icon="business"
                placeholder="Reported item ID"
              ></v-text-field>
            </v-flex>
            <v-flex xs12>
              <v-text-field
                prepend-icon="business"
                placeholder="Description of issue"
              ></v-text-field>
            </v-flex>
            <v-flex xs6>
              <v-text-field
                prepend-icon="business"
                placeholder="Location"
              ></v-text-field>
            </v-flex>
            <v-flex xs3 d-flex>
              <v-select 
              :items="area"
              value="area.value"
              label="Area"
              ></v-select>
            </v-flex>
            <v-flex xs3 d-flex>
              <v-select
              :items="priorities"
              label="Priority"
              ></v-select>
            </v-flex>
          </v-layout>
        </v-container>
        <v-card-actions>
            
            <img :src="imageUrl" height="150" v-if="imageUrl"/>
            <v-text-field label="Select Image" @click='pickFile' v-model='imageName' prepend-icon='attach_file'></v-text-field>
				<input
					type="file"
					style="display: none"
					ref="image"
					accept="image/*"
					@change="onFilePicked"
				>          
            
            <v-spacer></v-spacer>
          <v-btn flat color="primary" >Cancel</v-btn>
          <v-btn type="submit" @click="submitTicket" flat color="primary" >Save</v-btn>
        </v-card-actions>
      </v-card>
      </form>
    </v-dialog>

  </v-app>

</template>

<script>

import axios from 'axios'
  export default {
    data: () => ({
      title: "Image Upload",
      dialog: false,
      imageName: '',
      imageUrl: '',
      imageFile: '',
      dialog: false,
      area: [
        { text: 'ELECTRIC', value: 'ELECTRIC' },
        { text: 'CLEANING', value: '' }, //TODO
        { text: 'IT' },
        { text: 'STORAGE' },
        { text: 'MAINTENANCE' },
        { text: 'SECURITY' }
      ],
      
      priorities: [
        { text: 'HIGH', value: '1' },
        { text: 'LOW', value: '0' }
      ],
      newTicketDialog: false,
      drawer: null,
      username: 'Rosa',
      datetime: new Date().toISOString().slice(0,10),
      leftBarItems: [
        { icon: 'contacts', text: 'Maintenance staff' },
        {
          icon: 'keyboard_arrow_up',
          'icon-alt': 'keyboard_arrow_down',
          text: 'Tickets',
          model: true,
          children: [
            { icon: 'history', text: 'Current tickets' }
          ]
        }
      ],
      adminHeaders: [
          {
            text: 'Ticket No.',
            align: 'center',
            sortable: true,
            value: 'ticketId'
          },
          {
            text: 'Item name',
            align: 'center',
            sortable: true,
            value: 'itemName'
          },
          {
            text: 'Issue description',
            align: 'center',
            sortable: true,
            value: 'issueDescription'
          },
          {
            text: 'Status',
            align: 'center',
            sortable: true,
            value: 'status'
          }
        ],
        adminTickets: [        
          {
              ticketId: '00',
              itemName: 'chair',
              issueDescription: 'description of issue',
              status: 'LOW'
          },
          {
              ticketId: '01',
              itemName: 'table',
              issueDescription: 'description of issue',
              status: 'HIGH' 
          }
        ]
    }),
    props: {
      source: String
    },
    methods: {

      //TODO GET adminTickets
      //TODO POST ticket
      //TODO PUT ticket
      
      submitTicket: function () {
        axios(
          {
            method: 'post',
            url: 'http://10.43.102.7:8080/',
            data: 'algo'//TODO
          }
        )
        .then(response => {
            console.log(response.data);            
        })
        .catch(error => {
          console.log(error);
        })
      },

      pickFile () {
            this.$refs.image.click ()
        },
		
      onFilePicked (e) {
        const files = e.target.files
        if(files[0] !== undefined) {
          this.imageName = files[0].name
          if(this.imageName.lastIndexOf('.') <= 0) {
            return
          }
          const fr = new FileReader ()
          fr.readAsDataURL(files[0])
          fr.addEventListener('load', () => {
            this.imageUrl = fr.result
            this.imageFile = files[0] // this is an image file that can be sent to server...
          })
        } else {
          this.imageName = ''
          this.imageFile = ''
          this.imageUrl = ''
        }
      }
      
    }
  }

</script>