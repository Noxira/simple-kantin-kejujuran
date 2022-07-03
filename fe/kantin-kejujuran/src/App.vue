<script setup>
// import HelloWorld from "./components/HelloWorld.vue";
const todos_asc = ([{"content": "Make A Video", "category": "business", "done": false, "createdAt": 1653906191876}])
</script>

<template>
	<main class="app">
		
		<section class="app-title">
			<h2 class="title">
				Kantin Kejujuran
			</h2>
		</section>

		<section class="item-list">
			<div class="list" id="todo-list">

				<div v-for="item in todos_asc" :class="`item ${item.done && 'done'}`">
					<label>
						<input type="checkbox" v-model="item.done" />
						<span :class="`bubble ${
							item.category == 'business' 
								? 'business' 
								: 'personal'
						}`"></span>
					</label>

					<div class="item-content">
						<input type="text" v-model="item.content" />
					</div>

					<div class="actions">
						<button class="delete" @click="removeTodo(todo)">Delete</button>
					</div>
				</div>

			</div>
		</section>

	</main>
</template>

<style>
@import "./assets/base.css";
</style>
