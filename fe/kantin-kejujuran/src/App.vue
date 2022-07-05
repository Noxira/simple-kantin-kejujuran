<script setup>
import { onMounted, ref} from 'vue'
// import HelloWorld from "./components/HelloWorld.vue";
const items = ref([])
const balance = ref(0)
const input_name = ref("")
const input_price = ref()
const img_link = ref("")
const input_desc = ref("")
const item_sort = ref(0)
const last_added = ref("")

const updateSort = (type) => {
  item_sort.value = type
  updateItems(item_sort.value)
}

const updateBal = () => {
    let formdata = new FormData()
    formdata.append('saldo_terbarukan', balance.value)

    fetch(
      'https://kantin-kejujuran-nox.herokuapp.com/ubah-saldo',
      { 
        method: 'POST',
        body: formdata
      }
      )
    .then((res) => {return res.json()})
    .then((data) => {
        if (data.return_code != 1){
          alert('Gagal mengupdate saldo')
        } 
    })
} 

const addItem = () => {
    if (input_name.value === "" || input_price.value <= 0) {
      return
    }
    if (input_name.value == last_added.value){
      last_added.value = ""
      return
    }
    last_added.value = input_name.value

    let formdata = new FormData()
    formdata.append('nama', input_name.value)
    formdata.append('harga', input_price.value)

    if (img_link.value !== ""){
      formdata.append('link_gambar', img_link.value)
    }
    if (input_desc.value !== ""){
      formdata.append('deskripsi', input_desc.value)
    }

    fetch(
      'https://kantin-kejujuran-nox.herokuapp.com/tambah-barang',
      { 
        method: 'POST',
        body: formdata
      }
      )
    .then((res) => {return res.json()})
    .then((data) => {
        if (data.return_code != 1){
          alert('Gagal menambahkan barang')
        } 
        else { 
          updateItems(1)
          input_name.value = ""
          input_price.value = null
          input_desc.value = ""
          img_link.value = ""
        }
    })
}

const getBalance = () => {
  fetch(
    'https://kantin-kejujuran-nox.herokuapp.com/cek-saldo',
    { 
      method: 'GET'
    }
  )
  .then((res) => {return res.json()})
  .then((data) => {
    balance.value = data.saldo
  })
}

const updateItems = (mode) => {
  fetch(
    'https://kantin-kejujuran-nox.herokuapp.com/barang-dijual?sort=' + mode,
    { 
      method: 'GET'
    }
  )
  .then((res) => {return res.json()})
  .then((data) => {
    items.value = data
  })
}

const buyItem = (item) => {
  let formdata = new FormData()
  formdata.append('id', item._id)

  fetch(
    'https://kantin-kejujuran-nox.herokuapp.com/hapus-barang',
    { 
      method: 'POST',
      body: formdata
    }
    )
  .then((res) => {
      return res.json()
    })
  .then((data) => {
    console.log(data)
  })

}
 
onMounted(() => {
  getBalance()
  updateItems(item_sort.value)
})


</script>

<template>
	<main class="app">
		
		<section class="app-title">
			<h2 class="title">
				Kantin Kejujuran
			</h2>
		</section>

    <hr>

    <section class="create-listing">
			<h3>Daftarkan Barang Untuk Dijual</h3>

			<form id="new-listing-form" @submit.prevent="addItem()">
				<h4 style="padding-bottom: 1%">Deskripsikan Barang Mu!</h4>

        <div>
          <text>
            Nama Barang:
          </text>
          <input 
            type="text" 
            name="nama" 
            id="nama" 
            placeholder="Barang langka bgt"
            v-model="input_name" />
        </div>

        <div>
          <text>
            Deskripsi Barang:
          </text>
          <input 
            type="text" 
            name="deskripsi" 
            id="deskripsi" 
            placeholder="Barang ini dibuat oleh XYZ"
            v-model="input_desc" />
        </div>

        <div>
          <text>
            Harga Barang:
          </text>
          <input 
            type="number" 
            name="harga" 
            id="harga" 
            placeholder="5000"
            ondrop="return false;" 
            onpaste="return false;"
            onkeypress="return event.charCode>=48 && event.charCode<=57" required
            v-model="input_price" />
        </div>

        <div>
          <text>
            Link Gambar (bila ada):
          </text>
          <input 
            type="text" 
            name="link_gambar" 
            id="link_gambar" 
            placeholder="https://"
            v-model="img_link" />
        </div>

        <div class="actions" style="padding-top: 1%">
				  <button class="submit" @click="addItem()">Tambah Item</button>
        </div>
			</form>
		</section>
    
    <hr>
		
    <section class="canteen-balance">
        <div>
          <text>
            Saldo Kantin:
          </text>
          <input 
            type="number" 
            name="harga" 
            id="harga"
            ondrop="return false;" 
            onpaste="return false;"
            onkeypress="return event.charCode>=48 && event.charCode<=57" required
            v-model="balance" /> 
        </div>

        <div class="actions" style="padding-top: 1%">
          <button class="submit" @click="updateBal()">Ubah Balance</button>
        </div>
    </section>

    <hr>

    <section class="item-list">
			<div class="list" id="item-list">
        
        <div class="actions" style="padding: 1%; display: flex">
          <h3 style="padding-right: 1%" > Sort By: </h3>
          <button class="submit" @click="updateSort(0)">Date (Asc)</button>
          <button class="submit" @click="updateSort(1)">Date (Desc)</button>
          <button class="submit" @click="updateSort(2)">Name (Asc)</button>
          <button class="submit" @click="updateSort(3)">Name (Desc)</button>
        </div>

				<div v-for="item in items" class="item">
        
          <div id="container">
            <div>
              <img :src="item.link_gambar" :alt ="item.nama">
            </div>

            <div class="item-title" style="vertical-align: middle;">
              <h3>
                {{item.nama}}
              </h3>
            </div>
    
            <div class="actions">
              <h3 style="font-size: 1rem; margin-right:3%">
                {{item.harga}}
              </h3>
              <button class="buy" @click="buyItem(item); updateItems(0)">beli</button>
            </div>
          
          </div>
          
          <div id="container" style="min-height: 30px">
            <div style="width: 70%;">
              <text id="deskripsi">
                {{item.deskripsi}}
              </text>
            </div>

            <div style="width: 30%; text-align: end;">
              <text>
              {{item.tanggal}}
              </text>
            </div>

          </div>

        </div>


			</div>
		</section>

	</main>
</template>

<style>
@import "./assets/base.css";
</style>
