<template>
  <v-container class="my-5">
    <Header @clicked="onClickHeader"></Header>
    <NavDraw ref="navdraw"></NavDraw>
    <v-alert
      :value="alertPedidoFeito"
      transition="slide-y-transition"
      dense
      color="dark green"
      dismissible
      type="success"
      @input="alertPedidoFeito = false"
    >
      Pedido enviado
    </v-alert>
    <v-alert
      :value="alertPedidoCancelado"
      transition="slide-y-transition"
      dense
      color="dark green"
      dismissible
      type="success"
      @input="alertPedidoCancelado = false"
    >
      Pedido cancelado
    </v-alert>
    <v-alert
      :value="alertErro"
      transition="slide-y-transition"
      dense
      color="dark red"
      dismissible
      type="error"
      @input="alertErro = false"
    >
      Erro!
    </v-alert>
    <v-alert
      :value="alertViagemEditada"
      transition="slide-y-transition"
      dense
      color="dark green"
      dismissible
      type="success"
      @input="alertViagemEditada = false"
    >
      Viagem Editada
    </v-alert>
    <v-alert
      :value="alertViagemEliminada"
      transition="slide-y-transition"
      dense
      color="dark green"
      dismissible
      type="success"
      @input="alertViagemEliminada = false"
    >
      Viagem Eliminada
    </v-alert>
    <v-card class="mx-auto text-center" max-width="344" outlined elevation="2">
      <v-list-item three-line>
        <v-list-item-content>
          <v-list-item-title class="text-h6 overline mb-1">
            Partida: {{ viagem.localInicio }}
          </v-list-item-title>
          <v-list-item-title class="text-h6 overline mb-1">
            Destino: {{ viagem.localDestino }}
          </v-list-item-title>

          <v-list-item-title class="text-h6 overline mb-1">
            Condutor: {{ viagem.idCondutor }}
          </v-list-item-title>

          <div class="text-overline mb-4">
            Lugares Disponíveis: {{ viagem.lugaresDisp }}
          </div>
          <div class="text-overline mb-4">
            Permite Bagagem: {{ viagem.bagagem ? "Sim" : "Não" }}
          </div>

          <div class="text-overline mb-4">
            Custo da Viagem: {{ viagem.custoPessoa }}€
          </div>

          <v-list-item-subtitle
            >Data e Hora: {{ viagem.dataInicio }} {{ viagem.horaInicio }}
          </v-list-item-subtitle>
          <v-spacer></v-spacer>
          <v-div v-if="viagem.descricao || viagem.descricao == 'null'">
            <v-list-item-subtitle
              >Descrição: {{ viagem.descricao }}
            </v-list-item-subtitle>
          </v-div>
        </v-list-item-content>
      </v-list-item>

      <!-- Lista de Utilizadores aceites de uma viagem -->
      <v-div v-if="tabela.length > 0">
        <v-card class="mx-auto" max-width="200" tile>
          <v-list disabled>
            <v-subheader>Utilizadores Aceites</v-subheader>
            <v-list-item-group color="primary">
              <v-list-item v-for="(user, i) in tabela" :key="i">
                <v-list-item-content>
                  <v-list-item-title
                    v-text="user.fk_Utilizador_username"
                  ></v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-card>
      </v-div>

      <GmapMap
        :center="coordinates"
        :zoom="zoom"
        style="height: 360px; margin: 32px auto"
        :options="{
          mapTypeControl: false,
          streetViewControl: false,
          fullscreenControl: false,
        }"
      ></GmapMap>

      <v-div class="text-center" v-if="viagem.estado != 'Finalizada'">
        <!-- Butões de Passageiro SEM Pedido -->
        <div
          v-if="
            this.username != viagem.idCondutor &&
            !this.pedido &&
            !this.pedidoAceite
          "
        >
          <v-btn
            class="ma-2"
            color="success"
            outlined
            @click="registarPassageiro"
          >
            Registar na viagem
            <v-icon right> mdi-account-check-outline </v-icon>
          </v-btn>
        </div>

        <!-- Butões de Passageiro COM Pedido -->
        <div v-else-if="this.username != viagem.idCondutor && pedido">
          <v-btn class="ma-2" color="primary" outlined @click="enviarMsg">
            Enviar Mensagem
            <v-icon right> mdi-android-messages </v-icon>
          </v-btn>
          <!-- Pedido Aceite -->
          <v-div v-if="pedidoAceite">
            <v-btn
              disabled
              class="ma-2"
              color="red"
              outlined
              @click="deletePassageiro"
            >
              Cancelar Pedido
              <v-icon right> mdi-delete-outline </v-icon>
            </v-btn>
          </v-div>
          <!-- Pedido por aceitar -->
          <v-div v-else>
            <v-btn class="ma-2" color="red" outlined @click="deletePassageiro">
              Cancelar Pedido
              <v-icon right> mdi-delete-outline </v-icon>
            </v-btn>
          </v-div>
        </div>

        <!-- Butões de Condutor  -->
        <v-div
          class="text-center"
          v-else-if="
            this.username == viagem.idCondutor && viagem.estado == 'Agendada'
          "
        >
          <v-btn class="ma-2" color="success" outlined @click="startViagem">
            Iniciar viagem
            <v-icon right> mdi-play-circle-outline </v-icon>
          </v-btn>
          <v-btn
            class="ma-2"
            color="orange"
            outlined
            pill
            @click="dialog = !dialog"
          >
            Editar Viagem
            <v-icon right> mdi-pencil-outline </v-icon>
          </v-btn>

          <v-btn
            class="ma-2"
            color="red"
            outlined
            pill
            @click="dialogDelete = !dialogDelete"
          >
            Eliminar Viagem
            <v-icon right> mdi-delete-outline </v-icon>
          </v-btn>
        </v-div>
        <!-- Butões de Condutor depois de iniciar viagem  -->
        <v-div
          v-if="
            viagem.estado == 'A decorrer' && this.username == viagem.idCondutor
          "
        >
          <v-btn class="ma-2" color="red" outlined pill @click="terminarViagem">
            Terminar Viagem
            <v-icon right> mdi-delete-outline </v-icon>
          </v-btn>
        </v-div>
      </v-div>
      <v-div class="text-center" v-else>
        <h3>Viagem Terminada</h3>
      </v-div>

      <!-- Dialog de Delete -->
      <v-dialog v-model="dialogDelete" max-width="500px">
        <v-card>
          <v-card-title color="#7e380e" class="text-h5"
            >Tem a certeza que quer eliminar a viagem?</v-card-title
          >
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="#7e380e" text @click="dialogDelete = !dialogDelete"
              >Cancel</v-btn
            >
            <v-btn color="#7e380e" text @click="eliminarViagem">Eliminar</v-btn>
            <v-spacer></v-spacer>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- Dialog de Editar Viagem -->
      <v-dialog v-model="dialog" max-width="800px">
        <v-card>
          <v-card-title>
            <span class="text-h5"> Editar Viagem </span>
          </v-card-title>

          <v-card-text>
            <v-container>
              <!-- <v-row>
        <v-col cols="11">
          <v-select
            height="44px"
            v-model="formData.fk_Carro_matricula"
            clear
            :rules="rules.required"
            :items="carros.map((carro) => carro.matricula)"
            label="Escolher Viatura"
            dense
          />
        </v-col>
      </v-row> -->
              <v-row>
                <v-col cols="11" md="5">
                  <v-text-field
                    v-model="viagem.localInicio"
                    id="autocomplete"
                    :rules="[...rules.required, ...rules.length30]"
                    :counter="30"
                    label="Ponto de Partida"
                  />
                </v-col>
                <v-spacer></v-spacer>
                <v-col cols="11" md="5">
                  <v-text-field
                    v-model="viagem.localDestino"
                    :rules="[...rules.required, ...rules.length30]"
                    :counter="30"
                    label="Ponto de Chegada"
                  />
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="11" sm="5">
                  <v-menu
                    ref="menu"
                    v-model="menu"
                    :close-on-content-click="false"
                    :return-value.sync="viagem.dataInicio"
                    transition="scale-transition"
                    offset-y
                    min-width="auto"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field
                        :rules="rules.required"
                        v-model="viagem.dataInicio"
                        label="Data da viagem"
                        prepend-icon="mdi-calendar"
                        readonly
                        v-bind="attrs"
                        v-on="on"
                      ></v-text-field>
                    </template>
                    <v-date-picker
                      v-model="viagem.dataInicio"
                      no-title
                      scrollable
                    >
                      <v-spacer></v-spacer>
                      <v-btn text color="primary" @click="menu = false">
                        Cancel
                      </v-btn>
                      <v-btn
                        text
                        color="primary"
                        @click="$refs.menu.save(viagem.dataInicio)"
                      >
                        OK
                      </v-btn>
                    </v-date-picker>
                  </v-menu>
                </v-col>
                <v-spacer></v-spacer>
                <v-col cols="11" sm="5">
                  <v-menu
                    ref="menuTime"
                    v-model="menuTime"
                    :close-on-content-click="false"
                    :nudge-right="40"
                    :return-value.sync="viagem.horaInicio"
                    transition="scale-transition"
                    offset-y
                    max-width="290px"
                    min-width="290px"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field
                        :rules="rules.required"
                        v-model="viagem.horaInicio"
                        label="Hora de Ínicio"
                        prepend-icon="mdi-clock-time-four-outline"
                        readonly
                        v-bind="attrs"
                        v-on="on"
                      ></v-text-field>
                    </template>
                    <v-time-picker
                      v-if="menuTime"
                      v-model="viagem.horaInicio"
                      full-width
                      @click:minute="$refs.menuTime.save(viagem.horaInicio)"
                    ></v-time-picker>
                  </v-menu>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="11" md="5">
                  <v-select
                    height="44px"
                    v-model="viagem.lugaresDisp"
                    clear
                    :rules="rules.required"
                    :items="lugares"
                    label="Lugares Disponíveis"
                    dense
                  />
                </v-col>

                <v-spacer />
                <v-col cols="11" md="5">
                  <v-text-field
                    v-model="viagem.regularidade"
                    :rules="rules.length30"
                    :counter="30"
                    label="Regularidade"
                  />
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="11" md="5">
                  <v-text-field
                    v-model="viagem.custoPessoa"
                    label="Custo mínimo por pessoa"
                  />
                </v-col>
                <v-spacer />
                <v-col cols="11" md="5">
                  <v-checkbox v-model="viagem.bagagem" label="Bagagem" />
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="12">
                  <v-text-field v-model="viagem.descricao" label="Descrição" />
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="#7e380e" text @click="close"> Cancelar </v-btn>
            <v-btn color="#7e380e" text @click="editarViagem"> Guardar </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card>
  </v-container>
</template>

<script>
import Header from "../components/Header.vue";
import NavDraw from "../components/NavDraw.vue";
import { mapState } from "vuex";

export default {
  name: "Viagem",

  components: {
    Header,
    NavDraw,
  },

  data() {
    return {
      coordinates: {
        lat: 41.560681613621156, 
        lng: -8.396301253582003,
      },
      zoom: 15,
      tabela: [],
      tab: null,
      viagem: {},
      dialog: false,
      dialogDelete: false,
      dialogTerminar: false,
      rules: {
        required: [(v) => !!v || "Field is required"],
        length30: [
          (v) =>
            (v && v.length <= 30) ||
            "Field must be less or equal than 30 characters",
        ],
        length75: [
          (v) =>
            (v && v.length <= 75) ||
            "Field must be less or equal than 75 characters",
        ],
        length100: [
          (v) =>
            (v && v.length <= 100) ||
            "Field must be less or equal than 100 characters",
        ],
      },
      lugares: ["1", "2", "3", "4", "5", "6"],
      pedido: false,
      pedidoID: 0,
      pedidoAceite: false,
      aceites: [],
      alertPedidoFeito: false,
      alertPedidoCancelado: false,
      alertViagemEditada: false,
      alertViagemEliminada: false,
      alertErro: false,
    };
  },

  computed: mapState({
    username: (state) => state.auth.username,
  }),

  created() {
    this.initialize();

    // GET Lista de Passageiros de uma viagem 
    this.$request("get", "viagem/passageiros/" + this.$route.params.id)
      .then((response) => {
        console.log(response.data);
        this.tabela = response.data.Passageiros;
      })
      .catch((error) => {
        console.log(error);
      });
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },

  mounted() {
    this.geolocate();
  },

  methods: {
    geolocate: function () {
      navigator.geolocation.getCurrentPosition((position) => {
        this.coordinates = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };
      });
    },
    initialize() {
      this.$request("get", "viagem/" + this.$route.params.id)
        .then((response) => {
          this.viagem = response.data.Viagem[0];
        })
        .catch((error) => {
          console.log(error);
        });

      // Verifica se o user fez um pedido nesta viagem
      this.$request("get", "pedido/todos")
        .then((response) => {
          console.log("RESPONSE", response);
          response.data.Pedidos.map((pedido) => {
            //console.log("ITEM", pedido);
            //console.log("USER", this.username);
            if (
              pedido.viagem == this.viagem.id &&
              pedido.username == this.username
            ) {
              this.pedido = true;
              this.pedidoID = pedido.id;
            }

            if (
              pedido.estado == "Aceite" &&
              pedido.viagem == this.viagem.id &&
              pedido.username == this.username
            ) {
              this.pedidoAceite = true;
              this.aceites.push(pedido);
              this.pedido = true;
            }
          });
        })
        .catch((error) => {
          console.log(error);
        });
    },

    registarPassageiro() {
      var payload = new FormData();
      payload.append("username", this.username);
      payload.append("idViagem", this.$route.params.id);
      payload.append("nrPessoas", 1);
      payload.append("pickupLocal", this.viagem.localInicio);
      payload.append("localDestino", this.viagem.localDestino);

      this.$request("post", "pedido/registo", payload)
        .then((response) => {
          console.log(response);
          this.alertPedidoFeito = true;
          var notificacao={  
          userDestino : this.viagem.idCondutor,  
          titulo : "Pedido para uma Viagem",
          mensagem : "O utilizador "+ this.username+" fez um pedido para registar-se numa viagem sua." ,
          viagem: this.$route.params.id
          };
          this.$socket.emit("pedido", notificacao );
        })
        .catch((error) => {
          console.log(error);
          this.alertErro = true;
        });

      this.pedido = true;
    },

    deletePassageiro() {
      this.$request("delete", "pedido/" + this.pedidoID + "/remove")
        .then((response) => {
          console.log(response);
          this.alertPedidoCancelado = true;
          var notificacao={  
          userDestino : this.viagem.idCondutor,  
          titulo : "Cancelar pedido",
          mensagem : "O utilizador "+ this.username+" cancelou um pedido de uma viagem" ,
          viagem: this.$route.params.id
          };
          this.$socket.emit("viagem", notificacao );
        })
        .catch((error) => {
          console.log(error);
          this.alert = true;
        });
      this.pedido = false;
      this.pedidoID = 0;
    },

    editViagemDialog() {
      this.dialog = !this.dialog;
    },

    editarViagem() {
      var payload = new FormData();
      payload.append("lugaresDisp", this.viagem.lugaresDisp);
      payload.append("localInicio", this.viagem.localInicio);
      payload.append("fk_Carro_matricula", this.viagem.username);
      payload.append("localDestino", this.viagem.localDestino);
      payload.append("regularidade", this.viagem.regularidade);
      payload.append("dataInicio", this.viagem.dataInicio);
      payload.append("bagagem", this.viagem.bagagem ? 1 : 0);
      payload.append("horaInicio", this.viagem.horaInicio);
      payload.append("custoPessoa", this.viagem.custoPessoa);
      payload.append("kmsViagem", this.viagem.kmsViagem);
      payload.append("idCondutor", this.username);
      payload.append("descricao", this.viagem.descricao);
      console.log(this.viagem);

      this.$request("put", "viagem/" + this.viagem.id + "/update", payload)
        .then((response) => {
          console.log(response);
          this.dialog = !this.dialog;
          this.alertViagemEditada = true;
          this.tabela.forEach(user => {
          var notificacao={  
                userDestino : user.fk_Utilizador_username,  
                titulo : "Viagem Editada",
                mensagem : "O condutor " + this.username + " editou uma viagem onde está registado",
                viagem: this.$route.params.id
              };
          this.$socket.emit("viagem", notificacao );
          });
        })
        .catch((error) => {
          console.log(error);
          this.alertErro = true;
        });
    },

    startViagem() {
      var payload = new FormData();
      payload.append("estado", "A decorrer");
      this.$request("put", "viagem/" + this.viagem.id + "/update", payload)
        .then((response) => {
          console.log(response);
          this.tabela.forEach((user) => {
            this.$request("put", "viagem/usufrui/" + this.viagem.id + "&" + user.fk_Utilizador_username +"/update", payload)
              .then((response)=> {
              console.log(response);
               var notificacao={  
                userDestino : user.fk_Utilizador_username,  
                titulo : "Viagem Iniciada",
                mensagem : "O condutor " + this.username + " inciou uma viagem onde está registado",
                viagem: this.$route.params.id
              };
              this.$socket.emit("viagem", notificacao );
              
            });
          this.$router.go();
              }).catch((error)=>{
                console.log(error)
              })
            
         
        
        })
        .catch((error) => {
          console.log(error);
        });
    },

    eliminarViagem() {
              // TODO: Mudar o estado dos pedidos desta viagem para "Eliminada" e eliminar as entradas na tabela usufrui
      // apaga Viagem
      this.$request("delete", "viagem/" + this.$route.params.id + "/remove")
        .then((response) => {
          console.log(response);
          this.alertViagemEliminada = true;
        })
        .catch((error) => {
          console.log(error);
          this.alertErro = true;
        });

      // muda estado dos Pedidos para "Eliminada"
      // TODO
      // this.$request("delete", "pedido/" + this.$route.params.id + "/eliminar")
      //   .then((response) => {
      //     console.log(response);
      //     this.alertViagemEliminada = true;
      //   })
      //   .catch((error) => {
      //     console.log(error);
      //     this.alertErro = true;
      //   });
      

      // apaga entradas em Usufrui
      // TODO

      this.dialogDelete = !this.dialogDelete;
    },

    terminarViagem() {
      var payload = new FormData();
      payload.append("estado", "Finalizada");
      this.$request("put", "viagem/" + this.viagem.id + "/update", payload)
        .then((response) => {
          console.log(response);
           this.tabela.forEach(user => {
              this.$request("put", "viagem/usufrui/" + this.viagem.id + "&" + user.fk_Utilizador_username +"/update", payload)
              .then((response)=> {
              console.log(response);
               var notificacao={  
                userDestino : user.fk_Utilizador_username,  
                titulo : "Viagem Iniciada",
                mensagem : "O condutor " + this.username + " inciou uma viagem onde está registado",
                viagem: this.$route.params.id
              };
              this.$socket.emit("viagem", notificacao );
          }); 
          this.$router.go();
              }).catch((error)=>{
                console.log(error)
              })
         
        })
        .catch((error) => {
          console.log(error);
        });
    },

    enviarMsg(){
      var payload= new FormData();
      payload.append('userorigem', this.username)
      payload.append('userdestino', this.viagem.idCondutor)
      this.$request("post","mensagem/registoMailBox",payload)
        .then((response) => {
          console.log(response);
          this.$router.push({name: "inbox"})
        })
        .catch((error) => {
          console.log(error);
        });
        

    },
    close() {
      this.dialog = false;
    },

    onClickHeader() {
      this.$refs.navdraw.fixNav();
    },
  },
 
};
</script>
