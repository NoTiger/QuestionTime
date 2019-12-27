<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light my-navbar" v-bind:class=" { 'navbarOpen': show }">
    <div class="container">
      <router-link
       :to="{ name: 'home' }" class="navbar-brand"
        >Kick Ass Question Time</router-link
      >
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" @click.stop="toggleNavbar()">
            <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent" v-bind:class="{ 'show': show }">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item active m-1">
            <router-link :to="{ name: 'home' }" class="btn btn-sm btn-success"
              >Home</router-link
            >
          </li>
          <li class="nav-item m-1">
            <router-link
              :to="{ name: 'question-editor' }"
              class="btn btn-sm btn-success"
              >Ask Question</router-link
            >
          </li>
          <li class="nav-item m-1">
            <a
              class="btn btn-sm btn-outline-secondary"
              href="/accounts/logout/"
              tabindex="-1"
              aria-disabled="true"
            >
              Logout
            </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style>
.my-navbar {
  border-bottom: 1px solid #ddd;
}

.navbar-brand {
  font-weight: bold;
  font-size: 130%;
}

.navbar-brand:hover {
  color: #dc3545 !important;
}
</style>

<script>
export default {
  name: "NavbarComponent",
  props: {
  },
  data() {
    return {
      show:true,
    }
  },
  methods: {
    toggleNavbar() {
      this.show = !this.show;
    }
  }
};
</script>
