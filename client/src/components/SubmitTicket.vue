<template>
    <v-dialog v-model="newTicketDialog" width="800px">
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
                
                <v-text-field
                  placeholder="Ticket ID"
                ></v-text-field>
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
            <v-flex xs12>
              <v-avatar size="40px" class="mr-3">
                  <img
                    src="//ssl.gstatic.com/s2/oz/images/sge/grey_silhouette.png"
                    alt=""
                  >
                </v-avatar>
              <v-text-field
                prepend-icon="user"
                placeholder="Assigned staff"
              ></v-text-field>
            </v-flex>
          </v-layout>
        </v-container>
        <v-card-actions>
          <v-btn flat color="primary">Attach photo</v-btn>
          <v-spacer></v-spacer>
          <v-btn flat color="primary" @click="newTicketDialog = false">Cancel</v-btn>
          <v-btn flat @click="newTicketDialog = false">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>