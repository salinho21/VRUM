<template>
  <v-card>
    <v-navigation-drawer
      app
      clipped
      v-if="drawerOn"
      permanent
      :expand-on-hover="expandOnHover"
      :mini-variant="miniVariant"
      color="#7e380e"
      class="navBar"
    >
      <v-list nav dense dark>
        <v-list-item link to="/homeLogado">
          <v-list-item-icon>
            <v-icon>mdi-home</v-icon>
          </v-list-item-icon>
          <v-list-item-title class="white--text">Home</v-list-item-title>
        </v-list-item>

        <v-list-item link to="/profile">
          <v-list-item-icon>
            <v-icon>mdi-account</v-icon>
          </v-list-item-icon>
          <v-list-item-title class="white--text">Perfil</v-list-item-title>
        </v-list-item>

        <v-list-item link to="/viagens">
          <v-list-item-icon>
            <v-icon>mdi-car</v-icon>
          </v-list-item-icon>
          <v-list-item-title class="white--text"
            >Viagens Disponíveis</v-list-item-title
          >
        </v-list-item>

        <v-list-item link to="/search">
          <v-list-item-icon>
            <v-icon>mdi-magnify</v-icon>
          </v-list-item-icon>
          <v-list-item-title class="white--text"
            >Procurar Viagem</v-list-item-title
          >
        </v-list-item>

        <v-list-item link to="/criarviagem">
          <v-list-item-icon>
            <v-icon>mdi-steering</v-icon>
          </v-list-item-icon>
          <v-list-item-title class="white--text"
            >Inserir Viagem</v-list-item-title
          >
        </v-list-item>

        <v-list-item link to="/historico">
          <v-list-item-icon>
            <v-icon>mdi-history</v-icon>
          </v-list-item-icon>
          <v-list-item-title class="white--text">Histórico</v-list-item-title>
        </v-list-item>

                <v-list-item link to="/carteira">
          <v-list-item-icon>
            <v-icon>mdi-credit-card-outline</v-icon>
          </v-list-item-icon>
          <v-list-item-title class="white--text">Carteira</v-list-item-title>
        </v-list-item>

        <!-- List group se for uma secção da barra de navegação lateral que se divida em subsecções-->
        <v-list-group  :value="false" no-action>
          <template v-slot:activator>
            <v-list-item-icon>
            <v-icon :color="cor">mdi-bell-ring</v-icon>
          </v-list-item-icon>
            <v-list-item-title :class="corText" 
              >Notificações</v-list-item-title
            >
          </template>
          
          <v-list-item link to="/pedidos">
          <v-list-item-icon>
            <v-icon>mdi-clipboard</v-icon>
          </v-list-item-icon>
            <v-list-item-title class="white--text">Pedidos</v-list-item-title>
          </v-list-item>
          
          <v-list-item link to="/inbox">
          <v-list-item-icon>
            <v-icon>mdi-mail</v-icon>
          </v-list-item-icon>
            <v-list-item-title class="white--text">Mensagens</v-list-item-title>
          </v-list-item>
          <v-list-item link to="/notifications">
          <v-list-item-icon>
            <v-icon>mdi-bell-ring</v-icon>
          </v-list-item-icon>
            <v-list-item-title class="white--text">Notificações</v-list-item-title>
          </v-list-item>
        </v-list-group>

        <v-list-item link to="/settings">
          <v-list-item-icon>
            <v-icon>mdi-cog</v-icon>
          </v-list-item-icon>
          <v-list-item-title class="white--text">Definições</v-list-item-title>
        </v-list-item>
      </v-list>
      <template v-slot:append>
        <div class="pa-2">
          <v-btn block @click="logout">
            <v-list-item-icon>
              <v-icon>mdi-exit-to-app</v-icon>
            </v-list-item-icon>
            Logout
          </v-btn>
        </div>
      </template>
    </v-navigation-drawer>
  </v-card>
</template>

<script>
import {mapActions} from "vuex"
import { mapState } from "vuex";

export default {
  computed: mapState({
    username: (state) => state.auth.username,
  }),
  data() {
    return {
      miniVariant: true,
      expandOnHover: true,
      drawerOn: true,
      tempDrawer: false,
      cor:'white',
      corText:'white--text'
    }
  },
  
 
  
  methods: {
   ...mapActions({
      logOut: 'auth/logOut'
    }),
    
    logout(){
      this.logOut()
      this.$router.push('/')
    },
    //função de fixação da barra de navegação lateral
    fixNav: function () {
      this.expandOnHover = !this.expandOnHover;
      this.miniVariant = !this.miniVariant;
      this.drawerOn = false;
      this.$nextTick(() => (this.drawerOn = true));
    },
  }
}
</script>

<style scoped>
/* css da barra de navegação lateral */
header {
  background: #2a3f54;
  padding: 10px;
}

h1 {
  color: white;
  text-align: center;
}
.navBar {
  align-self: right;
  text-align: left;
}
h3 {
  color: white;
}
.ava {
  margin-top: 50px;
}
</style>
